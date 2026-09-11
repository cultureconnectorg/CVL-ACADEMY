"""CVLN Academy billing document core.

Billing is separate from payment. CVLN Wallet proves value movement; this module
owns invoice/credit-note lifecycle and traceability. Economy 3D remains pricing
authority. Legal issuance is fail-closed until issuer and tax policy are explicit.
"""

from __future__ import annotations

import hashlib
import os
from typing import Any, Dict


class BillingPolicyError(ValueError):
    pass


class BillingNotReady(BillingPolicyError):
    pass


class OrderNotPaid(BillingPolicyError):
    pass


DOCUMENT_INTENT = "INVOICE_INTENT"
DOCUMENT_ISSUED = "ISSUED"
DOCUMENT_VOID = "VOID"
DOCUMENT_CREDITED = "CREDITED"


def billing_idempotency_key(order_id: str, document_type: str = "INVOICE") -> str:
    material = f"cvln-academy:{document_type}:{order_id}".encode("utf-8")
    return hashlib.sha256(material).hexdigest()


def issuer_profile() -> Dict[str, Any]:
    """Return explicit deployment configuration only; never infer legal data."""
    return {
        "legal_name": os.environ.get("ACADEMY_BILLING_LEGAL_NAME", "").strip(),
        "country": os.environ.get("ACADEMY_BILLING_COUNTRY", "").strip().upper(),
        "registration_id": os.environ.get(
            "ACADEMY_BILLING_REGISTRATION_ID", ""
        ).strip(),
        "registration_scheme": os.environ.get(
            "ACADEMY_BILLING_REGISTRATION_SCHEME", "0002"
        ).strip(),
        "vat_id": os.environ.get("ACADEMY_BILLING_VAT_ID", "").strip(),
        "address_line1": os.environ.get(
            "ACADEMY_BILLING_ADDRESS_LINE1", ""
        ).strip(),
        "city": os.environ.get("ACADEMY_BILLING_CITY", "").strip(),
        "postal_code": os.environ.get("ACADEMY_BILLING_POSTAL_CODE", "").strip(),
        "invoice_series": os.environ.get(
            "ACADEMY_BILLING_INVOICE_SERIES", ""
        ).strip(),
        "einvoice_profile": os.environ.get(
            "ACADEMY_BILLING_EINVOICE_PROFILE", "FACTUR-X_EN16931"
        ).strip(),
    }


def issuer_ready_for_legal_issuance() -> bool:
    profile = issuer_profile()
    return all(
        profile[field]
        for field in (
            "legal_name",
            "country",
            "registration_id",
            "address_line1",
            "city",
            "postal_code",
            "invoice_series",
        )
    )


def build_invoice_intent(order: Dict[str, Any]) -> Dict[str, Any]:
    """Create immutable billing intent from a confirmed paid order."""
    if order.get("status") != "PAID":
        raise OrderNotPaid("Invoice intent requires a PAID commercial order")
    order_id = str(order.get("order_id") or "").strip()
    if not order_id:
        raise BillingPolicyError("Paid order is missing order_id")
    pricing = order.get("pricing_snapshot")
    if not isinstance(pricing, dict):
        raise BillingPolicyError("Paid order is missing immutable pricing_snapshot")
    if order.get("amount_eur") is None or order.get("currency") != "EUR":
        raise BillingPolicyError("Paid order has unsupported monetary snapshot")

    return {
        "billing_document_id": f"bill_{billing_idempotency_key(order_id)[:20]}",
        "idempotency_key": billing_idempotency_key(order_id),
        "document_type": "INVOICE",
        "status": DOCUMENT_INTENT,
        "legal_invoice_number": None,
        "order_id": order_id,
        "user_id": order.get("user_id"),
        "user_frek_id": order.get("user_frek_id"),
        "economy_code": order.get("economy_code"),
        "economy_requirement_id": order.get("economy_requirement_id"),
        "amount_eur": order.get("amount_eur"),
        "currency": "EUR",
        "pricing_snapshot": pricing,
        "payment_source": "CVLN_WALLET",
        "payment_attempt_id": order.get("payment_attempt_id"),
        "wallet_entity_id": order.get("wallet_entity_id"),
        "wallet_response": order.get("wallet_response"),
        "paid_at": order.get("paid_at"),
        "issuer_profile_snapshot": issuer_profile(),
        "legal_issuance_ready": issuer_ready_for_legal_issuance(),
        "einvoice_format": None,
        "einvoice_validation": "NOT_RUN",
        "artifact": None,
        "issued_at": None,
        "credited_by": None,
    }


def assert_legal_issuance_ready(document: Dict[str, Any]) -> None:
    if document.get("status") != DOCUMENT_INTENT:
        raise BillingPolicyError("Only an invoice intent can be issued")
    if not issuer_ready_for_legal_issuance():
        raise BillingNotReady("Billing issuer profile is incomplete")
    if not document.get("payment_attempt_id"):
        raise BillingNotReady("Payment evidence is missing")
    if not document.get("pricing_snapshot"):
        raise BillingNotReady("Pricing evidence is missing")
