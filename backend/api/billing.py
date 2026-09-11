"""Billing API: paid commercial order -> Factur-X invoice artifacts."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Response
from pydantic import BaseModel, Field
from pymongo import ReturnDocument

from auth import get_current_user
from billing import (
    BillingNotReady,
    BillingPolicyError,
    DOCUMENT_ISSUANCE_FAILED,
    DOCUMENT_ISSUED,
    DOCUMENT_ISSUING,
    OrderNotPaid,
    assert_legal_issuance_ready,
    build_invoice_intent,
    issuer_profile,
)
from billing_einvoice import (
    assert_buyer_profile_ready,
    decode_artifact,
    generate_invoice_artifacts,
    tax_policy,
)
from db import db, utc_now_iso
from models import User

router = APIRouter(prefix="/billing", tags=["billing"])


class BillingProfileInput(BaseModel):
    legal_name: str = Field(min_length=1, max_length=160)
    address_line1: str = Field(min_length=1, max_length=200)
    city: str = Field(min_length=1, max_length=120)
    postal_code: str = Field(min_length=1, max_length=32)
    country: str = Field(min_length=2, max_length=2)
    vat_id: Optional[str] = Field(default=None, max_length=64)
    registration_id: Optional[str] = Field(default=None, max_length=64)
    registration_scheme: Optional[str] = Field(default="0002", max_length=16)


def _billing_error(exc: Exception) -> HTTPException:
    if isinstance(exc, BillingNotReady):
        return HTTPException(status_code=409, detail=str(exc))
    return HTTPException(status_code=422, detail=str(exc))


@router.get("/readiness")
async def billing_readiness(current: User = Depends(get_current_user)):
    del current
    issuer = issuer_profile()
    try:
        policy = tax_policy()
        tax_ready = True
        tax_error = None
    except BillingPolicyError as exc:
        policy = None
        tax_ready = False
        tax_error = str(exc)
    return {
        "issuer_configured": all(
            issuer.get(k)
            for k in (
                "legal_name",
                "country",
                "registration_id",
                "address_line1",
                "city",
                "postal_code",
                "invoice_series",
            )
        ),
        "tax_configured": tax_ready,
        "tax_policy": policy,
        "tax_error": tax_error,
        "einvoice_profile": issuer.get("einvoice_profile"),
    }


@router.put("/profile")
async def upsert_billing_profile(
    inp: BillingProfileInput, current: User = Depends(get_current_user)
):
    now = utc_now_iso()
    profile = {
        "user_id": current.id,
        "frek_id": current.frek_id,
        "email": str(current.email),
        "legal_name": inp.legal_name.strip(),
        "address_line1": inp.address_line1.strip(),
        "city": inp.city.strip(),
        "postal_code": inp.postal_code.strip(),
        "country": inp.country.strip().upper(),
        "vat_id": (inp.vat_id or "").strip() or None,
        "registration_id": (inp.registration_id or "").strip() or None,
        "registration_scheme": (inp.registration_scheme or "0002").strip(),
        "updated_at": now,
    }
    assert_buyer_profile_ready(profile)
    await db.billing_profiles.update_one(
        {"user_id": current.id},
        {"$set": profile, "$setOnInsert": {"created_at": now}},
        upsert=True,
    )
    return await db.billing_profiles.find_one({"user_id": current.id}, {"_id": 0})


@router.get("/profile")
async def get_billing_profile(current: User = Depends(get_current_user)):
    profile = await db.billing_profiles.find_one({"user_id": current.id}, {"_id": 0})
    if not profile:
        raise HTTPException(status_code=404, detail="BILLING_PROFILE_NOT_FOUND")
    return profile


@router.post("/orders/{order_id}/invoice-intent")
async def ensure_invoice_intent(
    order_id: str, current: User = Depends(get_current_user)
):
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
        raise _billing_error(exc) from exc

    now = utc_now_iso()
    document["created_at"] = now
    document["updated_at"] = now
    await db.billing_documents.update_one(
        {"idempotency_key": document["idempotency_key"]},
        {"$setOnInsert": document},
        upsert=True,
    )
    return await db.billing_documents.find_one(
        {"idempotency_key": document["idempotency_key"]}, {"_id": 0}
    )


async def _reserve_invoice_number(document: dict) -> dict:
    if document.get("legal_invoice_number"):
        return document
    issuer = issuer_profile()
    year = datetime.now(timezone.utc).year
    sequence_id = f"invoice:{issuer['invoice_series']}:{year}"
    sequence = await db.billing_sequences.find_one_and_update(
        {"sequence_id": sequence_id},
        {
            "$inc": {"value": 1},
            "$setOnInsert": {
                "sequence_id": sequence_id,
                "series": issuer["invoice_series"],
                "year": year,
                "created_at": utc_now_iso(),
            },
            "$set": {"updated_at": utc_now_iso()},
        },
        upsert=True,
        return_document=ReturnDocument.AFTER,
    )
    number = f"{issuer['invoice_series']}-{year}-{int(sequence['value']):06d}"
    reserved = await db.billing_documents.find_one_and_update(
        {
            "billing_document_id": document["billing_document_id"],
            "legal_invoice_number": None,
        },
        {
            "$set": {
                "legal_invoice_number": number,
                "status": DOCUMENT_ISSUING,
                "number_reserved_at": utc_now_iso(),
                "updated_at": utc_now_iso(),
            }
        },
        return_document=ReturnDocument.AFTER,
    )
    if reserved:
        return reserved
    return await db.billing_documents.find_one(
        {"billing_document_id": document["billing_document_id"]}, {"_id": 0}
    )


@router.post("/orders/{order_id}/issue")
async def issue_order_invoice(order_id: str, current: User = Depends(get_current_user)):
    document = await db.billing_documents.find_one(
        {"order_id": order_id, "user_id": current.id, "document_type": "INVOICE"},
        {"_id": 0},
    )
    if not document:
        await ensure_invoice_intent(order_id, current)
        document = await db.billing_documents.find_one(
            {"order_id": order_id, "user_id": current.id, "document_type": "INVOICE"},
            {"_id": 0},
        )
    if document.get("status") == DOCUMENT_ISSUED:
        return document

    profile = await db.billing_profiles.find_one({"user_id": current.id}, {"_id": 0})
    if not profile:
        raise HTTPException(status_code=409, detail="BILLING_PROFILE_REQUIRED")
    try:
        assert_buyer_profile_ready(profile)
        if document.get("status") == DOCUMENT_ISSUANCE_FAILED:
            document["status"] = "INVOICE_INTENT"
        assert_legal_issuance_ready(document)
        tax_policy()
    except BillingPolicyError as exc:
        raise _billing_error(exc) from exc

    document = await _reserve_invoice_number(document)
    if document.get("status") == DOCUMENT_ISSUED:
        return document

    issuance_started = datetime.now(timezone.utc)
    candidate = dict(document)
    candidate["buyer_profile_snapshot"] = profile
    candidate["issuer_profile_snapshot"] = issuer_profile()
    try:
        artifact = generate_invoice_artifacts(candidate, profile, issuance_started)
    except Exception as exc:
        await db.billing_documents.update_one(
            {"billing_document_id": document["billing_document_id"]},
            {
                "$set": {
                    "status": DOCUMENT_ISSUANCE_FAILED,
                    "issuance_error": str(exc)[:1000],
                    "updated_at": utc_now_iso(),
                }
            },
        )
        raise HTTPException(
            status_code=422, detail="EINVOICE_GENERATION_FAILED"
        ) from exc

    issued_at = artifact["issued_at"]
    await db.billing_documents.update_one(
        {"billing_document_id": document["billing_document_id"]},
        {
            "$set": {
                "status": DOCUMENT_ISSUED,
                "buyer_profile_snapshot": profile,
                "issuer_profile_snapshot": issuer_profile(),
                "einvoice_format": artifact["format"],
                "einvoice_validation": artifact["xsd_validation"],
                "artifact": artifact,
                "issued_at": issued_at,
                "issuance_error": None,
                "updated_at": issued_at,
            }
        },
    )
    return await db.billing_documents.find_one(
        {"billing_document_id": document["billing_document_id"]}, {"_id": 0}
    )


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
        raise HTTPException(status_code=404, detail="INVOICE_NOT_FOUND")
    artifact = document.pop("artifact", None)
    if artifact:
        document["artifact"] = {
            "format": artifact.get("format"),
            "xml_sha256": artifact.get("xml_sha256"),
            "pdf_sha256": artifact.get("pdf_sha256"),
            "xml_size": artifact.get("xml_size"),
            "pdf_size": artifact.get("pdf_size"),
            "xsd_validation": artifact.get("xsd_validation"),
            "schematron_validation": artifact.get("schematron_validation"),
        }
    return document


@router.get("/orders/{order_id}/invoice/{kind}")
async def download_order_invoice_artifact(
    order_id: str, kind: str, current: User = Depends(get_current_user)
):
    document = await db.billing_documents.find_one(
        {
            "order_id": order_id,
            "user_id": current.id,
            "document_type": "INVOICE",
            "status": DOCUMENT_ISSUED,
        },
        {"_id": 0},
    )
    if not document:
        raise HTTPException(status_code=404, detail="ISSUED_INVOICE_NOT_FOUND")
    try:
        payload, media_type = decode_artifact(document, kind)
    except BillingPolicyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    extension = "pdf" if kind == "pdf" else "xml"
    filename = f"{document['legal_invoice_number']}.{extension}"
    return Response(
        content=payload,
        media_type=media_type,
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
