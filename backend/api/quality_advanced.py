"""Advanced Quality Evidence API."""

from __future__ import annotations

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from auth import require_role
from models import User
from services import quality_advanced

router = APIRouter(prefix="/quality-advanced", tags=["quality"])
Admin = Depends(require_role("admin", "super_admin", "founder"))


class NeedsAssessment(BaseModel):
    user_id: str = Field(min_length=1, max_length=240)
    formation_code: str = Field(min_length=1, max_length=120)
    needs: List[str] = Field(default_factory=list)
    prerequisites: List[str] = Field(default_factory=list)
    accommodations: List[str] = Field(default_factory=list)
    evidence_refs: List[str] = Field(min_length=1)


class AttendanceProof(BaseModel):
    user_id: str = Field(min_length=1, max_length=240)
    formation_code: str = Field(min_length=1, max_length=120)
    session_id: str = Field(min_length=1, max_length=240)
    mode: str = Field(min_length=2, max_length=40)
    attended: bool
    evidence_ref: str = Field(min_length=1, max_length=500)
    signature_attestation_id: Optional[str] = Field(default=None, max_length=240)
    signature_verification_id: Optional[str] = Field(default=None, max_length=240)


class LearningEvidencePack(BaseModel):
    user_id: str = Field(min_length=1, max_length=240)
    formation_code: str = Field(min_length=1, max_length=120)
    cohort_id: Optional[str] = Field(default=None, max_length=240)
    evidence_node_ids: List[str] = Field(min_length=1)
    evidence_refs: List[str] = Field(min_length=1)


class AccessibilityReview(BaseModel):
    formation_code: str = Field(min_length=1, max_length=120)
    scope: str = Field(min_length=3, max_length=2000)
    findings: List[str] = Field(default_factory=list)
    actions: List[str] = Field(default_factory=list)
    evidence_refs: List[str] = Field(min_length=1)


class TrainerRecord(BaseModel):
    trainer_id: str = Field(min_length=1, max_length=240)
    display_name: str = Field(min_length=2, max_length=240)
    competencies: List[str] = Field(min_length=1)
    assigned_formations: List[str] = Field(default_factory=list)
    evidence_refs: List[str] = Field(min_length=1)


class QualityRetention(BaseModel):
    record_type: str = Field(min_length=2, max_length=120)
    retention_days: int = Field(ge=0)
    policy_version_id: str = Field(min_length=1, max_length=240)
    evidence_refs: List[str] = Field(min_length=1)


def _raise(exc: Exception):
    if isinstance(exc, LookupError):
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    if isinstance(exc, PermissionError):
        raise HTTPException(status_code=403, detail=str(exc)) from exc
    raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.post("/needs")
async def needs(payload: NeedsAssessment, current: User = Admin):
    try:
        return await quality_advanced.record_needs_assessment(
            actor_id=current.id, **payload.model_dump()
        )
    except ValueError as exc:
        _raise(exc)


@router.post("/attendance")
async def attendance(payload: AttendanceProof, current: User = Admin):
    try:
        return await quality_advanced.record_attendance_proof(
            actor_id=current.id, **payload.model_dump()
        )
    except ValueError as exc:
        _raise(exc)


@router.post("/learning-evidence-pack")
async def learning_evidence_pack(
    payload: LearningEvidencePack, current: User = Admin
):
    try:
        return await quality_advanced.compose_learning_evidence(
            actor_id=current.id, **payload.model_dump()
        )
    except (LookupError, ValueError) as exc:
        _raise(exc)


@router.post("/accessibility")
async def accessibility(payload: AccessibilityReview, current: User = Admin):
    try:
        return await quality_advanced.record_accessibility_review(
            actor_id=current.id, **payload.model_dump()
        )
    except ValueError as exc:
        _raise(exc)


@router.post("/trainers")
async def trainer(payload: TrainerRecord, current: User = Admin):
    try:
        return await quality_advanced.register_trainer_record(
            actor_id=current.id, **payload.model_dump()
        )
    except ValueError as exc:
        _raise(exc)


@router.get("/kpis/{formation_code}")
async def kpis(formation_code: str, current: User = Admin):
    return await quality_advanced.quality_kpis(formation_code)


@router.post("/retention")
async def retention(payload: QualityRetention, current: User = Admin):
    try:
        return await quality_advanced.record_quality_retention_policy(
            actor_id=current.id, **payload.model_dump()
        )
    except (LookupError, ValueError) as exc:
        _raise(exc)
