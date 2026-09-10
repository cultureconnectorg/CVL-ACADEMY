from __future__ import annotations

import pytest
from mongomock_motor import AsyncMongoMockClient

from services import (
    accounting_mappings,
    expert_access,
    external_expert_actions,
    policy_registry,
    professional_governance,
    risk_advanced,
)


@pytest.fixture
async def expert_db(monkeypatch):
    client = AsyncMongoMockClient()
    test_db = client["cvln_external_expert_actions_test"]
    for module in (
        accounting_mappings,
        expert_access,
        external_expert_actions,
        policy_registry,
        professional_governance,
        risk_advanced,
    ):
        monkeypatch.setattr(module, "db", test_db)
    yield test_db
    client.close()


async def _key(domain: str, scope: list[str], metadata: dict | None = None):
    case = await professional_governance.create_case(
        actor_id="admin",
        title=f"{domain} case",
        domain=domain,
        description="Scoped expert case",
        metadata=metadata or {},
    )
    expert = await professional_governance.create_expert(
        actor_id="admin",
        display_name=f"{domain} expert",
        email=f"{domain.lower()}@example.test",
        domains=[domain],
    )
    assignment = await professional_governance.assign_expert(
        actor_id="admin",
        case_id=case["id"],
        expert_id=expert["id"],
        scope=["case:read", *scope],
    )
    raw, _ = await professional_governance.issue_expert_api_key(
        actor_id="admin",
        assignment_id=assignment["id"],
        expires_at="2099-09-10T00:00:00+00:00",
    )
    return case, expert, raw


@pytest.mark.asyncio
async def test_privacy_review_cannot_escape_case_processor_scope(expert_db):
    await expert_db.privacy_processors.insert_one({"id": "PROC-1", "status": "PROPOSED"})
    case, _, raw = await _key(
        "PRIVACY",
        ["privacy:processor:review"],
        {"processor_ids": ["PROC-1"]},
    )
    result = await external_expert_actions.privacy_review_processor(
        raw_key=raw,
        case_id=case["id"],
        processor_id="PROC-1",
        recommendation="approve",
        rationale="DPA reviewed",
        evidence_refs=["DPA-1"],
    )
    assert result["status"] == "EXTERNAL_RECOMMENDATION_ONLY"
    assert result["recommendation"] == "APPROVE"
    await expert_db.privacy_processors.insert_one({"id": "PROC-2", "status": "PROPOSED"})
    with pytest.raises(PermissionError, match="outside assigned"):
        await external_expert_actions.privacy_review_processor(
            raw_key=raw,
            case_id=case["id"],
            processor_id="PROC-2",
            recommendation="approve",
            rationale="No",
            evidence_refs=["DPA-2"],
        )


@pytest.mark.asyncio
async def test_pentester_submits_findings_without_internal_source_access(expert_db):
    case, _, raw = await _key(
        "SECURITY", ["security:pentest:submit", "security:pentest:retest"]
    )
    finding = await external_expert_actions.submit_pentest_finding(
        raw_key=raw,
        case_id=case["id"],
        title="IDOR",
        severity="HIGH",
        attack_surface="public API",
        evidence_refs=["PENTEST-PROOF-1"],
        remediation_recommendation="enforce ownership",
    )
    assert finding["status"] == "SUBMITTED_EXTERNAL"
    retest = await external_expert_actions.submit_pentest_retest(
        raw_key=raw,
        case_id=case["id"],
        finding_id=finding["id"],
        outcome="PASS",
        evidence_refs=["RETEST-1"],
    )
    assert retest["outcome"] == "PASS"


@pytest.mark.asyncio
async def test_accountant_mapping_is_restricted_to_case_event_types(expert_db):
    case, _, raw = await _key(
        "ACCOUNTING",
        ["accounting:mapping:write"],
        {"allowed_event_types": ["PAYMENT_CAPTURED"]},
    )
    result = await external_expert_actions.accountant_define_mapping(
        raw_key=raw,
        case_id=case["id"],
        event_type="PAYMENT_CAPTURED",
        debit_account="512",
        credit_account="706",
        version="1.0.0",
        effective_at="2026-09-10T00:00:00+00:00",
        evidence_refs=["ACC-EXPERT-1"],
    )
    assert result["event_type"] == "PAYMENT_CAPTURED"
    with pytest.raises(PermissionError, match="outside assigned case"):
        await external_expert_actions.accountant_define_mapping(
            raw_key=raw,
            case_id=case["id"],
            event_type="REFUND",
            debit_account="706",
            credit_account="512",
            version="1.0.0",
            effective_at="2026-09-10T00:00:00+00:00",
            evidence_refs=["ACC-EXPERT-2"],
        )


@pytest.mark.asyncio
async def test_broker_can_only_review_assigned_risk_coverage(expert_db):
    await expert_db.risks.insert_one({"id": "RISK-1", "level": 4})
    await expert_db.insurance_policies.insert_one(
        {"id": "POL-1", "coverage_types": ["CYBER"]}
    )
    await expert_db.risk_insurance_links.insert_one(
        {"id": "LINK-1", "risk_id": "RISK-1", "insurance_policy_id": "POL-1"}
    )
    case, _, raw = await _key(
        "RISK", ["risk:coverage:review"], {"risk_ids": ["RISK-1"]}
    )
    reviewed = await external_expert_actions.broker_review_coverage(
        raw_key=raw,
        case_id=case["id"],
        link_id="LINK-1",
        coverage_confirmed=True,
        rationale="Policy wording confirms coverage",
        evidence_refs=["POLICY-PDF-1"],
    )
    assert reviewed["coverage_confirmed"] is True


@pytest.mark.asyncio
async def test_quality_review_is_limited_to_scoped_formation(expert_db):
    await expert_db.quality_scopes.insert_one(
        {"id": "QSCOPE-1", "formation_code": "FMS-A", "status": "ACTIVE"}
    )
    await expert_db.quality_learner_evidence.insert_one(
        {"id": "QE-1", "formation_code": "FMS-A"}
    )
    await expert_db.quality_learner_evidence.insert_one(
        {"id": "QE-2", "formation_code": "OTHER"}
    )
    case, _, raw = await _key(
        "QUALITY",
        ["quality:evidence:review"],
        {"quality_scope_ids": ["QSCOPE-1"]},
    )
    row = await external_expert_actions.quality_review_evidence(
        raw_key=raw,
        case_id=case["id"],
        evidence_id="QE-1",
        outcome="ACCEPT",
        rationale="Evidence sufficient",
        evidence_refs=["QUAL-REVIEW-1"],
    )
    assert row["status"] == "EXTERNAL_QUALITY_REVIEW"
    with pytest.raises(PermissionError, match="outside assigned case"):
        await external_expert_actions.quality_review_evidence(
            raw_key=raw,
            case_id=case["id"],
            evidence_id="QE-2",
            outcome="ACCEPT",
            rationale="No",
            evidence_refs=["QUAL-REVIEW-2"],
        )
