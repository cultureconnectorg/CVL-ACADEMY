"""ACA-0024 (Founder decision, W-FUNNEL-2 "Regular Use", 2026-09-07) —
CONTINUATION_ENGINE: `GET /user/learning-path`'s `next_action` must
resume a returning learner's real, most-recently-touched in-progress
module first, instead of only ever surfacing the earliest untouched
module in curriculum order.

Real gap this closes: a learner who genuinely started work in a later
formation (their `last_activity_at` timestamp proves it — see the
progress writes in api/learning.py and api/quizzes.py) previously saw
`next_action` point at an earlier, still-untouched module simply
because it came first in formation/module order — a "next step" card
that ignored what the learner was actually doing.
"""

from __future__ import annotations

import pytest
from mongomock_motor import AsyncMongoMockClient

import api.learning as learning_module
from models import User


def _user() -> User:
    # No onboarding pole set -> is_formation_unlocked short-circuits to
    # (True, "") for every formation, keeping this test about the
    # resume/continuation logic itself, not formation-lock rules
    # (already covered elsewhere).
    return User(
        frek_id="FREK-1",
        email="learner@example.com",
        display_name="Learner",
        password_hash="x",
        role="student",
        metier_vise=None,
    )


def _formation(code, pole, module_code):
    return {
        "code": code,
        "name": f"Formation {code}",
        "pole": pole,
        "pole_name": pole,
        "pole_color": "#000000",
        "duration_h": 10,
        "cc": 5,
        "modules": [{"code": module_code, "name": f"Module {module_code}"}],
    }


@pytest.fixture
async def legacy_db(monkeypatch):
    client = AsyncMongoMockClient()
    mock_db = client["cvln_continuation_engine_test"]
    monkeypatch.setattr(learning_module, "db", mock_db)
    return mock_db


@pytest.fixture
def no_canonical(monkeypatch):
    """Canonical convergence stays out of this test — every domain
    reports empty, so `next_action` is decided entirely by the legacy
    resume/sequential logic under test."""
    import fms_canonical
    import klt_canonical
    import kor_canonical
    import frk_canonical

    async def empty_list(*_a, **_kw):
        return []

    async def empty_progress(*_a, **_kw):
        return []

    for module, fn_names in (
        (fms_canonical, ("list_canonical_formations", "get_user_canonical_progress")),
        (klt_canonical, ("list_canonical_klt_formations", "get_user_klt_progress")),
        (kor_canonical, ("list_canonical_kor_formations", "get_user_kor_progress")),
        (frk_canonical, ("list_canonical_frk_formations", "get_user_frk_progress")),
    ):
        monkeypatch.setattr(module, fn_names[0], empty_list)
        monkeypatch.setattr(module, fn_names[1], empty_progress)


@pytest.mark.asyncio
async def test_fresh_learner_falls_back_to_sequential_order(legacy_db, no_canonical):
    """No `last_activity_at` anywhere (brand-new learner) -> resume
    loop finds nothing -> byte-identical pre-ACA-0024 behavior: the
    first unlocked, untouched module in (own_pole + other_poles)
    order."""
    await legacy_db.formations.insert_one(_formation("AAA-01", "AAA", "AAA01-M01"))
    await legacy_db.formations.insert_one(_formation("BBB-01", "BBB", "BBB01-M01"))

    result = await learning_module.user_learning_path(current=_user())
    na = result["next_action"]
    assert na is not None
    assert na["formation_code"] == "AAA-01"
    assert na["status"] == "available"
    assert na.get("resume") is not True


@pytest.mark.asyncio
async def test_resumes_touched_module_over_earlier_untouched_one(legacy_db, no_canonical):
    """Formation AAA-01 (sorts first) has never been touched. Formation
    BBB-01's module is genuinely in progress with a real
    `last_activity_at` stamp. The learner must be sent back to BBB-01,
    not to the untouched AAA-01 module curriculum order would otherwise
    pick."""
    await legacy_db.formations.insert_one(_formation("AAA-01", "AAA", "AAA01-M01"))
    await legacy_db.formations.insert_one(_formation("BBB-01", "BBB", "BBB01-M01"))
    user = _user()
    await legacy_db.progress.insert_one(
        {
            "user_id": user.id,
            "formation_code": "BBB-01",
            "module_code": "BBB01-M01",
            "hook_viewed_at": "2026-09-05T00:00:00+00:00",
            "last_activity_at": "2026-09-05T00:00:00+00:00",
        }
    )

    result = await learning_module.user_learning_path(current=user)
    na = result["next_action"]
    assert na is not None
    assert na["formation_code"] == "BBB-01"
    assert na["status"] == "in_progress"
    assert na["resume"] is True


@pytest.mark.asyncio
async def test_most_recently_touched_module_wins_among_several(legacy_db, no_canonical):
    """Two formations both genuinely in progress -> the one with the
    LATER `last_activity_at` is the resume target, not merely "some"
    in-progress module."""
    await legacy_db.formations.insert_one(_formation("AAA-01", "AAA", "AAA01-M01"))
    await legacy_db.formations.insert_one(_formation("BBB-01", "BBB", "BBB01-M01"))
    user = _user()
    await legacy_db.progress.insert_one(
        {
            "user_id": user.id,
            "formation_code": "AAA-01",
            "module_code": "AAA01-M01",
            "hook_viewed_at": "2026-09-01T00:00:00+00:00",
            "last_activity_at": "2026-09-01T00:00:00+00:00",  # older
        }
    )
    await legacy_db.progress.insert_one(
        {
            "user_id": user.id,
            "formation_code": "BBB-01",
            "module_code": "BBB01-M01",
            "hook_viewed_at": "2026-09-06T00:00:00+00:00",
            "last_activity_at": "2026-09-06T00:00:00+00:00",  # newer
        }
    )

    result = await learning_module.user_learning_path(current=user)
    na = result["next_action"]
    assert na is not None
    assert na["formation_code"] == "BBB-01"
    assert na["resume"] is True


@pytest.mark.asyncio
async def test_validated_module_with_timestamp_never_offered_as_resume(legacy_db, no_canonical):
    """A module the learner already fully validated must never come
    back as a "resume" target just because it carries a
    `last_activity_at` stamp from when it was in progress — the
    sequential fallback must find the OTHER, genuinely-untouched
    module instead."""
    await legacy_db.formations.insert_one(_formation("AAA-01", "AAA", "AAA01-M01"))
    await legacy_db.formations.insert_one(_formation("BBB-01", "BBB", "BBB01-M01"))
    user = _user()
    await legacy_db.progress.insert_one(
        {
            "user_id": user.id,
            "formation_code": "AAA-01",
            "module_code": "AAA01-M01",
            "hook_viewed_at": "2026-09-01T00:00:00+00:00",
            "objectives_viewed_at": "2026-09-01T00:00:00+00:00",
            "course_progress_pct": 100,
            "workshop_viewed_at": "2026-09-01T00:00:00+00:00",
            "deliverable_submitted_at": "2026-09-01T00:00:00+00:00",
            "quiz_passed": True,
            "mini_mission_committed_at": "2026-09-01T00:00:00+00:00",
            "last_activity_at": "2026-09-01T00:00:00+00:00",
        }
    )

    result = await learning_module.user_learning_path(current=user)
    na = result["next_action"]
    assert na is not None
    assert na["formation_code"] == "BBB-01"
    assert na["status"] == "available"
    assert na.get("resume") is not True
