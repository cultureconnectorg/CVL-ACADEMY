"""Evidence-first production readiness and deduplication APIs."""

from __future__ import annotations

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from auth import require_role
from models import User
from services import architecture_reuse, production_gates

router = APIRouter(prefix="/production-gates", tags=["production-readiness"])
Admin = Depends(require_role("admin", "super_admin", "founder"))


class GateEvidenceCreate(BaseModel):
    commit_sha: str = Field(min_length=7, max_length=64)
    environment: str = Field(min_length=2, max_length=80)
    evidence_refs: List[str] = Field(min_length=1)
    result: str
    notes: Optional[str] = Field(default=None, max_length=4000)


class XcpEvidenceCreate(BaseModel):
    evidence_refs: List[str] = Field(min_length=1)
    status: str


class BuildDecisionCreate(BaseModel):
    theme: str
    component: str
    decision: str
    canonical_owner: str
    evidence_ref: str


@router.post("/{gate_id}/evidence")
async def record_gate_evidence(
    gate_id: str, payload: GateEvidenceCreate, current: User = Admin
):
    try:
        return await production_gates.record_gate_evidence(
            actor_id=current.id, gate_id=gate_id, **payload.model_dump()
        )
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.get("/{gate_id}")
async def evaluate_gate(
    gate_id: str, commit_sha: Optional[str] = None, current: User = Admin
):
    try:
        return await production_gates.evaluate_gate(gate_id=gate_id, commit_sha=commit_sha)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("")
async def evaluate_all(commit_sha: Optional[str] = None, current: User = Admin):
    return await production_gates.evaluate_all(commit_sha=commit_sha)


@router.post("/xcp/{primitive_id}/evidence")
async def record_xcp_evidence(
    primitive_id: str, payload: XcpEvidenceCreate, current: User = Admin
):
    try:
        return await production_gates.record_xcp_evidence(
            actor_id=current.id, primitive_id=primitive_id, **payload.model_dump()
        )
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.post("/architecture/sync")
async def sync_architecture_manifest(current: User = Admin):
    return await architecture_reuse.sync_manifest(actor_id=current.id)


@router.post("/architecture/build-decisions")
async def register_build_decision(payload: BuildDecisionCreate, current: User = Admin):
    try:
        return await architecture_reuse.register_build_decision(
            actor_id=current.id, **payload.model_dump()
        )
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc


@router.get("/architecture/gate")
async def architecture_gate(current: User = Admin):
    return await architecture_reuse.gate()
