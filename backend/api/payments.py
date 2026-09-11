"""ACA-0026 — payment API with Economy 3D transaction gates."""
from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends, HTTPException, Request

from auth import get_current_user
from models import User
from payments import (
    CheckoutRequest,
    CheckoutSession,
    EconomyPolicyBlockedError,
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
async def start_checkout(body: CheckoutRequest, current: User = Depends(get_current_user)):
    try:
        return await create_checkout(
            user_id=current.id,
            offer_id=body.offer_id,
            formation_code=body.formation_code,
            success_url=body.success_url,
            cancel_url=body.cancel_url,
        )
    except OfferNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except EconomyPolicyBlockedError as exc:
        # 409: the requested commercial action conflicts with the canonical
        # Economy 3D state/gates; this is not an authentication failure.
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    except ProviderNotConfiguredError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc


@router.get("/mine", response_model=List[PaymentRecord])
async def my_payments(current: User = Depends(get_current_user)):
    return await list_payments_for_user(current.id)


@router.post("/webhook/stripe")
async def stripe_webhook(request: Request):
    raw_body = await request.body()
    sig_header = request.headers.get("stripe-signature", "")
    try:
        await handle_stripe_webhook(raw_body, sig_header)
    except InvalidWebhookSignatureError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"received": True}
