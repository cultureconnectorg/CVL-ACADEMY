from __future__ import annotations

import pytest
from mongomock_motor import AsyncMongoMockClient

from services import incident_core, professional_governance
from services import quality_core as quality


@pytest.fixture
async def quality_db(monkeypatch):
    client = AsyncMongoMockClient()
    test_db = client["cvln_quality_test"]
    for module in (quality, incident_core, professional_governance):
        monkeypatch.setattr(module, "db", test_db)
    yield test_db
    client.close()


@pytest.mark.asyncio
async def test_partner_is_unverified_without_evidence_and_scope_requires_partner(quality_db):
    partner = await quality.register_partner(
        actor_id="admin-1",
        name="Quality Partner",
        organisation="Partner Org",
        claimed_certifications=["QUALIOPI"],
    )
    assert partner["verification_status"] == "UNVERIFIED"

    scope = await quality.assign_formation_scope(
        actor_id="admin-1",
        partner_id=partner["id"],
        formation_code="FMS-01",
        evidence_refs=["CONTRACT-1"],
    )
    assert scope["formation_code"] == "FMS-01"

    with pytest.raises(LookupError):
        await quality.assign_formation_scope(
            actor_id="admin-1",
            partner_id="missing",
            formation_code="FMS-02",
            evidence_refs=["CONTRACT-2"],
        )


@pytest.mark.asyncio
async def test_scope_assignment_requires_authority_or_contract_evidence(quality_db):
    partner = await quality.register_partner(
        actor_id="admin-1", name="Quality Partner", organisation="Partner Org"
    )
    with pytest.raises(ValueError, match="requires contractual/authority evidence"):
        await quality.assign_formation_scope(
            actor_id="admin-1",
            partner_id=partner["id"],
            formation_code="FMS-01",
            evidence_refs=[],
        )


@pytest.mark.asyncio
async def test_learner_quality_file_composes_evidence_attendance_and_satisfaction(quality_db):
    await quality.record_learner_quality_evidence(
        actor_id="trainer-1",
        user_id="u1",
        formation_code="FMS-01",
        cohort_id="C1",
        evidence_type="prerequisite",
        evidence_ref="EVID-1",
    )
    await quality.record_attendance(
        actor_id="trainer-1",
        user_id="u1",
        formation_code="FMS-01",
        session_id="S1",
        mode="physical",
        attended=True,
        evidence_ref="SIGN-1",
    )
    await quality.record_satisfaction(
        user_id="u1", formation_code="FMS-01", score=5, comment="Très bien"
    )

    dossier = await quality.learner_quality_file("u1", "FMS-01")
    assert len(dossier["evidence"]) == 1
    assert len(dossier["attendance"]) == 1
    assert len(dossier["satisfaction"]) == 1


@pytest.mark.asyncio
async def test_signed_attendance_requires_proof_reference(quality_db):
    with pytest.raises(ValueError, match="requires evidence_ref"):
        await quality.record_attendance(
            actor_id="trainer-1",
            user_id="u1",
            formation_code="FMS-01",
            session_id="S1",
            mode="physical",
            attended=True,
            signed_at="2026-09-10T10:00:00+00:00",
            evidence_ref=None,
        )


@pytest.mark.asyncio
async def test_satisfaction_summary_is_real_aggregate(quality_db):
    await quality.record_satisfaction(user_id="u1", formation_code="FMS-01", score=5)
    await quality.record_satisfaction(user_id="u2", formation_code="FMS-01", score=3)
    summary = await quality.satisfaction_summary("FMS-01")
    assert summary == {"formation_code": "FMS-01", "responses": 2, "average": 4.0}


@pytest.mark.asyncio
async def test_satisfaction_analysis_exposes_distribution_without_fake_governance_threshold(quality_db):
    for idx, score in enumerate([2, 3, 4, 5], start=1):
        await quality.record_satisfaction(
            user_id=f"u{idx}", formation_code="FMS-01", score=score
        )
    analysis = await quality.satisfaction_analysis("FMS-01")
    assert analysis["responses"] == 4
    assert analysis["distribution"] == {"1": 0, "2": 1, "3": 1, "4": 1, "5": 1}
    assert analysis["trend_delta"] == 2.0
    assert analysis["governance_decision"] is None


@pytest.mark.asyncio
async def test_complaint_workflow_and_improvement_source_requirement(quality_db):
    complaint = await quality.create_complaint(
        actor_id="u1",
        user_id="u1",
        formation_code="FMS-01",
        category="quality",
        description="Un problème documenté",
        severity="medium",
    )
    assert complaint["status"] == "OPEN"
    assert complaint["quality_level"] == "UNCLASSIFIED"

    updated = await quality.transition_complaint(
        actor_id="quality-1",
        complaint_id=complaint["id"],
        state="RESOLVED",
        resolution="Correction appliquée",
    )
    assert updated["status"] == "RESOLVED"

    with pytest.raises(ValueError, match="source signal"):
        await quality.create_improvement_action(
            actor_id="quality-1",
            title="Improve onboarding",
            source_refs=[],
            owner="quality",
        )

    action = await quality.create_improvement_action(
        actor_id="quality-1",
        title="Improve onboarding",
        source_refs=[complaint["id"]],
        owner="quality",
    )
    assert action["status"] == "OPEN"


