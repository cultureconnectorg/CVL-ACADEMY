"""Legal document/version/publication API."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from auth import require_role
from models import User
from services import legal_documents


router = APIRouter(prefix="/legal/documents", tags=["legal-documents"])
Admin = Depends(require_role("admin", "super_admin", "founder"))


class DocumentCreate(BaseModel):
    case_id: str = Field(min_length=1, max_length=240)
    matter_id: str = Field(min_length=1, max_length=240)
    document_type: str = Field(min_length=2, max_length=80)
    title: str = Field(min_length=2, max_length=240)
    jurisdiction: Optional[str] = Field(default=None, max_length=120)
    content_hash: str = Field(min_length=64, max_length=64)
    evidence_refs: List[str] = Field(min_length=1)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class VersionCreate(BaseModel):
    content_hash: str = Field(min_length=64, max_length=64)
    evidence_refs: List[str] = Field(min_length=1)


class StateChange(BaseModel):
    status: str = Field(min_length=3, max_length=40)
    evidence_refs: List[str] = Field(default_factory=list)


class PublishPayload(BaseModel):
    policy_version_id: str = Field(min_length=1, max_length=240)
    authority_level: str = Field(min_length=2, max_length=80)
    evidence_refs: List[str] = Field(min_length=1)


def _translate(exc: Exception):
    if isinstance(exc, LookupError):
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    if isinstance(exc, PermissionError):
        raise HTTPException(status_code=403, detail=str(exc)) from exc
    raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.post("")
async def create_document(payload: DocumentCreate, current: User = Admin):
    try:
        return await legal_documents.create_document(
            actor_id=current.id, **payload.model_dump()
        )
    except (LookupError, ValueError, PermissionError) as exc:
        _translate(exc)


@router.post("/{document_id}/versions")
async def add_version(
    document_id: str,
    payload: VersionCreate,
    current: User = Admin,
):
    try:
        return await legal_documents.add_version(
            actor_id=current.id,
            document_id=document_id,
            **payload.model_dump(),
        )
    except (LookupError, ValueError, PermissionError) as exc:
        _translate(exc)


@router.patch("/{document_id}/state")
async def transition(
    document_id: str,
    payload: StateChange,
    current: User = Admin,
):
    try:
        return await legal_documents.transition_document(
            actor_id=current.id,
            document_id=document_id,
            status=payload.status,
            evidence_refs=payload.evidence_refs,
        )
    except (LookupError, ValueError, PermissionError) as exc:
        _translate(exc)


@router.post("/{document_id}/publish")
async def publish(
    document_id: str,
    payload: PublishPayload,
    current: User = Admin,
):
    try:
        return await legal_documents.publish_document(
            actor_id=current.id,
            actor_role=current.role,
            document_id=document_id,
            **payload.model_dump(),
        )
    except (LookupError, ValueError, PermissionError) as exc:
        _translate(exc)
