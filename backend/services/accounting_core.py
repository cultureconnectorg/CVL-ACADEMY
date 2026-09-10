"""Evidence-first accounting primitives for CVLN Academy.

The Academy masters require invoice numbering, credit notes, revenue splits,
payment reconciliation, periods, tax-preparation mappings and an accounting
workspace. This module implements the control/data layer without inventing tax
rates, legal invoice wording or revenue-share percentages. Monetary amounts are
stored in integer cents.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, Optional

from db import db, utc_now_iso


PERIOD_STATES = {"OPEN", "CLOSED"}


def _id(prefix: str) -> str:
    return f"{prefix}-{uuid.uuid4()}"


def _to_cents(amount_eur: float) -> int:
    cents = round(amount_eur * 100)
    if cents < 0:
        raise ValueError("amount cannot be negative")
    return cents


async def _next_number(sequence: str, year: int) -> int:
    row = await db.accounting_sequences.find_one_and_update(
        {"sequence": sequence, "year": year},
        {"$inc": {"value": 1}, "$setOnInsert": {"created_at": utc_now_iso()}},
        upsert=True,
        return_document=True,
    )
    return int(row["value"])


async def create_invoice_from_payment(
    *,
    actor_id: str,
    payment_id: str,
    issuer_name: str,
    customer_name: str,
    customer_address: Optional[str] = None,
) -> Dict[str, Any]:
    existing = await db.accounting_invoices.find_one({"payment_id": payment_id}, {"_id": 0})
    if existing:
        return existing
    payment = await db.payments.find_one({"id": payment_id}, {"_id": 0})
    if not payment:
        raise LookupError("payment not found")
    if payment.get("status") != "paid":
        raise ValueError("invoice can only be issued for a paid payment")
    year = datetime.now(timezone.utc).year
    seq = await _next_number("invoice", year)
    number = f"INV-{year}-{seq:06d}"
    row = {
        "id": _id("INV"),
        "number": number,
        "payment_id": payment_id,
        "checkout_session_id": payment.get("checkout_session_id"),
        "user_id": payment.get("user_id"),
        "offer_id": payment.get("offer_id"),
        "amount_cents": _to_cents(float(payment.get("amount_eur", 0))),
        "currency": payment.get("currency", "EUR"),
        "issuer_name": issuer_name,
        "customer_name": customer_name,
        "customer_address": customer_address,
        "status": "ISSUED",
        "issued_by": actor_id,
        "issued_at": utc_now_iso(),
    }
    await db.accounting_invoices.insert_one(dict(row))
    return row


async def create_credit_note(
    *,
    actor_id: str,
    invoice_id: str,
    amount_cents: int,
    reason: str,
) -> Dict[str, Any]:
    if amount_cents <= 0:
        raise ValueError("credit note amount must be positive")
    invoice = await db.accounting_invoices.find_one({"id": invoice_id}, {"_id": 0})
    if not invoice:
        raise LookupError("invoice not found")
    existing = await db.accounting_credit_notes.find(
        {"invoice_id": invoice_id, "status": "ISSUED"}, {"_id": 0}
    ).to_list(1000)
    already = sum(int(row["amount_cents"]) for row in existing)
    if already + amount_cents > int(invoice["amount_cents"]):
        raise ValueError("credit notes cannot exceed invoice amount")
    year = datetime.now(timezone.utc).year
    seq = await _next_number("credit_note", year)
    row = {
        "id": _id("CN"),
        "number": f"CN-{year}-{seq:06d}",
        "invoice_id": invoice_id,
        "amount_cents": amount_cents,
        "currency": invoice["currency"],
        "reason": reason,
        "status": "ISSUED",
        "issued_by": actor_id,
        "issued_at": utc_now_iso(),
    }
    await db.accounting_credit_notes.insert_one(dict(row))
    return row


async def create_revenue_split(
    *,
    actor_id: str,
    source_type: str,
    source_id: str,
    amount_cents: int,
    allocations: Iterable[Dict[str, Any]],
) -> Dict[str, Any]:
    if amount_cents <= 0:
        raise ValueError("split amount must be positive")
    rows = [dict(item) for item in allocations]
    if not rows:
        raise ValueError("at least one allocation is required")
    total = 0
    for row in rows:
        cents = int(row.get("amount_cents", 0))
        if cents < 0 or not row.get("beneficiary"):
            raise ValueError("invalid revenue allocation")
        total += cents
    if total != amount_cents:
        raise ValueError("allocations must exactly equal source amount")
    split = {
        "id": _id("SPLIT"),
        "source_type": source_type.upper(),
        "source_id": source_id,
        "amount_cents": amount_cents,
        "allocations": rows,
        "status": "RECORDED",
        "created_by": actor_id,
        "created_at": utc_now_iso(),
    }
    await db.accounting_revenue_splits.insert_one(dict(split))
    return split


async def reconcile_payment(*, actor_id: str, payment_id: str) -> Dict[str, Any]:
    payment = await db.payments.find_one({"id": payment_id}, {"_id": 0})
    if not payment:
        raise LookupError("payment not found")
    checkout = None
    if payment.get("checkout_session_id"):
        checkout = await db.payment_checkout_sessions.find_one(
            {"id": payment["checkout_session_id"]}, {"_id": 0}
        )
    provider_intent = payment.get("provider_payment_intent_id")
    status_match = bool(checkout) and checkout.get("status") == payment.get("status")
    provider_evidence = bool(provider_intent) if payment.get("status") == "paid" else True
    reconciled = status_match and provider_evidence
    row = {
        "id": _id("RECON"),
        "payment_id": payment_id,
        "payment_status": payment.get("status"),
        "checkout_status": checkout.get("status") if checkout else None,
        "provider_payment_intent_id": provider_intent,
        "reconciled": reconciled,
        "issues": [],
        "checked_by": actor_id,
        "checked_at": utc_now_iso(),
    }
    if not checkout:
        row["issues"].append("CHECKOUT_NOT_FOUND")
    elif not status_match:
        row["issues"].append("STATUS_MISMATCH")
    if payment.get("status") == "paid" and not provider_intent:
        row["issues"].append("PROVIDER_PAYMENT_INTENT_MISSING")
    await db.accounting_reconciliations.insert_one(dict(row))
    return row


async def create_period(*, actor_id: str, code: str, starts_at: str, ends_at: str) -> Dict[str, Any]:
    if starts_at >= ends_at:
        raise ValueError("accounting period start must precede end")
    row = {
        "id": _id("PERIOD"),
        "code": code,
        "starts_at": starts_at,
        "ends_at": ends_at,
        "status": "OPEN",
        "created_by": actor_id,
        "created_at": utc_now_iso(),
    }
    await db.accounting_periods.insert_one(dict(row))
    return row


async def close_period(*, actor_id: str, period_id: str) -> Dict[str, Any]:
    row = await db.accounting_periods.find_one({"id": period_id}, {"_id": 0})
    if not row:
        raise LookupError("accounting period not found")
    if row["status"] == "CLOSED":
        return row
    now = utc_now_iso()
    await db.accounting_periods.update_one(
        {"id": period_id, "status": "OPEN"},
        {"$set": {"status": "CLOSED", "closed_at": now, "closed_by": actor_id}},
    )
    return {**row, "status": "CLOSED", "closed_at": now, "closed_by": actor_id}


async def register_account_mapping(
    *, actor_id: str, event_type: str, debit_account: str, credit_account: str,
    tax_code: Optional[str] = None, evidence_refs: Iterable[str] = (),
) -> Dict[str, Any]:
    row = {
        "id": _id("MAP"),
        "event_type": event_type.upper(),
        "debit_account": debit_account,
        "credit_account": credit_account,
        "tax_code": tax_code,
        "evidence_refs": list(evidence_refs),
        "status": "ACTIVE",
        "created_by": actor_id,
        "created_at": utc_now_iso(),
        "updated_at": utc_now_iso(),
    }
    await db.accounting_mappings.update_one(
        {"event_type": row["event_type"]}, {"$set": row}, upsert=True
    )
    return row


async def tax_preparation_summary() -> Dict[str, Any]:
    invoices = await db.accounting_invoices.find({"status": "ISSUED"}, {"_id": 0}).to_list(100000)
    credits = await db.accounting_credit_notes.find({"status": "ISSUED"}, {"_id": 0}).to_list(100000)
    gross = sum(int(row["amount_cents"]) for row in invoices)
    credit_total = sum(int(row["amount_cents"]) for row in credits)
    mappings = await db.accounting_mappings.find({"status": "ACTIVE"}, {"_id": 0}).to_list(1000)
    return {
        "currency": "EUR",
        "gross_invoiced_cents": gross,
        "credit_notes_cents": credit_total,
        "net_invoiced_cents": gross - credit_total,
        "active_mappings": mappings,
        "tax_amounts": None,
        "tax_amounts_status": "NOT_COMPUTED_WITHOUT_VERIFIED_TAX_POLICY",
    }
