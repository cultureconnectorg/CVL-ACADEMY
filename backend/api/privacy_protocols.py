"""Privacy protocol APIs (PRI-04/05/09/10/16/22/29/31/33/34/35)."""

from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from auth import require_role
from models import User
from services import privacy_protocols

router = APIRouter(prefix="/privacy-protocols", tags=["privacy"])
Admin = Depends(require_role("admin", "super_admin", "founder"))


class LegalBasisCreate(BaseModel):
    code: str
    label: str
    jurisdiction: str
    authority_ref: str
    rationale: str = Field(min_length=3)
    evidence_refs: List[str] = Field(min_length=1)


class PurposeAssessment(BaseModel):
    requested_purpose: str
    compatible: bool
    rationale: str = Field(min_length=3)
    evidence_refs: List[str] = Field(min_length=1)


class MinimisationAssessment(BaseModel):
    required_fields: List[str] = Field(min_length=1)
    collected_fields: List[str] = Field(min_length=1)
    rationale: str = Field(min_length=3)
    evidence_refs: List[str] = Field(min_length=1)


class FrekConsentProof(BaseModel):
    frek_proof_ref: str
    proof_status: str
    evidence_refs: List[str] = Field(min_length=1)


class PrivacyRequestCreate(BaseModel):
    user_id: str
    request_type: str
    processing_activity_id: str
    rationale: str = Field(min_length=3)
    evidence_refs: List[str] = Field(min_length=1)


class PrivacyRequestTransition(BaseModel):
    status: str
    evidence_refs: List[str] = Field(min_length=1)


class PseudonymisationCreate(BaseModel):
    name: str
    operation: str
    key_or_vault_ref: str
    policy_version_id: str
    evidence_refs: List[str] = Field(min_length=1)


class ResidencyCreate(BaseModel):
    data_class_code: str
    allowed_regions: List[str] = Field(min_length=1)
    prohibited_regions: List[str] = Field(default_factory=list)
    policy_version_id: str
    evidence_refs: List[str] = Field(min_length=1)


class BreachCreate(BaseModel):
    incident_id: str
    hypothesis: str = Field(min_length=3)
    evidence_refs: List[str] = Field(min_length=1)


class BreachFinding(BaseModel):
    finding: str = Field(min_length=3)
    evidence_refs: List[str] = Field(min_length=1)
    status: str = "INVESTIGATING"


class MinorAssessment(BaseModel):
    user_id: str
    jurisdiction: str
    age_or_age_band: str
    outcome: str
    authority_ref: str
    rationale: str = Field(min_length=3)
    evidence_refs: List[str] = Field(min_length=1)


class JurisdictionPack(BaseModel):
    jurisdiction: str
    regulatory_scope_ids: List[str] = Field(min_length=1)
    policy_version_ids: List[str] = Field(min_length=1)
    evidence_refs: List[str] = Field(min_length=1)


class PrivacyEvidencePack(BaseModel):
    title: str
    evidence_node_ids: List[str] = Field(min_length=1)
    evidence_refs: List[str] = Field(min_length=1)


def _raise(exc: Exception):
    status = 404 if isinstance(exc, LookupError) else 422
    raise HTTPException(status_code=status, detail=str(exc)) from exc


@router.post("/legal-bases")
async def legal_basis(payload: LegalBasisCreate, current: User = Admin):
    try:
        return await privacy_protocols.register_legal_basis(
            actor_id=current.id, **payload.model_dump()
        )
    except (LookupError, ValueError) as exc:
        _raise(exc)


@router.post("/processing-activities/{activity_id}/purpose-assessment")
async def purpose(
    activity_id: str, payload: PurposeAssessment, current: User = Admin
):
    try:
        return await privacy_protocols.assess_purpose_limitation(
            actor_id=current.id,
            processing_activity_id=activity_id,
            **payload.model_dump(),
        )
    except (LookupError, ValueError) as exc:
        _raise(exc)


@router.post("/processing-activities/{activity_id}/minimisation")
async def minimisation(
    activity_id: str, payload: MinimisationAssessment, current: User = Admin
):
    try:
        return await privacy_protocols.assess_data_minimisation(
            actor_id=current.id,
            processing_activity_id=activity_id,
            **payload.model_dump(),
        )
    except (LookupError, ValueError) as exc:
        _raise(exc)


@router.post("/consents/{consent_id}/frek-proof")
async def consent_frek(
    consent_id: str, payload: FrekConsentProof, current: User = Admin
):
    try:
        return await privacy_protocols.record_consent_frek_proof(
            actor_id=current.id,
            consent_id=consent_id,
            **payload.model_dump(),
        )
    except (LookupError, ValueError) as exc:
        _raise(exc)


@router.post("/requests")
async def privacy_request(payload: PrivacyRequestCreate, current: User = Admin):
    try:
        return await privacy_protocols.create_restriction_or_objection(
            actor_id=current.id, **payload.model_dump()
        )
    except (LookupError, ValueError) as exc:
        _raise(exc)


@router.patch("/requests/{request_id}")
async def privacy_request_transition(
    request_id: str, payload: PrivacyRequestTransition, current: User = Admin
):
    try:
        return await privacy_protocols.transition_restriction_or_objection(
            actor_id=current.id,
            request_id=request_id,
            **payload.model_dump(),
        )
    except (LookupError, ValueError) as exc:
        _raise(exc)


@router.post("/pseudonymisation")
async def pseudonymisation(payload: PseudonymisationCreate, current: User = Admin):
    try:
        return await privacy_protocols.register_pseudonymisation_policy(
            actor_id=current.id, **payload.model_dump()
        )
    except (LookupError, ValueError) as exc:
        _raise(exc)


@router.post("/residency")
async def residency(payload: ResidencyCreate, current: User = Admin):
    try:
        return await privacy_protocols.register_data_residency_rule(
            actor_id=current.id, **payload.model_dump()
        )
    except (LookupError, ValueError) as exc:
        _raise(exc)


@router.post("/breach-investigations")
async def breach(payload: BreachCreate, current: User = Admin):
    try:
        return await privacy_protocols.open_breach_investigation(
            actor_id=current.id, **payload.model_dump()
        )
    except (LookupError, ValueError) as exc:
        _raise(exc)


@router.post("/breach-investigations/{investigation_id}/findings")
async def breach_finding(
    investigation_id: str, payload: BreachFinding, current: User = Admin
):
    try:
        return await privacy_protocols.record_breach_finding(
            actor_id=current.id,
            investigation_id=investigation_id,
            **payload.model_dump(),
        )
    except (LookupError, ValueError) as exc:
        _raise(exc)


@router.post("/minor-assessments")
async def minor(payload: MinorAssessment, current: User = Admin):
    try:
        return await privacy_protocols.assess_minor_user(
            actor_id=current.id, **payload.model_dump()
        )
    except (LookupError, ValueError) as exc:
        _raise(exc)


@router.post("/jurisdiction-packs")
async def jurisdiction_pack(payload: JurisdictionPack, current: User = Admin):
    try:
        return await privacy_protocols.create_jurisdiction_pack(
            actor_id=current.id, **payload.model_dump()
        )
    except (LookupError, ValueError) as exc:
        _raise(exc)


@router.post("/evidence-packs")
async def evidence_pack(payload: PrivacyEvidencePack, current: User = Admin):
    try:
        return await privacy_protocols.create_privacy_evidence_pack(
            actor_id=current.id, **payload.model_dump()
        )
    except (LookupError, ValueError) as exc:
        _raise(exc)
