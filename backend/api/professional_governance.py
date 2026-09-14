"""Professional governance API — additive P0 runtime for CVLN Academy."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr, Field

from auth import get_current_user, require_role
from db import db
from models import User
from services import professional_governance as gov

router = APIRouter(prefix="/governance", tags=["governance"])

AdminUser = Depends(require_role("admin", "super_admin", "founder"))


class CaseCreate(BaseModel):
    title: str = Field(min_length=3, max_length=200)
    domain: str = Field(min_length=2, max_length=40)
    description: str = Field(min_length=3, max_length=5000)
    sensitivity: str = Field(default="INTERNAL", max_length=30)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class StatusChange(BaseModel):
    status: str


class ExpertCreate(BaseModel):
    display_name: str = Field(min_length=2, max_length=160)
    email: EmailStr
    domains: List[str] = Field(min_length=1)
    organisation: Optional[str] = Field(default=None, max_length=200)


class ExpertAssignmentCreate(BaseModel):
    expert_id: str
    scope: List[str] = Field(min_length=1)
    authority_level: str = "A3_EXTERNAL_EXPERT"


class ExpertKeyIssue(BaseModel):
    expires_at: str = Field(min_length=10, max_length=64)


class DocumentVersionCreate(BaseModel):
    document_type: str
    title: str
    content_hash: str = Field(min_length=64, max_length=128)
    parent_version_id: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class DecisionCreate(BaseModel):
    subject: str = Field(min_length=3, max_length=300)
    rationale: str = Field(min_length=3, max_length=5000)
    state: str = "PROPOSED"
    evidence_refs: List[str] = Field(default_factory=list)


@router.post("/cases")
async def create_case(payload: CaseCreate, current: User = AdminUser):
    return await gov.create_case(actor_id=current.id, **payload.model_dump())


@router.get("/cases")
async def list_cases(
    domain: Optional[str] = None,
    status: Optional[str] = None,
    current: User = Depends(get_current_user),
):
    if current.role == "student":
        raise HTTPException(status_code=403, detail="Professional workspace required")
    query: Dict[str, Any] = {}
    if domain:
        query["domain"] = domain.upper()
    if status:
        query["status"] = status.upper()
    return await db.professional_cases.find(query, {"_id": 0}).sort("created_at", -1).to_list(500)


@router.get("/cases/{case_id}")
async def get_case(case_id: str, current: User = Depends(get_current_user)):
    if current.role == "student":
        raise HTTPException(status_code=403, detail="Professional workspace required")
    case = await db.professional_cases.find_one({"id": case_id}, {"_id": 0})
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    assignments = await db.governance_expert_assignments.find(
        {"case_id": case_id}, {"_id": 0}
    ).to_list(200)
    decisions = await db.governance_decisions.find({"case_id": case_id}, {"_id": 0}).to_list(500)
    documents = await db.governance_document_versions.find(
        {"case_id": case_id}, {"_id": 0}
    ).to_list(500)
    return {**case, "assignments": assignments, "decisions": decisions, "document_versions": documents}


@router.patch("/cases/{case_id}/status")
async def change_case_status(case_id: str, payload: StatusChange, current: User = AdminUser):
    try:
        return await gov.transition_case(case_id=case_id, status=payload.status, actor_id=current.id)
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.post("/experts")
async def create_expert(payload: ExpertCreate, current: User = AdminUser):
    return await gov.create_expert(actor_id=current.id, **payload.model_dump())


@router.get("/experts")
async def list_experts(current: User = AdminUser):
    return await db.governance_experts.find({}, {"_id": 0}).sort("created_at", -1).to_list(500)


@router.post("/cases/{case_id}/assignments")
async def assign_expert(case_id: str, payload: ExpertAssignmentCreate, current: User = AdminUser):
    try:
        return await gov.assign_expert(actor_id=current.id, case_id=case_id, **payload.model_dump())
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.post("/assignments/{assignment_id}/api-key")
async def issue_expert_api_key(
    assignment_id: str, payload: ExpertKeyIssue, current: User = AdminUser
):
    try:
        raw, record = await gov.issue_expert_api_key(
            actor_id=current.id,
            assignment_id=assignment_id,
            expires_at=payload.expires_at,
        )
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return {"api_key": raw, "record": record}


@router.post("/api-keys/{key_id}/rotate")
async def rotate_expert_api_key(
    key_id: str, payload: ExpertKeyIssue, current: User = AdminUser
):
    try:
        raw, record = await gov.rotate_expert_api_key(
            actor_id=current.id,
            key_id=key_id,
            expires_at=payload.expires_at,
        )
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    return {"api_key": raw, "record": record}


@router.post("/cases/{case_id}/documents/versions")
async def register_document_version(case_id: str, payload: DocumentVersionCreate, current: User = AdminUser):
    try:
        return await gov.register_document_version(actor_id=current.id, case_id=case_id, **payload.model_dump())
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.post("/cases/{case_id}/decisions")
async def create_decision(case_id: str, payload: DecisionCreate, current: User = AdminUser):
    try:
        return await gov.create_decision(actor_id=current.id, case_id=case_id, **payload.model_dump())
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.patch("/decisions/{decision_id}/state")
async def transition_decision(decision_id: str, payload: StatusChange, current: User = AdminUser):
    try:
        return await gov.transition_decision(actor_id=current.id, decision_id=decision_id, state=payload.status)
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc


@router.get("/audit")
async def audit_trail(
    resource_type: Optional[str] = None,
    resource_id: Optional[str] = None,
    current: User = AdminUser,
):
    query: Dict[str, Any] = {}
    if resource_type:
        query["resource_type"] = resource_type
    if resource_id:
        query["resource_id"] = resource_id
    return await db.governance_audit_events.find(query, {"_id": 0}).sort("created_at", -1).to_list(1000)
