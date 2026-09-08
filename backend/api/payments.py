"""ACA-0026 — real payment/funding runtime API.

`POST /payments/checkout` and `GET /payments/mine` require real
authenticated identity, same as every other domain router.
`POST /payments/webhook/stripe` is deliberately the one unauthenticated
route in this file — Stripe (like every real PSP) delivers webhooks
without a user session, authenticity comes from the signature check
inside `handle_stripe_webhook` instead, exactly as Stripe's own
integration guide requires.
"""

from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends, HTTPException, Request

from auth import get_current_user
from models import User
from payments import (
    CheckoutRequest,
    CheckoutSession,
    InvalidWebhookSignatureError,
    OfferNotFoundError,
    PaymentRecord,
    ProviderNotConfiguredError,
    create_checkout,
    handle_stripe_webhook,
    list_payments_for_user,
)

router = APIRouter(prefix="/payments", tags=["payments"])


@router.post("/checkout", response_model=CheckoutSession)
async def start_checkout(
    body: CheckoutRequest, current: User = Depends(get_current_user)
):
    """Creates a real checkout attempt against a real `commerce.
    catalog` offer. Returns a real, provider-issued `checkout_url` when
    a real payment provider is configured; when it isn't, this raises
    503 rather than returning a session with a fabricated or empty
    URL — `NO_FAKE_PAID_STATE` extends to "no fake checkout" too."""
    try:
        return await create_checkout(
            user_id=current.id,
            offer_id=body.offer_id,
            success_url=body.success_url,
            cancel_url=body.cancel_url,
        )
    except OfferNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ProviderNotConfiguredError as e:
        raise HTTPException(status_code=503, detail=str(e))


@router.get("/mine", response_model=List[PaymentRecord])
async def my_payments(current: User = Depends(get_current_user)):
    return await list_payments_for_user(current.id)


@router.post("/webhook/stripe")
async def stripe_webhook(request: Request):
    raw_body = await request.body()
    sig_header = request.headers.get("stripe-signature", "")
    try:
        await handle_stripe_webhook(raw_body, sig_header)
    except InvalidWebhookSignatureError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"received": True}
