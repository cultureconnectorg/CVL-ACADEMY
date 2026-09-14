from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pytest
from mongomock_motor import AsyncMongoMockClient

from services import accounting_advanced, policy_registry, professional_governance


@pytest.fixture
async def accounting_db(monkeypatch):
    client = AsyncMongoMockClient()
    test_db = client["cvln_accounting_advanced_test"]
    for module in (accounting_advanced, policy_registry, professional_governance):
        monkeypatch.setattr(module, "db", test_db)
    yield test_db
    client.close()


def _past() -> str:
    return (datetime.now(timezone.utc) - timedelta(hours=1)).isoformat()


@pytest.mark.asyncio
async def test_entity_binding_uses_registered_legal_entity(accounting_db):
    entity = await accounting_advanced.register_accounting_entity(
        actor_id="admin",
        code="ACADEMY-FR",
        legal_name="CVLN Academy Test Entity",
        registration_ref="REG-EVID-1",
        invoice_prefix="ACA",
        evidence_refs=["REGISTRY-1"],
    )
    await accounting_db.accounting_invoices.insert_one(
        {
            "id": "INV-1",
            "issuer_name": "placeholder",
            "amount_cents": 10000,
            "status": "ISSUED",
        }
    )
    bound = await accounting_advanced.attach_invoice_entity(
        actor_id="admin",
        invoice_id="INV-1",
        entity_id=entity["id"],
        evidence_refs=["ENTITY-BIND-1"],
    )
    assert bound["issuer_name"] == entity["legal_name"]
    assert bound["accounting_entity_id"] == entity["id"]


@pytest.mark.asyncio
async def test_supporting_document_requires_real_hash_and_links_period(accounting_db):
    await accounting_db.accounting_periods.insert_one(
        {"id": "P1", "status": "OPEN", "starts_at": _past(), "ends_at": "2030-01-01T00:00:00+00:00"}
    )
    with pytest.raises(ValueError, match="SHA-256"):
        await accounting_advanced.register_supporting_document(
            actor_id="admin",
            document_type="EXPENSE_RECEIPT",
            document_ref="receipt.pdf",
            content_hash="bad",
            period_id="P1",
            evidence_refs=["UPLOAD-1"],
        )
    doc = await accounting_advanced.register_supporting_document(
        actor_id="admin",
        document_type="EXPENSE_RECEIPT",
        document_ref="receipt.pdf",
        content_hash="a" * 64,
        period_id="P1",
        amount_cents=2500,
        evidence_refs=["UPLOAD-1"],
    )
    assert doc["period_id"] == "P1"
    assert doc["amount_cents"] == 2500


@pytest.mark.asyncio
async def test_profitability_uses_registered_revenue_and_cost_lines(accounting_db):
    await accounting_advanced.record_revenue_line(
        actor_id="accountant",
        amount_cents=140000,
        source_ref="INVOICE-1",
        formation_code="FMS-A",
        learner_id="L1",
        evidence_refs=["REV-1"],
    )
    for cost_type, cents in (
        ("PARTNER", 20000),
        ("PAYMENT_FEES", 5000),
        ("SUPPORT", 8000),
        ("DELIVERY", 12000),
    ):
        await accounting_advanced.record_cost_line(
            actor_id="accountant",
            cost_type=cost_type,
            amount_cents=cents,
            source_ref=f"COST-{cost_type}",
            formation_code="FMS-A",
            learner_id="L1",
            evidence_refs=[f"EVID-{cost_type}"],
        )
    summary = await accounting_advanced.profitability_summary(
        formation_code="FMS-A", learner_id="L1"
    )
    assert summary["revenue_cents"] == 140000
    assert summary["cost_cents"] == 45000
    assert summary["margin_cents"] == 95000
    assert summary["cost_by_type"]["PARTNER"] == 20000


@pytest.mark.asyncio
async def test_tax_package_never_claims_tax_validated(accounting_db):
    period = {
        "id": "PERIOD-1",
        "starts_at": "2026-09-01T00:00:00+00:00",
        "ends_at": "2026-10-01T00:00:00+00:00",
        "status": "OPEN",
    }
    await accounting_db.accounting_periods.insert_one(period)
    await accounting_db.accounting_invoices.insert_one(
        {
            "id": "INV-1",
            "amount_cents": 10000,
            "status": "ISSUED",
            "issued_at": "2026-09-10T12:00:00+00:00",
        }
    )
    policy = await policy_registry.register_version(
        actor_id="founder",
        policy_key="ACCOUNTING_TAX_PREPARATION",
        version="1.0.0",
        kind="POLICY",
        title="Tax preparation",
        content={"prepared_not_validated": True},
        effective_at=_past(),
        evidence_refs=["ACC-008"],
    )
    package = await accounting_advanced.prepare_tax_package(
        actor_id="accountant",
        period_id="PERIOD-1",
        policy_version_id=policy["id"],
        evidence_refs=["ACCOUNTANT-WORKPAPER-1"],
    )
    assert package["status"] == "PREPARED"
    assert package["tax_validated"] is False
    assert package["gross_invoiced_cents"] == 10000


@pytest.mark.asyncio
async def test_period_csv_export_has_stable_columns(accounting_db):
    await accounting_db.accounting_periods.insert_one(
        {
            "id": "PERIOD-1",
            "starts_at": "2026-09-01T00:00:00+00:00",
            "ends_at": "2026-10-01T00:00:00+00:00",
            "status": "OPEN",
        }
    )
    await accounting_db.accounting_invoices.insert_one(
        {
            "id": "INV-1",
            "number": "INV-2026-000001",
            "payment_id": "PAY-1",
            "amount_cents": 12345,
            "currency": "EUR",
            "status": "ISSUED",
            "issued_at": "2026-09-10T12:00:00+00:00",
        }
    )
    exported = await accounting_advanced.export_period_csv("PERIOD-1")
    assert exported["format"] == "CSV"
    assert exported["row_count"] == 1
    assert "number,payment_id,amount_cents,currency,issued_at" in exported["content"]
