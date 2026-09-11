"""Academy commercial runtime: Economy 3D -> order -> CVLN Wallet -> entitlement."""

from __future__ import annotations

import uuid

import httpx
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from pymongo import ReturnDocument

from auth import get_current_user
from billing import build_invoice_intent
from commercial import (
    CommercialPolicyError,
    EligibilityRequired,
    NotForSale,
    QuoteRequired,
    amount_eur_to_jcc,
    entitlement_filter,
    resolve_offer,
)
from db import db, utc_now_iso
from models import User
from services.cvln_wallet import (
    CVLNWalletAmbiguousResult,
    CVLNWalletNotConfigured,
    cvln_wallet,
)

router = APIRouter(prefix="/commercial", tags=["commercial"])


class OrderCreate(BaseModel):
    economy_code: str
    offer_kind: str = "path"


def _policy_http_error(exc: Exception) -> HTTPException:
    if isinstance(exc, NotForSale):
        return HTTPException(status_code=409, detail="NOT_FOR_SALE")
    if isinstance(exc, QuoteRequired):
        return HTTPException(status_code=409, detail="QUOTE_REQUIRED")
    if isinstance(exc, EligibilityRequired):
        return HTTPException(status_code=409, detail="ELIGIBILITY_REQUIRED")
    if isinstance(exc, KeyError):
        return HTTPException(status_code=404, detail="ECONOMY_CODE_NOT_FOUND")
    return HTTPException(status_code=409, detail=str(exc))


@router.get("/wallet-status")
async def wallet_status(current: User = Depends(get_current_user)):
    del current
    return cvln_wallet.describe()


@router.get("/offers/{economy_code}")
async def get_offer(
    economy_code: str,
    offer_kind: str = "path",
    current: User = Depends(get_current_user),
):
    del current
    try:
        return resolve_offer(economy_code, offer_kind)
    except (CommercialPolicyError, KeyError) as exc:
        raise _policy_http_error(exc) from exc


@router.post("/orders")
async def create_order(inp: OrderCreate, current: User = Depends(get_current_user)):
    try:
        offer = resolve_offer(inp.economy_code, inp.offer_kind)
    except (CommercialPolicyError, KeyError) as exc:
        raise _policy_http_error(exc) from exc

    try:
        wallet_entity = await cvln_wallet.entity_info()
    except CVLNWalletNotConfigured as exc:
        raise HTTPException(
            status_code=503, detail="CVLN_WALLET_NOT_CONFIGURED"
        ) from exc
    except CVLNWalletAmbiguousResult as exc:
        raise HTTPException(status_code=503, detail="CVLN_WALLET_UNAVAILABLE") from exc
    except httpx.HTTPStatusError as exc:
        raise HTTPException(
            status_code=502, detail="CVLN_WALLET_REJECTED_ENTITY_AUTH"
        ) from exc

    rate_eur = float(wallet_entity.get("rate_eur", 0))
    amount_jcc = amount_eur_to_jcc(float(offer["amount_eur"]), rate_eur)
    now = utc_now_iso()
    order = {
        "order_id": f"ord_{uuid.uuid4().hex[:16]}",
        "user_id": current.id,
        "user_frek_id": current.frek_id,
        "economy_code": offer["economy_code"],
        "economy_requirement_id": offer["requirement_id"],
        "offer_kind": offer["offer_kind"],
        "amount_eur": offer["amount_eur"],
        "currency": "EUR",
        "wallet_asset": "JCC",
        "wallet_rate_eur_per_jcc": rate_eur,
        "wallet_amount_jcc": amount_jcc,
        "wallet_entity_id": wallet_entity.get("entity_id"),
        "pricing_snapshot": offer,
        "status": "PENDING_PAYMENT",
        "payment_attempt_id": None,
        "wallet_response": None,
        "created_at": now,
        "updated_at": now,
        "paid_at": None,
    }
    await db.commercial_orders.insert_one(dict(order))
    return order


@router.get("/orders/{order_id}")
async def get_order(order_id: str, current: User = Depends(get_current_user)):
    order = await db.commercial_orders.find_one(
        {"order_id": order_id, "user_id": current.id}, {"_id": 0}
    )
    if not order:
        raise HTTPException(status_code=404, detail="ORDER_NOT_FOUND")
    return order


