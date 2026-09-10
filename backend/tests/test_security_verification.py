from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pytest
from mongomock_motor import AsyncMongoMockClient

from services import assurance_core, authority_policy, evidence_graph, expert_access
from services import policy_registry, professional_governance, security_remediation
from services import security_verification, threat_model


@pytest.fixture
async def security_db(monkeypatch):
    client = AsyncMongoMockClient()
    test_db = client["cvln_security_verification_test"]
    for module in (
        assurance_core,
        authority_policy,
        evidence_graph,
        expert_access,
        policy_registry,
        professional_governance,
        security_remediation,
        security_verification,
        threat_model,
    ):
        monkeypatch.setattr(module, "db", test_db)
    yield test_db
    client.close()


def _past() -> str:
    return (datetime.now(timezone.utc) - timedelta(hours=1)).isoformat()


async def _risk_policy():
    return await authority_policy.register_policy_version(
        actor_id="founder",
        policy_key="SECURITY_RISK_ACCEPTANCE",
        version="1.0.0",
        title="Security risk acceptance",
        rules=[
            {
                "id": "A5-ALLOW",
                "priority": 1,
                "effect": "ALLOW",
                "reason": "Founder may accept scoped security risk",
                "conditions": {
                    "actor_roles": ["FOUNDER"],
                    "actions": ["SECURITY_RISK_ACCEPT"],
                    "domains": ["SECURITY"],
                    "minimum_authority_level": "A5_FOUNDER_SYSTEMIC",
                },
            }
        ],
        effective_at=_past(),
        doctrine_ref="GOV-14",
        evidence_refs=["SEC-010"],
    )


@pytest.mark.asyncio
async def test_asset_inventory_records_runtime_surfaces(security_db):
    asset = await security_verification.register_asset(
        actor_id="security",
        name="Academy API",
        asset_type="API",
        owner="platform",
        exposure="internet",
        criticality="high",
        endpoints=["/api/auth/login", "/api/payments/webhook"],
        services=["fastapi"],
        data_stores=["mongo"],
        attack_surfaces=["HTTP", "WEBHOOK"],
        evidence_refs=["ROUTE-TREE-1"],
    )
    assert asset["inventory_complete"] is True
    assert "/api/auth/login" in asset["endpoints"]
    assert asset["data_stores"] == ["mongo"]


@pytest.mark.asyncio
async def test_attack_suite_cannot_pass_with_missing_required_areas(security_db):
    partial = await security_verification.record_attack_suite_run(
        actor_id="security",
        suite="APPLICATION",
        run_ref="CI-100",
        covered_areas=["AUTH", "RBAC", "IDOR"],
        evidence_refs=["CI-100-ARTIFACT"],
    )
    assert partial["passed"] is False
    assert "SSRF" in partial["missing_areas"]

    complete = await security_verification.record_attack_suite_run(
        actor_id="security",
        suite="PAYMENT",
        run_ref="CI-101",
        covered_areas=sorted(security_verification.PAYMENT_ATTACK_AREAS),
        evidence_refs=["CI-101-ARTIFACT"],
    )
    assert complete["passed"] is True


@pytest.mark.asyncio
async def test_retest_is_required_to_resolve_finding(security_db):
    finding = await assurance_core.create_security_finding(
        actor_id="security",
        title="IDOR",
        severity="HIGH",
        asset_id=None,
        evidence_refs=["ATTACK-1"],
        remediation="Enforce ownership checks",
    )
    failed = await security_verification.record_finding_retest(
        actor_id="security",
        finding_id=finding["id"],
        passed=False,
        test_refs=["test_idor.py::test_cross_owner_denied"],
        evidence_refs=["CI-200"],
    )
    assert failed["finding_status"] == "REMEDIATING"
    passed = await security_verification.record_finding_retest(
        actor_id="security",
        finding_id=finding["id"],
        passed=True,
        test_refs=["test_idor.py::test_cross_owner_denied"],
        evidence_refs=["CI-201"],
    )
    assert passed["finding_status"] == "RESOLVED"


