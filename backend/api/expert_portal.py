"""External-expert portal API with case-scoped credentials."""

from __future__ import annotations

from typing import Any, Optional

from fastapi import APIRouter, Depends, Header, HTTPException
from pydantic import BaseModel, Field

from auth import require_role
from db import db
from models import User
from services import (
    accounting_workspace,
    expert_access,
    external_expert_actions,
    legal_expert_ops,
    legal_policy,
    legal_workspace,
    privacy_advanced,
    quality_advanced,
    risk_advanced,
    security_verification,
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


class PrivacyProcessorReview(BaseModel):
    recommendation: str
    rationale: str = Field(min_length=3, max_length=4000)
    evidence_refs: list[str] = Field(min_length=1)


class PentestFindingCreate(BaseModel):
    title: str = Field(min_length=3, max_length=240)
    severity: str
    attack_surface: str = Field(min_length=2, max_length=500)
    evidence_refs: list[str] = Field(min_length=1)
    remediation_recommendation: str = Field(default="", max_length=4000)


class PentestRetestCreate(BaseModel):
    outcome: str
    evidence_refs: list[str] = Field(min_length=1)


class ExpertMappingCreate(BaseModel):
    event_type: str
    debit_account: str
    credit_account: str
    version: str
    effective_at: str
    evidence_refs: list[str] = Field(min_length=1)
    tax_code: Optional[str] = None
    supersedes_version_id: Optional[str] = None


class BrokerCoverageReview(BaseModel):
    coverage_confirmed: bool
    rationale: str = Field(min_length=3, max_length=4000)
    evidence_refs: list[str] = Field(min_length=1)


class QualityEvidenceReview(BaseModel):
    outcome: str
    rationale: str = Field(min_length=3, max_length=4000)
    evidence_refs: list[str] = Field(min_length=1)


def _credential(x_cvln_expert_key: str | None = Header(default=None)) -> str:
    if not x_cvln_expert_key:
        raise HTTPException(status_code=401, detail="Expert credential required")
    return x_cvln_expert_key


def _translate(exc: Exception):
    if isinstance(exc, LookupError):
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    if isinstance(exc, PermissionError):
        raise HTTPException(status_code=403, detail=str(exc)) from exc
    raise HTTPException(status_code=400, detail=str(exc)) from exc


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
async def expert_legal_workspace(case_id: str, raw_key: str = Depends(_credential)):
    try:
        return await legal_workspace.get_workspace(raw_key=raw_key, case_id=case_id)
    except (LookupError, PermissionError) as exc:
        _translate(exc)


@router.get("/privacy/cases/{case_id}/workspace")
async def expert_privacy_workspace(case_id: str, raw_key: str = Depends(_credential)):
    try:
        return await privacy_advanced.get_privacy_workspace(raw_key=raw_key, case_id=case_id)
    except (LookupError, PermissionError) as exc:
        _translate(exc)


@router.get("/quality/cases/{case_id}/workspace")
async def expert_quality_workspace(case_id: str, raw_key: str = Depends(_credential)):
    try:
        return await quality_advanced.get_quality_workspace(raw_key=raw_key, case_id=case_id)
    except (LookupError, PermissionError) as exc:
        _translate(exc)


@router.get("/security/cases/{case_id}/pentest-workspace")
async def expert_pentest_workspace(case_id: str, raw_key: str = Depends(_credential)):
    try:
        return await security_verification.get_pentest_workspace(
            raw_key=raw_key, case_id=case_id
        )
    except (LookupError, PermissionError) as exc:
        _translate(exc)


@router.get("/risk/cases/{case_id}/broker-workspace")
async def expert_broker_workspace(case_id: str, raw_key: str = Depends(_credential)):
    try:
        return await risk_advanced.get_broker_workspace(raw_key=raw_key, case_id=case_id)
    except (LookupError, PermissionError) as exc:
        _translate(exc)


@router.get("/accounting/cases/{case_id}/workspace")
async def accountant_workspace(case_id: str, raw_key: str = Depends(_credential)):
    try:
        return await accounting_workspace.get_workspace(raw_key=raw_key, case_id=case_id)
    except (LookupError, PermissionError) as exc:
        _translate(exc)


@router.patch("/legal/cases/{case_id}/matters/{matter_id}")
async def expert_modify_legal_matter(
    case_id: str,
    matter_id: str,
    payload: LegalMatterExpertPatch,
    raw_key: str = Depends(_credential),
):
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
    except (LookupError, PermissionError, ValueError) as exc:
        _translate(exc)


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
    except (LookupError, PermissionError, ValueError) as exc:
        _translate(exc)


@router.post("/privacy/cases/{case_id}/processors/{processor_id}/review")
async def expert_privacy_processor_review(
    case_id: str,
    processor_id: str,
    payload: PrivacyProcessorReview,
    raw_key: str = Depends(_credential),
):
    try:
        return await external_expert_actions.privacy_review_processor(
            raw_key=raw_key,
            case_id=case_id,
            processor_id=processor_id,
            **payload.model_dump(),
        )
    except (LookupError, PermissionError, ValueError) as exc:
        _translate(exc)


@router.post("/security/cases/{case_id}/pentest-findings")
async def expert_submit_pentest_finding(
    case_id: str,
    payload: PentestFindingCreate,
    raw_key: str = Depends(_credential),
):
    try:
        return await external_expert_actions.submit_pentest_finding(
            raw_key=raw_key, case_id=case_id, **payload.model_dump()
        )
    except (LookupError, PermissionError, ValueError) as exc:
        _translate(exc)


@router.post("/security/cases/{case_id}/pentest-findings/{finding_id}/retest")
async def expert_submit_pentest_retest(
    case_id: str,
    finding_id: str,
    payload: PentestRetestCreate,
    raw_key: str = Depends(_credential),
):
    try:
        return await external_expert_actions.submit_pentest_retest(
            raw_key=raw_key,
            case_id=case_id,
            finding_id=finding_id,
            **payload.model_dump(),
        )
    except (LookupError, PermissionError, ValueError) as exc:
        _translate(exc)


@router.post("/accounting/cases/{case_id}/mappings")
async def expert_define_accounting_mapping(
    case_id: str,
    payload: ExpertMappingCreate,
    raw_key: str = Depends(_credential),
):
    try:
        return await external_expert_actions.accountant_define_mapping(
            raw_key=raw_key, case_id=case_id, **payload.model_dump()
        )
    except (LookupError, PermissionError, ValueError) as exc:
        _translate(exc)


@router.post("/risk/cases/{case_id}/coverage/{link_id}/review")
async def expert_review_risk_coverage(
    case_id: str,
    link_id: str,
    payload: BrokerCoverageReview,
    raw_key: str = Depends(_credential),
):
    try:
        return await external_expert_actions.broker_review_coverage(
            raw_key=raw_key,
            case_id=case_id,
            link_id=link_id,
            **payload.model_dump(),
        )
    except (LookupError, PermissionError, ValueError) as exc:
        _translate(exc)


@router.post("/quality/cases/{case_id}/evidence/{evidence_id}/review")
async def expert_review_quality_evidence(
    case_id: str,
    evidence_id: str,
    payload: QualityEvidenceReview,
    raw_key: str = Depends(_credential),
):
    try:
        return await external_expert_actions.quality_review_evidence(
            raw_key=raw_key,
            case_id=case_id,
            evidence_id=evidence_id,
            **payload.model_dump(),
        )
    except (LookupError, PermissionError, ValueError) as exc:
        _translate(exc)


@router.delete("/keys/{key_id}")
async def revoke_key(key_id: str, current: User = Admin):
    try:
        return await expert_access.revoke_expert_api_key(actor_id=current.id, key_id=key_id)
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
