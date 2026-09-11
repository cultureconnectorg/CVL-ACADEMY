"""Governance escalation protocol API (GOV-13)."""

from __future__ import annotations

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from auth import require_role
from models import User
from services import governance_protocols

router = APIRouter(prefix="/governance-protocols", tags=["governance"])
Admin = Depends(require_role("admin", "super_admin", "founder"))


class EscalationCreate(BaseModel):
    source_type: str
    source_id: str
    domain: str
    severity: str
    target_authority_level: str
    reason: str = Field(min_length=3, max_length=4000)
    evidence_refs: List[str] = Field(min_length=1)
    case_id: Optional[str] = None


class EscalationAcknowledge(BaseModel):
    authority_decision_id: str
    evidence_refs: List[str] = Field(min_length=1)


class EscalationClose(BaseModel):
    status: str
    resolution: str = Field(min_length=3, max_length=4000)
    evidence_refs: List[str] = Field(min_length=1)


def _raise(exc: Exception):
    if isinstance(exc, LookupError):
        status = 404
    elif isinstance(exc, PermissionError):
        status = 403
    else:
        status = 422
    raise HTTPException(status_code=status, detail=str(exc)) from exc


@router.post("/escalations")
async def create_escalation(payload: EscalationCreate, current: User = Admin):
    try:
        return await governance_protocols.create_escalation(
            actor_id=current.id, **payload.model_dump()
        )
    except (LookupError, ValueError, PermissionError) as exc:
        _raise(exc)


@router.post("/escalations/{escalation_id}/acknowledge")
async def acknowledge_escalation(
    escalation_id: str,
    payload: EscalationAcknowledge,
    current: User = Admin,
):
    try:
        return await governance_protocols.acknowledge_escalation(
            actor_id=current.id,
            escalation_id=escalation_id,
            **payload.model_dump(),
        )
    except (LookupError, ValueError, PermissionError) as exc:
        _raise(exc)


@router.post("/escalations/{escalation_id}/close")
async def close_escalation(
    escalation_id: str, payload: EscalationClose, current: User = Admin
):
    try:
        return await governance_protocols.close_escalation(
            actor_id=current.id,
            escalation_id=escalation_id,
            **payload.model_dump(),
        )
    except (LookupError, ValueError, PermissionError) as exc:
        _raise(exc)


@router.get("/escalations/gate")
async def escalation_gate(domain: Optional[str] = None, current: User = Admin):
    return await governance_protocols.escalation_gate(domain=domain)
