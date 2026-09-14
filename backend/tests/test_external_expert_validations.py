from __future__ import annotations

import pytest
from mongomock_motor import AsyncMongoMockClient

from services import expert_access, external_expert_validations, professional_governance


@pytest.fixture
async def validation_db(monkeypatch):
    client = AsyncMongoMockClient()
    test_db = client["cvln_external_expert_validations_test"]
    for module in (expert_access, external_expert_validations, professional_governance):
        monkeypatch.setattr(module, "db", test_db)
    yield test_db
    client.close()


async def _key(domain: str, scopes: list[str], metadata: dict):
    case = await professional_governance.create_case(
        actor_id="admin",
        title=f"{domain} case",
        domain=domain,
        description="Scoped external review",
        metadata=metadata,
    )
    expert = await professional_governance.create_expert(
        actor_id="admin",
        display_name="External expert",
        email=f"{domain.lower()}@example.test",
        domains=[domain],
    )
    assignment = await professional_governance.assign_expert(
        actor_id="admin",
        case_id=case["id"],
        expert_id=expert["id"],
        scope=scopes,
    )
    raw, _ = await professional_governance.issue_expert_api_key(
        actor_id="admin",
        assignment_id=assignment["id"],
        expires_at="2099-09-10T00:00:00+00:00",
    )
    return case, raw


@pytest.mark.asyncio
async def test_accountant_reconciliation_review_is_period_scoped(validation_db):
    await validation_db.accounting_periods.insert_one(
        {"id": "PER-1", "starts_at": "2026-09-01T00:00:00+00:00", "ends_at": "2026-10-01T00:00:00+00:00"}
    )
    await validation_db.payments.insert_one(
        {"id": "PAY-1", "created_at": "2026-09-10T10:00:00+00:00"}
    )
    await validation_db.accounting_reconciliations.insert_one(
        {"id": "REC-1", "payment_id": "PAY-1", "reconciled": True}
    )
    case, raw = await _key(
        "ACCOUNTING",
        ["accounting:reconciliation:review"],
        {"accounting_period_ids": ["PER-1"]},
    )
    row = await external_expert_validations.accountant_review_reconciliation(
        raw_key=raw,
        case_id=case["id"],
        reconciliation_id="REC-1",
        outcome="VALIDATED",
        rationale="Bank and provider evidence agree",
        evidence_refs=["BANK-1", "PROVIDER-1"],
    )
    assert row["outcome"] == "VALIDATED"


@pytest.mark.asyncio
async def test_tax_package_validation_never_exists_without_expert_evidence(validation_db):
    await validation_db.accounting_tax_packages.insert_one(
        {"id": "TAX-1", "period_id": "PER-1", "status": "PREPARED", "tax_validated": False}
    )
    case, raw = await _key(
        "ACCOUNTING",
        ["accounting:tax:review"],
        {"accounting_period_ids": ["PER-1"]},
    )
    row = await external_expert_validations.accountant_validate_tax_package(
        raw_key=raw,
        case_id=case["id"],
        tax_package_id="TAX-1",
        outcome="EXPERT_VALIDATED",
        rationale="Reviewed against supplied tax evidence",
        evidence_refs=["TAX-OPINION-1"],
    )
    assert row["outcome"] == "EXPERT_VALIDATED"
    package = await validation_db.accounting_tax_packages.find_one({"id": "TAX-1"})
    assert package["tax_validated"] is True
    assert package["tax_validation_status"] == "EXPERT_VALIDATED_WITH_EVIDENCE"


@pytest.mark.asyncio
async def test_dpo_processing_review_is_case_scoped(validation_db):
    await validation_db.privacy_processing_activities.insert_one({"id": "ROPA-1"})
    await validation_db.privacy_processing_activities.insert_one({"id": "ROPA-2"})
    case, raw = await _key(
        "PRIVACY",
        ["privacy:processing:review"],
        {"processing_activity_ids": ["ROPA-1"]},
    )
    row = await external_expert_validations.privacy_validate_processing_activity(
        raw_key=raw,
        case_id=case["id"],
        activity_id="ROPA-1",
        outcome="VALIDATED",
        rationale="Purpose and legal basis reviewed",
        evidence_refs=["DPO-1"],
    )
    assert row["outcome"] == "VALIDATED"
    with pytest.raises(PermissionError, match="outside assigned"):
        await external_expert_validations.privacy_validate_processing_activity(
            raw_key=raw,
            case_id=case["id"],
            activity_id="ROPA-2",
            outcome="VALIDATED",
            rationale="No",
            evidence_refs=["DPO-2"],
        )


@pytest.mark.asyncio
async def test_quality_correction_does_not_mutate_source_evidence(validation_db):
    await validation_db.quality_scopes.insert_one(
        {"id": "QS-1", "formation_code": "FMS-A", "status": "ACTIVE"}
    )
    await validation_db.quality_learner_evidence.insert_one(
        {"id": "QE-1", "formation_code": "FMS-A", "evidence_type": "ATTENDANCE"}
    )
    case, raw = await _key(
        "QUALITY",
        ["quality:evidence:correct"],
        {"quality_scope_ids": ["QS-1"]},
    )
    row = await external_expert_validations.quality_record_correction(
        raw_key=raw,
        case_id=case["id"],
        evidence_id="QE-1",
        correction={"note": "missing signature"},
        rationale="Correction proposed after audit",
        evidence_refs=["AUDIT-1"],
    )
    assert row["status"] == "PROPOSED_CORRECTION"
    source = await validation_db.quality_learner_evidence.find_one({"id": "QE-1"})
    assert "note" not in source


@pytest.mark.asyncio
async def test_broker_recommendation_is_not_automatic_risk_authority(validation_db):
    await validation_db.risks.insert_one({"id": "RISK-1", "status": "OPEN"})
    case, raw = await _key(
        "RISK",
        ["risk:recommendation:write"],
        {"risk_ids": ["RISK-1"]},
    )
    row = await external_expert_validations.broker_record_recommendation(
        raw_key=raw,
        case_id=case["id"],
        risk_id="RISK-1",
        recommendation="Increase cyber coverage",
        rationale="Exposure exceeds current limit",
        evidence_refs=["BROKER-1"],
    )
    assert row["status"] == "EXTERNAL_RECOMMENDATION_ONLY"
    risk = await validation_db.risks.find_one({"id": "RISK-1"})
    assert risk["status"] == "OPEN"
