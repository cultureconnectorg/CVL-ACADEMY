"""ACA-0007/ACA-0008 — Physical & Hybrid delivery domain model, proof.

Drives `physical_delivery.py`'s real service functions against a real
formation document (with `EXTERNAL` context) and proves the one link
`fms_canonical/delivery_architecture.py` names as the ACA-0007 blocker:
`get_delivery_architecture()` returns `PHYSICAL` `status="AVAILABLE"`
once (and only once) a real, future, capacity-remaining
`TrainingSession` exists — `"ELIGIBLE_PENDING_OFFER"` otherwise, exactly
as before this module existed.

DB-backed pieces run against `mongomock_motor.AsyncMongoMockClient` — no
live MongoDB in this sandbox, same convention as
`test_rail2_kor01_e2e.py`.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pytest
from mongomock_motor import AsyncMongoMockClient

import fms_canonical.delivery_architecture as delivery_architecture_module
import physical_delivery as physical_delivery_module
from fms_canonical.delivery_architecture import get_delivery_architecture
from physical_delivery import (
    Location,
    TrainingSession,
    cancel_enrollment,
    create_location,
    create_session,
    enroll,
    has_bookable_session,
    mark_attendance,
    my_enrollments,
    session_attendance,
)


@pytest.fixture
async def phys_db(monkeypatch):
    client = AsyncMongoMockClient()
    mock_db = client["cvln_physical_sessions_test"]
    for module in (physical_delivery_module, delivery_architecture_module):
        monkeypatch.setattr(module, "db", mock_db)
    return mock_db


def _future_iso(hours: int = 48) -> str:
    return (datetime.now(timezone.utc) + timedelta(hours=hours)).isoformat()


async def _seed_formation(mock_db, code: str = "KOR-01") -> None:
    await mock_db.formations.insert_one(
        {"code": code, "contexts": ["INTERNAL", "EXTERNAL"]}
    )


async def _seed_location(mock_db, capacity: int = 2) -> Location:
    loc = Location(
        name="Antenne Lanbi",
        address="1 rue des Antennes",
        city="Fort-de-France",
        territoire="martinique",
        capacity=capacity,
    )
    return await create_location(loc)


@pytest.mark.asyncio
async def test_enroll_fills_capacity_then_waitlists(phys_db):
    loc = await _seed_location(phys_db, capacity=1)
    session = TrainingSession(
        formation_code="KOR-01",
        location_id=loc.id,
        starts_at=_future_iso(),
        ends_at=_future_iso(hours=52),
        capacity=1,
        created_by="staff-1",
    )
    session = await create_session(session)

    first = await enroll(session.id, "user-1")
    assert first.status == "enrolled"

    second = await enroll(session.id, "user-2")
    assert second.status == "waitlisted"

    stored = await phys_db.physical_sessions.find_one({"id": session.id}, {"_id": 0})
    assert stored["enrolled_count"] == 1
    assert stored["status"] == "full"


@pytest.mark.asyncio
async def test_enroll_twice_rejected(phys_db):
    loc = await _seed_location(phys_db, capacity=5)
    session = await create_session(
        TrainingSession(
            formation_code="KOR-01",
            location_id=loc.id,
            starts_at=_future_iso(),
            ends_at=_future_iso(hours=52),
            capacity=5,
            created_by="staff-1",
        )
    )
    await enroll(session.id, "user-1")
    with pytest.raises(ValueError):
        await enroll(session.id, "user-1")


@pytest.mark.asyncio
async def test_cancel_promotes_oldest_waitlisted(phys_db):
    loc = await _seed_location(phys_db, capacity=1)
    session = await create_session(
        TrainingSession(
            formation_code="KOR-01",
            location_id=loc.id,
            starts_at=_future_iso(),
            ends_at=_future_iso(hours=52),
            capacity=1,
            created_by="staff-1",
        )
    )
    await enroll(session.id, "user-1")
    await enroll(session.id, "user-2")  # waitlisted

    await cancel_enrollment(session.id, "user-1")

    remaining = await my_enrollments("user-2")
    assert len(remaining) == 1
    assert remaining[0].status == "enrolled"

    stored = await phys_db.physical_sessions.find_one({"id": session.id}, {"_id": 0})
    assert stored["enrolled_count"] == 1
    assert stored["status"] == "full"


@pytest.mark.asyncio
async def test_mark_attendance_updates_enrollment(phys_db):
    loc = await _seed_location(phys_db, capacity=5)
    session = await create_session(
        TrainingSession(
            formation_code="KOR-01",
            location_id=loc.id,
            starts_at=_future_iso(),
            ends_at=_future_iso(hours=52),
            capacity=5,
            created_by="staff-1",
        )
    )
    await enroll(session.id, "user-1")
    record = await mark_attendance(session.id, "user-1", True, marked_by="staff-1")
    assert record.present is True

    attendance = await session_attendance(session.id)
    assert len(attendance) == 1
    assert attendance[0].user_id == "user-1"


@pytest.mark.asyncio
async def test_delivery_architecture_flips_to_available_with_real_session(phys_db):
    await _seed_formation(phys_db, "KOR-01")

    before = await get_delivery_architecture("KOR-01")
    physical_before = next(m for m in before.delivery_modes if m.mode == "PHYSICAL")
    assert physical_before.status == "ELIGIBLE_PENDING_OFFER"

    loc = await _seed_location(phys_db, capacity=3)
    await create_session(
        TrainingSession(
            formation_code="KOR-01",
            location_id=loc.id,
            starts_at=_future_iso(),
            ends_at=_future_iso(hours=52),
            capacity=3,
            created_by="staff-1",
        )
    )

    assert await has_bookable_session("KOR-01") is True

    after = await get_delivery_architecture("KOR-01")
    physical_after = next(m for m in after.delivery_modes if m.mode == "PHYSICAL")
    assert physical_after.status == "AVAILABLE"

    e_learning = next(m for m in after.delivery_modes if m.mode == "E_LEARNING")
    assert e_learning.status == "AVAILABLE"


@pytest.mark.asyncio
async def test_delivery_architecture_ignores_past_session(phys_db):
    await _seed_formation(phys_db, "KOR-01")
    loc = await _seed_location(phys_db, capacity=3)
    await create_session(
        TrainingSession(
            formation_code="KOR-01",
            location_id=loc.id,
            starts_at=_future_iso(hours=-48),
            ends_at=_future_iso(hours=-44),
            capacity=3,
            created_by="staff-1",
        )
    )

    arch = await get_delivery_architecture("KOR-01")
    physical = next(m for m in arch.delivery_modes if m.mode == "PHYSICAL")
    assert physical.status == "ELIGIBLE_PENDING_OFFER"
