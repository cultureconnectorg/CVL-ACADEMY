"""Security Verification Core API (SEC-001..010/013/014)."""

from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from auth import require_role
from models import User
from services import security_verification

router = APIRouter(prefix="/security/verification", tags=["security-verification"])
Admin = Depends(require_role("admin", "super_admin", "founder"))


class AssetCreate(BaseModel):
    name: str = Field(min_length=2, max_length=240)
    asset_type: str = Field(min_length=2, max_length=80)
    owner: str = Field(min_length=1, max_length=240)
    exposure: str = Field(min_length=2, max_length=80)
    criticality: str = Field(min_length=2, max_length=80)
    endpoints: List[str] = Field(default_factory=list)
    services: List[str] = Field(default_factory=list)
    data_stores: List[str] = Field(default_factory=list)
    attack_surfaces: List[str] = Field(default_factory=list)
    evidence_refs: List[str] = Field(default_factory=list)


class CiGateRun(BaseModel):
    gate: str
    run_ref: str = Field(min_length=1, max_length=500)
    passed: bool
    findings: List[str] = Field(default_factory=list)
    evidence_refs: List[str] = Field(min_length=1)


class AttackRun(BaseModel):
    suite: str
    run_ref: str = Field(min_length=1, max_length=500)
    covered_areas: List[str] = Field(min_length=1)
    failed_cases: List[str] = Field(default_factory=list)
    evidence_refs: List[str] = Field(min_length=1)


class FindingRetest(BaseModel):
    passed: bool
    test_refs: List[str] = Field(min_length=1)
    evidence_refs: List[str] = Field(min_length=1)


class RiskAcceptance(BaseModel):
    actor_role: str = Field(min_length=2, max_length=80)
    authority_level: str = Field(min_length=2, max_length=80)
    rationale: str = Field(min_length=3, max_length=4000)
    expires_at: str = Field(min_length=10, max_length=64)
    policy_version_id: str = Field(min_length=1, max_length=240)
    evidence_refs: List[str] = Field(min_length=1)


class EvidencePackCreate(BaseModel):
    title: str = Field(min_length=3, max_length=240)
    evidence_node_ids: List[str] = Field(min_length=1)
    evidence_refs: List[str] = Field(min_length=1)


def _translate(exc: Exception):
    if isinstance(exc, LookupError):
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    if isinstance(exc, PermissionError):
        raise HTTPException(status_code=403, detail=str(exc)) from exc
    raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.post("/assets")
async def create_asset(payload: AssetCreate, current: User = Admin):
    try:
        return await security_verification.register_asset(
            actor_id=current.id, **payload.model_dump()
        )
    except ValueError as exc:
        _translate(exc)


@router.post("/ci-gates")
async def record_ci_gate(payload: CiGateRun, current: User = Admin):
    try:
        return await security_verification.record_ci_gate(
            actor_id=current.id, **payload.model_dump()
        )
    except ValueError as exc:
        _translate(exc)


@router.post("/attack-runs")
async def record_attack_run(payload: AttackRun, current: User = Admin):
    try:
        return await security_verification.record_attack_suite_run(
            actor_id=current.id, **payload.model_dump()
        )
    except ValueError as exc:
        _translate(exc)


@router.post("/findings/{finding_id}/retest")
async def retest_finding(
    finding_id: str, payload: FindingRetest, current: User = Admin
):
    try:
        return await security_verification.record_finding_retest(
            actor_id=current.id,
            finding_id=finding_id,
            **payload.model_dump(),
        )
    except (LookupError, ValueError) as exc:
        _translate(exc)


@router.post("/findings/{finding_id}/risk-acceptance")
async def accept_finding_risk(
    finding_id: str, payload: RiskAcceptance, current: User = Admin
):
    try:
        return await security_verification.accept_finding_risk(
            actor_id=current.id,
            finding_id=finding_id,
            **payload.model_dump(),
        )
    except (LookupError, ValueError, PermissionError) as exc:
        _translate(exc)


@router.post("/risk-acceptances/expire")
async def expire_risk_acceptances(current: User = Admin):
    return {
        "expired_ids": await security_verification.expire_risk_acceptances(
            actor_id=current.id
        )
    }


@router.get("/release-gate")
async def release_gate(current: User = Admin):
    return await security_verification.security_release_gate()


@router.post("/evidence-packs")
async def create_evidence_pack(payload: EvidencePackCreate, current: User = Admin):
    try:
        return await security_verification.create_security_evidence_pack(
            actor_id=current.id, **payload.model_dump()
        )
    except (LookupError, ValueError) as exc:
        _translate(exc)
