"""Operational privacy controls: retention, deletion, processors and cascades."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from auth import get_current_user, require_role
from models import User
from services import privacy_ops

router = APIRouter(prefix="/privacy-ops", tags=["privacy"])
Admin = Depends(require_role("admin", "super_admin", "founder"))


class RetentionRuleCreate(BaseModel):
    data_class: str
    retention_days: int = Field(ge=0)
    trigger: str
    action: str
    legal_hold_blocks: bool = True
    evidence_refs: List[str] = Field(default_factory=list)


class ProcessorCreate(BaseModel):
    name: str
    service: str
    data_classes: List[str]
    regions: List[str]
    dpa_evidence_ref: Optional[str] = None
    subprocessor_url: Optional[str] = None


class StateChange(BaseModel):
    status: str


class DeletionCreate(BaseModel):
    reason: str = Field(min_length=3, max_length=2000)


class DeletionTransition(BaseModel):
    status: str
    impact: Optional[Dict[str, Any]] = None


class DeletionExecution(BaseModel):
    resource_type: str
    action: str
    evidence_ref: str


class IncidentCascade(BaseModel):
    impact: int = Field(ge=1, le=5)
    probability: int = Field(ge=1, le=5)
    owner: Optional[str] = None
    mitigation: Optional[str] = None
    deadline: Optional[str] = None
    evidence_refs: List[str] = Field(default_factory=list)


def _raise(exc: Exception):
    status = 404 if isinstance(exc, LookupError) else 422
    raise HTTPException(status_code=status, detail=str(exc)) from exc


@router.post("/retention-rules")
async def create_retention_rule(payload: RetentionRuleCreate, current: User = Admin):
    try:
        return await privacy_ops.create_retention_rule(
            actor_id=current.id, **payload.model_dump()
        )
    except ValueError as exc:
        _raise(exc)


@router.post("/processors")
async def create_processor(payload: ProcessorCreate, current: User = Admin):
    return await privacy_ops.register_processor(actor_id=current.id, **payload.model_dump())


@router.patch("/processors/{processor_id}")
async def transition_processor(processor_id: str, payload: StateChange, current: User = Admin):
    try:
        return await privacy_ops.transition_processor(
            actor_id=current.id, processor_id=processor_id, status=payload.status
        )
    except (LookupError, ValueError) as exc:
        _raise(exc)


@router.post("/deletion-requests/me")
async def create_my_deletion_request(
    payload: DeletionCreate, current: User = Depends(get_current_user)
):
    return await privacy_ops.create_deletion_request(
        actor_id=current.id, user_id=current.id, reason=payload.reason
    )


@router.patch("/deletion-requests/{request_id}")
async def transition_deletion_request(
    request_id: str, payload: DeletionTransition, current: User = Admin
):
    try:
        return await privacy_ops.transition_deletion_request(
            actor_id=current.id,
            request_id=request_id,
            status=payload.status,
            impact=payload.impact,
        )
    except (LookupError, ValueError) as exc:
        _raise(exc)


@router.post("/deletion-requests/{request_id}/execution")
async def record_deletion_execution(
    request_id: str, payload: DeletionExecution, current: User = Admin
):
    try:
        return await privacy_ops.record_deletion_execution(
            actor_id=current.id, request_id=request_id, **payload.model_dump()
        )
    except (LookupError, ValueError) as exc:
        _raise(exc)


@router.post("/incidents/{incident_id}/risk")
async def cascade_incident_to_risk(
    incident_id: str, payload: IncidentCascade, current: User = Admin
):
    try:
        return await privacy_ops.cascade_privacy_incident_to_risk(
            actor_id=current.id, incident_id=incident_id, **payload.model_dump()
        )
    except (LookupError, ValueError) as exc:
        _raise(exc)
