"""ACA-0026 payment runtime with Economy 3D line-level gating."""
from __future__ import annotations

import uuid
from typing import Optional

from commerce.catalog import get_offer
from db import db, utc_now_iso
from services.canonical_convergence import get_canonical_authority_map
from services.economy_runtime import evaluate_runtime_row, runtime_decisions

from .models import CheckoutSession, PaymentRecord
from .provider import (
    STRIPE_WEBHOOK_SECRET,
    create_remote_checkout_session,
    is_provider_configured,
    verify_stripe_webhook_signature,
)


class OfferNotFoundError(ValueError):
    pass


class EconomyPolicyBlockedError(ValueError):
    """The requested formation/offer combination is blocked by its Economy 3D row."""


class ProviderNotConfiguredError(RuntimeError):
    pass


async def _enforce_economy_policy(*, formation_code: str, offer_id: str) -> dict:
    authority = await get_canonical_authority_map()
    decisions = await runtime_decisions(
        db, [formation_code], canonicalized_codes=set(authority)
    )
    row = decisions.get(formation_code)
    if not row:
        raise EconomyPolicyBlockedError(
            f"Aucune ligne Economy 3D pour la formation {formation_code}."
        )
    base_runtime = row["runtime"]
    decision = evaluate_runtime_row(
        row,
        satisfied_gates=set(base_runtime.get("satisfied_gates", [])),
        offer_id=offer_id,
    )
    if not decision["sale_allowed"]:
        reasons = ", ".join(decision.get("reasons") or [decision.get("sale_reason", "BLOCKED")])
        missing = decision.get("missing_gates") or []
        suffix = f"; gates manquants={missing}" if missing else ""
        raise EconomyPolicyBlockedError(
            f"Economy 3D bloque {formation_code} avec {offer_id}: {reasons}{suffix}"
        )
    return decision


async def create_checkout(
    *,
    user_id: str,
    offer_id: str,
    success_url: str,
    cancel_url: str,
    formation_code: str | None = None,
) -> CheckoutSession:
    offer = get_offer(offer_id)
    if not offer:
        raise OfferNotFoundError(f"Offre inconnue: {offer_id}")

    economy_decision = None
    if formation_code:
        economy_decision = await _enforce_economy_policy(
            formation_code=formation_code, offer_id=offer_id
        )

    idempotency_key = uuid.uuid4().hex
    session = CheckoutSession(
        user_id=user_id,
        offer_id=offer_id,
        formation_code=formation_code,
        amount_eur=offer.price_eur,
        idempotency_key=idempotency_key,
    )
    session_doc = session.model_dump()
    if economy_decision:
        session_doc["economy_decision"] = economy_decision

    payment = PaymentRecord(
        checkout_session_id=session.id,
        user_id=user_id,
        offer_id=offer_id,
        formation_code=formation_code,
        amount_eur=offer.price_eur,
    )

    if not is_provider_configured():
        await db.payment_checkout_sessions.insert_one(session_doc)
        await db.payments.insert_one(payment.model_dump())
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
        session_doc = session.model_dump()
        if economy_decision:
            session_doc["economy_decision"] = economy_decision

    await db.payment_checkout_sessions.insert_one(session_doc)
    await db.payments.insert_one(payment.model_dump())
    return session


class InvalidWebhookSignatureError(ValueError):
    pass


async def handle_stripe_webhook(raw_body: bytes, sig_header: str) -> Optional[PaymentRecord]:
    if not STRIPE_WEBHOOK_SECRET:
        raise InvalidWebhookSignatureError(
            "STRIPE_WEBHOOK_SECRET non configuré — impossible de vérifier un webhook réel."
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
        return None
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
        {"$set": {
            "status": new_status,
            "provider_payment_intent_id": data_object.get("payment_intent"),
            "last_provider_event_id": event_id,
            "updated_at": now,
        }},
        return_document=True,
    )
    if not updated:
        return None
    return PaymentRecord(**{k: v for k, v in updated.items() if k != "_id"})


async def list_payments_for_user(user_id: str) -> list[PaymentRecord]:
    docs = await db.payments.find({"user_id": user_id}, {"_id": 0}).sort("created_at", -1).to_list(1000)
    return [PaymentRecord(**d) for d in docs]
