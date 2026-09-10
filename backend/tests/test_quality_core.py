from __future__ import annotations

import pytest
from mongomock_motor import AsyncMongoMockClient

from services import quality_core as quality


@pytest.fixture
async def quality_db(monkeypatch):
    client = AsyncMongoMockClient()
    test_db = client["cvln_quality_test"]
    monkeypatch.setattr(quality, "db", test_db)
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
async def test_satisfaction_summary_is_real_aggregate(quality_db):
    await quality.record_satisfaction(user_id="u1", formation_code="FMS-01", score=5)
    await quality.record_satisfaction(user_id="u2", formation_code="FMS-01", score=3)
    summary = await quality.satisfaction_summary("FMS-01")
    assert summary == {"formation_code": "FMS-01", "responses": 2, "average": 4.0}


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
