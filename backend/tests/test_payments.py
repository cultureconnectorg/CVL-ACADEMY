"""ACA-0026 — real payment/funding runtime tests.

The one thing every test in this file ultimately proves, one way or
another: `NO_FAKE_PAID_STATE` holds. No code path in `payments/`
outside a real, signature-verified webhook can ever produce a `"paid"`
status."""

from __future__ import annotations

import json
import time

import pytest
from mongomock_motor import AsyncMongoMockClient

import payments.provider as provider_module
import payments.service as service_module
from payments.provider import (
    sign_stripe_payload,
    verify_stripe_webhook_signature,
)
from payments.service import (
    InvalidWebhookSignatureError,
    OfferNotFoundError,
    ProviderNotConfiguredError,
    create_checkout,
    handle_stripe_webhook,
    list_payments_for_user,
)

WEBHOOK_SECRET = "whsec_test_secret_1234567890"


# ---------------- webhook signature verification (real algorithm) ----------------


def test_valid_signature_verifies():
    body = b'{"id":"evt_1","type":"checkout.session.completed"}'
    sig = sign_stripe_payload(body, WEBHOOK_SECRET)
    assert verify_stripe_webhook_signature(body, sig, WEBHOOK_SECRET) is True


def test_tampered_body_fails_verification():
    body = b'{"id":"evt_1","type":"checkout.session.completed"}'
    sig = sign_stripe_payload(body, WEBHOOK_SECRET)
    tampered = body.replace(b"evt_1", b"evt_2")
    assert verify_stripe_webhook_signature(tampered, sig, WEBHOOK_SECRET) is False


def test_wrong_secret_fails_verification():
    body = b'{"id":"evt_1"}'
    sig = sign_stripe_payload(body, WEBHOOK_SECRET)
    assert verify_stripe_webhook_signature(body, sig, "whsec_wrong") is False


def test_expired_timestamp_fails_verification():
    body = b'{"id":"evt_1"}'
    old_ts = int(time.time()) - 10_000
    sig = sign_stripe_payload(body, WEBHOOK_SECRET, timestamp=old_ts)
    assert verify_stripe_webhook_signature(body, sig, WEBHOOK_SECRET) is False


def test_malformed_header_fails_verification():
    body = b'{"id":"evt_1"}'
    assert verify_stripe_webhook_signature(body, "garbage", WEBHOOK_SECRET) is False
    assert verify_stripe_webhook_signature(body, "", WEBHOOK_SECRET) is False


def test_multiple_v1_signatures_any_match_passes():
    """Real Stripe behavior during a signing-secret rotation: more than
    one v1= value in the header, any match is accepted."""
    body = b'{"id":"evt_1"}'
    ts = int(time.time())
    real_sig = sign_stripe_payload(body, WEBHOOK_SECRET, timestamp=ts).split("v1=")[1]
    header = f"t={ts},v1=deadbeef,v1={real_sig}"
    assert verify_stripe_webhook_signature(body, header, WEBHOOK_SECRET) is True


# ---------------- checkout creation ----------------


@pytest.fixture
async def payments_db(monkeypatch):
    client = AsyncMongoMockClient()
    mock_db = client["cvln_aca0026_payments_test"]
    monkeypatch.setattr(service_module, "db", mock_db)
    return mock_db


@pytest.mark.asyncio
async def test_checkout_raises_offer_not_found(payments_db):
    with pytest.raises(OfferNotFoundError):
        await create_checkout(
            user_id="u1",
            offer_id="does-not-exist",
            success_url="https://example.test/ok",
            cancel_url="https://example.test/cancel",
        )


@pytest.mark.asyncio
async def test_checkout_raises_provider_not_configured_when_unset(
    payments_db, monkeypatch
):
    """The critical NO_FAKE_PAID_STATE / no-fake-checkout proof: with no
    STRIPE_SECRET_KEY/STRIPE_WEBHOOK_SECRET set, create_checkout must
    refuse rather than return a session with a fabricated URL."""
    monkeypatch.setattr(provider_module, "STRIPE_SECRET_KEY", None)
    monkeypatch.setattr(provider_module, "STRIPE_WEBHOOK_SECRET", None)
    with pytest.raises(ProviderNotConfiguredError):
        await create_checkout(
            user_id="u1",
            offer_id="academy-access",
            success_url="https://example.test/ok",
            cancel_url="https://example.test/cancel",
        )
    # The attempt is still recorded as a real fact, but never as paid.
    stored = await payments_db.payment_checkout_sessions.find_one({"user_id": "u1"})
    assert stored is not None
    assert stored["status"] == "pending"
    assert stored["checkout_url"] is None


@pytest.mark.asyncio
async def test_checkout_succeeds_with_real_provider_response(payments_db, monkeypatch):
    monkeypatch.setattr(provider_module, "STRIPE_SECRET_KEY", "sk_test_x")
    monkeypatch.setattr(provider_module, "STRIPE_WEBHOOK_SECRET", WEBHOOK_SECRET)
    monkeypatch.setattr(service_module, "STRIPE_WEBHOOK_SECRET", WEBHOOK_SECRET)

    async def fake_remote(**kwargs):
        return {"id": "cs_test_123", "url": "https://checkout.stripe.com/cs_test_123"}

    monkeypatch.setattr(service_module, "create_remote_checkout_session", fake_remote)

    session = await create_checkout(
        user_id="u1",
        offer_id="academy-access",
        success_url="https://example.test/ok",
        cancel_url="https://example.test/cancel",
    )
    assert session.provider_session_id == "cs_test_123"
    assert session.checkout_url == "https://checkout.stripe.com/cs_test_123"
    assert session.status == "pending"  # still pending -- only a webhook can pay it


