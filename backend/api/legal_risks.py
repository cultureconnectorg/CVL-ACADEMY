from __future__ import annotations

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from auth import require_role
from models import User
from services import legal_risks

router = APIRouter(prefix="/legal/risks", tags=["legal-risks"])
Admin = Depends(require_role("admin", "super_admin", "founder"))


class LegalRiskCreate(BaseModel):
    title: str = Field(min_length=3, max_length=240)
    impact: int = Field(ge=1, le=5)
    probability: int = Field(ge=1, le=5)
    control_effectiveness: int = Field(default=0, ge=0, le=5)
    owner: Optional[str] = Field(default=None, max_length=240)
    mitigation: Optional[str] = Field(default=None, max_length=4000)
    deadline: Optional[str] = Field(default=None, max_length=120)
    evidence_refs: List[str] = Field(min_length=1)


def _translate(exc: Exception):
    if isinstance(exc, LookupError):
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.post("/matters/{matter_id}")
async def create_legal_risk(
    matter_id: str,
    payload: LegalRiskCreate,
    current: User = Admin,
):
    try:
        return await legal_risks.register_legal_risk(
            actor_id=current.id,
            matter_id=matter_id,
            **payload.model_dump(),
        )
    except (LookupError, ValueError) as exc:
        _translate(exc)


@router.get("/matters/{matter_id}")
async def get_matter_risks(matter_id: str, current: User = Admin):
    try:
        return await legal_risks.list_matter_risks(matter_id)
    except LookupError as exc:
        _translate(exc)
