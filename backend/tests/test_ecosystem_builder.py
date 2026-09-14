"""ACA-0030 — Ecosystem Builder surface tests.

`compute_ecosystem_builder_surface` composes `services.professional_
profile.compute_professional_profile` (already separately tested in
test_professional_profile.py) plus three new real reads (skill_evidence
as verified proofs, validated user_missions, event_log filtered by
`payload.user_id`) and derives the consumer/learner/professional/
builder stage from them. This suite proves each stage transition on
its own real trigger, and that the composition never invents Projects/
Collaborations/Network/Economic rows (see the module docstring's scope
contract)."""

from __future__ import annotations

import pytest
from mongomock_motor import AsyncMongoMockClient

import certification.service as certification_service_module
import services.ecosystem_builder as builder_module
import services.professional_profile as profile_module
import skills.progression as skills_progression_module
from services.ecosystem_builder import compute_ecosystem_builder_surface
from services.professional_profile import set_profile_visibility


class FakeUser:
    def __init__(self, id, frek_id, display_name, stade="graine"):
        self.id = id
        self.frek_id = frek_id
        self.display_name = display_name
        self.stade = stade


@pytest.fixture
async def builder_db(monkeypatch):
    client = AsyncMongoMockClient()
    mock_db = client["cvln_aca0030_builder_test"]
    monkeypatch.setattr(builder_module, "db", mock_db)
    monkeypatch.setattr(profile_module, "db", mock_db)
    monkeypatch.setattr(skills_progression_module, "db", mock_db)
    monkeypatch.setattr(certification_service_module, "db", mock_db)
    return mock_db


@pytest.mark.asyncio
async def test_fresh_user_is_consumer_stage_with_empty_evidence(builder_db):
    user = FakeUser("u1", "FREK-001", "Ada")
    surface = await compute_ecosystem_builder_surface(user)
    assert surface.stage == "consumer"
    assert surface.portfolio == []
    assert surface.credentials == []
    assert surface.verified_proofs == []
    assert surface.missions_completed == []
    assert surface.ecosystem_history == []


@pytest.mark.asyncio
async def test_skill_evidence_without_acquisition_is_learner_stage(builder_db):
    await builder_db.skill_evidence.insert_one(
        {
            "user_id": "u1",
            "skill_id": "FMS01-A1",
            "evidence_type": "module_completion",
            "ref": "FMS-01-M01",
            "sha256": "deadbeef",
            "ts": "2026-01-01T00:00:00Z",
        }
    )
    user = FakeUser("u1", "FREK-001", "Ada")
    surface = await compute_ecosystem_builder_surface(user)
    assert surface.stage == "learner"
    assert len(surface.verified_proofs) == 1
    assert surface.verified_proofs[0].sha256 == "deadbeef"


@pytest.mark.asyncio
async def test_validated_mission_without_acquisition_is_learner_stage(builder_db):
    await builder_db.user_missions.insert_many(
        [
            {
                "user_id": "u1",
                "mission_code": "M-01",
                "status": "validated",
                "accepted_at": "2026-01-01T00:00:00Z",
                "submitted_at": "2026-01-02T00:00:00Z",
            },
            {
                "user_id": "u1",
                "mission_code": "M-02",
                "status": "accepted",  # not validated -- must NOT count
                "accepted_at": "2026-01-01T00:00:00Z",
            },
        ]
    )
    user = FakeUser("u1", "FREK-001", "Ada")
    surface = await compute_ecosystem_builder_surface(user)
    assert surface.stage == "learner"
    assert len(surface.missions_completed) == 1
    assert surface.missions_completed[0].mission_code == "M-01"


@pytest.mark.asyncio
async def test_acquired_skill_reaches_professional_stage(builder_db):
    await builder_db.skills.insert_one(
        {
            "id": "FMS01-A1",
            "metier": "FMS",
            "niveau": "A01",
            "bloc": "B1",
            "label": "Compétence A1",
            "version": "1.0",
            "source": "admin",
        }
    )
    await builder_db.user_skills.insert_one(
        {
            "user_id": "u1",
            "skill_id": "FMS01-A1",
            "state": "acquired",
            "progression_pct": 100,
            "evidence_count": 2,
        }
    )
    user = FakeUser("u1", "FREK-001", "Ada")
    surface = await compute_ecosystem_builder_surface(user)
    assert surface.stage == "professional"
    assert len(surface.portfolio) == 1
    assert surface.is_public is False  # opt-in default -- not yet a builder


