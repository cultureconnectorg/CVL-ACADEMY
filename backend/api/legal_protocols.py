"""Legal protocol APIs (LEG-11/12/19/20/23/24)."""

from __future__ import annotations

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from auth import require_role
from models import User
from services import legal_protocols

router = APIRouter(prefix="/legal/protocols", tags=["legal-protocols"])
Admin = Depends(require_role("admin", "super_admin", "founder"))


class RiskClassificationCreate(BaseModel):
    category: str
    rationale: str = Field(min_length=3, max_length=4000)
    authority_ref: str
    policy_version_id: str
    evidence_refs: List[str] = Field(min_length=1)


class LegalEscalationCreate(BaseModel):
    severity: str
    target_authority_level: str
    reason: str = Field(min_length=3, max_length=4000)
    evidence_refs: List[str] = Field(min_length=1)


class ConfidentialityCreate(BaseModel):
    resource_type: str
    resource_id: str
    classification: str
    rationale: str = Field(min_length=3, max_length=4000)
    authority_ref: str
    policy_version_id: str
    evidence_refs: List[str] = Field(min_length=1)


class RetentionRuleCreate(BaseModel):
    record_type: str
    jurisdiction: str
    retention_days: int = Field(ge=0)
    trigger: str
    action: str
    policy_version_id: str
    authority_decision_id: str
    evidence_refs: List[str] = Field(min_length=1)


class JurisdictionMapCreate(BaseModel):
    jurisdiction: str
    regulatory_scope_ids: List[str] = Field(min_length=1)
    rationale: str = Field(min_length=3, max_length=4000)
    evidence_refs: List[str] = Field(min_length=1)


class RegulatoryRequirementCreate(BaseModel):
    requirement_key: str
    scope_id: str
    title: str
    requirement: str = Field(min_length=3, max_length=12000)
    authority_ref: str
    source_refs: List[str] = Field(min_length=1)
    effective_at: str
    review_due_at: Optional[str] = None


def _raise(exc: Exception):
    if isinstance(exc, LookupError):
        status = 404
    elif isinstance(exc, PermissionError):
        status = 403
    else:
        status = 422
    raise HTTPException(status_code=status, detail=str(exc)) from exc


@router.post("/risks/{risk_id}/classification")
async def classify_risk(
    risk_id: str, payload: RiskClassificationCreate, current: User = Admin
):
    try:
        return await legal_protocols.classify_legal_risk(
            actor_id=current.id,
            risk_id=risk_id,
            **payload.model_dump(),
        )
    except (LookupError, ValueError, PermissionError) as exc:
        _raise(exc)


@router.post("/matters/{matter_id}/escalations")
async def escalate_matter(
    matter_id: str, payload: LegalEscalationCreate, current: User = Admin
):
    try:
        return await legal_protocols.escalate_legal_matter(
            actor_id=current.id,
            matter_id=matter_id,
            **payload.model_dump(),
        )
    except (LookupError, ValueError, PermissionError) as exc:
        _raise(exc)


@router.post("/confidentiality-classifications")
async def classify_confidentiality(
    payload: ConfidentialityCreate, current: User = Admin
):
    try:
        return await legal_protocols.classify_privilege_confidentiality(
            actor_id=current.id, **payload.model_dump()
        )
    except (LookupError, ValueError, PermissionError) as exc:
        _raise(exc)


@router.post("/retention-rules")
async def register_retention(payload: RetentionRuleCreate, current: User = Admin):
    try:
        return await legal_protocols.register_legal_retention_rule(
            actor_id=current.id, **payload.model_dump()
        )
    except (LookupError, ValueError, PermissionError) as exc:
        _raise(exc)


@router.post("/matters/{matter_id}/jurisdictions")
async def map_jurisdiction(
    matter_id: str, payload: JurisdictionMapCreate, current: User = Admin
):
    try:
        return await legal_protocols.map_jurisdiction(
            actor_id=current.id,
            matter_id=matter_id,
            **payload.model_dump(),
        )
    except (LookupError, ValueError, PermissionError) as exc:
        _raise(exc)


@router.post("/regulatory-requirements")
async def regulatory_requirement(
    payload: RegulatoryRequirementCreate, current: User = Admin
):
    try:
        return await legal_protocols.register_regulatory_requirement(
            actor_id=current.id, **payload.model_dump()
        )
    except (LookupError, ValueError, PermissionError) as exc:
        _raise(exc)
