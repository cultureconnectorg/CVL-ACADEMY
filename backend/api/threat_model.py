"""Defensive threat-model registry API."""

from __future__ import annotations

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from auth import require_role
from models import User
from services import threat_model

router = APIRouter(prefix="/security/threats", tags=["security"])
Admin = Depends(require_role("admin", "super_admin", "founder"))


class ThreatCreate(BaseModel):
    title: str = Field(min_length=3, max_length=240)
    category: str
    asset_id: Optional[str] = None
    attack_surface: str
    abuse_case: str
    severity: str
    mitigations: List[str] = Field(default_factory=list)
    test_refs: List[str] = Field(default_factory=list)


class EvidenceAdd(BaseModel):
    mitigation: Optional[str] = None
    test_ref: Optional[str] = None
    evidence_ref: Optional[str] = None


class StateChange(BaseModel):
    status: str


def _raise(exc: Exception):
    status = 404 if isinstance(exc, LookupError) else 422
    raise HTTPException(status_code=status, detail=str(exc)) from exc


@router.post("")
async def create_threat(payload: ThreatCreate, current: User = Admin):
    try:
        return await threat_model.create_threat(actor_id=current.id, **payload.model_dump())
    except (LookupError, ValueError) as exc:
        _raise(exc)


@router.post("/{threat_id}/evidence")
async def add_evidence(threat_id: str, payload: EvidenceAdd, current: User = Admin):
    try:
        return await threat_model.add_threat_evidence(
            actor_id=current.id, threat_id=threat_id, **payload.model_dump()
        )
    except LookupError as exc:
        _raise(exc)


@router.patch("/{threat_id}")
async def transition(threat_id: str, payload: StateChange, current: User = Admin):
    try:
        return await threat_model.transition_threat(
            actor_id=current.id, threat_id=threat_id, status=payload.status
        )
    except (LookupError, ValueError) as exc:
        _raise(exc)


@router.get("/release-gate")
async def release_gate(current: User = Admin):
    return await threat_model.threat_release_gate()
