"""Canonical Incident Core API (XCP-005)."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from auth import require_role
from models import User
from services import incident_core

router = APIRouter(prefix="/incidents", tags=["governance-incident"])
Admin = Depends(require_role("admin", "super_admin", "founder"))


class IncidentCreate(BaseModel):
    title: str = Field(min_length=3, max_length=240)
    description: str = Field(min_length=3, max_length=4000)
    severity: str = Field(min_length=3, max_length=20)
    domains: List[str] = Field(min_length=1)
    evidence_refs: List[str] = Field(min_length=1)
    data_classes: List[str] = Field(default_factory=list)
    asset_id: Optional[str] = Field(default=None, max_length=240)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class IncidentState(BaseModel):
    status: str = Field(min_length=4, max_length=30)
    evidence_refs: List[str] = Field(default_factory=list)


class ProjectionRequest(BaseModel):
    security_remediation: Optional[str] = Field(default=None, max_length=4000)
    jurisdiction: Optional[str] = Field(default=None, max_length=120)
    risk_impact: Optional[int] = Field(default=None, ge=1, le=5)
    risk_probability: Optional[int] = Field(default=None, ge=1, le=5)
    risk_owner: Optional[str] = Field(default=None, max_length=240)
    risk_mitigation: Optional[str] = Field(default=None, max_length=4000)
    risk_deadline: Optional[str] = Field(default=None, max_length=64)


def _translate(exc: Exception):
    if isinstance(exc, LookupError):
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.post("")
async def create_incident(payload: IncidentCreate, current: User = Admin):
    try:
        return await incident_core.create_incident(actor_id=current.id, **payload.model_dump())
    except ValueError as exc:
        _translate(exc)


@router.get("/{incident_id}")
async def get_incident(incident_id: str, current: User = Admin):
    try:
        return await incident_core.get_incident(incident_id)
    except LookupError as exc:
        _translate(exc)


@router.patch("/{incident_id}/state")
async def transition_incident(incident_id: str, payload: IncidentState, current: User = Admin):
    try:
        return await incident_core.transition_incident(
            actor_id=current.id,
            incident_id=incident_id,
            status=payload.status,
            evidence_refs=payload.evidence_refs,
        )
    except (LookupError, ValueError) as exc:
        _translate(exc)


@router.post("/{incident_id}/project")
async def project_incident(incident_id: str, payload: ProjectionRequest, current: User = Admin):
    try:
        return await incident_core.project_incident(
            actor_id=current.id, incident_id=incident_id, **payload.model_dump()
        )
    except (LookupError, ValueError) as exc:
        _translate(exc)
