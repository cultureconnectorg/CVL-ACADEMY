"""ECON-02 (Audit Chirurgical 2026-09-07) — quiz reward duplication.

Real, exploitable gap this suite closes and proves closed: every
passing quiz submission recomputed `new_cc = current.cc_credits +
cc_earned` from a request-scoped snapshot and re-credited it, with no
check that the quiz had already been passed before — a repeated pass
(the same correct answers submitted again) re-credited CC every time.

A genuine pedagogical re-attempt stays allowed and tracked (attempts,
latest score) — only the economic credit is now capped to the first
pass, matching the module's own doctrine ("une nouvelle tentative
pédagogique peut être autorisée... mais jamais un nouveau crédit
économique pour le même événement acquis").

DB-backed pieces run against `mongomock_motor.AsyncMongoMockClient` —
same convention as every other suite in this repo.
"""

from __future__ import annotations

import pytest
from mongomock_motor import AsyncMongoMockClient

import api.quizzes as quizzes_module
import badges_engine as badges_module
import services.frek_core as frek_core_module
from api.quizzes import submit_module_quiz
from models import QuizSubmission, User
from quiz import build_quiz

MODULE = {
    "code": "FMS-01-M01",
    "name": "Poser son univers artistique",
    "duration_h": 4,
    "stade": "graine",
    "deliverable": "Fiche univers artistique v1",
    "hook": "Un artiste martiniquais sans positionnement clair",
    "frek_signal": "FREK-WORK archive_livrable",
}


def _correct_answers():
    quiz = build_quiz(MODULE)
    return {
        str(q["n"]): next(c["id"] for c in q["choices"] if c["correct"]) for q in quiz
    }


@pytest.fixture
async def quiz_db(monkeypatch):
    client = AsyncMongoMockClient()
    mock_db = client["cvln_quiz_econ02_test"]
    for module in (quizzes_module, frek_core_module, badges_module):
        monkeypatch.setattr(module, "db", mock_db)
    return mock_db


def _user() -> User:
    return User(
        frek_id="FREK-STUDENT",
        email="student@example.com",
        display_name="Student",
        password_hash="x",
        role="student",
        cc_credits=0,
    )


async def _seed_formation_ready_for_quiz(db, user_id):
    await db.formations.insert_one(
        {
            "code": "FMS-01",
            "name": "Test Formation",
            "pole": "FMS",
            "pole_name": "Formation & Savoirs",
            "pole_color": "#000",
            "duration_h": 4,
            "stades": ["graine"],
            "cc": 4,
            "badge_name": "Badge",
            "prerequisites": "",
            "debouches": "",
            "description": "",
            "objective_strategic": "",
            "modules": [MODULE],
        }
    )
    await db.progress.insert_one(
        {
            "user_id": user_id,
            "module_code": "FMS-01-M01",
            "hook_viewed_at": "2026-09-07T00:00:00Z",
            "objectives_viewed_at": "2026-09-07T00:00:00Z",
            "course_progress_pct": 100,
            "workshop_viewed_at": "2026-09-07T00:00:00Z",
            "deliverable_submitted_at": "2026-09-07T00:00:00Z",
        }
    )


@pytest.mark.asyncio
async def test_first_pass_credits_cc(quiz_db):
    user = _user()
    await quiz_db.users.insert_one(user.model_dump())
    await _seed_formation_ready_for_quiz(quiz_db, user.id)

    result = await submit_module_quiz(
        "FMS-01",
        "FMS-01-M01",
        QuizSubmission(module_code="FMS-01-M01", answers=_correct_answers()),
        current=user,
    )
    assert result.passed is True
    assert result.cc_earned == 4
    assert result.signal_emitted != ""

    stored = await quiz_db.users.find_one({"id": user.id}, {"_id": 0})
    assert stored["cc_credits"] == 4


@pytest.mark.asyncio
async def test_pass_x100_credits_cc_exactly_once(quiz_db):
    """The audit's own required proof: pass x100 -> reward attribué
    exactement 1 fois."""
    user = _user()
    await quiz_db.users.insert_one(user.model_dump())
    await _seed_formation_ready_for_quiz(quiz_db, user.id)

    results = []
    for _ in range(100):
        fresh = User(**(await quiz_db.users.find_one({"id": user.id}, {"_id": 0})))
        results.append(
            await submit_module_quiz(
                "FMS-01",
                "FMS-01-M01",
                QuizSubmission(module_code="FMS-01-M01", answers=_correct_answers()),
                current=fresh,
            )
        )

    assert results[0].cc_earned == 4
    assert all(r.cc_earned == 0 for r in results[1:])
    # A genuine re-attempt is still scored and passes every time — only
    # the economic credit is capped.
    assert all(r.passed for r in results)
    assert all(r.signal_emitted == "" for r in results[1:])

    stored = await quiz_db.users.find_one({"id": user.id}, {"_id": 0})
    assert stored["cc_credits"] == 4  # not 4*100

    progress = await quiz_db.progress.find_one(
        {"user_id": user.id, "module_code": "FMS-01-M01"}, {"_id": 0}
    )
    assert progress["quiz_attempts"] == 100  # every real attempt still tracked


@pytest.mark.asyncio
async def test_stale_snapshot_cannot_replay_a_credit(quiz_db):
    """Reproduces the exact original bug shape: a caller holding a
    `current` User snapshot from *before* the first pass submits again
    with that same stale object."""
    user = _user()
    await quiz_db.users.insert_one(user.model_dump())
    await _seed_formation_ready_for_quiz(quiz_db, user.id)

    stale_snapshot = User(**(await quiz_db.users.find_one({"id": user.id}, {"_id": 0})))
    first = await submit_module_quiz(
        "FMS-01",
        "FMS-01-M01",
        QuizSubmission(module_code="FMS-01-M01", answers=_correct_answers()),
        current=stale_snapshot,
    )
    assert first.cc_earned == 4

    second = await submit_module_quiz(
        "FMS-01",
        "FMS-01-M01",
        QuizSubmission(module_code="FMS-01-M01", answers=_correct_answers()),
        current=stale_snapshot,  # still reports cc_credits=0
    )
    assert second.cc_earned == 0

    stored = await quiz_db.users.find_one({"id": user.id}, {"_id": 0})
    assert stored["cc_credits"] == 4  # not 8


@pytest.mark.asyncio
async def test_failed_attempt_never_credits(quiz_db):
    user = _user()
    await quiz_db.users.insert_one(user.model_dump())
    await _seed_formation_ready_for_quiz(quiz_db, user.id)

    wrong_answers = {str(q["n"]): "ZZZ" for q in build_quiz(MODULE)}
    result = await submit_module_quiz(
        "FMS-01",
        "FMS-01-M01",
        QuizSubmission(module_code="FMS-01-M01", answers=wrong_answers),
        current=user,
    )
    assert result.passed is False
    assert result.cc_earned == 0

    stored = await quiz_db.users.find_one({"id": user.id}, {"_id": 0})
    assert stored["cc_credits"] == 0
