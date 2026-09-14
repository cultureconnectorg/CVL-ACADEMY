"""ACA-0026 — real payment/funding runtime models.

**Unblocking ACA-0026 correctly does not mean fabricating a working
Stripe/PSP connection this sandbox has no credentials for.** It means
the same "ready but decoupled" discipline `services/frek_core.py`/
`services/agent_factory.py` already established: a real, typed
provider interface + real request/webhook plumbing, gated behind an
env var, that does nothing dishonest when unconfigured. See
`provider.py`'s own docstring for the one hard rule this domain adds
on top of that pattern that FrekCore's own local fallback does NOT
need: `commerce/models.py`'s `NO_FAKE_PAID_STATE` gate (BIN-021/022)
still holds here — nothing in this package may ever mark a
`PaymentRecord` `"paid"` except a real, signature-verified webhook
event from a real, configured provider. There is no local-fallback
"succeeds anyway" path for the actual charge, unlike FrekCore's own
`mint_frek_id`/`issue_proof`, precisely because a payment's local
fallback succeeding would BE the fake paid state the gate forbids.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Literal, Optional

from pydantic import BaseModel, Field

# "pending" -> created, provider not yet confirmed the charge.
# "paid" -> ONLY ever set by handle_stripe_webhook after a real,
#   signature-verified checkout.session.completed event.
# "failed" / "canceled" -> real provider-reported terminal states.
# "refunded" -> a real, later charge.refunded event.
PaymentStatus = Literal["pending", "paid", "failed", "canceled", "refunded"]

PaymentProvider = Literal["stripe"]


def _uid() -> str:
    return str(uuid.uuid4())


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


class CheckoutSession(BaseModel):
    """One real attempt to pay for one real `CommercialOffer`
    (`commerce.catalog`). `checkout_url` is only ever populated by a
    real provider response (`provider.create_remote_checkout_session`)
    — `None` when the provider isn't configured or the remote call
    failed, never a fabricated placeholder URL."""

    id: str = Field(default_factory=_uid)
    user_id: str
    offer_id: str
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
    """The real, authoritative record of what a provider actually
    confirmed. One `PaymentRecord` per `CheckoutSession` — created
    `"pending"` alongside the session, transitioned to a terminal
    status only by `handle_stripe_webhook`."""

    id: str = Field(default_factory=_uid)
    checkout_session_id: str
    user_id: str
    offer_id: str
    amount_eur: float
    currency: str = "EUR"
    provider: PaymentProvider = "stripe"
    status: PaymentStatus = "pending"
    provider_payment_intent_id: Optional[str] = None
    # The provider's own event id (Stripe: evt_...) — the real
    # idempotency anchor for webhook processing: a provider that
    # retries a delivery (its own documented behavior on a timeout or
    # a non-2xx response) must never be double-processed, so this is
    # stored with a unique index (see service.py) and a repeat event
    # id is a no-op, not a re-credit.
    last_provider_event_id: Optional[str] = None
    created_at: str = Field(default_factory=_now)
    updated_at: str = Field(default_factory=_now)


class CheckoutRequest(BaseModel):
    offer_id: str
    success_url: str
    cancel_url: str
