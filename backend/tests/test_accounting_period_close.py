from __future__ import annotations

import pytest
from mongomock_motor import AsyncMongoMockClient

from services import accounting_core


@pytest.fixture
async def accounting_db(monkeypatch):
    client = AsyncMongoMockClient()
    test_db = client["cvln_accounting_close_test"]
    monkeypatch.setattr(accounting_core, "db", test_db)
    yield test_db
    client.close()


async def _period():
    return await accounting_core.create_period(
        actor_id="admin",
        code="2026-09",
        starts_at="2026-09-01T00:00:00+00:00",
        ends_at="2026-10-01T00:00:00+00:00",
    )


@pytest.mark.asyncio
async def test_close_gate_blocks_unreconciled_paid_payment_and_missing_invoice(accounting_db):
    period = await _period()
    await accounting_db.payments.insert_one(
        {
            "id": "PAY-1",
            "checkout_session_id": "CHK-1",
            "status": "paid",
            "provider_payment_intent_id": "pi_1",
            "created_at": "2026-09-10T12:00:00+00:00",
        }
    )
    gate = await accounting_core.period_close_gate(period["id"])
    assert gate["pass"] is False
    assert gate["missing_invoice_payment_ids"] == ["PAY-1"]
    assert gate["unreconciled_payments"][0]["payment_id"] == "PAY-1"

    with pytest.raises(ValueError, match="close gate failed"):
        await accounting_core.close_period(
            actor_id="admin",
            period_id=period["id"],
            review_note="Attempt close",
            evidence_refs=["REVIEW-1"],
        )


@pytest.mark.asyncio
async def test_close_gate_passes_after_real_reconciliation_and_invoice(accounting_db):
    period = await _period()
    await accounting_db.payment_checkout_sessions.insert_one({"id": "CHK-1", "status": "paid"})
    await accounting_db.payments.insert_one(
        {
            "id": "PAY-1",
            "checkout_session_id": "CHK-1",
            "user_id": "u1",
            "offer_id": "offer-1",
            "amount_eur": 1400.0,
            "currency": "EUR",
            "status": "paid",
            "provider_payment_intent_id": "pi_1",
            "created_at": "2026-09-10T12:00:00+00:00",
        }
    )
    reconciliation = await accounting_core.reconcile_payment(actor_id="accountant", payment_id="PAY-1")
    assert reconciliation["reconciled"] is True
    await accounting_core.create_invoice_from_payment(
        actor_id="accountant",
        payment_id="PAY-1",
        issuer_name="CVLN Academy",
        customer_name="Learner",
    )

    gate = await accounting_core.period_close_gate(period["id"])
    assert gate["pass"] is True
    closed = await accounting_core.close_period(
        actor_id="accountant",
        period_id=period["id"],
        review_note="Reconciliations and invoice checked",
        evidence_refs=[reconciliation["id"], "ACCOUNTANT-SIGNOFF-1"],
    )
    assert closed["status"] == "CLOSED"
    assert closed["close_evidence_refs"][-1] == "ACCOUNTANT-SIGNOFF-1"


@pytest.mark.asyncio
async def test_open_period_anomaly_blocks_close_until_evidence_backed_resolution(accounting_db):
    period = await _period()
    anomaly = await accounting_core.create_period_anomaly(
        actor_id="accountant",
        period_id=period["id"],
        code="MISSING_SUPPORTING_DOCUMENT",
        description="Supplier proof missing",
        evidence_refs=["CHECKLIST-1"],
    )
    assert (await accounting_core.period_close_gate(period["id"]))["pass"] is False

    with pytest.raises(ValueError, match="requires explanation and evidence"):
        await accounting_core.resolve_period_anomaly(
            actor_id="accountant",
            anomaly_id=anomaly["id"],
            resolution="Found",
            evidence_refs=[],
        )

    resolved = await accounting_core.resolve_period_anomaly(
        actor_id="accountant",
        anomaly_id=anomaly["id"],
        resolution="Supporting document attached and checked",
        evidence_refs=["DOC-1"],
    )
    assert resolved["status"] == "RESOLVED"
    assert (await accounting_core.period_close_gate(period["id"]))["pass"] is True


@pytest.mark.asyncio
async def test_period_boundaries_require_timezone_and_unique_code(accounting_db):
    with pytest.raises(ValueError, match="timezone"):
        await accounting_core.create_period(
            actor_id="admin",
            code="bad",
            starts_at="2026-09-01T00:00:00",
            ends_at="2026-10-01T00:00:00+00:00",
        )
    await _period()
    with pytest.raises(ValueError, match="already exists"):
        await _period()
