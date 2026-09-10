"""Security disclosure and incident-classification APIs (SEC-38..SEC-40)."""

from __future__ import annotations

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from auth import require_role
from models import User
from services import security_incident_protocol

router = APIRouter(prefix="/security-protocol", tags=["security"])
Admin = Depends(require_role("admin", "super_admin", "founder"))


class DisclosureCreate(BaseModel):
    summary: str = Field(min_length=3, max_length=4000)
    reporter_ref: str = Field(min_length=1, max_length=500)
    channel: str = Field(min_length=2, max_length=80)
    evidence_refs: List[str] = Field(min_length=1)
    asset_id: Optional[str] = None
    canonical_incident_id: Optional[str] = None


class DisclosureTransition(BaseModel):
    status: str
    rationale: str = Field(min_length=3, max_length=4000)
    evidence_refs: List[str] = Field(min_length=1)
    finding_id: Optional[str] = None


class SecurityIncidentClassification(BaseModel):
    sev_level: str
    rationale: str = Field(min_length=3, max_length=4000)
    evidence_refs: List[str] = Field(min_length=1)


def _raise(exc: Exception):
    status = 404 if isinstance(exc, LookupError) else 422
    raise HTTPException(status_code=status, detail=str(exc)) from exc


@router.post("/disclosures")
async def create_disclosure(payload: DisclosureCreate, current: User = Admin):
    try:
        return await security_incident_protocol.record_vulnerability_disclosure(
            actor_id=current.id, **payload.model_dump()
        )
    except (LookupError, ValueError) as exc:
        _raise(exc)


@router.patch("/disclosures/{disclosure_id}")
async def transition_disclosure(
    disclosure_id: str, payload: DisclosureTransition, current: User = Admin
):
    try:
        return await security_incident_protocol.transition_vulnerability_disclosure(
            actor_id=current.id, disclosure_id=disclosure_id, **payload.model_dump()
        )
    except (LookupError, ValueError) as exc:
        _raise(exc)


@router.post("/incidents/{incident_id}/classification")
async def classify_incident(
    incident_id: str, payload: SecurityIncidentClassification, current: User = Admin
):
    try:
        return await security_incident_protocol.classify_security_incident(
            actor_id=current.id, incident_id=incident_id, **payload.model_dump()
        )
    except (LookupError, ValueError) as exc:
        _raise(exc)


@router.get("/incidents/{incident_id}/classification")
async def get_incident_classification(incident_id: str, current: User = Admin):
    try:
        return await security_incident_protocol.get_current_security_incident_classification(
            incident_id
        )
    except LookupError as exc:
        _raise(exc)
