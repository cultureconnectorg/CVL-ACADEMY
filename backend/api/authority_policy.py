"""Authority Policy Engine API (XCP-001 + Protocol Master GOV-02)."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from auth import get_current_user, require_role
from models import User
from services import authority_policy, authority_policy_protocol

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


class AuthorityProtocolEvaluation(BaseModel):
    action: str = Field(min_length=2, max_length=160)
    authority_context: str = Field(min_length=1, max_length=240)
    policy_version_id: str = Field(min_length=1, max_length=240)
    evidence_ref: str = Field(min_length=1, max_length=500)
    control_version_ref: str = Field(min_length=1, max_length=500)
    frek_proof_ref: str = Field(min_length=1, max_length=500)
    production_gate_evidence_ref: str = Field(min_length=1, max_length=500)
    expert_review_ref: str = Field(min_length=1, max_length=500)
    cvln_ios_ref: str = Field(min_length=1, max_length=500)
    integration_refs: Dict[str, str] = Field(min_length=1)
    policy_context: Dict[str, Any] = Field(default_factory=dict)
    request_id: Optional[str] = Field(default=None, max_length=240)


def _translate(exc: Exception):
    if isinstance(exc, LookupError):
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    if isinstance(exc, PermissionError):
        raise HTTPException(status_code=403, detail=str(exc)) from exc
    raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.post("/policies/versions")
async def register_policy(payload: PolicyVersionCreate, current: User = Admin):
    try:
        body = payload.model_dump()
        body["rules"] = [
            rule.model_dump(exclude_none=True) for rule in payload.rules
        ]
        return await authority_policy.register_policy_version(
            actor_id=current.id, **body
        )
    except ValueError as exc:
        _translate(exc)


@router.post("/evaluate")
async def evaluate(
    payload: AuthorityEvaluation,
    current: User = Depends(get_current_user),
):
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


@router.post("/protocol/evaluate")
async def evaluate_protocol(
    payload: AuthorityProtocolEvaluation,
    current: User = Depends(get_current_user),
):
    """Execute exact Protocol Master GOV-02 before authority evaluation."""
    try:
        return await authority_policy_protocol.execute_authority_policy_protocol(
            actor_id=current.id,
            actor_role=current.role,
            **payload.model_dump(),
        )
    except (LookupError, ValueError, PermissionError) as exc:
        _translate(exc)


@router.get("/decisions/{decision_id}")
async def decision(decision_id: str, current: User = Admin):
    try:
        return await authority_policy.get_decision(decision_id)
    except LookupError as exc:
        _translate(exc)
