"""Accounting control APIs for CVLN Academy."""

from __future__ import annotations

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from auth import require_role
from models import User
from services import accounting_core

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
    code: str
    starts_at: str
    ends_at: str


class MappingCreate(BaseModel):
    event_type: str
    debit_account: str
    credit_account: str
    tax_code: Optional[str] = None
    evidence_refs: List[str] = Field(default_factory=list)


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


@router.post("/periods/{period_id}/close")
async def close_period(period_id: str, current: User = Admin):
    try:
        return await accounting_core.close_period(actor_id=current.id, period_id=period_id)
    except LookupError as exc:
        _raise(exc)


@router.post("/mappings")
async def register_mapping(payload: MappingCreate, current: User = Admin):
    return await accounting_core.register_account_mapping(
        actor_id=current.id, **payload.model_dump()
    )


@router.get("/tax-preparation")
async def tax_preparation(current: User = Admin):
    return await accounting_core.tax_preparation_summary()
