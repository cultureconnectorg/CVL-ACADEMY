"""Legal P0 API for matters, review policy and contract lifecycle."""

from __future__ import annotations

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from auth import require_role
from models import User
from services import legal_ops

router = APIRouter(prefix="/legal", tags=["legal"])
Admin = Depends(require_role("admin", "super_admin", "founder"))


class MatterCreate(BaseModel):
    title: str = Field(min_length=3, max_length=240)
    matter_type: str = Field(min_length=2, max_length=80)
    jurisdiction: Optional[str] = Field(default=None, max_length=120)
    case_id: Optional[str] = Field(default=None, max_length=240)
    owner_id: Optional[str] = Field(default=None, max_length=240)
    risk_ids: List[str] = Field(default_factory=list)
    evidence_refs: List[str] = Field(default_factory=list)


class MatterState(BaseModel):
    status: str


class ReviewDecision(BaseModel):
    external_review_required: bool
    rationale: str = Field(min_length=3, max_length=4000)
    policy_ref: str = Field(min_length=1, max_length=240)
    evidence_refs: List[str] = Field(default_factory=list)


class ContractCreate(BaseModel):
    title: str = Field(min_length=3, max_length=240)
    contract_type: str = Field(min_length=2, max_length=80)
    counterparty: str = Field(min_length=2, max_length=240)
    matter_id: Optional[str] = None
    jurisdiction: Optional[str] = Field(default=None, max_length=120)
    starts_at: Optional[str] = None
    ends_at: Optional[str] = None
    renewal_at: Optional[str] = None
    document_id: Optional[str] = None
    evidence_refs: List[str] = Field(default_factory=list)


class ContractState(BaseModel):
    status: str
    evidence_refs: List[str] = Field(default_factory=list)


def _translate(exc: Exception):
    if isinstance(exc, LookupError):
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.post("/matters")
async def create_matter(payload: MatterCreate, current: User = Admin):
    return await legal_ops.create_legal_matter(actor_id=current.id, **payload.model_dump())


@router.patch("/matters/{matter_id}/state")
async def change_matter_state(matter_id: str, payload: MatterState, current: User = Admin):
    try:
        return await legal_ops.transition_legal_matter(
            actor_id=current.id, matter_id=matter_id, status=payload.status
        )
    except (LookupError, ValueError) as exc:
        _translate(exc)


@router.post("/matters/{matter_id}/review-decision")
async def review_decision(matter_id: str, payload: ReviewDecision, current: User = Admin):
    try:
        return await legal_ops.record_review_policy_decision(
            actor_id=current.id, matter_id=matter_id, **payload.model_dump()
        )
    except (LookupError, ValueError) as exc:
        _translate(exc)


@router.post("/contracts")
async def create_contract(payload: ContractCreate, current: User = Admin):
    try:
        return await legal_ops.create_contract(actor_id=current.id, **payload.model_dump())
    except LookupError as exc:
        _translate(exc)


@router.patch("/contracts/{contract_id}/state")
async def change_contract_state(
    contract_id: str, payload: ContractState, current: User = Admin
):
    try:
        return await legal_ops.transition_contract(
            actor_id=current.id,
            contract_id=contract_id,
            status=payload.status,
            evidence_refs=payload.evidence_refs,
        )
    except (LookupError, ValueError) as exc:
        _translate(exc)
