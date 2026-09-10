"""Data governance APIs (DAT-01..DAT-14)."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from auth import require_role
from models import User
from services import data_governance

router = APIRouter(prefix="/data-governance", tags=["data"])
Admin = Depends(require_role("admin", "super_admin", "founder"))


class DatasetCreate(BaseModel):
    name: str
    source_system: str
    source_ref: str
    content_hash: str = Field(min_length=64, max_length=64)
    owner: str
    evidence_refs: List[str] = Field(min_length=1)
    classification_resource_id: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class LineageCreate(BaseModel):
    parent_dataset_id: str
    child_dataset_id: str
    transformation: str
    code_or_job_ref: str
    evidence_refs: List[str] = Field(min_length=1)


class ArchiveCreate(BaseModel):
    archive_ref: str
    archive_hash: str = Field(min_length=64, max_length=64)
    evidence_refs: List[str] = Field(min_length=1)


class DerivedCreate(BaseModel):
    source_dataset_id: str
    derived_dataset_id: str
    anonymisation_execution_ref: str
    evidence_refs: List[str] = Field(min_length=1)


class EligibilityDecision(BaseModel):
    policy_version_id: str
    eligible: bool
    rationale: str
    evidence_refs: List[str] = Field(min_length=1)
    authority_level: str = "A5_FOUNDER_SYSTEMIC"


class LicenseCreate(BaseModel):
    derived_asset_id: str
    licensee_id: str
    purpose: str
    starts_at: str
    ends_at: str
    policy_version_id: str
    evidence_refs: List[str] = Field(min_length=1)


class WithdrawalCreate(BaseModel):
    reason: str
    evidence_refs: List[str] = Field(min_length=1)


class AccessAuditCreate(BaseModel):
    dataset_id: str
    action: str
    purpose: str
    decision: str
    evidence_refs: List[str] = Field(min_length=1)


def _translate(exc: Exception):
    if isinstance(exc, LookupError):
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    if isinstance(exc, PermissionError):
        raise HTTPException(status_code=403, detail=str(exc)) from exc
    raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.post("/datasets")
async def create_dataset(payload: DatasetCreate, current: User = Admin):
    try:
        return await data_governance.register_dataset(actor_id=current.id, **payload.model_dump())
    except (LookupError, PermissionError, ValueError) as exc:
        _translate(exc)


@router.post("/lineage")
async def create_lineage(payload: LineageCreate, current: User = Admin):
    try:
        return await data_governance.record_lineage(actor_id=current.id, **payload.model_dump())
    except (LookupError, PermissionError, ValueError) as exc:
        _translate(exc)


@router.post("/datasets/{dataset_id}/archive")
async def archive_dataset(dataset_id: str, payload: ArchiveCreate, current: User = Admin):
    try:
        return await data_governance.archive_dataset(
            actor_id=current.id, dataset_id=dataset_id, **payload.model_dump()
        )
    except (LookupError, PermissionError, ValueError) as exc:
        _translate(exc)


@router.post("/derived-assets")
async def create_derived(payload: DerivedCreate, current: User = Admin):
    try:
        return await data_governance.register_anonymised_derived_asset(
            actor_id=current.id, **payload.model_dump()
        )
    except (LookupError, PermissionError, ValueError) as exc:
        _translate(exc)


@router.post("/derived-assets/{derived_asset_id}/eligibility")
async def decide_eligibility(
    derived_asset_id: str, payload: EligibilityDecision, current: User = Admin
):
    try:
        return await data_governance.decide_commercial_eligibility(
            actor_id=current.id,
            actor_role=current.role,
            derived_asset_id=derived_asset_id,
            **payload.model_dump(),
        )
    except (LookupError, PermissionError, ValueError) as exc:
        _translate(exc)


@router.post("/licenses")
async def create_license(payload: LicenseCreate, current: User = Admin):
    try:
        return await data_governance.issue_dataset_license(
            actor_id=current.id, **payload.model_dump()
        )
    except (LookupError, PermissionError, ValueError) as exc:
        _translate(exc)


@router.post("/licenses/{license_id}/withdraw")
async def withdraw_license(
    license_id: str, payload: WithdrawalCreate, current: User = Admin
):
    try:
        return await data_governance.withdraw_dataset_license(
            actor_id=current.id, license_id=license_id, **payload.model_dump()
        )
    except (LookupError, PermissionError, ValueError) as exc:
        _translate(exc)


@router.post("/access-audit")
async def audit_access(payload: AccessAuditCreate, current: User = Admin):
    try:
        return await data_governance.audit_data_access(actor_id=current.id, **payload.model_dump())
    except (LookupError, PermissionError, ValueError) as exc:
        _translate(exc)
