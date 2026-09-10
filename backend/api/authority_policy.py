"""Authority Policy Engine API (XCP-001)."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from auth import get_current_user, require_role
from models import User
from services import authority_policy

router = APIRouter(prefix="/authority", tags=["authority"])
Admin = Depends(require_role("admin", "super_admin", "founder"))


class PolicyRule(BaseModel):
    id: Optional[str] = None
    priority: Optional[int] = None
    effect: str
    reason: str = Field(min_length=3, max_length=1000)
    conditions: Dict[str, Any] = Field(default_factory=dict)


class PolicyVersionCreate(BaseModel):
    policy_key: str = Field(min_length=2, max_length=120)
    version: str = Field(min_length=1, max_length=80)
    title: str = Field(min_length=3, max_length=240)
    rules: List[PolicyRule] = Field(min_length=1)
    effective_at: str = Field(min_length=10, max_length=64)
    doctrine_ref: str = Field(min_length=1, max_length=240)
    evidence_refs: List[str] = Field(min_length=1)
    supersedes_version_id: Optional[str] = Field(default=None, max_length=240)


class AuthorityEvaluation(BaseModel):
    action: str = Field(min_length=2, max_length=160)
    context: Dict[str, Any] = Field(default_factory=dict)
    policy_version_id: str = Field(min_length=1, max_length=240)
    request_id: Optional[str] = Field(default=None, max_length=240)


def _translate(exc: Exception):
    if isinstance(exc, LookupError):
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.post("/policies/versions")
async def register_policy(payload: PolicyVersionCreate, current: User = Admin):
    try:
        body = payload.model_dump()
        body["rules"] = [rule.model_dump(exclude_none=True) for rule in payload.rules]
        return await authority_policy.register_policy_version(actor_id=current.id, **body)
    except ValueError as exc:
        _translate(exc)


@router.post("/evaluate")
async def evaluate(payload: AuthorityEvaluation, current: User = Depends(get_current_user)):
    try:
        return await authority_policy.evaluate_authority(
            actor_id=current.id,
            actor_role=current.role,
            action=payload.action,
            context=payload.context,
            policy_version_id=payload.policy_version_id,
            request_id=payload.request_id,
        )
    except (LookupError, ValueError) as exc:
        _translate(exc)


@router.get("/decisions/{decision_id}")
async def decision(decision_id: str, current: User = Admin):
    try:
        return await authority_policy.get_decision(decision_id)
    except LookupError as exc:
        _translate(exc)
