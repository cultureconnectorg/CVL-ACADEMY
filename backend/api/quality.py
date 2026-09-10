"""Quality evidence API for Academy P0 workflows."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from auth import get_current_user, require_role
from models import User
from services import quality_core as quality

router = APIRouter(prefix="/quality", tags=["quality"])
Staff = Depends(require_role("trainer", "corrector", "jury", "admin", "super_admin", "founder"))
Admin = Depends(require_role("admin", "super_admin", "founder"))


class PartnerCreate(BaseModel):
    name: str = Field(min_length=2, max_length=160)
    organisation: str = Field(min_length=2, max_length=200)
    evidence_refs: List[str] = Field(default_factory=list)
    claimed_certifications: List[str] = Field(default_factory=list)


class ScopeCreate(BaseModel):
    partner_id: str
    formation_code: str
    cohort_id: Optional[str] = None
    evidence_refs: List[str] = Field(min_length=1)


class EvidenceCreate(BaseModel):
    user_id: str
    formation_code: str
    cohort_id: Optional[str] = None
    evidence_type: str
    evidence_ref: str
    metadata: Dict[str, Any] = Field(default_factory=dict)


class AttendanceCreate(BaseModel):
    user_id: str
    formation_code: str
    session_id: str
    mode: str
    attended: bool
    signed_at: Optional[str] = None
    evidence_ref: Optional[str] = None


class SatisfactionCreate(BaseModel):
    formation_code: str
    score: int = Field(ge=1, le=5)
    comment: Optional[str] = Field(default=None, max_length=4000)


class ComplaintCreate(BaseModel):
    formation_code: Optional[str] = None
    category: str
    description: str = Field(min_length=3, max_length=8000)
    severity: str = "MEDIUM"
    quality_level: Optional[str] = None


class ComplaintEscalation(BaseModel):
    quality_level: str
    evidence_refs: List[str] = Field(min_length=1)
    projection_domains: List[str] = Field(default_factory=list)


class ComplaintState(BaseModel):
    state: str
    resolution: Optional[str] = None


class ImprovementCreate(BaseModel):
    title: str
    source_refs: List[str] = Field(min_length=1)
    owner: str
    due_at: Optional[str] = None


class AuditPackCreate(BaseModel):
    partner_id: str
    formation_code: str
    cohort_id: Optional[str] = None
    node_ids: List[str] = Field(min_length=1)
    evidence_refs: List[str] = Field(min_length=1)


def _translate(exc: Exception):
    if isinstance(exc, LookupError):
        status = 404
    elif isinstance(exc, PermissionError):
        status = 403
    else:
        status = 422
    raise HTTPException(status_code=status, detail=str(exc)) from exc


@router.post("/partners")
async def create_partner(payload: PartnerCreate, current: User = Admin):
    return await quality.register_partner(actor_id=current.id, **payload.model_dump())


@router.post("/scopes")
async def create_scope(payload: ScopeCreate, current: User = Admin):
    try:
        return await quality.assign_formation_scope(actor_id=current.id, **payload.model_dump())
    except (LookupError, ValueError) as exc:
        _translate(exc)


@router.post("/evidence")
async def add_evidence(payload: EvidenceCreate, current: User = Staff):
    return await quality.record_learner_quality_evidence(
        actor_id=current.id, **payload.model_dump()
    )


@router.get("/learners/{user_id}/file")
async def get_learner_file(
    user_id: str,
    formation_code: Optional[str] = None,
    current: User = Staff,
):
    return await quality.learner_quality_file(user_id, formation_code)


@router.post("/attendance")
async def add_attendance(payload: AttendanceCreate, current: User = Staff):
    try:
        return await quality.record_attendance(actor_id=current.id, **payload.model_dump())
    except ValueError as exc:
        _translate(exc)


@router.post("/satisfaction/me")
async def add_my_satisfaction(
    payload: SatisfactionCreate,
    current: User = Depends(get_current_user),
):
    return await quality.record_satisfaction(user_id=current.id, **payload.model_dump())


@router.get("/formations/{formation_code}/satisfaction")
async def satisfaction_summary(formation_code: str, current: User = Staff):
    return await quality.satisfaction_summary(formation_code)


@router.get("/formations/{formation_code}/satisfaction-analysis")
async def satisfaction_analysis(formation_code: str, current: User = Staff):
    return await quality.satisfaction_analysis(formation_code)


@router.post("/complaints/me")
async def create_my_complaint(
    payload: ComplaintCreate,
    current: User = Depends(get_current_user),
):
    try:
        return await quality.create_complaint(
            actor_id=current.id,
            user_id=current.id,
            **payload.model_dump(),
        )
    except ValueError as exc:
        _translate(exc)


@router.post("/complaints/{complaint_id}/classify-escalate")
async def classify_escalate_complaint(
    complaint_id: str,
    payload: ComplaintEscalation,
    current: User = Staff,
):
    try:
        return await quality.classify_and_escalate_complaint(
            actor_id=current.id,
            complaint_id=complaint_id,
            **payload.model_dump(),
        )
    except (LookupError, ValueError) as exc:
        _translate(exc)


@router.patch("/complaints/{complaint_id}")
async def update_complaint(
    complaint_id: str,
    payload: ComplaintState,
    current: User = Staff,
):
    try:
        return await quality.transition_complaint(
            actor_id=current.id,
            complaint_id=complaint_id,
            state=payload.state,
            resolution=payload.resolution,
        )
    except (LookupError, ValueError) as exc:
        _translate(exc)


@router.post("/improvement-actions")
async def create_improvement(payload: ImprovementCreate, current: User = Staff):
    try:
        return await quality.create_improvement_action(
            actor_id=current.id, **payload.model_dump()
        )
    except ValueError as exc:
        _translate(exc)


@router.post("/audit-packs")
async def create_audit_pack(payload: AuditPackCreate, current: User = Staff):
    try:
        return await quality.create_quality_audit_pack(
            actor_id=current.id, **payload.model_dump()
        )
    except (LookupError, ValueError, PermissionError) as exc:
        _translate(exc)


@router.get("/partners/{partner_id}/workspace")
async def partner_workspace(partner_id: str, current: User = Staff):
    try:
        return await quality.quality_partner_workspace(partner_id)
    except LookupError as exc:
        _translate(exc)
