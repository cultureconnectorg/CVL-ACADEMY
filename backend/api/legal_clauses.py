from __future__ import annotations

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from auth import require_role
from models import User
from services import legal_clauses

router = APIRouter(prefix="/legal/clauses", tags=["legal-clauses"])
Admin = Depends(require_role("admin", "super_admin", "founder"))


class ClauseCreate(BaseModel):
    case_id: str
    code: str
    title: str
    context_tags: List[str] = Field(default_factory=list)
    content_hash: str = Field(min_length=64, max_length=64)
    evidence_refs: List[str] = Field(min_length=1)


class ClauseVersionCreate(BaseModel):
    content_hash: str = Field(min_length=64, max_length=64)
    evidence_refs: List[str] = Field(min_length=1)


class ClauseUsageCreate(BaseModel):
    document_id: str
    version_id: Optional[str] = None
    evidence_refs: List[str] = Field(min_length=1)


def _translate(exc: Exception):
    if isinstance(exc, LookupError):
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    if isinstance(exc, PermissionError):
        raise HTTPException(status_code=403, detail=str(exc)) from exc
    raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.post("")
async def create_clause(payload: ClauseCreate, current: User = Admin):
    try:
        return await legal_clauses.create_clause(actor_id=current.id, **payload.model_dump())
    except (LookupError, ValueError, PermissionError) as exc:
        _translate(exc)


@router.post("/{clause_id}/versions")
async def add_version(clause_id: str, payload: ClauseVersionCreate, current: User = Admin):
    try:
        return await legal_clauses.add_clause_version(
            actor_id=current.id, clause_id=clause_id, **payload.model_dump()
        )
    except (LookupError, ValueError, PermissionError) as exc:
        _translate(exc)


@router.post("/{clause_id}/usages")
async def add_usage(clause_id: str, payload: ClauseUsageCreate, current: User = Admin):
    try:
        return await legal_clauses.register_usage(
            actor_id=current.id, clause_id=clause_id, **payload.model_dump()
        )
    except (LookupError, ValueError, PermissionError) as exc:
        _translate(exc)


@router.get("/versions/{version_id}/impact")
async def version_impact(version_id: str, current: User = Admin):
    return await legal_clauses.impact_for_version(version_id)
