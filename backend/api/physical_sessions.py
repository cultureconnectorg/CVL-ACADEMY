"""ACA-0007/ACA-0008 — Physical training sessions API.

Trainer/admin schedule real sessions against a real formation + location;
students enroll/cancel with real capacity/waitlist accounting; trainers
mark real attendance. Never touches progression/CC-credit/signal state
(see physical_delivery.py's own module docstring — ACA-0008's
no-double-counting guarantee).
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from auth import get_current_user, require_role
from certification.service import get_user_display_info
from models import ADMIN_ROLES, User
from physical_delivery import (
    AttendanceRecord,
    Enrollment,
    Location,
    Territoire,
    TrainingSession,
    cancel_enrollment,
    create_location,
    create_session,
    enroll,
    get_session,
    list_all_sessions,
    list_locations,
    list_sessions_for_formation,
    list_sessions_for_trainer,
    mark_attendance,
    my_enrollments,
    session_attendance,
)
from db import db

router = APIRouter(tags=["physical-sessions"])

# RBAC must be explicit (Founder decision, PHYSICAL/HYBRID assessment
# architecture, 2026-09-07) — "A jury/corrector/admin/trainer must not
# all automatically receive identical permissions." Every operational
# physical-delivery action below is scoped to admin-tier staff plus, for
# roster/attendance operations only, the ONE trainer a session was
# actually assigned to — never the old blanket STAFF_ROLES (which
# silently also admitted jury and corrector into scheduling and roster
# access they have no real reason to hold: their authority is grading,
# already governed separately by JURY_ROLES in api/certification.py).
SESSION_OPS_ROLES = (*ADMIN_ROLES, "trainer")


async def _assert_session_staff(session: TrainingSession, current: User) -> None:
    """Admin-tier always passes; a "trainer" passes ONLY for the exact
    session they were assigned to (`TrainingSession.trainer_user_id`) —
    never any trainer for any session."""
    if current.role in ADMIN_ROLES:
        return
    if current.role == "trainer" and session.trainer_user_id == current.id:
        return
    raise HTTPException(
        status_code=403,
        detail="Accès réservé au formateur assigné à cette session ou à un administrateur.",
    )


class LocationInput(BaseModel):
    name: str
    address: str
    city: str
    territoire: Territoire
    capacity: int


class SessionInput(BaseModel):
    formation_code: str
    location_id: str
    starts_at: str
    ends_at: str
    capacity: int
    trainer_user_id: Optional[str] = None


@router.post("/admin/physical-locations", response_model=Location)
async def admin_create_location(
    payload: LocationInput, current: User = Depends(require_role(*ADMIN_ROLES))
):
    """Shared infrastructure — admin-tier only. A trainer runs sessions
    at a location, but does not create the location itself (real-world
    parallel to how `physical-sessions` distinguishes "schedule my own
    class" from "stand up a new venue")."""
    loc = Location(
        name=payload.name,
        address=payload.address,
        city=payload.city,
        territoire=payload.territoire,
        capacity=payload.capacity,
    )
    return await create_location(loc)


@router.get("/physical-locations", response_model=List[Location])
async def get_locations(current: User = Depends(get_current_user)):
    return await list_locations()


@router.post("/admin/physical-sessions", response_model=TrainingSession)
async def admin_create_session(
    payload: SessionInput, current: User = Depends(require_role(*SESSION_OPS_ROLES))
):
    # A trainer can only ever schedule themselves — never assign, and
    # never impersonate, a colleague; only admin-tier can set an
    # arbitrary (or no) trainer_user_id.
    trainer_user_id = payload.trainer_user_id
    if current.role == "trainer":
        trainer_user_id = current.id
    try:
        session = TrainingSession(
            formation_code=payload.formation_code,
            location_id=payload.location_id,
            starts_at=payload.starts_at,
            ends_at=payload.ends_at,
            capacity=payload.capacity,
            trainer_user_id=trainer_user_id,
            created_by=current.id,
        )
        return await create_session(session)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/formations/{formation_code}/physical-sessions", response_model=List[TrainingSession])
async def formation_sessions(formation_code: str, current: User = Depends(get_current_user)):
    return await list_sessions_for_formation(formation_code)


@router.get("/physical-sessions/assigned", response_model=List[TrainingSession])
async def assigned_sessions(current: User = Depends(require_role(*SESSION_OPS_ROLES))):
    """Trainer UX — every real session this trainer was assigned to
    (past or future, so a roster stays reachable after the fact).
    Admin-tier sees every session, for oversight."""
    if current.role in ADMIN_ROLES:
        return await list_all_sessions()
    return await list_sessions_for_trainer(current.id)


@router.post("/physical-sessions/{session_id}/enroll", response_model=Enrollment)
async def session_enroll(session_id: str, current: User = Depends(get_current_user)):
    try:
        return await enroll(session_id, current.id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/physical-sessions/{session_id}/cancel-enrollment")
async def session_cancel_enrollment(session_id: str, current: User = Depends(get_current_user)):
    try:
        await cancel_enrollment(session_id, current.id)
        return {"ok": True}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/physical-sessions/mine", response_model=List[Enrollment])
async def my_physical_enrollments(current: User = Depends(get_current_user)):
    return await my_enrollments(current.id)


@router.post("/physical-sessions/{session_id}/attendance/{user_id}", response_model=AttendanceRecord)
async def session_mark_attendance(
    session_id: str, user_id: str, present: bool,
    current: User = Depends(get_current_user),
):
    session = await get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session introuvable.")
    await _assert_session_staff(session, current)
    try:
        return await mark_attendance(session_id, user_id, present, current.id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/physical-sessions/{session_id}/attendance", response_model=List[AttendanceRecord])
async def get_session_attendance(
    session_id: str, current: User = Depends(get_current_user)
):
    session = await get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session introuvable.")
    await _assert_session_staff(session, current)
    return await session_attendance(session_id)


@router.get("/physical-sessions/{session_id}/roster")
async def get_session_roster(
    session_id: str, current: User = Depends(get_current_user)
) -> List[Dict[str, Any]]:
    """Trainer/staff roster view: every real enrollment for this
    session, joined with the real attendance record (if any) and a
    display-safe user identity — the one place a trainer sees who to
    mark present/absent and, once graded, whose practical assessment
    is theirs to record. Never fabricates a row: only real
    `Enrollment` documents appear, in `enrolled_at` order."""
    session = await get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session introuvable.")
    await _assert_session_staff(session, current)

    enrollments = (
        await db.physical_enrollments.find(
            {"session_id": session_id, "status": {"$ne": "cancelled"}}, {"_id": 0}
        )
        .sort("enrolled_at", 1)
        .to_list(1000)
    )
    attendance_docs = await db.physical_attendance.find(
        {"session_id": session_id}, {"_id": 0}
    ).to_list(1000)
    attendance_by_user = {a["user_id"]: a for a in attendance_docs}

    roster: List[Dict[str, Any]] = []
    for enr in enrollments:
        user_info = await get_user_display_info(enr["user_id"])
        attendance = attendance_by_user.get(enr["user_id"])
        roster.append(
            {
                "user_id": enr["user_id"],
                "display_name": (user_info or {}).get("display_name", "—"),
                "frek_id": (user_info or {}).get("frek_id", "—"),
                "enrollment_status": enr["status"],
                "enrolled_at": enr["enrolled_at"],
                "present": attendance["present"] if attendance else None,
                "marked_at": attendance["marked_at"] if attendance else None,
            }
        )
    return roster
