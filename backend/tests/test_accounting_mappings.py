from __future__ import annotations

import pytest
from mongomock_motor import AsyncMongoMockClient

from services import accounting_mappings, policy_registry, professional_governance


@pytest.fixture
async def mapping_db(monkeypatch):
    client = AsyncMongoMockClient()
    test_db = client["cvln_accounting_mappings_test"]
    for module in (accounting_mappings, policy_registry, professional_governance):
        monkeypatch.setattr(module, "db", test_db)
    yield test_db
    client.close()


@pytest.mark.asyncio
async def test_first_mapping_is_versioned_and_current_view_points_to_policy(mapping_db):
    row = await accounting_mappings.register_mapping_version(
        actor_id="accountant-1",
        event_type="PAYMENT_PAID",
        debit_account="BANK",
        credit_account="TRAINING_REVENUE",
        version="1.0.0",
        effective_at="2026-09-10T00:00:00+00:00",
        evidence_refs=["ACCOUNTANT-REVIEW-1"],
    )
    assert row["policy_version_id"].startswith("POLV-")
    assert row["policy_version"] == "1.0.0"
    assert row["tax_validation_status"] == "NOT_VALIDATED_BY_MAPPING"
    current = await accounting_mappings.get_mapping("payment_paid")
    assert current["policy_hash"] == row["policy_hash"]


@pytest.mark.asyncio
async def test_mapping_change_requires_explicit_supersession_and_preserves_history(mapping_db):
    first = await accounting_mappings.register_mapping_version(
        actor_id="accountant-1",
        event_type="PAYMENT_PAID",
        debit_account="BANK",
        credit_account="TRAINING_REVENUE",
        version="1.0.0",
        effective_at="2026-09-10T00:00:00+00:00",
        evidence_refs=["ACCOUNTANT-REVIEW-1"],
    )
    with pytest.raises(ValueError, match="explicitly superseded"):
        await accounting_mappings.register_mapping_version(
            actor_id="accountant-1",
            event_type="PAYMENT_PAID",
            debit_account="BANK",
            credit_account="TRAINING_REVENUE_V2",
            version="1.1.0",
            effective_at="2026-09-10T00:00:00+00:00",
            evidence_refs=["ACCOUNTANT-REVIEW-2"],
        )

    second = await accounting_mappings.register_mapping_version(
        actor_id="accountant-1",
        event_type="PAYMENT_PAID",
        debit_account="BANK",
        credit_account="TRAINING_REVENUE_V2",
        version="1.1.0",
        effective_at="2026-09-10T00:00:00+00:00",
        evidence_refs=["ACCOUNTANT-REVIEW-2"],
        supersedes_version_id=first["policy_version_id"],
    )
    history = await accounting_mappings.list_mapping_history("PAYMENT_PAID")
    assert len(history) == 2
    old = next(item for item in history if item["id"] == first["policy_version_id"])
    assert old["status"] == "SUPERSEDED"
    assert second["credit_account"] == "TRAINING_REVENUE_V2"


@pytest.mark.asyncio
async def test_mapping_requires_evidence_and_timezone(mapping_db):
    with pytest.raises(ValueError, match="requires evidence"):
        await accounting_mappings.register_mapping_version(
            actor_id="accountant-1",
            event_type="PAYMENT_PAID",
            debit_account="BANK",
            credit_account="TRAINING_REVENUE",
            version="1.0.0",
            effective_at="2026-09-10T00:00:00+00:00",
            evidence_refs=[],
        )
    with pytest.raises(ValueError, match="include timezone"):
        await accounting_mappings.register_mapping_version(
            actor_id="accountant-1",
            event_type="PAYMENT_PAID",
            debit_account="BANK",
            credit_account="TRAINING_REVENUE",
            version="1.0.0",
            effective_at="2026-09-10T00:00:00",
            evidence_refs=["ACCOUNTANT-REVIEW-1"],
        )


@pytest.mark.asyncio
async def test_tampered_current_projection_is_rejected(mapping_db):
    row = await accounting_mappings.register_mapping_version(
        actor_id="accountant-1",
        event_type="PAYMENT_PAID",
        debit_account="BANK",
        credit_account="TRAINING_REVENUE",
        version="1.0.0",
        effective_at="2026-09-10T00:00:00+00:00",
        evidence_refs=["ACCOUNTANT-REVIEW-1"],
    )
    await mapping_db.accounting_mappings.update_one(
        {"event_type": "PAYMENT_PAID"}, {"$set": {"policy_hash": "0" * 64}}
    )
    with pytest.raises(ValueError, match="projection integrity"):
        await accounting_mappings.get_mapping("PAYMENT_PAID")
    policy = await policy_registry.get_version(row["policy_version_id"])
    assert await policy_registry.verify_version_integrity(policy) is True
