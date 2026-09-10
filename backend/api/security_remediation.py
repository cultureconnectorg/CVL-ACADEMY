"""Security remediation API for SEC-011 / SEC-012 control-plane workflows."""

from __future__ import annotations

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from auth import require_role
from models import User
from services import security_remediation

router = APIRouter(prefix="/security/remediations", tags=["security"])
Admin = Depends(require_role("admin", "super_admin", "founder"))


class RemediationCreate(BaseModel):
    finding_id: Optional[str] = None
    threat_id: Optional[str] = None
    title: str = Field(min_length=3, max_length=240)
    proposed_change: str = Field(min_length=3, max_length=8000)
    target_system: str = Field(min_length=2, max_length=120)
    rollback_plan: str = Field(min_length=3, max_length=8000)
    test_plan: List[str] = Field(min_length=1)
    evidence_refs: List[str] = Field(min_length=1)


class RemediationAuthorize(BaseModel):
    authority_decision_ref: str = Field(min_length=1, max_length=240)


class RemediationTransition(BaseModel):
    status: str
    evidence_refs: List[str] = Field(default_factory=list)


class DispatchConfirmed(BaseModel):
    target: str
    remote_task_id: str = Field(min_length=1, max_length=240)
    evidence_refs: List[str] = Field(min_length=1)


def _translate(exc: Exception):
    status = 404 if isinstance(exc, LookupError) else 422
    raise HTTPException(status_code=status, detail=str(exc)) from exc


@router.post("")
async def create_remediation(payload: RemediationCreate, current: User = Admin):
    try:
        return await security_remediation.create_remediation(
            actor_id=current.id, **payload.model_dump()
        )
    except (LookupError, ValueError) as exc:
        _translate(exc)


@router.post("/{remediation_id}/authorize")
async def authorize_remediation(
    remediation_id: str, payload: RemediationAuthorize, current: User = Admin
):
    try:
        return await security_remediation.authorize_remediation(
            actor_id=current.id,
            remediation_id=remediation_id,
            authority_decision_ref=payload.authority_decision_ref,
        )
    except (LookupError, ValueError) as exc:
        _translate(exc)


@router.post("/{remediation_id}/dispatch-confirmed")
async def dispatch_confirmed(
    remediation_id: str, payload: DispatchConfirmed, current: User = Admin
):
    try:
        return await security_remediation.record_external_dispatch(
            actor_id=current.id,
            remediation_id=remediation_id,
            **payload.model_dump(),
        )
    except (LookupError, ValueError) as exc:
        _translate(exc)


@router.patch("/{remediation_id}")
async def transition(
    remediation_id: str, payload: RemediationTransition, current: User = Admin
):
    try:
        return await security_remediation.transition_remediation(
            actor_id=current.id,
            remediation_id=remediation_id,
            status=payload.status,
            evidence_refs=payload.evidence_refs,
        )
    except (LookupError, ValueError) as exc:
        _translate(exc)


@router.get("/release-gate")
async def release_gate(current: User = Admin):
    return await security_remediation.remediation_gate()
