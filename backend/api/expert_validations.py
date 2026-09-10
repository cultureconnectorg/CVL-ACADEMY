"""External expert scoped validation/correction endpoints."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, Header, HTTPException
from pydantic import BaseModel, Field

from services import external_expert_validations

router = APIRouter(prefix="/expert-validations", tags=["governance-expert"])


class ReviewPayload(BaseModel):
    outcome: str
    rationale: str = Field(min_length=3, max_length=4000)
    evidence_refs: list[str] = Field(min_length=1)


class BrokerRecommendation(BaseModel):
    recommendation: str = Field(min_length=3, max_length=4000)
    rationale: str = Field(min_length=3, max_length=4000)
    evidence_refs: list[str] = Field(min_length=1)


class QualityCorrection(BaseModel):
    correction: dict[str, Any]
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
    raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.post("/accounting/cases/{case_id}/reconciliations/{reconciliation_id}")
async def accountant_review_reconciliation(
    case_id: str,
    reconciliation_id: str,
    payload: ReviewPayload,
    raw_key: str = Depends(_credential),
):
    try:
        return await external_expert_validations.accountant_review_reconciliation(
            raw_key=raw_key,
            case_id=case_id,
            reconciliation_id=reconciliation_id,
            **payload.model_dump(),
        )
    except (LookupError, PermissionError, ValueError) as exc:
        _translate(exc)


@router.post("/accounting/cases/{case_id}/tax-packages/{tax_package_id}")
async def accountant_validate_tax_package(
    case_id: str,
    tax_package_id: str,
    payload: ReviewPayload,
    raw_key: str = Depends(_credential),
):
    try:
        return await external_expert_validations.accountant_validate_tax_package(
            raw_key=raw_key,
            case_id=case_id,
            tax_package_id=tax_package_id,
            **payload.model_dump(),
        )
    except (LookupError, PermissionError, ValueError) as exc:
        _translate(exc)


@router.post("/privacy/cases/{case_id}/processing/{activity_id}")
async def privacy_validate_processing_activity(
    case_id: str,
    activity_id: str,
    payload: ReviewPayload,
    raw_key: str = Depends(_credential),
):
    try:
        return await external_expert_validations.privacy_validate_processing_activity(
            raw_key=raw_key,
            case_id=case_id,
            activity_id=activity_id,
            **payload.model_dump(),
        )
    except (LookupError, PermissionError, ValueError) as exc:
        _translate(exc)


@router.post("/risk/cases/{case_id}/risks/{risk_id}/recommendations")
async def broker_record_recommendation(
    case_id: str,
    risk_id: str,
    payload: BrokerRecommendation,
    raw_key: str = Depends(_credential),
):
    try:
        return await external_expert_validations.broker_record_recommendation(
            raw_key=raw_key,
            case_id=case_id,
            risk_id=risk_id,
            **payload.model_dump(),
        )
    except (LookupError, PermissionError, ValueError) as exc:
        _translate(exc)


@router.post("/quality/cases/{case_id}/evidence/{evidence_id}/corrections")
async def quality_record_correction(
    case_id: str,
    evidence_id: str,
    payload: QualityCorrection,
    raw_key: str = Depends(_credential),
):
    try:
        return await external_expert_validations.quality_record_correction(
            raw_key=raw_key,
            case_id=case_id,
            evidence_id=evidence_id,
            **payload.model_dump(),
        )
    except (LookupError, PermissionError, ValueError) as exc:
        _translate(exc)
