"""Regulatory applicability map APIs (REG-01..REG-08)."""

from __future__ import annotations

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from auth import require_role
from models import User
from services import regulatory_applicability

router = APIRouter(prefix="/regulatory", tags=["regulatory"])
Admin = Depends(require_role("admin", "super_admin", "founder"))


class ScopeCreate(BaseModel):
    regulatory_id: str
    jurisdiction: str
    activity: str
    entity_ref: str
    product_scope: str
    evidence_refs: List[str] = Field(min_length=1)


class ApplicabilityDecision(BaseModel):
    outcome: str
    rationale: str = Field(min_length=3, max_length=4000)
    authority_ref: str
    source_refs: List[str] = Field(min_length=1)
    effective_at: str
    review_due_at: Optional[str] = None


def _translate(exc: Exception):
    if isinstance(exc, LookupError):
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.post("/scopes")
async def create_scope(payload: ScopeCreate, current: User = Admin):
    try:
        return await regulatory_applicability.declare_scope(
            actor_id=current.id, **payload.model_dump()
        )
    except ValueError as exc:
        _translate(exc)


@router.post("/scopes/{scope_id}/decision")
async def decide_scope(
    scope_id: str, payload: ApplicabilityDecision, current: User = Admin
):
    try:
        return await regulatory_applicability.record_applicability_decision(
            actor_id=current.id, scope_id=scope_id, **payload.model_dump()
        )
    except (LookupError, ValueError) as exc:
        _translate(exc)


@router.get("/gate")
async def gate(regulatory_id: Optional[str] = None, current: User = Admin):
    try:
        return await regulatory_applicability.applicability_gate(
            regulatory_id=regulatory_id
        )
    except ValueError as exc:
        _translate(exc)
