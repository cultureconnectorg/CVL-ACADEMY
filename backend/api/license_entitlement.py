"""XCP-007 license entitlement API."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from auth import require_role
from models import User
from services import license_entitlement

router = APIRouter(prefix="/licensing", tags=["licensing"])
Admin = Depends(require_role("admin", "super_admin", "founder"))


class TenantCreate(BaseModel):
    tenant_key: str = Field(min_length=1, max_length=120)
    display_name: str = Field(min_length=2, max_length=240)
    owner_ref: str = Field(min_length=1, max_length=240)
    evidence_refs: List[str] = Field(min_length=1)


class EntitlementCreate(BaseModel):
    version: str = Field(min_length=1, max_length=80)
    effective_at: str = Field(min_length=10, max_length=64)
    capabilities: List[str] = Field(min_length=1)
    public_constraints: Dict[str, Any] = Field(default_factory=dict)
    evidence_refs: List[str] = Field(min_length=1)
    supersedes_version_id: Optional[str] = Field(default=None, max_length=240)


def _raise(exc: Exception):
    if isinstance(exc, LookupError):
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    if isinstance(exc, PermissionError):
        raise HTTPException(status_code=403, detail=str(exc)) from exc
    raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.post("/tenants")
async def create_tenant(payload: TenantCreate, current: User = Admin):
    try:
        return await license_entitlement.register_tenant(
            actor_id=current.id, **payload.model_dump()
        )
    except ValueError as exc:
        _raise(exc)


@router.post("/tenants/{tenant_id}/entitlement")
async def set_entitlement(
    tenant_id: str, payload: EntitlementCreate, current: User = Admin
):
    try:
        return await license_entitlement.register_entitlement_version(
            actor_id=current.id,
            tenant_id=tenant_id,
            **payload.model_dump(),
        )
    except (LookupError, ValueError) as exc:
        _raise(exc)


@router.get("/tenants/{tenant_id}/entitlement")
async def get_entitlement(tenant_id: str, current: User = Admin):
    try:
        return await license_entitlement.entitlement_view(tenant_id)
    except (LookupError, ValueError) as exc:
        _raise(exc)


@router.get("/tenants/{tenant_id}/capabilities/{capability}")
async def check_capability(tenant_id: str, capability: str, current: User = Admin):
    try:
        return await license_entitlement.require_capability(tenant_id, capability)
    except (LookupError, ValueError, PermissionError) as exc:
        _raise(exc)
