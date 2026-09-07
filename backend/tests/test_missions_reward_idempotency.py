"""ECON-01 (Audit Chirurgical 2026-09-07) — mission reward farming.

Real, exploitable gap this suite closes and proves closed:
`POST /missions/{code}/submit` used to validate and credit a mission
with no check that it had ever been accepted, no re-verified
eligibility, and no protection against a second submit paying out a
second time — `new_cc = current.cc_credits + reward` from a snapshot
`current`, re-computed identically on every repeated call.

DB-backed pieces run against `mongomock_motor.AsyncMongoMockClient` —
same convention as every other suite in this repo.
"""

from __future__ import annotations

import pytest
from fastapi import HTTPException
from mongomock_motor import AsyncMongoMockClient

import api.missions as missions_module
import badges_engine as badges_module
import qualification.service as qualification_service_module
import services.frek_core as frek_core_module
from api.missions import accept_mission, submit_mission
from models import User


@pytest.fixture
async def mis_db(monkeypatch):
    client = AsyncMongoMockClient()
    mock_db = client["cvln_missions_econ01_test"]
    for module in (
        missions_module,
        frek_core_module,
        badges_module,
        qualification_service_module,
    ):
        monkeypatch.setattr(module, "db", mock_db)
    return mock_db


def _user(cc_credits=0) -> User:
    return User(
        frek_id="FREK-STUDENT",
        email="student@example.com",
        display_name="Student",
        password_hash="x",
        role="student",
        cc_credits=cc_credits,
    )


async def _seed_mission(db, code="MIS-1", reward=20, required=None):
    await db.missions.insert_one(
        {
            "id": "m1",
            "code": code,
            "title": "Test Mission",
            "description": "desc",
            "pole": "FMS",
            "cc_reward": reward,
            "stade_required": "graine",
            "entity": "CVLN",
            "status_type": "open",
            "required_qualification_codes": required or [],
        }
    )


@pytest.mark.asyncio
async def test_submit_without_accept_is_rejected(mis_db):
    await _seed_mission(mis_db)
    user = _user()
    await mis_db.users.insert_one(user.model_dump())

    with pytest.raises(HTTPException) as exc:
        await submit_mission("MIS-1", current=user)
    assert exc.value.status_code == 400

    stored = await mis_db.users.find_one({"id": user.id}, {"_id": 0})
    assert stored["cc_credits"] == 0  # never credited


@pytest.mark.asyncio
async def test_accept_then_submit_credits_reward_exactly_once(mis_db):
    await _seed_mission(mis_db, reward=20)
    user = _user()
    await mis_db.users.insert_one(user.model_dump())

    await accept_mission("MIS-1", current=user)
    result = await submit_mission("MIS-1", current=user)
    assert result["cc_earned"] == 20

    stored = await mis_db.users.find_one({"id": user.id}, {"_id": 0})
    assert stored["cc_credits"] == 20


@pytest.mark.asyncio
async def test_submit_x100_credits_reward_exactly_once(mis_db):
    """The audit's own required proof: submit x100 -> reward attribué
    exactement 1 fois."""
    await _seed_mission(mis_db, reward=15)
    user = _user()
    await mis_db.users.insert_one(user.model_dump())
    await accept_mission("MIS-1", current=user)

    results = []
    for _ in range(100):
        # Each call re-reads `current` fresh the way FastAPI's
        # `Depends(get_current_user)` would on a real repeated HTTP
        # request — never the same stale in-memory object across
        # calls, so this genuinely exercises the server-side guard,
        # not just Python-level idempotency of a single object.
        fresh = User(**(await mis_db.users.find_one({"id": user.id}, {"_id": 0})))
        results.append(await submit_mission("MIS-1", current=fresh))

    assert results[0]["cc_earned"] == 15
    assert all(r["cc_earned"] == 0 for r in results[1:])
    assert all(r.get("already_validated") for r in results[1:])

    stored = await mis_db.users.find_one({"id": user.id}, {"_id": 0})
    assert stored["cc_credits"] == 15  # not 15*100


@pytest.mark.asyncio
async def test_stale_snapshot_cannot_replay_a_credit(mis_db):
    """Reproduces the exact original bug shape: a caller holding a
    `current` User snapshot from *before* the first submit tries to
    submit again with that same stale object — must still credit
    nothing on the second call."""
    await _seed_mission(mis_db, reward=25)
    user = _user()
    await mis_db.users.insert_one(user.model_dump())
    await accept_mission("MIS-1", current=user)

    stale_snapshot = User(**(await mis_db.users.find_one({"id": user.id}, {"_id": 0})))
    first = await submit_mission("MIS-1", current=stale_snapshot)
    assert first["cc_earned"] == 25

    # `stale_snapshot` still reports cc_credits=0 (captured before the
    # first submit) — exactly the kind of object the pre-fix code used
    # to trust for `new_cc = current.cc_credits + reward`.
    second = await submit_mission("MIS-1", current=stale_snapshot)
    assert second["cc_earned"] == 0
    assert second["already_validated"] is True

    stored = await mis_db.users.find_one({"id": user.id}, {"_id": 0})
    assert stored["cc_credits"] == 25  # not 50


@pytest.mark.asyncio
async def test_missing_qualification_blocks_accept(mis_db):
    await _seed_mission(mis_db, reward=10, required=["QUAL-X"])
    user = _user()
    await mis_db.users.insert_one(user.model_dump())
    with pytest.raises(HTTPException) as exc:
        await accept_mission("MIS-1", current=user)
    assert exc.value.status_code == 403


@pytest.mark.asyncio
async def test_qualification_revoked_after_accept_blocks_submit(mis_db):
    """The re-check ECON-01 adds: eligibility held at accept time is
    not assumed to still hold at submit time."""
    await _seed_mission(mis_db, reward=10, required=["QUAL-X"])
    user = _user()
    await mis_db.users.insert_one(user.model_dump())
    await mis_db.qualifications.insert_one(
        {
            "id": "q1",
            "user_id": user.id,
            "qualification_code": "QUAL-X",
            "issued_at": "2026-09-07T00:00:00Z",
        }
    )

    await accept_mission("MIS-1", current=user)  # eligible at accept time

    # Qualification revoked before submit (e.g. certification voided).
    await mis_db.qualifications.delete_many({"user_id": user.id})

    with pytest.raises(HTTPException) as exc:
        await submit_mission("MIS-1", current=user)
    assert exc.value.status_code == 403

    stored = await mis_db.users.find_one({"id": user.id}, {"_id": 0})
    assert stored["cc_credits"] == 0  # never credited


@pytest.mark.asyncio
async def test_submit_unknown_mission_404(mis_db):
    user = _user()
    await mis_db.users.insert_one(user.model_dump())
    with pytest.raises(HTTPException) as exc:
        await submit_mission("NOPE", current=user)
    assert exc.value.status_code == 404
