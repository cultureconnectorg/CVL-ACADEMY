"""ACA-0007/ACA-0008 — Physical training sessions API.

Trainer/admin schedule real sessions against a real formation + location;
students enroll/cancel with real capacity/waitlist accounting; trainers
mark real attendance. Never touches progression/CC-credit/signal state
(see physical_delivery.py's own module docstring — ACA-0008's
no-double-counting guarantee).
"""

from __future__ import annotations

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from auth import get_current_user, require_role
from models import STAFF_ROLES, User
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
    list_locations,
    list_sessions_for_formation,
    mark_attendance,
    my_enrollments,
    session_attendance,
)

router = APIRouter(tags=["physical-sessions"])


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
    payload: LocationInput, current: User = Depends(require_role(*STAFF_ROLES))
):
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
    payload: SessionInput, current: User = Depends(require_role(*STAFF_ROLES))
):
    try:
        session = TrainingSession(
            formation_code=payload.formation_code,
            location_id=payload.location_id,
            starts_at=payload.starts_at,
            ends_at=payload.ends_at,
            capacity=payload.capacity,
            trainer_user_id=payload.trainer_user_id,
            created_by=current.id,
        )
        return await create_session(session)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/formations/{formation_code}/physical-sessions", response_model=List[TrainingSession])
async def formation_sessions(formation_code: str, current: User = Depends(get_current_user)):
    return await list_sessions_for_formation(formation_code)


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
    current: User = Depends(require_role(*STAFF_ROLES)),
):
    session = await get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session introuvable.")
    try:
        return await mark_attendance(session_id, user_id, present, current.id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/physical-sessions/{session_id}/attendance", response_model=List[AttendanceRecord])
async def get_session_attendance(session_id: str, current: User = Depends(require_role(*STAFF_ROLES))):
    return await session_attendance(session_id)