@router.post("/orders/{order_id}/pay-wallet")
async def pay_order_with_wallet(
    order_id: str, current: User = Depends(get_current_user)
):
    attempt_id = f"pay_{uuid.uuid4().hex[:16]}"
    now = utc_now_iso()

    order = await db.commercial_orders.find_one_and_update(
        {
            "order_id": order_id,
            "user_id": current.id,
            "status": "PENDING_PAYMENT",
        },
        {
            "$set": {
                "status": "PAYMENT_PROCESSING",
                "payment_attempt_id": attempt_id,
                "updated_at": now,
            }
        },
        return_document=ReturnDocument.AFTER,
    )
    if not order:
        existing = await db.commercial_orders.find_one(
            {"order_id": order_id, "user_id": current.id}, {"_id": 0}
        )
        if not existing:
            raise HTTPException(status_code=404, detail="ORDER_NOT_FOUND")
        if existing.get("status") == "PAID":
            return existing
        if existing.get("status") in {"PAYMENT_PROCESSING", "REQUIRES_REVIEW"}:
            raise HTTPException(status_code=409, detail=existing["status"])
        raise HTTPException(status_code=409, detail="ORDER_NOT_PAYABLE")

    note = f"CVLN Academy {order['economy_code']} order={order_id} attempt={attempt_id}"
    try:
        wallet_result = await cvln_wallet.charge(
            current.frek_id,
            float(order["wallet_amount_jcc"]),
            note,
            attempt_id,
        )
    except CVLNWalletNotConfigured as exc:
        await db.commercial_orders.update_one(
            {"order_id": order_id, "payment_attempt_id": attempt_id},
            {"$set": {"status": "PENDING_PAYMENT", "updated_at": utc_now_iso()}},
        )
        raise HTTPException(
            status_code=503, detail="CVLN_WALLET_NOT_CONFIGURED"
        ) from exc
    except CVLNWalletAmbiguousResult as exc:
        await db.commercial_orders.update_one(
            {"order_id": order_id, "payment_attempt_id": attempt_id},
            {
                "$set": {
                    "status": "REQUIRES_REVIEW",
                    "updated_at": utc_now_iso(),
                    "review_reason": "WALLET_OUTCOME_AMBIGUOUS",
                }
            },
        )
        raise HTTPException(status_code=409, detail="REQUIRES_REVIEW") from exc
    except httpx.HTTPStatusError as exc:
        await db.commercial_orders.update_one(
            {"order_id": order_id, "payment_attempt_id": attempt_id},
            {
                "$set": {
                    "status": "PAYMENT_FAILED",
                    "updated_at": utc_now_iso(),
                    "failure_status_code": exc.response.status_code,
                }
            },
        )
        raise HTTPException(status_code=402, detail="WALLET_PAYMENT_REJECTED") from exc

    paid_at = utc_now_iso()
    entitlement = {
        "entitlement_id": f"ent_{uuid.uuid4().hex[:16]}",
        "user_id": current.id,
        "user_frek_id": current.frek_id,
        "economy_code": order["economy_code"],
        "source": "CVLN_WALLET",
        "source_order_id": order_id,
        "status": "ACTIVE",
        "granted_at": paid_at,
        "revoked_at": None,
    }
    await db.academy_entitlements.update_one(
        entitlement_filter(current.id, order["economy_code"]),
        {"$setOnInsert": entitlement},
        upsert=True,
    )
    await db.commercial_orders.update_one(
        {"order_id": order_id, "payment_attempt_id": attempt_id},
        {
            "$set": {
                "status": "PAID",
                "wallet_response": wallet_result,
                "paid_at": paid_at,
                "updated_at": paid_at,
            }
        },
    )
    paid_order = await db.commercial_orders.find_one(
        {"order_id": order_id}, {"_id": 0}
    )
    billing_document = build_invoice_intent(paid_order)
    billing_document["created_at"] = paid_at
    billing_document["updated_at"] = paid_at
    await db.billing_documents.update_one(
        {"idempotency_key": billing_document["idempotency_key"]},
        {"$setOnInsert": billing_document},
        upsert=True,
    )
    return paid_order


@router.get("/entitlements/mine")
async def my_entitlements(current: User = Depends(get_current_user)):
    return await db.academy_entitlements.find(
        {"user_id": current.id, "status": "ACTIVE"}, {"_id": 0}
    ).to_list(500)
