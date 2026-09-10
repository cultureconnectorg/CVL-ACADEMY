"""P0 Assurance API: legal, privacy, security and risk registries/gates."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from auth import get_current_user, require_role
from models import User
from services import assurance_core as core
from services import risk_ops

router = APIRouter(prefix="/assurance", tags=["assurance"])
Admin = Depends(require_role("admin", "super_admin", "founder"))
Founder = Depends(require_role("founder"))


class LegalDocumentCreate(BaseModel):
    title: str = Field(min_length=3, max_length=240)
    document_type: str = Field(min_length=2, max_length=80)
    case_id: Optional[str] = None
    jurisdiction: Optional[str] = Field(default=None, max_length=120)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class StateChange(BaseModel):
    state: str


class ClauseCreate(BaseModel):
    code: str = Field(min_length=2, max_length=80)
    title: str = Field(min_length=2, max_length=240)
    text_hash: str = Field(min_length=64, max_length=128)
    version: int = Field(ge=1)
    tags: List[str] = Field(default_factory=list)


class DataClassCreate(BaseModel):
    code: str
    name: str
    sensitivity: str
    retention_days: Optional[int] = Field(default=None, ge=0)
    legal_basis_required: bool = True


class ProcessingActivityCreate(BaseModel):
    name: str
    purpose: str
    data_classes: List[str] = Field(min_length=1)
    legal_basis: str
    processors: List[str] = Field(default_factory=list)
    regions: List[str] = Field(default_factory=list)


class ConsentCreate(BaseModel):
    purpose: str
    policy_version: str
    granted: bool
    evidence: Dict[str, Any] = Field(default_factory=dict)


class DsarCreate(BaseModel):
    request_type: str


class PrivacyIncidentCreate(BaseModel):
    title: str
    severity: str
    data_classes: List[str]
    description: str


class PrivacyIncidentCascade(BaseModel):
    impact: int = Field(ge=1, le=5)
    probability: int = Field(ge=1, le=5)
    owner: Optional[str] = None
    mitigation: Optional[str] = None
    deadline: Optional[str] = None
    jurisdiction: Optional[str] = Field(default=None, max_length=120)
    evidence_refs: List[str] = Field(default_factory=list)


class SecurityAssetCreate(BaseModel):
    name: str
    asset_type: str
    owner: str
    exposure: str
    criticality: str


class SecurityFindingCreate(BaseModel):
    title: str
    severity: str
    asset_id: Optional[str] = None
    evidence_refs: List[str] = Field(default_factory=list)
    remediation: str


class RiskAcceptanceCreate(BaseModel):
    rationale: str = Field(min_length=3)
    expires_at: str


class RiskCreate(BaseModel):
    title: str
    domain: str
    impact: int = Field(ge=1, le=5)
    probability: int = Field(ge=1, le=5)
    control_effectiveness: int = Field(default=0, ge=0, le=5)
    owner: Optional[str] = None
    mitigation: Optional[str] = None
    deadline: Optional[str] = None
    evidence_refs: List[str] = Field(default_factory=list)


class TreatmentCreate(BaseModel):
    treatment: str


class IncidentCascadeCreate(BaseModel):
    incident_type: str = Field(min_length=2, max_length=80)
    incident_id: str = Field(min_length=1, max_length=240)
    title: str = Field(min_length=3, max_length=240)
    domain: str = Field(min_length=2, max_length=120)
    impact: int = Field(ge=1, le=5)
    probability: int = Field(ge=1, le=5)
    owner: Optional[str] = None
    mitigation: Optional[str] = None
    deadline: Optional[str] = None
    evidence_refs: List[str] = Field(default_factory=list)


class InsuranceReviewTriggerCreate(BaseModel):
    reason: str = Field(min_length=3, max_length=2000)
    coverage_types: List[str] = Field(min_length=1)
    broker_or_provider: Optional[str] = Field(default=None, max_length=240)


class InsuranceReviewRecord(BaseModel):
    coverage_confirmed: bool
    evidence_refs: List[str] = Field(default_factory=list)
    notes: Optional[str] = Field(default=None, max_length=4000)


def _translate(exc: Exception):
    if isinstance(exc, LookupError):
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.post("/legal/documents")
async def create_legal_document(payload: LegalDocumentCreate, current: User = Admin):
    return await core.create_legal_document(actor_id=current.id, **payload.model_dump())


@router.patch("/legal/documents/{document_id}/state")
async def transition_legal_document(document_id: str, payload: StateChange, current: User = Admin):
    try:
        return await core.transition_legal_document(actor_id=current.id, document_id=document_id, state=payload.state)
    except (LookupError, ValueError) as exc:
        _translate(exc)


@router.post("/legal/clauses")
async def create_clause(payload: ClauseCreate, current: User = Admin):
    return await core.register_clause(actor_id=current.id, **payload.model_dump())


@router.post("/legal/documents/{document_id}/clauses/{clause_id}")
async def link_clause(document_id: str, clause_id: str, current: User = Admin):
    try:
        return await core.link_clause_usage(actor_id=current.id, document_id=document_id, clause_id=clause_id)
    except LookupError as exc:
        _translate(exc)


@router.get("/legal/clauses/{clause_id}/impact")
async def get_clause_impact(clause_id: str, current: User = Admin):
    return await core.clause_impact(clause_id)


@router.post("/privacy/data-classes")
async def create_data_class(payload: DataClassCreate, current: User = Admin):
    return await core.register_data_class(actor_id=current.id, **payload.model_dump())


@router.post("/privacy/processing-activities")
async def create_processing_activity(payload: ProcessingActivityCreate, current: User = Admin):
    return await core.register_processing_activity(actor_id=current.id, **payload.model_dump())


@router.post("/privacy/consents/me")
async def record_my_consent(payload: ConsentCreate, current: User = Depends(get_current_user)):
    return await core.record_consent(actor_id=current.id, user_id=current.id, **payload.model_dump())


@router.get("/privacy/consents/me")
async def get_my_consents(current: User = Depends(get_current_user)):
    return await core.current_consents(current.id)


@router.post("/privacy/dsar/me")
async def create_my_dsar(payload: DsarCreate, current: User = Depends(get_current_user)):
    return await core.create_dsar(actor_id=current.id, user_id=current.id, request_type=payload.request_type)


@router.post("/privacy/incidents")
async def create_privacy_incident(payload: PrivacyIncidentCreate, current: User = Admin):
    return await core.create_privacy_incident(actor_id=current.id, **payload.model_dump())


@router.post("/privacy/incidents/{incident_id}/cascade")
async def cascade_privacy_incident(
    incident_id: str, payload: PrivacyIncidentCascade, current: User = Admin
):
    try:
        return await risk_ops.cascade_privacy_incident(
            actor_id=current.id, incident_id=incident_id, **payload.model_dump()
        )
    except (LookupError, ValueError) as exc:
        _translate(exc)


@router.post("/security/assets")
async def create_security_asset(payload: SecurityAssetCreate, current: User = Admin):
    return await core.create_security_asset(actor_id=current.id, **payload.model_dump())


@router.post("/security/findings")
async def create_security_finding(payload: SecurityFindingCreate, current: User = Admin):
    try:
        return await core.create_security_finding(actor_id=current.id, **payload.model_dump())
    except ValueError as exc:
        _translate(exc)


@router.post("/security/findings/{finding_id}/accept-risk")
async def accept_security_risk(finding_id: str, payload: RiskAcceptanceCreate, current: User = Founder):
    try:
        return await core.accept_security_risk(actor_id=current.id, finding_id=finding_id, **payload.model_dump())
    except LookupError as exc:
        _translate(exc)


@router.get("/security/release-gate")
async def security_release_gate(current: User = Admin):
    return await core.release_security_gate()


@router.post("/risks")
async def create_risk(payload: RiskCreate, current: User = Admin):
    try:
        return await core.create_risk(actor_id=current.id, **payload.model_dump())
    except ValueError as exc:
        _translate(exc)


@router.post("/risks/{risk_id}/treatment")
async def set_risk_treatment(risk_id: str, payload: TreatmentCreate, current: User = Admin):
    try:
        return await core.set_risk_treatment(actor_id=current.id, risk_id=risk_id, treatment=payload.treatment)
    except (LookupError, ValueError) as exc:
        _translate(exc)


@router.get("/risks/critical-gate")
async def critical_risk_gate(current: User = Admin):
    return await core.critical_risk_gate()


@router.post("/risks/cascade-incident")
async def cascade_incident(payload: IncidentCascadeCreate, current: User = Admin):
    try:
        return await risk_ops.cascade_incident_to_risk(actor_id=current.id, **payload.model_dump())
    except (LookupError, ValueError) as exc:
        _translate(exc)


@router.post("/risks/{risk_id}/insurance-review")
async def create_insurance_review(
    risk_id: str, payload: InsuranceReviewTriggerCreate, current: User = Admin
):
    try:
        return await risk_ops.create_insurance_review_trigger(
            actor_id=current.id, risk_id=risk_id, **payload.model_dump()
        )
    except (LookupError, ValueError) as exc:
        _translate(exc)


@router.post("/risks/{risk_id}/insurance-review/auto")
async def auto_insurance_review(risk_id: str, current: User = Admin):
    try:
        result = await risk_ops.auto_insurance_review_for_critical_risk(
            actor_id=current.id, risk_id=risk_id
        )
        return {"triggered": result is not None, "review": result}
    except LookupError as exc:
        _translate(exc)


@router.patch("/insurance-reviews/{trigger_id}")
async def record_insurance_review(
    trigger_id: str, payload: InsuranceReviewRecord, current: User = Admin
):
    try:
        return await risk_ops.record_insurance_review(
            actor_id=current.id, trigger_id=trigger_id, **payload.model_dump()
        )
    except (LookupError, ValueError) as exc:
        _translate(exc)
