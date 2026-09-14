"""ACA-0026 — real payment/funding runtime. See `models.py`,
`provider.py`, `service.py` module docstrings for the `NO_FAKE_PAID_
STATE` discipline this package enforces on top of `commerce/`'s
existing DECIDED_V1 catalogue."""

from __future__ import annotations

from .models import CheckoutRequest, CheckoutSession, PaymentRecord, PaymentStatus
from .provider import is_provider_configured
from .service import (
    InvalidWebhookSignatureError,
    OfferNotFoundError,
    ProviderNotConfiguredError,
    create_checkout,
    handle_stripe_webhook,
    list_payments_for_user,
)

__all__ = [
    "CheckoutRequest",
    "CheckoutSession",
    "PaymentRecord",
    "PaymentStatus",
    "is_provider_configured",
    "InvalidWebhookSignatureError",
    "OfferNotFoundError",
    "ProviderNotConfiguredError",
    "create_checkout",
    "handle_stripe_webhook",
    "list_payments_for_user",
]
