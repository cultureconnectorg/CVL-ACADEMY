from __future__ import annotations

import pytest
from mongomock_motor import AsyncMongoMockClient

from services import accounting_core


@pytest.fixture
async def accounting_db(monkeypatch):
    client = AsyncMongoMockClient()
    test_db = client["cvln_accounting_test"]
    monkeypatch.setattr(accounting_core, "db", test_db)
    yield test_db
    client.close()


@pytest.mark.asyncio
async def test_invoice_requires_real_paid_payment_and_is_idempotent(accounting_db):
    await accounting_db.payments.insert_one(
        {
            "id": "PAY-1",
            "checkout_session_id": "CHK-1",
            "user_id": "u1",
            "offer_id": "offer-1",
            "amount_eur": 1400.0,
            "currency": "EUR",
            "status": "pending",
        }
    )
    with pytest.raises(ValueError, match="paid payment"):
        await accounting_core.create_invoice_from_payment(
            actor_id="admin-1",
            payment_id="PAY-1",
            issuer_name="CVLN Academy",
            customer_name="Learner",
        )

    await accounting_db.payments.update_one(
        {"id": "PAY-1"},
        {"$set": {"status": "paid", "provider_payment_intent_id": "pi_real_ref"}},
    )
    first = await accounting_core.create_invoice_from_payment(
        actor_id="admin-1",
        payment_id="PAY-1",
        issuer_name="CVLN Academy",
        customer_name="Learner",
    )
    second = await accounting_core.create_invoice_from_payment(
        actor_id="admin-1",
        payment_id="PAY-1",
        issuer_name="CVLN Academy",
        customer_name="Learner",
    )
    assert first["id"] == second["id"]
    assert first["amount_cents"] == 140000
    assert first["number"].startswith("INV-")


@pytest.mark.asyncio
async def test_credit_notes_cannot_exceed_original_invoice(accounting_db):
    await accounting_db.accounting_invoices.insert_one(
        {
            "id": "INV-1",
            "amount_cents": 10000,
            "currency": "EUR",
            "status": "ISSUED",
        }
    )
    note = await accounting_core.create_credit_note(
        actor_id="admin-1",
        invoice_id="INV-1",
        amount_cents=4000,
        reason="Partial refund",
    )
    assert note["amount_cents"] == 4000
    with pytest.raises(ValueError, match="exceed"):
        await accounting_core.create_credit_note(
            actor_id="admin-1",
            invoice_id="INV-1",
            amount_cents=7000,
            reason="Too much",
        )


@pytest.mark.asyncio
async def test_revenue_split_must_balance_exactly(accounting_db):
    split = await accounting_core.create_revenue_split(
        actor_id="admin-1",
        source_type="INVOICE",
        source_id="INV-1",
        amount_cents=10000,
        allocations=[
            {"beneficiary": "academy", "amount_cents": 7000},
            {"beneficiary": "partner", "amount_cents": 3000},
        ],
    )
    assert sum(x["amount_cents"] for x in split["allocations"]) == 10000

    with pytest.raises(ValueError, match="exactly equal"):
        await accounting_core.create_revenue_split(
            actor_id="admin-1",
            source_type="INVOICE",
            source_id="INV-1",
            amount_cents=10000,
            allocations=[{"beneficiary": "academy", "amount_cents": 9000}],
        )


@pytest.mark.asyncio
async def test_payment_reconciliation_requires_provider_evidence_for_paid_state(accounting_db):
    await accounting_db.payment_checkout_sessions.insert_one(
        {"id": "CHK-1", "status": "paid"}
    )
    await accounting_db.payments.insert_one(
        {
            "id": "PAY-1",
            "checkout_session_id": "CHK-1",
            "status": "paid",
            "provider_payment_intent_id": None,
        }
    )
    result = await accounting_core.reconcile_payment(actor_id="admin-1", payment_id="PAY-1")
    assert result["reconciled"] is False
    assert "PROVIDER_PAYMENT_INTENT_MISSING" in result["issues"]

    await accounting_db.payments.update_one(
        {"id": "PAY-1"}, {"$set": {"provider_payment_intent_id": "pi_evidence"}}
    )
    result = await accounting_core.reconcile_payment(actor_id="admin-1", payment_id="PAY-1")
    assert result["reconciled"] is True


@pytest.mark.asyncio
async def test_period_close_and_tax_summary_do_not_invent_tax_amounts(accounting_db):
    period = await accounting_core.create_period(
        actor_id="admin-1",
        code="2026-09",
        starts_at="2026-09-01T00:00:00+00:00",
        ends_at="2026-10-01T00:00:00+00:00",
    )
    gate = await accounting_core.period_close_gate(period["id"])
    assert gate["pass"] is True
    closed = await accounting_core.close_period(
        actor_id="admin-1",
        period_id=period["id"],
        review_note="Empty period reviewed",
        evidence_refs=["ACCOUNTANT-REVIEW-1"],
    )
    assert closed["status"] == "CLOSED"
    assert closed["close_gate_snapshot"]["pass"] is True

    await accounting_core.register_account_mapping(
        actor_id="admin-1",
        event_type="PAYMENT_PAID",
        debit_account="BANK",
        credit_account="TRAINING_REVENUE",
        evidence_refs=["ACCOUNTANT-VALIDATION-PENDING"],
    )
    summary = await accounting_core.tax_preparation_summary()
    assert summary["tax_amounts"] is None
    assert summary["tax_amounts_status"] == "NOT_COMPUTED_WITHOUT_VERIFIED_TAX_POLICY"
