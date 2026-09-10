from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pytest
from mongomock_motor import AsyncMongoMockClient

from services import evidence_graph, expert_access, policy_registry, professional_governance
from services import quality_advanced, quality_core


@pytest.fixture
async def quality_db(monkeypatch):
    client = AsyncMongoMockClient()
    test_db = client["cvln_quality_advanced_test"]
    for module in (
        evidence_graph,
        expert_access,
        policy_registry,
        professional_governance,
        quality_advanced,
        quality_core,
    ):
        monkeypatch.setattr(module, "db", test_db)
    yield test_db
    client.close()


def _past() -> str:
    return (datetime.now(timezone.utc) - timedelta(hours=1)).isoformat()


@pytest.mark.asyncio
async def test_needs_assessment_is_added_to_learner_quality_evidence(quality_db):
    assessment = await quality_advanced.record_needs_assessment(
        actor_id="advisor",
        user_id="L1",
        formation_code="FMS-A",
        needs=["Improve arrangement"],
        prerequisites=["DAW basics"],
        accommodations=[],
        evidence_refs=["INTERVIEW-1"],
    )
    assert assessment["status"] == "RECORDED"
    evidence = await quality_db.quality_learner_evidence.find_one(
        {"user_id": "L1"}, {"_id": 0}
    )
    assert evidence["evidence_ref"] == assessment["id"]


@pytest.mark.asyncio
async def test_signed_attendance_requires_independent_verification(quality_db):
    with pytest.raises(ValueError, match="attestation and verification"):
        await quality_advanced.record_attendance_proof(
            actor_id="trainer",
            user_id="L1",
            formation_code="FMS-A",
            session_id="S1",
            mode="PHYSICAL",
            attended=True,
            evidence_ref="SESSION-1",
            signature_attestation_id="NSIG-1",
        )
    await quality_db.native_signature_verifications.insert_one(
        {
            "id": "NSIGVER-1",
            "attestation_id": "NSIG-1",
            "status": "VERIFIED_FREK",
            "verified_at": "2026-09-10T12:00:00+00:00",
        }
    )
    row = await quality_advanced.record_attendance_proof(
        actor_id="trainer",
        user_id="L1",
        formation_code="FMS-A",
        session_id="S1",
        mode="PHYSICAL",
        attended=True,
        evidence_ref="SESSION-1",
        signature_attestation_id="NSIG-1",
        signature_verification_id="NSIGVER-1",
    )
    assert row["signature_verified"] is True


@pytest.mark.asyncio
async def test_kpis_are_metrics_not_governance_thresholds(quality_db):
    await quality_core.record_satisfaction(user_id="L1", formation_code="FMS-A", score=2)
    await quality_core.record_satisfaction(user_id="L2", formation_code="FMS-A", score=5)
    await quality_core.record_attendance(
        actor_id="trainer",
        user_id="L1",
        formation_code="FMS-A",
        session_id="S1",
        mode="DIGITAL",
        attended=True,
        evidence_ref="ATT-1",
    )
    metrics = await quality_advanced.quality_kpis("FMS-A")
    assert metrics["status"] == "EVIDENCE_METRICS_ONLY"
    assert metrics["governance_decision"] is None
    assert metrics["attendance_rate"] == 1.0


@pytest.mark.asyncio
async def test_quality_retention_binds_immutable_policy(quality_db):
    policy = await policy_registry.register_version(
        actor_id="founder",
        policy_key="QUALITY_RETENTION",
        version="1.0.0",
        kind="POLICY",
        title="Quality retention",
        content={"retain_evidence_days": 1825},
        effective_at=_past(),
        evidence_refs=["QLT-015"],
    )
    row = await quality_advanced.record_quality_retention_policy(
        actor_id="quality",
        record_type="ATTENDANCE",
        retention_days=1825,
        policy_version_id=policy["id"],
        evidence_refs=["RETENTION-DECISION-1"],
    )
    assert row["policy_hash"] == policy["content_hash"]


@pytest.mark.asyncio
async def test_quality_workspace_requires_assignment_and_scope(quality_db):
    partner = await quality_core.register_partner(
        actor_id="quality",
        name="Partner",
        organisation="Partner Org",
        evidence_refs=["CONTRACT-1"],
    )
    scope = await quality_core.assign_formation_scope(
        actor_id="quality",
        partner_id=partner["id"],
        formation_code="FMS-A",
        evidence_refs=["CONTRACT-1"],
    )
    case = await professional_governance.create_case(
        actor_id="admin",
        title="Quality review",
        domain="QUALITY",
        description="Partner review",
        metadata={"quality_scope_ids": [scope["id"]]},
    )
    expert = await professional_governance.create_expert(
        actor_id="admin",
        display_name="Quality Expert",
        email="quality@example.test",
        domains=["QUALITY"],
    )
    assignment = await professional_governance.assign_expert(
        actor_id="admin",
        case_id=case["id"],
        expert_id=expert["id"],
        scope=["quality:case:read"],
    )
    raw_key, _ = await professional_governance.issue_expert_api_key(
        actor_id="admin",
        assignment_id=assignment["id"],
        expires_at=(datetime.now(timezone.utc) + timedelta(hours=2)).isoformat(),
    )
    workspace = await quality_advanced.get_quality_workspace(
        raw_key=raw_key, case_id=case["id"]
    )
    assert workspace["global_access"] is False
    assert workspace["scopes"][0]["scope"]["id"] == scope["id"]
