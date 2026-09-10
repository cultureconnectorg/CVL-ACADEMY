"""Minimal external-expert portal API with case-scoped credentials."""

from __future__ import annotations

from fastapi import APIRouter, Depends, Header, HTTPException

from auth import require_role
from db import db
from models import User
from services import expert_access

router = APIRouter(prefix="/expert", tags=["governance-expert"])
Admin = Depends(require_role("admin", "super_admin", "founder"))


def _credential(x_cvln_expert_key: str | None = Header(default=None)) -> str:
    if not x_cvln_expert_key:
        raise HTTPException(status_code=401, detail="Expert credential required")
    return x_cvln_expert_key


@router.get("/cases/{case_id}")
async def expert_case(case_id: str, raw_key: str = Depends(_credential)):
    try:
        context = await expert_access.authorize_case_scope(raw_key, case_id, "case:read")
    except PermissionError as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc

    case = await db.professional_cases.find_one({"id": case_id}, {"_id": 0})
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    documents = await db.governance_document_versions.find(
        {"case_id": case_id}, {"_id": 0}
    ).to_list(500)
    decisions = await db.governance_decisions.find(
        {"case_id": case_id}, {"_id": 0}
    ).to_list(500)
    return {
        "case": case,
        "documents": documents,
        "decisions": decisions,
        "expert": {
            "id": context["expert"]["id"],
            "display_name": context["expert"]["display_name"],
        },
        "granted_scope": context["assignment"].get("scope", []),
    }


@router.delete("/keys/{key_id}")
async def revoke_key(key_id: str, current: User = Admin):
    try:
        return await expert_access.revoke_expert_api_key(actor_id=current.id, key_id=key_id)
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
