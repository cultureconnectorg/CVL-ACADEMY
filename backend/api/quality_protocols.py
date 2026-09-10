"""Quality improvement and proof APIs (QLT-21/QLT-27)."""

from __future__ import annotations

from typing import List
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from auth import require_role
from models import User
from services import quality_protocols

router = APIRouter(prefix="/quality-protocols", tags=["quality"])
Admin = Depends(require_role("admin", "super_admin", "founder"))


class ImprovementEvidence(BaseModel):
    status: str
    outcome: str = Field(min_length=3, max_length=4000)
    evidence_refs: List[str] = Field(min_length=1)


class QualityFrekProof(BaseModel):
    resource_type: str
    resource_id: str
    authority_decision_id: str
    policy_version_id: str
    evidence_refs: List[str] = Field(min_length=1)


def _raise(exc: Exception):
    status = 404 if isinstance(exc, LookupError) else 422
    raise HTTPException(status_code=status, detail=str(exc)) from exc


@router.patch("/improvement-actions/{action_id}")
async def improvement(action_id: str, payload: ImprovementEvidence, current: User = Admin):
    try:
        return await quality_protocols.record_improvement_evidence(
            actor_id=current.id, action_id=action_id, **payload.model_dump()
        )
    except (LookupError, ValueError) as exc:
        _raise(exc)


@router.post("/frek-proof")
async def frek_proof(payload: QualityFrekProof, current: User = Admin):
    try:
        return await quality_protocols.create_quality_frek_proof(
            actor_id=current.id, **payload.model_dump()
        )
    except (LookupError, ValueError) as exc:
        _raise(exc)
