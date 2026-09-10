"""R5 systemic escalation API (RSK-03/RSK-20)."""

from __future__ import annotations

from typing import List
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from auth import require_role
from models import User
from services import risk_escalation

router = APIRouter(prefix="/risk-escalation", tags=["risk"])
Admin = Depends(require_role("admin", "super_admin", "founder"))

class EscalationCreate(BaseModel):
    rationale: str = Field(min_length=3, max_length=4000)
    evidence_refs: List[str] = Field(min_length=1)


def _raise(exc: Exception):
    status = 404 if isinstance(exc, LookupError) else 422
    raise HTTPException(status_code=status, detail=str(exc)) from exc

@router.post("/risks/{risk_id}")
async def require_escalation(risk_id: str, payload: EscalationCreate, current: User = Admin):
    try:
        return await risk_escalation.require_systemic_escalation(
            actor_id=current.id, risk_id=risk_id, **payload.model_dump()
        )
    except (LookupError, ValueError) as exc:
        _raise(exc)

@router.post("/{escalation_id}/dispatch")
async def dispatch(escalation_id: str, current: User = Admin):
    try:
        return await risk_escalation.dispatch_to_cvlnios(
            actor_id=current.id, escalation_id=escalation_id
        )
    except (LookupError, ValueError) as exc:
        _raise(exc)

@router.get("/gate")
async def gate(current: User = Admin):
    return await risk_escalation.systemic_escalation_gate()
