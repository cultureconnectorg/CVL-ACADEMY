"""Canonical Doctrine / Policy Version Registry API (XCP-008)."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from auth import require_role
from models import User
from services import policy_registry

router = APIRouter(prefix="/policies", tags=["governance-policy"])
Admin = Depends(require_role("admin", "super_admin", "founder"))


class RegistryVersionCreate(BaseModel):
    policy_key: str = Field(min_length=2, max_length=120)
    version: str = Field(min_length=1, max_length=80)
    kind: str = Field(min_length=3, max_length=30)
    title: str = Field(min_length=3, max_length=240)
    content: Dict[str, Any] = Field(default_factory=dict)
    effective_at: str = Field(min_length=10, max_length=64)
    evidence_refs: List[str] = Field(min_length=1)
    supersedes_version_id: Optional[str] = Field(default=None, max_length=240)


def _translate(exc: Exception):
    if isinstance(exc, LookupError):
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.post("/versions")
async def register_version(payload: RegistryVersionCreate, current: User = Admin):
    try:
        return await policy_registry.register_version(actor_id=current.id, **payload.model_dump())
    except ValueError as exc:
        _translate(exc)


@router.get("/versions")
async def list_versions(policy_key: Optional[str] = None, current: User = Admin):
    return await policy_registry.list_versions(policy_key)


@router.get("/versions/{version_id}")
async def get_version(version_id: str, current: User = Admin):
    try:
        version = await policy_registry.get_version(version_id)
    except LookupError as exc:
        _translate(exc)
    return {
        **version,
        "integrity_valid": await policy_registry.verify_version_integrity(version),
    }
