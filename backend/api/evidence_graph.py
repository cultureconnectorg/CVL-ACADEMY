"""Evidence Graph API (XCP-004)."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from auth import require_role
from models import User
from services import evidence_graph

router = APIRouter(prefix="/evidence", tags=["governance-evidence"])
Admin = Depends(require_role("admin", "super_admin", "founder"))


class EvidenceNodeCreate(BaseModel):
    source_type: str = Field(min_length=2, max_length=120)
    source_id: str = Field(min_length=1, max_length=240)
    content_hash: str = Field(min_length=64, max_length=64)
    provenance_refs: List[str] = Field(min_length=1)
    access_policy_version_id: str = Field(min_length=1, max_length=240)
    classification_id: Optional[str] = Field(default=None, max_length=240)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class EvidenceLinkCreate(BaseModel):
    from_node_id: str = Field(min_length=1, max_length=240)
    to_node_id: str = Field(min_length=1, max_length=240)
    relation: str = Field(min_length=3, max_length=40)
    evidence_refs: List[str] = Field(min_length=1)


class EvidencePackCreate(BaseModel):
    title: str = Field(min_length=3, max_length=240)
    consumer: str = Field(min_length=3, max_length=40)
    node_ids: List[str] = Field(min_length=1)
    purpose: str = Field(min_length=3, max_length=2000)
    evidence_refs: List[str] = Field(min_length=1)


def _translate(exc: Exception):
    if isinstance(exc, LookupError):
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.post("/nodes")
async def create_node(payload: EvidenceNodeCreate, current: User = Admin):
    try:
        return await evidence_graph.register_node(actor_id=current.id, **payload.model_dump())
    except (LookupError, ValueError) as exc:
        _translate(exc)


@router.post("/links")
async def create_link(payload: EvidenceLinkCreate, current: User = Admin):
    try:
        return await evidence_graph.link_nodes(actor_id=current.id, **payload.model_dump())
    except (LookupError, ValueError) as exc:
        _translate(exc)


@router.post("/packs")
async def create_pack(payload: EvidencePackCreate, current: User = Admin):
    try:
        return await evidence_graph.create_pack(actor_id=current.id, **payload.model_dump())
    except (LookupError, ValueError) as exc:
        _translate(exc)


@router.get("/packs/{pack_id}")
async def get_pack(pack_id: str, current: User = Admin):
    try:
        return await evidence_graph.get_pack(pack_id)
    except LookupError as exc:
        _translate(exc)


@router.get("/integrity-gate")
async def integrity_gate(current: User = Admin):
    return await evidence_graph.integrity_gate()
