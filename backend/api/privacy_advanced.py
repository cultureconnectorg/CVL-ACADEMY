"""Advanced Privacy Core API (PRI-006/009/010/012/014)."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from auth import get_current_user, require_role
from models import User
from services import privacy_advanced

router = APIRouter(prefix="/privacy-advanced", tags=["privacy-advanced"])
Admin = Depends(require_role("admin", "super_admin", "founder"))


class RectificationCreate(BaseModel):
    resource_record_id: str = Field(min_length=1, max_length=240)
    requested_changes: Dict[str, Any]
    rationale: str = Field(min_length=3, max_length=4000)
    evidence_refs: List[str] = Field(min_length=1)


class EvidenceOnly(BaseModel):
    evidence_refs: List[str] = Field(min_length=1)


class RectificationExecution(BaseModel):
    adapter: str = Field(min_length=1, max_length=240)
    before_hash: str = Field(min_length=64, max_length=64)
    after_hash: str = Field(min_length=64, max_length=64)
    evidence_refs: List[str] = Field(min_length=1)


class AnonymisationRecipeCreate(BaseModel):
    data_class_code: str = Field(min_length=1, max_length=120)
    operations: Dict[str, str]
    policy_version_id: str = Field(min_length=1, max_length=240)
    evidence_refs: List[str] = Field(min_length=1)


class AnonymisationRunCreate(BaseModel):
    recipe_id: str = Field(min_length=1, max_length=240)
    resource_record_id: str = Field(min_length=1, max_length=240)
    before_hash: str = Field(min_length=64, max_length=64)
    candidate_hash: str = Field(min_length=64, max_length=64)
    adapter: str = Field(min_length=1, max_length=240)
    evidence_refs: List[str] = Field(min_length=1)
    metrics: Dict[str, Any] = Field(default_factory=dict)


class AnonymisationVerify(BaseModel):
    rationale: str = Field(min_length=3, max_length=4000)
    residual_reidentification_risk: str = Field(min_length=2, max_length=120)
    evidence_refs: List[str] = Field(min_length=1)


class CommercialAssetApproval(BaseModel):
    actor_role: str = Field(min_length=2, max_length=80)
    authority_level: str = Field(min_length=2, max_length=80)
    asset_name: str = Field(min_length=2, max_length=240)
    policy_version_id: str = Field(min_length=1, max_length=240)
    evidence_refs: List[str] = Field(min_length=1)


class CrossBorderAssessment(BaseModel):
    actor_role: str = Field(min_length=2, max_length=80)
    authority_level: str = Field(min_length=2, max_length=80)
    processor_id: str = Field(min_length=1, max_length=240)
    destination_region: str = Field(min_length=2, max_length=120)
    transfer_mechanism: str = Field(min_length=2, max_length=240)
    policy_version_id: str = Field(min_length=1, max_length=240)
    evidence_refs: List[str] = Field(min_length=1)


def _translate(exc: Exception):
    if isinstance(exc, LookupError):
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    if isinstance(exc, PermissionError):
        raise HTTPException(status_code=403, detail=str(exc)) from exc
    raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.post("/rectifications/me")
async def create_my_rectification(
    payload: RectificationCreate, current: User = Depends(get_current_user)
):
    try:
        return await privacy_advanced.create_rectification_request(
            actor_id=current.id,
            user_id=current.id,
            **payload.model_dump(),
        )
    except (LookupError, ValueError) as exc:
        _translate(exc)


@router.post("/rectifications/{rectification_id}/approve")
async def approve_rectification(
    rectification_id: str, payload: EvidenceOnly, current: User = Admin
):
    try:
        return await privacy_advanced.approve_rectification(
            actor_id=current.id,
            rectification_id=rectification_id,
            evidence_refs=payload.evidence_refs,
        )
    except (LookupError, ValueError) as exc:
        _translate(exc)


@router.post("/rectifications/{rectification_id}/execution")
async def record_rectification_execution(
    rectification_id: str, payload: RectificationExecution, current: User = Admin
):
    try:
        return await privacy_advanced.record_rectification_execution(
            actor_id=current.id,
            rectification_id=rectification_id,
            **payload.model_dump(),
        )
    except (LookupError, ValueError) as exc:
        _translate(exc)


@router.post("/anonymisation/recipes")
async def create_anonymisation_recipe(
    payload: AnonymisationRecipeCreate, current: User = Admin
):
    try:
        return await privacy_advanced.register_anonymisation_recipe(
            actor_id=current.id, **payload.model_dump()
        )
    except (LookupError, ValueError) as exc:
        _translate(exc)


@router.post("/anonymisation/runs")
async def create_anonymisation_run(
    payload: AnonymisationRunCreate, current: User = Admin
):
    try:
        return await privacy_advanced.record_anonymisation_run(
            actor_id=current.id, **payload.model_dump()
        )
    except (LookupError, ValueError) as exc:
        _translate(exc)


@router.post("/anonymisation/runs/{run_id}/verify")
async def verify_anonymisation(
    run_id: str, payload: AnonymisationVerify, current: User = Admin
):
    try:
        return await privacy_advanced.verify_anonymisation(
            actor_id=current.id, run_id=run_id, **payload.model_dump()
        )
    except (LookupError, ValueError) as exc:
        _translate(exc)


@router.post("/derived-assets/{anonymisation_run_id}/approve")
async def approve_derived_asset(
    anonymisation_run_id: str,
    payload: CommercialAssetApproval,
    current: User = Admin,
):
    try:
        return await privacy_advanced.approve_derived_knowledge_asset(
            actor_id=current.id,
            anonymisation_run_id=anonymisation_run_id,
            **payload.model_dump(),
        )
    except (LookupError, ValueError, PermissionError) as exc:
        _translate(exc)


@router.post("/cross-border")
async def assess_cross_border(
    payload: CrossBorderAssessment, current: User = Admin
):
    try:
        return await privacy_advanced.assess_cross_border_transfer(
            actor_id=current.id, **payload.model_dump()
        )
    except (LookupError, ValueError, PermissionError) as exc:
        _translate(exc)
