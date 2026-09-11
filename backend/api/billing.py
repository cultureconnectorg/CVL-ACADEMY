"""Billing document API: paid commercial order -> idempotent invoice intent."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException

from auth import get_current_user
from billing import BillingPolicyError, OrderNotPaid, build_invoice_intent
from db import db, utc_now_iso
from models import User

router = APIRouter(prefix="/billing", tags=["billing"])


@router.post("/orders/{order_id}/invoice-intent")
async def ensure_invoice_intent(order_id: str, current: User = Depends(get_current_user)):
    order = await db.commercial_orders.find_one(
        {"order_id": order_id, "user_id": current.id}, {"_id": 0}
    )
    if not order:
        raise HTTPException(status_code=404, detail="ORDER_NOT_FOUND")
    try:
        document = build_invoice_intent(order)
    except OrderNotPaid as exc:
        raise HTTPException(status_code=409, detail="ORDER_NOT_PAID") from exc
    except BillingPolicyError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc

    now = utc_now_iso()
    document["created_at"] = now
    document["updated_at"] = now
    await db.billing_documents.update_one(
        {"idempotency_key": document["idempotency_key"]},
        {"$setOnInsert": document},
        upsert=True,
    )
    stored = await db.billing_documents.find_one(
        {"idempotency_key": document["idempotency_key"]}, {"_id": 0}
    )
    return stored


@router.get("/orders/{order_id}/invoice")
async def get_order_invoice(order_id: str, current: User = Depends(get_current_user)):
    order = await db.commercial_orders.find_one(
        {"order_id": order_id, "user_id": current.id}, {"_id": 0, "order_id": 1}
    )
    if not order:
        raise HTTPException(status_code=404, detail="ORDER_NOT_FOUND")
    document = await db.billing_documents.find_one(
        {"order_id": order_id, "document_type": "INVOICE"}, {"_id": 0}
    )
    if not document:
        raise HTTPException(status_code=404, detail="INVOICE_INTENT_NOT_FOUND")
    return document
