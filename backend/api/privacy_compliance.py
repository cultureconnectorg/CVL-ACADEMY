"""Policy-driven Privacy Core API (PRI-002/003/004/005/007/013)."""

from __future__ import annotations

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from auth import get_current_user, require_role
from models import User
from services import privacy_compliance

router = APIRouter(prefix="/privacy", tags=["privacy-compliance"])
Admin = Depends(require_role("admin", "super_admin", "founder"))


class ProcessingActivityCreate(BaseModel):
    name: str = Field(min_length=3, max_length=240)
    purpose: str = Field(min_length=3, max_length=2000)
    data_classes: List[str] = Field(min_length=1)
    legal_basis: str = Field(min_length=2, max_length=240)
    processors: List[str] = Field(default_factory=list)
    regions: List[str] = Field(default_factory=list)
    controller: str = Field(min_length=2, max_length=240)
    recipients: List[str] = Field(default_factory=list)
    systems: List[str] = Field(default_factory=list)
    retention_refs: List[str] = Field(default_factory=list)
    transfer_mechanism: Optional[str] = Field(default=None, max_length=500)
    evidence_refs: List[str] = Field(min_length=1)


class ConsentPurposeCreate(BaseModel):
    purpose: str = Field(min_length=2, max_length=240)
    required: bool = False
    policy_version_id: str = Field(min_length=1, max_length=240)
    evidence_refs: List[str] = Field(min_length=1)


class ConsentDecision(BaseModel):
    purpose: str = Field(min_length=2, max_length=240)
    granted: bool
    policy_version_id: str = Field(min_length=1, max_length=240)
    evidence_refs: List[str] = Field(min_length=1)
    frek_evidence_ref: Optional[str] = Field(default=None, max_length=500)


class DsarCreate(BaseModel):
    request_type: str = Field(min_length=3, max_length=40)


class DsarIdentityEvidence(BaseModel):
    evidence_refs: List[str] = Field(min_length=1)


class DeletionApproval(BaseModel):
    actor_role: str = Field(min_length=2, max_length=80)
    authority_level: str = Field(min_length=2, max_length=80)
    policy_version_id: str = Field(min_length=1, max_length=240)
    evidence_refs: List[str] = Field(min_length=1)
    exception_refs: List[str] = Field(default_factory=list)


class DeletionSchedule(BaseModel):
    resource_record_ids: List[str] = Field(min_length=1)
    trigger_at: str = Field(min_length=10, max_length=64)
    retention_policy_version_id: str = Field(min_length=1, max_length=240)


class DeletionCompletion(BaseModel):
    evidence_refs: List[str] = Field(min_length=1)


class PrivacyIncidentCreate(BaseModel):
    title: str = Field(min_length=3, max_length=240)
    description: str = Field(min_length=3, max_length=8000)
    severity: str = Field(min_length=3, max_length=20)
    data_classes: List[str] = Field(default_factory=list)
    evidence_refs: List[str] = Field(min_length=1)
    asset_id: Optional[str] = Field(default=None, max_length=240)


class PrivacyIncidentProjection(BaseModel):
    risk_impact: int = Field(ge=1, le=5)
    risk_probability: int = Field(ge=1, le=5)
    risk_owner: Optional[str] = Field(default=None, max_length=240)
    risk_mitigation: Optional[str] = Field(default=None, max_length=4000)
    risk_deadline: Optional[str] = Field(default=None, max_length=64)
    jurisdiction: Optional[str] = Field(default=None, max_length=120)


def _translate(exc: Exception):
    if isinstance(exc, LookupError):
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    if isinstance(exc, PermissionError):
        raise HTTPException(status_code=403, detail=str(exc)) from exc
    raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.post("/processing-activities")
async def create_processing_activity(
    payload: ProcessingActivityCreate, current: User = Admin
):
    try:
        return await privacy_compliance.register_processing_activity(
            actor_id=current.id, **payload.model_dump()
        )
    except (LookupError, ValueError) as exc:
        _translate(exc)


@router.post("/consent-purposes")
async def create_consent_purpose(payload: ConsentPurposeCreate, current: User = Admin):
    try:
        return await privacy_compliance.register_consent_purpose(
            actor_id=current.id, **payload.model_dump()
        )
    except (LookupError, ValueError) as exc:
        _translate(exc)


@router.post("/consents/me")
async def record_my_consent(
    payload: ConsentDecision, current: User = Depends(get_current_user)
):
    try:
        return await privacy_compliance.record_consent(
            actor_id=current.id,
            user_id=current.id,
            source="SELF_SERVICE",
            **payload.model_dump(),
        )
    except (LookupError, ValueError, PermissionError) as exc:
        _translate(exc)


@router.get("/consents/me")
async def my_consent_preferences(current: User = Depends(get_current_user)):
    return await privacy_compliance.consent_preferences(current.id)


@router.post("/dsar/me")
async def create_my_dsar(payload: DsarCreate, current: User = Depends(get_current_user)):
    return await privacy_compliance.create_dsar(
        actor_id=current.id,
        user_id=current.id,
        request_type=payload.request_type,
    )


@router.post("/dsar/{dsar_id}/identity")
async def verify_dsar_identity(
    dsar_id: str, payload: DsarIdentityEvidence, current: User = Admin
):
    try:
        return await privacy_compliance.verify_dsar_identity(
            actor_id=current.id,
            dsar_id=dsar_id,
            evidence_refs=payload.evidence_refs,
        )
    except (LookupError, ValueError) as exc:
        _translate(exc)


@router.post("/dsar/{dsar_id}/export")
async def build_dsar_export(dsar_id: str, current: User = Admin):
    try:
        return await privacy_compliance.build_dsar_export(
            actor_id=current.id, dsar_id=dsar_id
        )
    except (LookupError, ValueError, PermissionError) as exc:
        _translate(exc)


@router.post("/deletion/{request_id}/approve")
async def approve_deletion(
    request_id: str, payload: DeletionApproval, current: User = Admin
):
    try:
        return await privacy_compliance.approve_deletion_request(
            actor_id=current.id,
            request_id=request_id,
            **payload.model_dump(),
        )
    except (LookupError, ValueError, PermissionError) as exc:
        _translate(exc)


@router.post("/deletion/{request_id}/schedule")
async def schedule_deletion(
    request_id: str, payload: DeletionSchedule, current: User = Admin
):
    try:
        return await privacy_compliance.schedule_deletion_retention_jobs(
            actor_id=current.id,
            request_id=request_id,
            **payload.model_dump(),
        )
    except (LookupError, ValueError) as exc:
        _translate(exc)


@router.post("/deletion/{request_id}/complete")
async def complete_deletion(
    request_id: str, payload: DeletionCompletion, current: User = Admin
):
    try:
        return await privacy_compliance.complete_deletion_from_retention(
            actor_id=current.id,
            request_id=request_id,
            evidence_refs=payload.evidence_refs,
        )
    except (LookupError, ValueError) as exc:
        _translate(exc)


@router.post("/incidents")
async def create_privacy_incident(payload: PrivacyIncidentCreate, current: User = Admin):
    try:
        return await privacy_compliance.open_privacy_incident(
            actor_id=current.id, **payload.model_dump()
        )
    except (LookupError, ValueError) as exc:
        _translate(exc)


@router.post("/incidents/{incident_id}/project")
async def project_privacy_incident(
    incident_id: str, payload: PrivacyIncidentProjection, current: User = Admin
):
    try:
        return await privacy_compliance.project_privacy_incident(
            actor_id=current.id,
            incident_id=incident_id,
            **payload.model_dump(),
        )
    except (LookupError, ValueError) as exc:
        _translate(exc)
