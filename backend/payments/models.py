"""ACA-0026 — real payment/funding runtime models."""
from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Literal, Optional

from pydantic import BaseModel, Field

PaymentStatus = Literal["pending", "paid", "failed", "canceled", "refunded"]
PaymentProvider = Literal["stripe"]


def _uid() -> str:
    return str(uuid.uuid4())


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


class CheckoutSession(BaseModel):
    id: str = Field(default_factory=_uid)
    user_id: str
    offer_id: str
    formation_code: Optional[str] = None
    amount_eur: float
    currency: str = "EUR"
    provider: PaymentProvider = "stripe"
    provider_session_id: Optional[str] = None
    checkout_url: Optional[str] = None
    status: PaymentStatus = "pending"
    idempotency_key: str
    created_at: str = Field(default_factory=_now)
    updated_at: str = Field(default_factory=_now)


class PaymentRecord(BaseModel):
    id: str = Field(default_factory=_uid)
    checkout_session_id: str
    user_id: str
    offer_id: str
    formation_code: Optional[str] = None
    amount_eur: float
    currency: str = "EUR"
    provider: PaymentProvider = "stripe"
    status: PaymentStatus = "pending"
    provider_payment_intent_id: Optional[str] = None
    last_provider_event_id: Optional[str] = None
    created_at: str = Field(default_factory=_now)
    updated_at: str = Field(default_factory=_now)


class CheckoutRequest(BaseModel):
    offer_id: str
    formation_code: Optional[str] = None
    success_url: str
    cancel_url: str
