from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from auth import require_role
from models import User
from services import legal_evidence

router = APIRouter(prefix="/legal/evidence", tags=["legal-evidence"])
Admin = Depends(require_role("admin", "super_admin", "founder"))


class LegalEvidencePackCreate(BaseModel):
    title: str = Field(min_length=2, max_length=240)
    purpose: str = Field(min_length=3, max_length=2000)
    node_ids: List[str] = Field(min_length=1)
    evidence_refs: List[str] = Field(min_length=1)


def _translate(exc: Exception):
    if isinstance(exc, LookupError):
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    if isinstance(exc, PermissionError):
        raise HTTPException(status_code=403, detail=str(exc)) from exc
    raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.post("/matters/{matter_id}/packs")
async def create_pack(
    matter_id: str,
    payload: LegalEvidencePackCreate,
    current: User = Admin,
):
    try:
        return await legal_evidence.create_legal_pack(
            actor_id=current.id,
            matter_id=matter_id,
            **payload.model_dump(),
        )
    except (LookupError, ValueError, PermissionError) as exc:
        _translate(exc)


@router.get("/matters/{matter_id}/packs")
async def list_packs(matter_id: str, current: User = Admin):
    try:
        return await legal_evidence.list_matter_packs(matter_id)
    except LookupError as exc:
        _translate(exc)