# ---------------- webhook processing ----------------


async def _seed_checkout(mock_db, *, provider_session_id="cs_test_abc"):
    from payments.models import CheckoutSession, PaymentRecord

    session = CheckoutSession(
        user_id="u1",
        offer_id="academy-access",
        amount_eur=24.90,
        provider_session_id=provider_session_id,
        idempotency_key="idem-1",
    )
    await mock_db.payment_checkout_sessions.insert_one(session.model_dump())
    record = PaymentRecord(
        checkout_session_id=session.id,
        user_id="u1",
        offer_id="academy-access",
        amount_eur=24.90,
    )
    await mock_db.payments.insert_one(record.model_dump())
    return session


@pytest.mark.asyncio
async def test_webhook_rejects_invalid_signature(payments_db, monkeypatch):
    monkeypatch.setattr(service_module, "STRIPE_WEBHOOK_SECRET", WEBHOOK_SECRET)
    body = b'{"id":"evt_1","type":"checkout.session.completed","data":{"object":{}}}'
    with pytest.raises(InvalidWebhookSignatureError):
        await handle_stripe_webhook(body, "t=1,v1=notreal")


@pytest.mark.asyncio
async def test_webhook_marks_payment_paid_on_real_verified_event(
    payments_db, monkeypatch
):
    monkeypatch.setattr(service_module, "STRIPE_WEBHOOK_SECRET", WEBHOOK_SECRET)
    session = await _seed_checkout(payments_db)

    event = {
        "id": "evt_real_1",
        "type": "checkout.session.completed",
        "data": {
            "object": {
                "id": session.provider_session_id,
                "payment_intent": "pi_test_1",
            }
        },
    }
    body = json.dumps(event).encode()
    sig = sign_stripe_payload(body, WEBHOOK_SECRET)

    record = await handle_stripe_webhook(body, sig)
    assert record is not None
    assert record.status == "paid"
    assert record.provider_payment_intent_id == "pi_test_1"

    stored_session = await payments_db.payment_checkout_sessions.find_one(
        {"id": session.id}
    )
    assert stored_session["status"] == "paid"


@pytest.mark.asyncio
async def test_webhook_expired_session_marks_canceled_not_paid(
    payments_db, monkeypatch
):
    monkeypatch.setattr(service_module, "STRIPE_WEBHOOK_SECRET", WEBHOOK_SECRET)
    session = await _seed_checkout(payments_db, provider_session_id="cs_expired")

    event = {
        "id": "evt_real_2",
        "type": "checkout.session.expired",
        "data": {"object": {"id": session.provider_session_id}},
    }
    body = json.dumps(event).encode()
    sig = sign_stripe_payload(body, WEBHOOK_SECRET)

    record = await handle_stripe_webhook(body, sig)
    assert record.status == "canceled"


@pytest.mark.asyncio
async def test_webhook_is_idempotent_on_replayed_event(payments_db, monkeypatch):
    """Stripe's own documented 'at least once' delivery guarantee means
    a real duplicate delivery of the same event id is a real case, not
    a hypothetical one -- must never double-process."""
    monkeypatch.setattr(service_module, "STRIPE_WEBHOOK_SECRET", WEBHOOK_SECRET)
    session = await _seed_checkout(payments_db, provider_session_id="cs_dup")

    event = {
        "id": "evt_dup_1",
        "type": "checkout.session.completed",
        "data": {
            "object": {"id": session.provider_session_id, "payment_intent": "pi_1"}
        },
    }
    body = json.dumps(event).encode()
    sig = sign_stripe_payload(body, WEBHOOK_SECRET)

    first = await handle_stripe_webhook(body, sig)
    second = await handle_stripe_webhook(body, sig)
    assert first.status == "paid"
    assert second.status == "paid"
    assert first.id == second.id

    count = await payments_db.payments.count_documents(
        {"checkout_session_id": session.id}
    )
    assert count == 1


@pytest.mark.asyncio
async def test_webhook_for_unknown_session_is_a_noop(payments_db, monkeypatch):
    monkeypatch.setattr(service_module, "STRIPE_WEBHOOK_SECRET", WEBHOOK_SECRET)
    event = {
        "id": "evt_unknown",
        "type": "checkout.session.completed",
        "data": {"object": {"id": "cs_never_created"}},
    }
    body = json.dumps(event).encode()
    sig = sign_stripe_payload(body, WEBHOOK_SECRET)
    result = await handle_stripe_webhook(body, sig)
    assert result is None


@pytest.mark.asyncio
async def test_webhook_ignores_unhandled_event_types(payments_db, monkeypatch):
    monkeypatch.setattr(service_module, "STRIPE_WEBHOOK_SECRET", WEBHOOK_SECRET)
    event = {"id": "evt_other", "type": "customer.created", "data": {"object": {}}}
    body = json.dumps(event).encode()
    sig = sign_stripe_payload(body, WEBHOOK_SECRET)
    result = await handle_stripe_webhook(body, sig)
    assert result is None


@pytest.mark.asyncio
async def test_list_payments_for_user(payments_db):
    await _seed_checkout(payments_db, provider_session_id="cs_list_1")
    payments = await list_payments_for_user("u1")
    assert len(payments) == 1
    assert payments[0].status == "pending"
