"""ACA-0028 — Professional FREK profile as identity surface tests.

`compute_professional_profile` composes three already-real, separately
tested sources (`skills.progression.get_user_progress`,
`certification.service.list_user_attempts`,
`certification.attestation.attestation_export_metadata`) — this suite
proves the composition itself (which skills/certs surface, in what
shape) plus the new visibility contract (`set_profile_visibility`,
`get_public_professional_profile`'s non-distinguishing 404 behavior).
"""

from __future__ import annotations

import pytest
from mongomock_motor import AsyncMongoMockClient

import certification.service as certification_service_module
import services.professional_profile as profile_module
import skills.progression as skills_progression_module
from services.professional_profile import (
    compute_professional_profile,
    get_public_professional_profile,
    set_profile_visibility,
)


class FakeUser:
    def __init__(self, id, frek_id, display_name, stade="graine"):
        self.id = id
        self.frek_id = frek_id
        self.display_name = display_name
        self.stade = stade


@pytest.fixture
async def profile_db(monkeypatch):
    client = AsyncMongoMockClient()
    mock_db = client["cvln_aca0028_profile_test"]
    monkeypatch.setattr(profile_module, "db", mock_db)
    monkeypatch.setattr(skills_progression_module, "db", mock_db)
    monkeypatch.setattr(certification_service_module, "db", mock_db)
    return mock_db


@pytest.mark.asyncio
async def test_empty_profile_has_no_skills_or_certs(profile_db):
    user = FakeUser("u1", "FREK-001", "Ada")
    profile = await compute_professional_profile(user)
    assert profile.frek_id == "FREK-001"
    assert profile.acquired_skills == []
    assert profile.certifications == []
    assert profile.badges_count == 0
    assert profile.is_public is False


@pytest.mark.asyncio
async def test_only_acquired_skills_surface(profile_db):
    await profile_db.skills.insert_many(
        [
            {
                "id": "FMS01-A1",
                "metier": "FMS",
                "niveau": "A01",
                "bloc": "B1",
                "label": "Compétence A1",
                "version": "1.0",
                "source": "admin",
            },
            {
                "id": "FMS01-A2",
                "metier": "FMS",
                "niveau": "A01",
                "bloc": "B1",
                "label": "Compétence A2",
                "version": "1.0",
                "source": "admin",
            },
        ]
    )
    await profile_db.user_skills.insert_many(
        [
            {
                "user_id": "u1",
                "skill_id": "FMS01-A1",
                "state": "acquired",
                "progression_pct": 100,
                "evidence_count": 3,
            },
            {
                "user_id": "u1",
                "skill_id": "FMS01-A2",
                "state": "in_progress",
                "progression_pct": 40,
                "evidence_count": 1,
            },
        ]
    )
    user = FakeUser("u1", "FREK-001", "Ada")
    profile = await compute_professional_profile(user)
    assert len(profile.acquired_skills) == 1
    assert profile.acquired_skills[0].skill_id == "FMS01-A1"
    assert profile.acquired_skills[0].evidence_count == 3
    assert profile.total_evidence_count == 4  # 3 + 1, all evidence counted


@pytest.mark.asyncio
async def test_only_passed_certifications_surface(profile_db):
    await profile_db.certification_attempts.insert_many(
        [
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
            },
            {
                "id": "a2",
                "user_id": "u1",
                "certification_code": "FMS02-A01",
                "formation_code": "FMS-02",
                "level": "A01",
                "rubric_version": "1.0",
                "status": "failed",
                "score_global": 40.0,
                "created_at": "2025-12-02T00:00:00Z",
            },
        ]
    )
    user = FakeUser("u1", "FREK-001", "Ada")
    profile = await compute_professional_profile(user)
    assert len(profile.certifications) == 1
    cert = profile.certifications[0]
    assert cert.certification_code == "FMS01-A01"
    assert cert.score_global == 87.5
    assert cert.mention == "Bien"
    assert cert.jury_signature_sha256 == "abc123"
    assert cert.graded_at == "2026-01-01T00:00:00Z"


@pytest.mark.asyncio
async def test_badges_count_reflects_real_count(profile_db):
    await profile_db.user_badges.insert_many(
        [
            {"user_id": "u1", "badge_code": "b1"},
            {"user_id": "u1", "badge_code": "b2"},
            {"user_id": "u2", "badge_code": "b3"},  # different user, not counted
        ]
    )
    user = FakeUser("u1", "FREK-001", "Ada")
    profile = await compute_professional_profile(user)
    assert profile.badges_count == 2


# ---------------- visibility ----------------


@pytest.mark.asyncio
async def test_default_visibility_is_private(profile_db):
    user = FakeUser("u1", "FREK-001", "Ada")
    profile = await compute_professional_profile(user)
    assert profile.is_public is False


@pytest.mark.asyncio
async def test_set_visibility_public_then_private(profile_db):
    user = FakeUser("u1", "FREK-001", "Ada")
    await set_profile_visibility("u1", True)
    profile = await compute_professional_profile(user)
    assert profile.is_public is True

    await set_profile_visibility("u1", False)
    profile = await compute_professional_profile(user)
    assert profile.is_public is False


@pytest.mark.asyncio
async def test_public_lookup_returns_none_for_unknown_frek_id(profile_db):
    assert await get_public_professional_profile("FREK-999") is None


@pytest.mark.asyncio
async def test_public_lookup_returns_none_when_private(profile_db):
    await profile_db.users.insert_one(
        {"id": "u1", "frek_id": "FREK-001", "display_name": "Ada", "stade": "pousse"}
    )
    # is_public never set -> defaults private
    assert await get_public_professional_profile("FREK-001") is None


@pytest.mark.asyncio
async def test_public_lookup_returns_profile_when_public(profile_db):
    await profile_db.users.insert_one(
        {"id": "u1", "frek_id": "FREK-001", "display_name": "Ada", "stade": "pousse"}
    )
    await set_profile_visibility("u1", True)
    profile = await get_public_professional_profile("FREK-001")
    assert profile is not None
    assert profile.frek_id == "FREK-001"
    assert profile.display_name == "Ada"
    assert profile.is_public is True
