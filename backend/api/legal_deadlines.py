from __future__ import annotations

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from auth import require_role
from models import User
from services import legal_deadlines

router = APIRouter(prefix="/legal/deadlines", tags=["legal-deadlines"])
Admin = Depends(require_role("admin", "super_admin", "founder"))


class DeadlineCreate(BaseModel):
    matter_id: str = Field(min_length=1, max_length=240)
    deadline_type: str = Field(min_length=2, max_length=80)
    title: str = Field(min_length=2, max_length=240)
    due_at: str
    owner_email: str = Field(min_length=3, max_length=320)
    reminder_days: List[int] = Field(min_length=1)
    contract_id: Optional[str] = Field(default=None, max_length=240)
    document_id: Optional[str] = Field(default=None, max_length=240)
    evidence_refs: List[str] = Field(min_length=1)


class DeadlineClose(BaseModel):
    status: str
    evidence_refs: List[str] = Field(min_length=1)


def _translate(exc: Exception):
    if isinstance(exc, LookupError):
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.post("")
async def create_deadline(payload: DeadlineCreate, current: User = Admin):
    try:
        return await legal_deadlines.create_deadline(
            actor_id=current.id, **payload.model_dump()
        )
    except (LookupError, ValueError) as exc:
        _translate(exc)


@router.post("/dispatch")
async def dispatch(current: User = Admin):
    return await legal_deadlines.dispatch_due_reminders(actor_id=current.id)


@router.patch("/{deadline_id}/close")
async def close_deadline(
    deadline_id: str,
    payload: DeadlineClose,
    current: User = Admin,
):
    try:
        return await legal_deadlines.close_deadline(
            actor_id=current.id,
            deadline_id=deadline_id,
            **payload.model_dump(),
        )
    except (LookupError, ValueError) as exc:
        _translate(exc)