@pytest.mark.asyncio
async def test_q5_complaint_requires_explicit_routing_and_creates_one_canonical_incident(quality_db):
    complaint = await quality.create_complaint(
        actor_id="u1",
        user_id="u1",
        formation_code="FMS-01",
        category="safety",
        description="Serious safety issue",
        severity="high",
    )
    with pytest.raises(ValueError, match="requires explicit projection_domains"):
        await quality.classify_and_escalate_complaint(
            actor_id="quality-1",
            complaint_id=complaint["id"],
            quality_level="Q5_LEGAL_SAFETY",
            evidence_refs=["Q-EVID-1"],
            projection_domains=[],
        )

    first = await quality.classify_and_escalate_complaint(
        actor_id="quality-1",
        complaint_id=complaint["id"],
        quality_level="Q5_LEGAL_SAFETY",
        evidence_refs=["Q-EVID-1"],
        projection_domains=["LEGAL", "RISK"],
    )
    second = await quality.classify_and_escalate_complaint(
        actor_id="quality-2",
        complaint_id=complaint["id"],
        quality_level="Q5_LEGAL_SAFETY",
        evidence_refs=["Q-EVID-2"],
        projection_domains=["LEGAL", "RISK"],
    )
    assert first["status"] == "ESCALATED"
    assert first["canonical_incident_id"] == second["canonical_incident_id"]
    assert await quality_db.incidents.count_documents({}) == 1


@pytest.mark.asyncio
async def test_quality_partner_workspace_cannot_browse_unassigned_formation(quality_db):
    partner = await quality.register_partner(
        actor_id="admin-1", name="Scoped Partner", organisation="Partner Org"
    )
    await quality.assign_formation_scope(
        actor_id="admin-1",
        partner_id=partner["id"],
        formation_code="FMS-01",
        cohort_id="C1",
        evidence_refs=["CONTRACT-1"],
    )
    await quality.record_learner_quality_evidence(
        actor_id="trainer",
        user_id="u1",
        formation_code="FMS-01",
        cohort_id="C1",
        evidence_type="assessment",
        evidence_ref="EV-1",
    )
    await quality.record_learner_quality_evidence(
        actor_id="trainer",
        user_id="u2",
        formation_code="FMS-99",
        cohort_id="C9",
        evidence_type="assessment",
        evidence_ref="EV-OTHER",
    )

    workspace = await quality.quality_partner_workspace(partner["id"])
    assert workspace["global_access"] is False
    assert len(workspace["scopes"]) == 1
    refs = [row["evidence_ref"] for row in workspace["scopes"][0]["learner_evidence"]]
    assert refs == ["EV-1"]
    assert "EV-OTHER" not in refs


@pytest.mark.asyncio
async def test_quality_audit_pack_reuses_evidence_graph_and_requires_scope(quality_db, monkeypatch):
    partner = await quality.register_partner(
        actor_id="admin-1", name="Quality Partner", organisation="Partner Org"
    )
    scope = await quality.assign_formation_scope(
        actor_id="admin-1",
        partner_id=partner["id"],
        formation_code="FMS-01",
        cohort_id="C1",
        evidence_refs=["CONTRACT-1"],
    )

    captured = {}

    async def fake_create_pack(**kwargs):
        captured.update(kwargs)
        return {
            "id": "EPACK-1",
            "consumer": kwargs["consumer"],
            "node_refs": [{"node_id": node_id} for node_id in kwargs["node_ids"]],
            "composition_mode": "REFERENCE_ONLY",
        }

    monkeypatch.setattr(quality.evidence_graph, "create_pack", fake_create_pack)
    pack = await quality.create_quality_audit_pack(
        actor_id="quality-1",
        partner_id=partner["id"],
        formation_code="FMS-01",
        cohort_id="C1",
        node_ids=["EVID-1", "EVID-2"],
        evidence_refs=["AUDIT-REQUEST-1"],
    )
    assert pack["consumer"] == "QUALITY"
    assert pack["composition_mode"] == "REFERENCE_ONLY"
    assert captured["evidence_refs"][0] == scope["id"]

    with pytest.raises(PermissionError, match="no active scope"):
        await quality.create_quality_audit_pack(
            actor_id="quality-1",
            partner_id=partner["id"],
            formation_code="FMS-99",
            cohort_id=None,
            node_ids=["EVID-1"],
            evidence_refs=["AUDIT-REQUEST-2"],
        )
