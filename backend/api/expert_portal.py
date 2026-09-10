"""External-expert portal API with case-scoped credentials."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, Header, HTTPException
from pydantic import BaseModel, Field

from auth import require_role
from db import db
from models import User
from services import (
    accounting_workspace,
    expert_access,
    legal_expert_ops,
    legal_policy,
    legal_workspace,
)

router = APIRouter(prefix="/expert", tags=["governance-expert"])
Admin = Depends(require_role("admin", "super_admin", "founder"))


class LegalMatterExpertPatch(BaseModel):
    patch: dict[str, Any]
    policy_version_id: str
    rationale: str
    evidence_refs: list[str] = Field(default_factory=list)


class LegalExternalApproval(BaseModel):
    policy_version_id: str = Field(min_length=1, max_length=240)
    rationale: str = Field(min_length=3, max_length=4000)
    evidence_refs: list[str] = Field(min_length=1)


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


@router.get("/legal/cases/{case_id}/workspace")
async def expert_legal_workspace(
    case_id: str,
    raw_key: str = Depends(_credential),
):
    try:
        return await legal_workspace.get_workspace(raw_key=raw_key, case_id=case_id)
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except PermissionError as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc


@router.patch("/legal/cases/{case_id}/matters/{matter_id}")
async def expert_modify_legal_matter(
    case_id: str,
    matter_id: str,
    payload: LegalMatterExpertPatch,
    raw_key: str = Depends(_credential),
):
    """FD-L01: direct legal-expert edit under scope, policy, evidence and audit."""
    try:
        return await legal_expert_ops.modify_legal_matter(
            raw_key=raw_key,
            case_id=case_id,
            matter_id=matter_id,
            patch=payload.patch,
            policy_version_id=payload.policy_version_id,
            rationale=payload.rationale,
            evidence_refs=payload.evidence_refs,
        )
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except PermissionError as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/legal/cases/{case_id}/matters/{matter_id}/external-approval")
async def expert_external_legal_approval(
    case_id: str,
    matter_id: str,
    payload: LegalExternalApproval,
    raw_key: str = Depends(_credential),
):
    try:
        return await legal_policy.record_external_expert_approval(
            raw_key=raw_key,
            case_id=case_id,
            matter_id=matter_id,
            **payload.model_dump(),
        )
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except PermissionError as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/accounting/cases/{case_id}/workspace")
async def accountant_workspace(case_id: str, raw_key: str = Depends(_credential)):
    try:
        return await accounting_workspace.get_workspace(raw_key=raw_key, case_id=case_id)
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except PermissionError as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc


@router.delete("/keys/{key_id}")
async def revoke_key(key_id: str, current: User = Admin):
    try:
        return await expert_access.revoke_expert_api_key(actor_id=current.id, key_id=key_id)
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
