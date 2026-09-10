from __future__ import annotations

import pytest
from mongomock_motor import AsyncMongoMockClient

from services import accounting_protocols, policy_registry, professional_governance


@pytest.fixture
async def accounting_protocol_db(monkeypatch):
    client = AsyncMongoMockClient()
    test_db = client["cvln_accounting_protocol_test"]
    for module in (accounting_protocols, policy_registry, professional_governance):
        monkeypatch.setattr(module, "db", test_db)
    yield test_db
    client.close()


async def _policy(key: str):
    return await policy_registry.register_version(
        actor_id="founder", policy_key=key, version="1.0.0", kind="POLICY",
        title=key, content={"human_validated": True},
        effective_at="2026-09-10T00:00:00+00:00", evidence_refs=[key]
    )


@pytest.mark.asyncio
async def test_refund_accounting_event_is_idempotent_and_can_bind_credit_note(accounting_protocol_db):
    await accounting_protocol_db.payments.insert_one({"id": "PAY-1", "status": "paid"})
    await accounting_protocol_db.accounting_credit_notes.insert_one({"id": "CN-1", "amount_cents": 5000})
    first = await accounting_protocols.record_refund_accounting_event(
        actor_id="accountant", refund_ref="REF-1", payment_id="PAY-1",
        amount_cents=5000, currency="EUR", evidence_refs=["PSP-REFUND-1"], credit_note_id="CN-1"
    )
    second = await accounting_protocols.record_refund_accounting_event(
        actor_id="accountant", refund_ref="REF-1", payment_id="PAY-1",
        amount_cents=5000, currency="EUR", evidence_refs=["PSP-REFUND-1"], credit_note_id="CN-1"
    )
    assert first["id"] == second["id"]
    assert first["posting_status"] == "UNMAPPED"


@pytest.mark.asyncio
async def test_revenue_recognition_is_prepared_not_validated(accounting_protocol_db):
    policy = await _policy("REVENUE_RECOGNITION")
    row = await accounting_protocols.prepare_revenue_recognition(
        actor_id="accountant", source_ref="INV-1", amount_cents=140000, currency="EUR",
        recognition_date="2026-09-11", policy_version_id=policy["id"],
        dimensions={"formation_code": "FMS-A"}, evidence_refs=["INV-1"]
    )
    assert row["status"] == "PREPARED_NOT_VALIDATED"


@pytest.mark.asyncio
async def test_missing_supporting_document_must_resolve_to_registered_document(accounting_protocol_db):
    await accounting_protocol_db.accounting_periods.insert_one({"id": "PER-1", "status": "OPEN"})
    missing = await accounting_protocols.register_missing_supporting_document(
        actor_id="accountant", period_id="PER-1", expected_document_type="RECEIPT",
        source_ref="TX-1", owner="ops", due_at="2026-09-20", evidence_refs=["RECON-1"]
    )
    with pytest.raises(LookupError):
        await accounting_protocols.resolve_missing_supporting_document(
            actor_id="accountant", missing_document_id=missing["id"],
            supporting_document_id="UNKNOWN", evidence_refs=["FOLLOWUP"]
        )
    await accounting_protocol_db.accounting_supporting_documents.insert_one({"id": "DOC-1"})
    resolved = await accounting_protocols.resolve_missing_supporting_document(
        actor_id="accountant", missing_document_id=missing["id"],
        supporting_document_id="DOC-1", evidence_refs=["DOC-1"]
    )
    assert resolved["status"] == "RESOLVED"


@pytest.mark.asyncio
async def test_fec_readiness_never_claims_fec_generation_or_legal_compliance(accounting_protocol_db):
    await accounting_protocol_db.accounting_periods.insert_one({"id": "PER-1", "status": "OPEN"})
    gate = await accounting_protocols.fec_readiness_gate(period_id="PER-1")
    assert gate["pass"] is True
    assert gate["fec_generated"] is False
    assert gate["legal_compliance_claimed"] is False

    await accounting_protocol_db.accounting_missing_documents.insert_one({"id": "M-1", "period_id": "PER-1", "status": "OPEN"})
    gate = await accounting_protocols.fec_readiness_gate(period_id="PER-1")
    assert gate["pass"] is False
    assert gate["blocking_count"] == 1


@pytest.mark.asyncio
async def test_financial_retention_requires_canonical_policy(accounting_protocol_db):
    wrong = await _policy("OTHER")
    with pytest.raises(ValueError, match="FINANCIAL_RETENTION"):
        await accounting_protocols.register_financial_retention_policy(
            actor_id="accountant", record_type="INVOICE", retention_days=3650,
            trigger="ISSUED", policy_version_id=wrong["id"], evidence_refs=["POLICY-REVIEW"]
        )
    policy = await _policy("FINANCIAL_RETENTION")
    row = await accounting_protocols.register_financial_retention_policy(
        actor_id="accountant", record_type="INVOICE", retention_days=3650,
        trigger="ISSUED", policy_version_id=policy["id"], evidence_refs=["POLICY-REVIEW"]
    )
    assert row["status"] == "ACTIVE"
