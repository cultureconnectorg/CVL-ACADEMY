from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pytest
from mongomock_motor import AsyncMongoMockClient

from services import assurance_core, authority_policy, evidence_graph, expert_access
from services import policy_registry, professional_governance, risk_advanced


@pytest.fixture
async def risk_db(monkeypatch):
    client = AsyncMongoMockClient()
    test_db = client["cvln_risk_advanced_test"]
    for module in (
        assurance_core,
        authority_policy,
        evidence_graph,
        expert_access,
        policy_registry,
        professional_governance,
        risk_advanced,
    ):
        monkeypatch.setattr(module, "db", test_db)
    yield test_db
    client.close()


def _past() -> str:
    return (datetime.now(timezone.utc) - timedelta(hours=1)).isoformat()


async def _critical_policy():
    return await authority_policy.register_policy_version(
        actor_id="founder",
        policy_key="CRITICAL_RISK_TREATMENT",
        version="1.0.0",
        title="Critical risk treatment",
        rules=[
            {
                "id": "A5",
                "priority": 1,
                "effect": "ALLOW",
                "reason": "Founder systemic authority required",
                "conditions": {
                    "actor_roles": ["FOUNDER"],
                    "actions": ["CRITICAL_RISK_TREATMENT"],
                    "domains": ["RISK"],
                    "minimum_authority_level": "A5_FOUNDER_SYSTEMIC",
                },
            }
        ],
        effective_at=_past(),
        doctrine_ref="GOV-14",
        evidence_refs=["RSK-004"],
    )


@pytest.mark.asyncio
async def test_critical_risk_treatment_requires_a5_and_evidence(risk_db):
    risk = await assurance_core.create_risk(
        actor_id="risk",
        title="Provider outage",
        domain="OPERATIONS",
        impact=5,
        probability=5,
    )
    policy = await _critical_policy()
    with pytest.raises(PermissionError, match="did not allow"):
        await risk_advanced.set_critical_risk_treatment(
            actor_id="operator",
            actor_role="OPERATOR",
            authority_level="A2_DOMAIN_REVIEWER",
            risk_id=risk["id"],
            treatment="MITIGATE",
            policy_version_id=policy["id"],
            owner="ops",
            mitigation="Failover",
            deadline="2026-09-20",
            evidence_refs=["PLAN-1"],
        )
    treated = await risk_advanced.set_critical_risk_treatment(
        actor_id="founder",
        actor_role="FOUNDER",
        authority_level="A5_FOUNDER_SYSTEMIC",
        risk_id=risk["id"],
        treatment="MITIGATE",
        policy_version_id=policy["id"],
        owner="ops",
        mitigation="Failover and restore test",
        deadline="2026-09-20",
        evidence_refs=["PLAN-1"],
    )
    assert treated["status"] == "TREATING"
    assert treated["authority"]["decision"] == "ALLOW"


@pytest.mark.asyncio
async def test_coverage_stays_unconfirmed_until_explicit_review(risk_db):
    risk = await assurance_core.create_risk(
        actor_id="risk",
        title="Cyber event",
        domain="SECURITY",
        impact=5,
        probability=4,
    )
    policy = await risk_advanced.register_insurance_policy(
        actor_id="risk",
        provider="Insurer",
        policy_ref="POLICY-1",
        coverage_types=["CYBER"],
        limits={"CYBER": 10000000},
        starts_at=(datetime.now(timezone.utc) - timedelta(days=1)).isoformat(),
        ends_at=(datetime.now(timezone.utc) + timedelta(days=365)).isoformat(),
        evidence_refs=["POLICY-PDF-1"],
    )
    link = await risk_advanced.link_risk_coverage(
        actor_id="risk",
        risk_id=risk["id"],
        insurance_policy_id=policy["id"],
        coverage_type="CYBER",
        evidence_refs=["MAPPING-1"],
    )
    assert link["coverage_confirmed"] is False
    gate = await risk_advanced.uncovered_asset_gate()
    assert gate["pass"] is False

    reviewed = await risk_advanced.review_coverage_link(
        actor_id="broker",
        link_id=link["id"],
        coverage_confirmed=True,
        rationale="Policy schedule explicitly covers cyber risk",
        evidence_refs=["BROKER-REVIEW-1"],
    )
    assert reviewed["status"] == "CONFIRMED"
    gate = await risk_advanced.uncovered_asset_gate()
    assert gate["pass"] is True


@pytest.mark.asyncio
async def test_renewal_alerts_return_90_60_30_windows(risk_db):
    now = datetime(2026, 9, 10, tzinfo=timezone.utc)
    for days, suffix in ((89, "90"), (59, "60"), (29, "30")):
        await risk_advanced.register_insurance_policy(
            actor_id="risk",
            provider=f"Insurer-{suffix}",
            policy_ref=f"P-{suffix}",
            coverage_types=["GENERAL"],
            limits={"GENERAL": 1000},
            starts_at=(now - timedelta(days=1)).isoformat(),
            ends_at=(now + timedelta(days=days)).isoformat(),
            evidence_refs=[f"E-{suffix}"],
        )
    alerts = await risk_advanced.renewal_alerts(as_of=now)
    thresholds = {row["threshold_days"] for row in alerts}
    assert thresholds == {30, 60, 90}


@pytest.mark.asyncio
async def test_broker_workspace_only_exposes_case_scoped_risks(risk_db):
    in_scope = await assurance_core.create_risk(
        actor_id="risk", title="In scope", domain="RISK", impact=4, probability=4
    )
    out_scope = await assurance_core.create_risk(
        actor_id="risk", title="Out scope", domain="RISK", impact=4, probability=4
    )
    case = await professional_governance.create_case(
        actor_id="admin",
        title="Broker review",
        domain="RISK",
        description="Scoped insurance review",
        metadata={"risk_ids": [in_scope["id"]], "insurance_policy_ids": []},
    )
    expert = await professional_governance.create_expert(
        actor_id="admin",
        display_name="Broker",
        email="broker@example.test",
        domains=["RISK"],
    )
    assignment = await professional_governance.assign_expert(
        actor_id="admin",
        case_id=case["id"],
        expert_id=expert["id"],
        scope=["risk:insurance:read"],
    )
    raw_key, _ = await professional_governance.issue_expert_api_key(
        actor_id="admin",
        assignment_id=assignment["id"],
        expires_at=(datetime.now(timezone.utc) + timedelta(hours=2)).isoformat(),
    )
    workspace = await risk_advanced.get_broker_workspace(raw_key=raw_key, case_id=case["id"])
    ids = {row["id"] for row in workspace["risks"]}
    assert in_scope["id"] in ids
    assert out_scope["id"] not in ids