@pytest.mark.asyncio
async def test_passed_certification_reaches_professional_stage(builder_db):
    await builder_db.certification_attempts.insert_one(
        {
            "id": "a1",
            "user_id": "u1",
            "certification_code": "FMS01-A01",
            "formation_code": "FMS-01",
            "level": "A01",
            "rubric_version": "1.0",
            "status": "passed",
            "score_global": 87.5,
            "mention": "Bien",
            "jury_signature": {
                "jury_id": "j1",
                "signed_at": "2026-01-01T00:00:00Z",
                "sha256": "abc123",
            },
            "graded_at": "2026-01-01T00:00:00Z",
            "created_at": "2025-12-01T00:00:00Z",
        }
    )
    user = FakeUser("u1", "FREK-001", "Ada")
    surface = await compute_ecosystem_builder_surface(user)
    assert surface.stage == "professional"
    assert len(surface.credentials) == 1
    assert surface.credentials[0].certification_code == "FMS01-A01"


@pytest.mark.asyncio
async def test_professional_plus_public_opt_in_reaches_builder_stage(builder_db):
    await builder_db.skills.insert_one(
        {
            "id": "FMS01-A1",
            "metier": "FMS",
            "niveau": "A01",
            "bloc": "B1",
            "label": "Compétence A1",
            "version": "1.0",
            "source": "admin",
        }
    )
    await builder_db.user_skills.insert_one(
        {
            "user_id": "u1",
            "skill_id": "FMS01-A1",
            "state": "acquired",
            "progression_pct": 100,
            "evidence_count": 2,
        }
    )
    user = FakeUser("u1", "FREK-001", "Ada")

    surface_before = await compute_ecosystem_builder_surface(user)
    assert surface_before.stage == "professional"

    await set_profile_visibility("u1", True)
    surface_after = await compute_ecosystem_builder_surface(user)
    assert surface_after.stage == "builder"
    assert surface_after.is_public is True


@pytest.mark.asyncio
async def test_ecosystem_history_filters_to_this_user_and_orders_newest_first(
    builder_db,
):
    await builder_db.event_log.insert_many(
        [
            {
                "event_type": "academy_badge_awarded",
                "payload": {"user_id": "u1", "badge_code": "B10"},
                "published_at": "2026-01-01T00:00:00Z",
            },
            {
                "event_type": "academy_first_value_reached",
                "payload": {"user_id": "u1"},
                "published_at": "2026-01-02T00:00:00Z",
            },
            {
                "event_type": "academy_badge_awarded",
                "payload": {"user_id": "u2", "badge_code": "B10"},  # other user
                "published_at": "2026-01-03T00:00:00Z",
            },
        ]
    )
    user = FakeUser("u1", "FREK-001", "Ada")
    surface = await compute_ecosystem_builder_surface(user)
    assert len(surface.ecosystem_history) == 2
    assert surface.ecosystem_history[0].event_type == "academy_first_value_reached"
    assert surface.ecosystem_history[1].event_type == "academy_badge_awarded"


@pytest.mark.asyncio
async def test_never_fabricates_projects_or_collaborations_fields(builder_db):
    """Scope guard: the response model itself must never grow a
    `projects`/`collaborations`/`network`/`economic_activity` field --
    those are MISSING/REQUIRES_OTHER_CVLN_SYSTEM per the gap matrix, and
    representing them (even as an empty list) would misleadingly imply
    they're built."""
    user = FakeUser("u1", "FREK-001", "Ada")
    surface = await compute_ecosystem_builder_surface(user)
    field_names = set(surface.model_dump().keys())
    for forbidden in ("projects", "collaborations", "network", "economic_activity"):
        assert forbidden not in field_names
