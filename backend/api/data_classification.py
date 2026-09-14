"""Data Classification Engine API (XCP-002 / PRI-001)."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from auth import require_role
from models import User
from services import data_classification

router = APIRouter(prefix="/classification", tags=["privacy-classification"])
Admin = Depends(require_role("admin", "super_admin", "founder"))


class ResourceDeclaration(BaseModel):
    resource_kind: str = Field(min_length=3, max_length=30)
    resource_type: str = Field(min_length=2, max_length=120)
    resource_id: str = Field(min_length=1, max_length=240)
    owner: str = Field(min_length=1, max_length=240)
    source: str = Field(min_length=1, max_length=120)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class ClassificationCreate(BaseModel):
    data_class_code: str = Field(min_length=1, max_length=120)
    policy_version_id: str = Field(min_length=1, max_length=240)
    access_policy_version_id: str = Field(min_length=1, max_length=240)
    purpose: str = Field(min_length=1, max_length=2000)
    legal_basis: Optional[str] = Field(default=None, max_length=1000)
    retention_days: int = Field(ge=0)
    processor_refs: List[str]
    locations: List[str] = Field(min_length=1)
    rationale: str = Field(min_length=3, max_length=4000)
    evidence_refs: List[str] = Field(min_length=1)
    handling_controls: Dict[str, Any] = Field(default_factory=dict)


def _translate(exc: Exception):
    if isinstance(exc, LookupError):
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.post("/resources")
async def declare_resource(payload: ResourceDeclaration, current: User = Admin):
    try:
        return await data_classification.declare_resource(
            actor_id=current.id, **payload.model_dump()
        )
    except ValueError as exc:
        _translate(exc)


@router.post("/resources/{resource_record_id}/classify")
async def classify_resource(
    resource_record_id: str, payload: ClassificationCreate, current: User = Admin
):
    try:
        return await data_classification.classify_resource(
            actor_id=current.id,
            resource_record_id=resource_record_id,
            **payload.model_dump(),
        )
    except (LookupError, ValueError) as exc:
        _translate(exc)


@router.get("/resources/{resource_record_id}")
async def get_resource(resource_record_id: str, current: User = Admin):
    try:
        return await data_classification.get_resource(resource_record_id)
    except LookupError as exc:
        _translate(exc)


@router.get("/unclassified-gate")
async def unclassified_gate(resource_kind: Optional[str] = None, current: User = Admin):
    try:
        return await data_classification.unclassified_gate(resource_kind=resource_kind)
    except ValueError as exc:
        _translate(exc)
