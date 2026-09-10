"""Accounting protocol APIs (ACC-05/06/16/18/21)."""

from __future__ import annotations

from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from auth import require_role
from models import User
from services import accounting_protocols

router = APIRouter(prefix="/accounting-protocols", tags=["accounting"])
Admin = Depends(require_role("admin", "super_admin", "founder"))

class RefundEventCreate(BaseModel):
    refund_ref: str
    payment_id: str
    amount_cents: int = Field(gt=0)
    currency: str = "EUR"
    evidence_refs: List[str] = Field(min_length=1)
    credit_note_id: Optional[str] = None

class RevenueRecognitionCreate(BaseModel):
    source_ref: str
    amount_cents: int = Field(ge=0)
    currency: str = "EUR"
    recognition_date: str
    policy_version_id: str
    dimensions: Dict[str, Any] = Field(default_factory=dict)
    evidence_refs: List[str] = Field(min_length=1)

class MissingDocumentCreate(BaseModel):
    period_id: str
    expected_document_type: str
    source_ref: str
    owner: str
    due_at: str
    evidence_refs: List[str] = Field(min_length=1)

class MissingDocumentResolve(BaseModel):
    supporting_document_id: str
    evidence_refs: List[str] = Field(min_length=1)

class RetentionPolicyCreate(BaseModel):
    record_type: str
    retention_days: int = Field(ge=0)
    trigger: str
    policy_version_id: str
    evidence_refs: List[str] = Field(min_length=1)


def _raise(exc: Exception):
    status = 404 if isinstance(exc, LookupError) else 422
    raise HTTPException(status_code=status, detail=str(exc)) from exc

@router.post("/refund-events")
async def refund_event(payload: RefundEventCreate, current: User = Admin):
    try: return await accounting_protocols.record_refund_accounting_event(actor_id=current.id, **payload.model_dump())
    except (LookupError, ValueError) as exc: _raise(exc)

@router.post("/revenue-recognition")
async def revenue_recognition(payload: RevenueRecognitionCreate, current: User = Admin):
    try: return await accounting_protocols.prepare_revenue_recognition(actor_id=current.id, **payload.model_dump())
    except (LookupError, ValueError) as exc: _raise(exc)

@router.post("/missing-documents")
async def missing_document(payload: MissingDocumentCreate, current: User = Admin):
    try: return await accounting_protocols.register_missing_supporting_document(actor_id=current.id, **payload.model_dump())
    except (LookupError, ValueError) as exc: _raise(exc)

@router.post("/missing-documents/{missing_document_id}/resolve")
async def resolve_missing_document(missing_document_id: str, payload: MissingDocumentResolve, current: User = Admin):
    try: return await accounting_protocols.resolve_missing_supporting_document(actor_id=current.id, missing_document_id=missing_document_id, **payload.model_dump())
    except (LookupError, ValueError) as exc: _raise(exc)

@router.get("/periods/{period_id}/fec-readiness")
async def fec_readiness(period_id: str, current: User = Admin):
    try: return await accounting_protocols.fec_readiness_gate(period_id=period_id)
    except (LookupError, ValueError) as exc: _raise(exc)

@router.post("/retention")
async def retention(payload: RetentionPolicyCreate, current: User = Admin):
    try: return await accounting_protocols.register_financial_retention_policy(actor_id=current.id, **payload.model_dump())
    except (LookupError, ValueError) as exc: _raise(exc)
