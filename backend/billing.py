"""CVLN Academy billing document core.

Billing is deliberately separate from payment. CVLN Wallet proves value movement;
this module owns invoice/credit-note lifecycle and traceability. Legal invoice
issuance remains fail-closed until an issuer/tax profile is explicitly configured.

Architecture references are recorded in docs/BILLING_OPEN_SOURCE_RESEARCH_2026-09.md.
No AGPL/source-available implementation is copied here.
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
    """Stable key: one invoice intent per order/document type."""
    material = f"cvln-academy:{document_type}:{order_id}".encode("utf-8")
    return hashlib.sha256(material).hexdigest()


def issuer_profile() -> Dict[str, Any]:
    """Return only explicit deployment configuration; never infer legal data."""
    return {
        "legal_name": os.environ.get("ACADEMY_BILLING_LEGAL_NAME", "").strip(),
        "country": os.environ.get("ACADEMY_BILLING_COUNTRY", "").strip().upper(),
        "registration_id": os.environ.get("ACADEMY_BILLING_REGISTRATION_ID", "").strip(),
        "vat_id": os.environ.get("ACADEMY_BILLING_VAT_ID", "").strip(),
        "invoice_series": os.environ.get("ACADEMY_BILLING_INVOICE_SERIES", "").strip(),
        "einvoice_profile": os.environ.get("ACADEMY_BILLING_EINVOICE_PROFILE", "").strip(),
    }


def issuer_ready_for_legal_issuance() -> bool:
    profile = issuer_profile()
    # VAT ID is intentionally not universally mandatory here: tax treatment is a
    # separate explicit policy. The minimum legal issuer identity must exist.
    return all(
        profile[field]
        for field in ("legal_name", "country", "registration_id", "invoice_series")
    )


def build_invoice_intent(order: Dict[str, Any]) -> Dict[str, Any]:
    """Create an immutable, non-legal invoice intent from a confirmed paid order."""
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
        "issued_at": None,
        "credited_by": None,
    }


def assert_legal_issuance_ready(document: Dict[str, Any]) -> None:
    """Fail closed before numbering/generating a legal invoice."""
    if document.get("status") != DOCUMENT_INTENT:
        raise BillingPolicyError("Only an invoice intent can be issued")
    if not issuer_ready_for_legal_issuance():
        raise BillingNotReady("Billing issuer profile is incomplete")
    if not document.get("payment_attempt_id"):
        raise BillingNotReady("Payment evidence is missing")
    # Tax/VAT is deliberately not guessed. A later tax policy adapter must set an
    # explicit validated tax treatment before this function is extended to issue.
    raise BillingNotReady("Tax/e-invoicing policy adapter is not configured")