@pytest.mark.asyncio
async def test_security_risk_acceptance_requires_a5_evidence_and_future_expiry(security_db):
    finding = await assurance_core.create_security_finding(
        actor_id="security",
        title="Known temporary exposure",
        severity="HIGH",
        asset_id=None,
        evidence_refs=["FIND-1"],
        remediation="Planned fix",
    )
    policy = await _risk_policy()
    with pytest.raises(ValueError, match="future"):
        await security_verification.accept_finding_risk(
            actor_id="founder",
            actor_role="FOUNDER",
            authority_level="A5_FOUNDER_SYSTEMIC",
            finding_id=finding["id"],
            rationale="Temporary acceptance",
            expires_at=(datetime.now(timezone.utc) - timedelta(minutes=1)).isoformat(),
            policy_version_id=policy["id"],
            evidence_refs=["DECISION-1"],
        )
    acceptance = await security_verification.accept_finding_risk(
        actor_id="founder",
        actor_role="FOUNDER",
        authority_level="A5_FOUNDER_SYSTEMIC",
        finding_id=finding["id"],
        rationale="Temporary acceptance while remediation deploys",
        expires_at=(datetime.now(timezone.utc) + timedelta(days=2)).isoformat(),
        policy_version_id=policy["id"],
        evidence_refs=["DECISION-1"],
    )
    assert acceptance["status"] == "ACTIVE"
    stored = await security_db.security_findings.find_one(
        {"id": finding["id"]}, {"_id": 0}
    )
    assert stored["status"] == "ACCEPTED"


@pytest.mark.asyncio
async def test_aggregate_release_gate_requires_ci_attack_threat_finding_and_remediation_green(
    security_db,
):
    for gate in sorted(security_verification.CI_GATES):
        await security_verification.record_ci_gate(
            actor_id="ci",
            gate=gate,
            run_ref=f"RUN-{gate}",
            passed=True,
            evidence_refs=[f"ARTIFACT-{gate}"],
        )
    for suite, areas in (
        ("APPLICATION", security_verification.REQUIRED_ATTACK_AREAS),
        ("PAYMENT", security_verification.PAYMENT_ATTACK_AREAS),
    ):
        await security_verification.record_attack_suite_run(
            actor_id="ci",
            suite=suite,
            run_ref=f"RUN-{suite}",
            covered_areas=sorted(areas),
            evidence_refs=[f"ARTIFACT-{suite}"],
        )
    gate = await security_verification.security_release_gate()
    assert gate["pass"] is True

    await threat_model.create_threat(
        actor_id="security",
        title="Token replay",
        category="AUTH",
        asset_id=None,
        attack_surface="API",
        abuse_case="Replay token",
        severity="HIGH",
    )
    gate = await security_verification.security_release_gate()
    assert gate["pass"] is False
    assert gate["threat_gate"]["blocking_count"] == 1


@pytest.mark.asyncio
async def test_pentest_workspace_is_black_box_and_case_scoped(security_db):
    case = await professional_governance.create_case(
        actor_id="admin",
        title="External pentest",
        domain="SECURITY",
        description="Black-box API assessment",
        sensitivity="SECURITY_RESTRICTED",
        metadata={
            "black_box_scope": {
                "base_url": "https://staging.academy.invalid",
                "allowed_routes": ["/api/auth/*"],
                "forbidden": ["source-code", "production-data"],
            }
        },
    )
    expert = await professional_governance.create_expert(
        actor_id="admin",
        display_name="Pentester",
        email="pentest@example.test",
        domains=["SECURITY"],
    )
    assignment = await professional_governance.assign_expert(
        actor_id="admin",
        case_id=case["id"],
        expert_id=expert["id"],
        scope=["security:pentest:read"],
    )
    raw_key, _ = await professional_governance.issue_expert_api_key(
        actor_id="admin",
        assignment_id=assignment["id"],
        expires_at=(datetime.now(timezone.utc) + timedelta(hours=4)).isoformat(),
    )
    workspace = await security_verification.get_pentest_workspace(
        raw_key=raw_key, case_id=case["id"]
    )
    assert workspace["internal_code_exposed"] is False
    assert workspace["unassigned_findings_exposed"] is False
    assert workspace["black_box_scope"]["allowed_routes"] == ["/api/auth/*"]
