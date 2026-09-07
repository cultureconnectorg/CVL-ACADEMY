"""ACA-0007/ACA-0008 — Physical & Hybrid delivery domain model.

Closes the gap `fms_canonical/delivery_architecture.py` names explicitly:
that module derives a formation's PHYSICAL delivery mode as real but
`status="ELIGIBLE_PENDING_OFFER"` — never `"AVAILABLE"` — "because no
code here, or anywhere in this package, claims a real bookable physical
session exists." This module is that missing piece: real `Location` /
`TrainingSession` / `Enrollment` / `AttendanceRecord` records, so a
PHYSICAL delivery mode can become truthfully `AVAILABLE` once (and only
once) a genuine scheduled, capacity-checked session actually exists.

`DELIVERY != COMMERCIAL_OFFER` still holds: a session here is a real
scheduled event with a real location/time/capacity, never a payment or
commercial offer (`ACA-0025`/`ACA-0026`, still not built, untouched by
this module).

ACA-0008 (Hybrid = E_LEARNING + PHYSICAL composed, no double-counting):
satisfied by construction — this module never reads or writes any
progression/CC-credit/signal field (`db.users`, `progression.py`,
`frek_core.emit_signal`). Attendance here is a fact about a physical
event only; it is deliberately not wired into the e-learning progression
engine this pass, so a learner's e-learning completion and physical
attendance can never double-count each other. Composing the two into one
"hybrid completion" view is a real, separate future decision (left
BLOCKED, not fabricated here).
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import List, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field

from db import db, utc_now_iso


def _uid() -> str:
    return str(uuid.uuid4())


# ---------------- Models ----------------

SessionStatus = Literal["scheduled", "full", "completed", "cancelled"]
EnrollmentStatus = Literal["enrolled", "waitlisted", "cancelled", "attended", "no_show"]

# The same territoire vocabulary onboarding.py already uses — never a new
# geography concept invented for this module.
Territoire = Literal[
    "martinique", "guadeloupe", "guyane", "france", "caraibe", "diaspora", "autre"
]


class Location(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=_uid)
    name: str
    address: str
    city: str
    territoire: Territoire
    capacity: int = Field(gt=0)
    created_at: str = Field(default_factory=utc_now_iso)


class TrainingSession(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=_uid)
    formation_code: str
    location_id: str
    starts_at: str  # ISO 8601, UTC
    ends_at: str
    capacity: int = Field(gt=0)
    enrolled_count: int = 0
    status: SessionStatus = "scheduled"
    trainer_user_id: Optional[str] = None
    created_by: str
    created_at: str = Field(default_factory=utc_now_iso)


class Enrollment(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=_uid)
    session_id: str
    user_id: str
    status: EnrollmentStatus = "enrolled"
    enrolled_at: str = Field(default_factory=utc_now_iso)


class AttendanceRecord(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=_uid)
    session_id: str
    user_id: str
    present: bool
    marked_by: str
    marked_at: str = Field(default_factory=utc_now_iso)


# ---------------- Pure helpers (unit-testable, no db) ----------------


def has_capacity(session: TrainingSession) -> bool:
    return session.enrolled_count < session.capacity


def next_session_status(session: TrainingSession, enrolled_count: int) -> SessionStatus:
    """Pure status transition: `scheduled`<->`full` track real capacity;
    `completed`/`cancelled` are terminal and never overridden by this
    function (a caller sets those explicitly)."""
    if session.status in ("completed", "cancelled"):
        return session.status
    return "full" if enrolled_count >= session.capacity else "scheduled"


def is_session_started(session: TrainingSession, now: Optional[datetime] = None) -> bool:
    now = now or datetime.now(timezone.utc)
    return datetime.fromisoformat(session.starts_at) <= now


# ---------------- DB-touching service functions ----------------


async def create_location(loc: Location) -> Location:
    await db.physical_locations.insert_one(loc.model_dump())
    return loc


async def list_locations() -> List[Location]:
    docs = await db.physical_locations.find({}, {"_id": 0}).to_list(500)
    return [Location(**d) for d in docs]


async def create_session(session: TrainingSession) -> TrainingSession:
    loc = await db.physical_locations.find_one({"id": session.location_id}, {"_id": 0})
    if not loc:
        raise ValueError("Lieu introuvable.")
    await db.physical_sessions.insert_one(session.model_dump())
    return session


async def list_sessions_for_formation(
    formation_code: str, include_past: bool = False
) -> List[TrainingSession]:
    query = {"formation_code": formation_code, "status": {"$in": ["scheduled", "full"]}}
    if not include_past:
        query["starts_at"] = {"$gte": utc_now_iso()}
    docs = (
        await db.physical_sessions.find(query, {"_id": 0}).sort("starts_at", 1).to_list(200)
    )
    return [TrainingSession(**d) for d in docs]


async def has_bookable_session(formation_code: str) -> bool:
    """The real, single source of truth `delivery_architecture.py` reads
    to decide whether PHYSICAL is honestly `AVAILABLE` for a formation —
    a real, future, capacity-remaining session, nothing else."""
    doc = await db.physical_sessions.find_one(
        {
            "formation_code": formation_code,
            "status": "scheduled",
            "starts_at": {"$gte": utc_now_iso()},
        },
        {"_id": 0, "id": 1},
    )
    return doc is not None


async def get_session(session_id: str) -> Optional[TrainingSession]:
    doc = await db.physical_sessions.find_one({"id": session_id}, {"_id": 0})
    return TrainingSession(**doc) if doc else None


async def enroll(session_id: str, user_id: str) -> Enrollment:
    session = await get_session(session_id)
    if not session:
        raise ValueError("Session introuvable.")
    if session.status == "cancelled":
        raise ValueError("Cette session est annulée.")
    existing = await db.physical_enrollments.find_one(
        {"session_id": session_id, "user_id": user_id, "status": {"$ne": "cancelled"}},
        {"_id": 0},
    )
    if existing:
        raise ValueError("Déjà inscrit à cette session.")
    status: EnrollmentStatus = "enrolled" if has_capacity(session) else "waitlisted"
    enr = Enrollment(session_id=session_id, user_id=user_id, status=status)
    await db.physical_enrollments.insert_one(enr.model_dump())
    if status == "enrolled":
        new_count = session.enrolled_count + 1
        await db.physical_sessions.update_one(
            {"id": session_id},
            {
                "$set": {
                    "enrolled_count": new_count,
                    "status": next_session_status(session, new_count),
                }
            },
        )
    return enr


async def cancel_enrollment(session_id: str, user_id: str) -> None:
    enr = await db.physical_enrollments.find_one(
        {"session_id": session_id, "user_id": user_id, "status": {"$in": ["enrolled", "waitlisted"]}},
        {"_id": 0},
    )
    if not enr:
        raise ValueError("Inscription introuvable.")
    was_enrolled = enr["status"] == "enrolled"
    await db.physical_enrollments.update_one(
        {"id": enr["id"]}, {"$set": {"status": "cancelled"}}
    )
    if was_enrolled:
        session = await get_session(session_id)
        if session:
            new_count = max(0, session.enrolled_count - 1)
            await db.physical_sessions.update_one(
                {"id": session_id},
                {
                    "$set": {
                        "enrolled_count": new_count,
                        "status": next_session_status(session, new_count),
                    }
                },
            )
            # A waitlisted enrollment can now be promoted — real capacity
            # freed, first-in-line by enrolled_at, never arbitrary.
            promoted = await db.physical_enrollments.find_one(
                {"session_id": session_id, "status": "waitlisted"},
                {"_id": 0},
                sort=[("enrolled_at", 1)],
            )
            if promoted:
                await db.physical_enrollments.update_one(
                    {"id": promoted["id"]}, {"$set": {"status": "enrolled"}}
                )
                await db.physical_sessions.update_one(
                    {"id": session_id},
                    {
                        "$set": {
                            "enrolled_count": new_count + 1,
                            "status": next_session_status(session, new_count + 1),
                        }
                    },
                )


async def my_enrollments(user_id: str) -> List[Enrollment]:
    docs = await db.physical_enrollments.find(
        {"user_id": user_id, "status": {"$ne": "cancelled"}}, {"_id": 0}
    ).to_list(200)
    return [Enrollment(**d) for d in docs]


async def mark_attendance(session_id: str, user_id: str, present: bool, marked_by: str) -> AttendanceRecord:
    enr = await db.physical_enrollments.find_one(
        {"session_id": session_id, "user_id": user_id, "status": {"$in": ["enrolled", "attended", "no_show"]}},
        {"_id": 0},
    )
    if not enr:
        raise ValueError("Cet utilisateur n'est pas inscrit à cette session.")
    rec = AttendanceRecord(session_id=session_id, user_id=user_id, present=present, marked_by=marked_by)
    await db.physical_attendance.insert_one(rec.model_dump())
    await db.physical_enrollments.update_one(
        {"id": enr["id"]}, {"$set": {"status": "attended" if present else "no_show"}}
    )
    return rec


async def session_attendance(session_id: str) -> List[AttendanceRecord]:
    docs = await db.physical_attendance.find({"session_id": session_id}, {"_id": 0}).to_list(500)
    return [AttendanceRecord(**d) for d in docs]
