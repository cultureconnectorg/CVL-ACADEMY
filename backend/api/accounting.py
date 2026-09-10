"""Accounting control APIs for CVLN Academy."""

from __future__ import annotations

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from auth import require_role
from models import User
from services import accounting_core, accounting_mappings

router = APIRouter(prefix="/accounting", tags=["accounting"])
Admin = Depends(require_role("admin", "super_admin", "founder"))


class InvoiceCreate(BaseModel):
    payment_id: str
    issuer_name: str
    customer_name: str
    customer_address: Optional[str] = None


class CreditNoteCreate(BaseModel):
    invoice_id: str
    amount_cents: int = Field(gt=0)
    reason: str = Field(min_length=3, max_length=2000)


class Allocation(BaseModel):
    beneficiary: str
    amount_cents: int = Field(ge=0)
    reference: Optional[str] = None


class RevenueSplitCreate(BaseModel):
    source_type: str
    source_id: str
    amount_cents: int = Field(gt=0)
    allocations: List[Allocation] = Field(min_length=1)


class PeriodCreate(BaseModel):
    code: str = Field(min_length=1, max_length=80)
    starts_at: str
    ends_at: str


class PeriodClose(BaseModel):
    review_note: str = Field(min_length=3, max_length=4000)
    evidence_refs: List[str] = Field(min_length=1)


class PeriodAnomalyCreate(BaseModel):
    code: str = Field(min_length=2, max_length=120)
    description: str = Field(min_length=3, max_length=4000)
    evidence_refs: List[str] = Field(min_length=1)


class PeriodAnomalyResolve(BaseModel):
    resolution: str = Field(min_length=3, max_length=4000)
    evidence_refs: List[str] = Field(min_length=1)


class MappingCreate(BaseModel):
    event_type: str
    debit_account: str
    credit_account: str
    version: str = Field(min_length=1, max_length=80)
    effective_at: str = Field(min_length=10, max_length=64)
    tax_code: Optional[str] = None
    evidence_refs: List[str] = Field(min_length=1)
    supersedes_version_id: Optional[str] = None


def _raise(exc: Exception):
    status = 404 if isinstance(exc, LookupError) else 422
    raise HTTPException(status_code=status, detail=str(exc)) from exc


@router.post("/invoices")
async def create_invoice(payload: InvoiceCreate, current: User = Admin):
    try:
        return await accounting_core.create_invoice_from_payment(
            actor_id=current.id, **payload.model_dump()
        )
    except (LookupError, ValueError) as exc:
        _raise(exc)


@router.post("/credit-notes")
async def create_credit_note(payload: CreditNoteCreate, current: User = Admin):
    try:
        return await accounting_core.create_credit_note(
            actor_id=current.id, **payload.model_dump()
        )
    except (LookupError, ValueError) as exc:
        _raise(exc)


@router.post("/revenue-splits")
async def create_revenue_split(payload: RevenueSplitCreate, current: User = Admin):
    try:
        return await accounting_core.create_revenue_split(
            actor_id=current.id,
            source_type=payload.source_type,
            source_id=payload.source_id,
            amount_cents=payload.amount_cents,
            allocations=[row.model_dump() for row in payload.allocations],
        )
    except ValueError as exc:
        _raise(exc)


@router.post("/reconciliation/payments/{payment_id}")
async def reconcile_payment(payment_id: str, current: User = Admin):
    try:
        return await accounting_core.reconcile_payment(
            actor_id=current.id, payment_id=payment_id
        )
    except LookupError as exc:
        _raise(exc)


@router.post("/periods")
async def create_period(payload: PeriodCreate, current: User = Admin):
    try:
        return await accounting_core.create_period(actor_id=current.id, **payload.model_dump())
    except ValueError as exc:
        _raise(exc)


@router.get("/periods/{period_id}/close-gate")
async def get_period_close_gate(period_id: str, current: User = Admin):
    try:
        return await accounting_core.period_close_gate(period_id)
    except LookupError as exc:
        _raise(exc)


@router.post("/periods/{period_id}/anomalies")
async def create_period_anomaly(
    period_id: str, payload: PeriodAnomalyCreate, current: User = Admin
):
    try:
        return await accounting_core.create_period_anomaly(
            actor_id=current.id, period_id=period_id, **payload.model_dump()
        )
    except (LookupError, ValueError) as exc:
        _raise(exc)


@router.patch("/period-anomalies/{anomaly_id}/resolve")
async def resolve_period_anomaly(
    anomaly_id: str, payload: PeriodAnomalyResolve, current: User = Admin
):
    try:
        return await accounting_core.resolve_period_anomaly(
            actor_id=current.id, anomaly_id=anomaly_id, **payload.model_dump()
        )
    except (LookupError, ValueError) as exc:
        _raise(exc)


@router.post("/periods/{period_id}/close")
async def close_period(period_id: str, payload: PeriodClose, current: User = Admin):
    try:
        return await accounting_core.close_period(
            actor_id=current.id, period_id=period_id, **payload.model_dump()
        )
    except (LookupError, ValueError) as exc:
        _raise(exc)


@router.post("/mappings")
async def register_mapping(payload: MappingCreate, current: User = Admin):
    try:
        return await accounting_mappings.register_mapping_version(
            actor_id=current.id, **payload.model_dump()
        )
    except (LookupError, ValueError) as exc:
        _raise(exc)


@router.get("/mappings/{event_type}")
async def get_mapping(event_type: str, current: User = Admin):
    try:
        return await accounting_mappings.get_mapping(event_type)
    except (LookupError, ValueError) as exc:
        _raise(exc)


@router.get("/mappings/{event_type}/history")
async def mapping_history(event_type: str, current: User = Admin):
    return await accounting_mappings.list_mapping_history(event_type)


@router.get("/tax-preparation")
async def tax_preparation(current: User = Admin):
    return await accounting_core.tax_preparation_summary()
