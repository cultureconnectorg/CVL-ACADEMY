"""Risk & Insurance advanced API."""

from __future__ import annotations

from typing import Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from auth import require_role
from models import User
from services import risk_advanced

router = APIRouter(prefix="/risk-advanced", tags=["risk-insurance"])
Admin = Depends(require_role("admin", "super_admin", "founder"))


class CriticalTreatment(BaseModel):
    actor_role: str = Field(min_length=2, max_length=80)
    authority_level: str = Field(min_length=2, max_length=80)
    treatment: str = Field(min_length=2, max_length=40)
    policy_version_id: str = Field(min_length=1, max_length=240)
    owner: str = Field(min_length=1, max_length=240)
    mitigation: str = Field(min_length=3, max_length=4000)
    deadline: str = Field(min_length=4, max_length=64)
    evidence_refs: List[str] = Field(min_length=1)


class InsurancePolicyCreate(BaseModel):
    provider: str = Field(min_length=2, max_length=240)
    policy_ref: str = Field(min_length=1, max_length=240)
    coverage_types: List[str] = Field(min_length=1)
    limits: Dict[str, int]
    starts_at: str = Field(min_length=10, max_length=64)
    ends_at: str = Field(min_length=10, max_length=64)
    evidence_refs: List[str] = Field(min_length=1)


class CoverageLinkCreate(BaseModel):
    insurance_policy_id: str = Field(min_length=1, max_length=240)
    coverage_type: str = Field(min_length=2, max_length=120)
    evidence_refs: List[str] = Field(min_length=1)


class CoverageReview(BaseModel):
    coverage_confirmed: bool
    rationale: str = Field(min_length=3, max_length=4000)
    evidence_refs: List[str] = Field(min_length=1)


class EvidencePackCreate(BaseModel):
    evidence_node_ids: List[str] = Field(min_length=1)
    evidence_refs: List[str] = Field(min_length=1)


def _raise(exc: Exception):
    if isinstance(exc, LookupError):
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    if isinstance(exc, PermissionError):
        raise HTTPException(status_code=403, detail=str(exc)) from exc
    raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.post("/risks/{risk_id}/critical-treatment")
async def critical_treatment(
    risk_id: str, payload: CriticalTreatment, current: User = Admin
):
    try:
        return await risk_advanced.set_critical_risk_treatment(
            actor_id=current.id,
            risk_id=risk_id,
            **payload.model_dump(),
        )
    except (LookupError, ValueError, PermissionError) as exc:
        _raise(exc)


@router.post("/insurance-policies")
async def insurance_policy(payload: InsurancePolicyCreate, current: User = Admin):
    try:
        return await risk_advanced.register_insurance_policy(
            actor_id=current.id, **payload.model_dump()
        )
    except ValueError as exc:
        _raise(exc)


@router.post("/risks/{risk_id}/coverage")
async def coverage_link(
    risk_id: str, payload: CoverageLinkCreate, current: User = Admin
):
    try:
        return await risk_advanced.link_risk_coverage(
            actor_id=current.id,
            risk_id=risk_id,
            **payload.model_dump(),
        )
    except (LookupError, ValueError) as exc:
        _raise(exc)


@router.post("/coverage/{link_id}/review")
async def review_coverage(
    link_id: str, payload: CoverageReview, current: User = Admin
):
    try:
        return await risk_advanced.review_coverage_link(
            actor_id=current.id,
            link_id=link_id,
            **payload.model_dump(),
        )
    except (LookupError, ValueError) as exc:
        _raise(exc)


@router.get("/uncovered-gate")
async def uncovered_gate(current: User = Admin):
    return await risk_advanced.uncovered_asset_gate()


@router.get("/insurance-renewals")
async def insurance_renewals(current: User = Admin):
    return await risk_advanced.renewal_alerts()


@router.post("/risks/{risk_id}/claim-package")
async def claim_package(
    risk_id: str, payload: EvidencePackCreate, current: User = Admin
):
    try:
        return await risk_advanced.create_claim_package(
            actor_id=current.id,
            risk_id=risk_id,
            **payload.model_dump(),
        )
    except (LookupError, ValueError) as exc:
        _raise(exc)


@router.post("/insurance-policies/{insurance_policy_id}/renewal-package")
async def renewal_package(
    insurance_policy_id: str,
    payload: EvidencePackCreate,
    current: User = Admin,
):
    try:
        return await risk_advanced.create_renewal_package(
            actor_id=current.id,
            insurance_policy_id=insurance_policy_id,
            **payload.model_dump(),
        )
    except (LookupError, ValueError) as exc:
        _raise(exc)
