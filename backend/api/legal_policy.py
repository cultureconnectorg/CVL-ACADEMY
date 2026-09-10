"""Legal authority API for policy-driven review and distinct approval states."""

from __future__ import annotations

from typing import Any, Dict, List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from auth import require_role
from models import User
from services import legal_policy


router = APIRouter(prefix="/legal/policy", tags=["legal-policy"])
Admin = Depends(require_role("admin", "super_admin", "founder"))


class ReviewRequirementPayload(BaseModel):
    policy_version_id: str = Field(min_length=1, max_length=240)
    authority_level: str = Field(min_length=2, max_length=80)
    risk_level: str = Field(min_length=2, max_length=80)
    context: Dict[str, Any] = Field(default_factory=dict)
    evidence_refs: List[str] = Field(min_length=1)


class ApprovalPayload(BaseModel):
    approval_kind: str = Field(min_length=3, max_length=80)
    policy_version_id: str = Field(min_length=1, max_length=240)
    authority_level: str = Field(min_length=2, max_length=80)
    rationale: str = Field(min_length=3, max_length=4000)
    evidence_refs: List[str] = Field(min_length=1)


def _translate(exc: Exception):
    if isinstance(exc, LookupError):
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    if isinstance(exc, PermissionError):
        raise HTTPException(status_code=403, detail=str(exc)) from exc
    raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.post("/matters/{matter_id}/review-requirement")
async def decide_review(
    matter_id: str,
    payload: ReviewRequirementPayload,
    current: User = Admin,
):
    try:
        return await legal_policy.decide_review_requirement(
            actor_id=current.id,
            actor_role=current.role,
            matter_id=matter_id,
            **payload.model_dump(),
        )
    except (LookupError, ValueError, PermissionError) as exc:
        _translate(exc)


@router.post("/matters/{matter_id}/approvals")
async def record_approval(
    matter_id: str,
    payload: ApprovalPayload,
    current: User = Admin,
):
    try:
        return await legal_policy.record_approval(
            actor_id=current.id,
            actor_role=current.role,
            matter_id=matter_id,
            **payload.model_dump(),
        )
    except (LookupError, ValueError, PermissionError) as exc:
        _translate(exc)


@router.get("/matters/{matter_id}/approvals")
async def approval_state(matter_id: str, current: User = Admin):
    try:
        return await legal_policy.approval_state(matter_id)
    except LookupError as exc:
        _translate(exc)
