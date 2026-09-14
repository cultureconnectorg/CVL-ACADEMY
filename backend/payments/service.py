"""ACA-0026 — real payment/funding runtime service layer.

Ties `commerce.catalog`'s real `DECIDED_V1` offers to a real checkout/
webhook lifecycle. See `models.py` and `provider.py` module docstrings
for the `NO_FAKE_PAID_STATE` discipline this layer enforces: only
`handle_stripe_webhook`, and only after a real signature verification,
may ever write `status="paid"`.
"""

from __future__ import annotations

import uuid
from typing import Optional

from commerce.catalog import get_offer
from db import db, utc_now_iso

from .models import CheckoutSession, PaymentRecord
from .provider import (
    create_remote_checkout_session,
    is_provider_configured,
    verify_stripe_webhook_signature,
    STRIPE_WEBHOOK_SECRET,
)


class OfferNotFoundError(ValueError):
    pass


class ProviderNotConfiguredError(RuntimeError):
    """Raised by `create_checkout` when no real payment provider is
    configured — the caller (api/payments.py) turns this into an
    honest 503, never a fabricated checkout URL."""


async def create_checkout(
    *, user_id: str, offer_id: str, success_url: str, cancel_url: str
) -> CheckoutSession:
    offer = get_offer(offer_id)
    if not offer:
        raise OfferNotFoundError(f"Offre inconnue: {offer_id}")

    idempotency_key = uuid.uuid4().hex
    session = CheckoutSession(
        user_id=user_id,
        offer_id=offer_id,
        amount_eur=offer.price_eur,
        idempotency_key=idempotency_key,
    )

    if not is_provider_configured():
        # Persist the attempt (real audit trail of "a checkout was
        # requested"), but never a fabricated checkout_url — the
        # caller must surface this as "payment provider not
        # configured", not a working link.
        await db.payment_checkout_sessions.insert_one(session.model_dump())
        await db.payments.insert_one(
            PaymentRecord(
                checkout_session_id=session.id,
                user_id=user_id,
                offer_id=offer_id,
                amount_eur=offer.price_eur,
            ).model_dump()
        )
        raise ProviderNotConfiguredError(
            "Aucun fournisseur de paiement réel configuré "
            "(STRIPE_SECRET_KEY/STRIPE_WEBHOOK_SECRET absents)."
        )

    remote = await create_remote_checkout_session(
        offer_id=offer_id,
        amount_eur=offer.price_eur,
        currency=session.currency,
        success_url=success_url,
        cancel_url=cancel_url,
        idempotency_key=idempotency_key,
    )
    if remote:
        session.provider_session_id = remote.get("id")
        session.checkout_url = remote.get("url")

    await db.payment_checkout_sessions.insert_one(session.model_dump())
    await db.payments.insert_one(
        PaymentRecord(
            checkout_session_id=session.id,
            user_id=user_id,
            offer_id=offer_id,
            amount_eur=offer.price_eur,
        ).model_dump()
    )
    return session


class InvalidWebhookSignatureError(ValueError):
    pass


async def handle_stripe_webhook(
    raw_body: bytes, sig_header: str
) -> Optional[PaymentRecord]:
    """Verifies the real Stripe signature, then processes exactly two
    real event types this integration needs
    (`checkout.session.completed`, `checkout.session.expired`) —
    anything else is acknowledged (so Stripe doesn't retry) but not
    acted on, since no other event maps to a `PaymentRecord`
    transition this codebase currently models."""
    if not STRIPE_WEBHOOK_SECRET:
        raise InvalidWebhookSignatureError(
            "STRIPE_WEBHOOK_SECRET non configuré — impossible de vérifier "
            "un webhook réel."
        )
    if not verify_stripe_webhook_signature(raw_body, sig_header, STRIPE_WEBHOOK_SECRET):
        raise InvalidWebhookSignatureError("Signature Stripe invalide.")

    import json

    event = json.loads(raw_body)
    event_id = event.get("id")
    event_type = event.get("type")
    data_object = (event.get("data") or {}).get("object") or {}
    provider_session_id = data_object.get("id")

    if event_type not in ("checkout.session.completed", "checkout.session.expired"):
        return None

    checkout_doc = await db.payment_checkout_sessions.find_one(
        {"provider_session_id": provider_session_id}
    )
    if not checkout_doc:
        # A real event for a session this process didn't create (or
        # already purged) — acknowledged, nothing to update.
        return None

    # Idempotent by provider event id: a retried delivery of the same
    # event must never re-process (Stripe's own documented "at least
    # once" delivery guarantee makes this a real, not hypothetical,
    # case). The unique index on (checkout_session_id,
    # last_provider_event_id) is NOT what enforces this — see
    # infra_indexes.py's own comment — this check is the actual guard;
    # the index only catches a genuine race between two concurrent
    # deliveries.
    existing = await db.payments.find_one(
        {"checkout_session_id": checkout_doc["id"], "last_provider_event_id": event_id}
    )
    if existing:
        return PaymentRecord(**{k: v for k, v in existing.items() if k != "_id"})

    new_status = "paid" if event_type == "checkout.session.completed" else "canceled"
    now = utc_now_iso()
    await db.payment_checkout_sessions.update_one(
        {"id": checkout_doc["id"]}, {"$set": {"status": new_status, "updated_at": now}}
    )
    updated = await db.payments.find_one_and_update(
        {"checkout_session_id": checkout_doc["id"]},
        {
            "$set": {
                "status": new_status,
                "provider_payment_intent_id": data_object.get("payment_intent"),
                "last_provider_event_id": event_id,
                "updated_at": now,
            }
        },
        return_document=True,
    )
    if not updated:
        return None
    return PaymentRecord(**{k: v for k, v in updated.items() if k != "_id"})


async def list_payments_for_user(user_id: str) -> list[PaymentRecord]:
    docs = (
        await db.payments.find({"user_id": user_id}, {"_id": 0})
        .sort("created_at", -1)
        .to_list(1000)
    )
    return [PaymentRecord(**d) for d in docs]
