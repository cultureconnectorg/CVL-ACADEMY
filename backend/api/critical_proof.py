"""Critical decision proof API."""

from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from auth import require_role
from models import User
from services import critical_proof

router = APIRouter(prefix="/critical-proof", tags=["trust"])
Admin = Depends(require_role("admin", "super_admin", "founder"))


class CriticalProofCreate(BaseModel):
    domain: str
    resource_type: str
    resource_id: str
    resource_hash: str = Field(min_length=64, max_length=64)
    authority_decision_id: str
    policy_version_id: str
    evidence_refs: List[str] = Field(min_length=1)


@router.post("")
async def create_proof(payload: CriticalProofCreate, current: User = Admin):
    try:
        return await critical_proof.create_critical_decision_proof(
            actor_id=current.id, **payload.model_dump()
        )
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except PermissionError as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.get("/gate/{domain}/{resource_type}/{resource_id}/{resource_hash}")
async def proof_gate(
    domain: str,
    resource_type: str,
    resource_id: str,
    resource_hash: str,
    current: User = Admin,
):
    try:
        return await critical_proof.proof_gate(
            domain=domain,
            resource_type=resource_type,
            resource_id=resource_id,
            resource_hash=resource_hash,
        )
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
