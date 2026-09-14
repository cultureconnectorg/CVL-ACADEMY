"""Advanced accounting API for evidence-first operational controls."""

from __future__ import annotations

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from auth import require_role
from models import User
from services import accounting_advanced

router = APIRouter(prefix="/accounting-advanced", tags=["accounting"])
Admin = Depends(require_role("admin", "super_admin", "founder"))


class AccountingEntityCreate(BaseModel):
    code: str = Field(min_length=1, max_length=80)
    legal_name: str = Field(min_length=2, max_length=240)
    registration_ref: str = Field(min_length=2, max_length=240)
    invoice_prefix: str = Field(min_length=1, max_length=20)
    evidence_refs: List[str] = Field(min_length=1)


class InvoiceEntityBind(BaseModel):
    entity_id: str = Field(min_length=1, max_length=240)
    evidence_refs: List[str] = Field(min_length=1)


class SupportingDocumentCreate(BaseModel):
    document_type: str = Field(min_length=2, max_length=80)
    document_ref: str = Field(min_length=1, max_length=500)
    content_hash: str = Field(min_length=64, max_length=64)
    vendor_id: Optional[str] = Field(default=None, max_length=240)
    invoice_id: Optional[str] = Field(default=None, max_length=240)
    period_id: Optional[str] = Field(default=None, max_length=240)
    amount_cents: Optional[int] = Field(default=None, ge=0)
    evidence_refs: List[str] = Field(min_length=1)


class ConnectorCreate(BaseModel):
    connector_type: str = Field(min_length=2, max_length=80)
    provider_name: str = Field(min_length=2, max_length=240)
    account_ref: str = Field(min_length=1, max_length=240)
    mode: str = Field(min_length=2, max_length=40)
    evidence_refs: List[str] = Field(min_length=1)


class CostLineCreate(BaseModel):
    cost_type: str = Field(min_length=2, max_length=120)
    amount_cents: int = Field(ge=0)
    source_ref: str = Field(min_length=1, max_length=500)
    formation_code: Optional[str] = None
    cohort_id: Optional[str] = None
    pole: Optional[str] = None
    entity_id: Optional[str] = None
    learner_id: Optional[str] = None
    expert_id: Optional[str] = None
    period_id: Optional[str] = None
    evidence_refs: List[str] = Field(min_length=1)


class RevenueLineCreate(BaseModel):
    amount_cents: int = Field(ge=0)
    source_ref: str = Field(min_length=1, max_length=500)
    formation_code: Optional[str] = None
    cohort_id: Optional[str] = None
    pole: Optional[str] = None
    entity_id: Optional[str] = None
    learner_id: Optional[str] = None
    period_id: Optional[str] = None
    evidence_refs: List[str] = Field(min_length=1)


class TaxPackageCreate(BaseModel):
    policy_version_id: str = Field(min_length=1, max_length=240)
    evidence_refs: List[str] = Field(min_length=1)


def _raise(exc: Exception):
    status = 404 if isinstance(exc, LookupError) else 422
    raise HTTPException(status_code=status, detail=str(exc)) from exc


@router.post("/entities")
async def create_entity(payload: AccountingEntityCreate, current: User = Admin):
    try:
        return await accounting_advanced.register_accounting_entity(
            actor_id=current.id, **payload.model_dump()
        )
    except ValueError as exc:
        _raise(exc)


@router.post("/invoices/{invoice_id}/entity")
async def bind_invoice_entity(
    invoice_id: str, payload: InvoiceEntityBind, current: User = Admin
):
    try:
        return await accounting_advanced.attach_invoice_entity(
            actor_id=current.id,
            invoice_id=invoice_id,
            **payload.model_dump(),
        )
    except (LookupError, ValueError) as exc:
        _raise(exc)


@router.post("/supporting-documents")
async def supporting_document(
    payload: SupportingDocumentCreate, current: User = Admin
):
    try:
        return await accounting_advanced.register_supporting_document(
            actor_id=current.id, **payload.model_dump()
        )
    except (LookupError, ValueError) as exc:
        _raise(exc)


@router.post("/connectors")
async def create_connector(payload: ConnectorCreate, current: User = Admin):
    try:
        return await accounting_advanced.register_connector(
            actor_id=current.id, **payload.model_dump()
        )
    except ValueError as exc:
        _raise(exc)


@router.post("/cost-lines")
async def cost_line(payload: CostLineCreate, current: User = Admin):
    try:
        return await accounting_advanced.record_cost_line(
            actor_id=current.id, **payload.model_dump()
        )
    except ValueError as exc:
        _raise(exc)


@router.post("/revenue-lines")
async def revenue_line(payload: RevenueLineCreate, current: User = Admin):
    try:
        return await accounting_advanced.record_revenue_line(
            actor_id=current.id, **payload.model_dump()
        )
    except ValueError as exc:
        _raise(exc)


@router.get("/profitability")
async def profitability(
    formation_code: Optional[str] = None,
    cohort_id: Optional[str] = None,
    pole: Optional[str] = None,
    entity_id: Optional[str] = None,
    learner_id: Optional[str] = None,
    expert_id: Optional[str] = None,
    period_id: Optional[str] = None,
    current: User = Admin,
):
    return await accounting_advanced.profitability_summary(
        formation_code=formation_code,
        cohort_id=cohort_id,
        pole=pole,
        entity_id=entity_id,
        learner_id=learner_id,
        expert_id=expert_id,
        period_id=period_id,
    )


@router.post("/periods/{period_id}/tax-package")
async def tax_package(
    period_id: str, payload: TaxPackageCreate, current: User = Admin
):
    try:
        return await accounting_advanced.prepare_tax_package(
            actor_id=current.id,
            period_id=period_id,
            **payload.model_dump(),
        )
    except (LookupError, ValueError) as exc:
        _raise(exc)


@router.get("/periods/{period_id}/export.csv")
async def period_csv(period_id: str, current: User = Admin):
    try:
        return await accounting_advanced.export_period_csv(period_id)
    except LookupError as exc:
        _raise(exc)
