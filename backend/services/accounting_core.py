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
ANOMALY_STATES = {"OPEN", "RESOLVED", "WAIVED"}


def _id(prefix: str) -> str:
    return f"{prefix}-{uuid.uuid4()}"


def _to_cents(amount_eur: float) -> int:
    cents = round(amount_eur * 100)
    if cents < 0:
        raise ValueError("amount cannot be negative")
    return cents


def _parse_instant(value: str, field: str) -> datetime:
    try:
        parsed = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{field} must be ISO-8601") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ValueError(f"{field} must include timezone")
    return parsed.astimezone(timezone.utc)


def _iso_utc(value: str, field: str) -> str:
    return _parse_instant(value, field).isoformat()


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
    existing = await db.accounting_invoices.find_one(
        {"payment_id": payment_id}, {"_id": 0}
    )
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
    provider_evidence = (
        bool(provider_intent) if payment.get("status") == "paid" else True
    )
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


async def create_period(
    *, actor_id: str, code: str, starts_at: str, ends_at: str
) -> Dict[str, Any]:
    start = _parse_instant(starts_at, "starts_at")
    end = _parse_instant(ends_at, "ends_at")
    if start >= end:
        raise ValueError("accounting period start must precede end")
    if await db.accounting_periods.find_one({"code": code.strip()}):
        raise ValueError("accounting period code already exists")
    row = {
        "id": _id("PERIOD"),
        "code": code.strip(),
        "starts_at": start.isoformat(),
        "ends_at": end.isoformat(),
        "status": "OPEN",
        "created_by": actor_id,
        "created_at": utc_now_iso(),
    }
    await db.accounting_periods.insert_one(dict(row))
    return row


async def create_period_anomaly(
    *,
    actor_id: str,
    period_id: str,
    code: str,
    description: str,
    evidence_refs: Iterable[str],
) -> Dict[str, Any]:
    period = await db.accounting_periods.find_one({"id": period_id}, {"_id": 0})
    if not period:
        raise LookupError("accounting period not found")
    if period["status"] != "OPEN":
        raise ValueError("cannot add anomaly to a closed period")
    refs = list(dict.fromkeys(evidence_refs))
    if not refs:
        raise ValueError("accounting anomaly requires evidence")
    row = {
        "id": _id("ACCANOM"),
        "period_id": period_id,
        "code": code.strip().upper(),
        "description": description.strip(),
        "evidence_refs": refs,
        "status": "OPEN",
        "created_by": actor_id,
        "created_at": utc_now_iso(),
        "updated_at": utc_now_iso(),
    }
    await db.accounting_period_anomalies.insert_one(dict(row))
    return row


async def resolve_period_anomaly(
    *,
    actor_id: str,
    anomaly_id: str,
    resolution: str,
    evidence_refs: Iterable[str],
) -> Dict[str, Any]:
    row = await db.accounting_period_anomalies.find_one(
        {"id": anomaly_id}, {"_id": 0}
    )
    if not row:
        raise LookupError("accounting period anomaly not found")
    if row["status"] != "OPEN":
        return row
    refs = list(dict.fromkeys(evidence_refs))
    if not refs or not resolution.strip():
        raise ValueError("anomaly resolution requires explanation and evidence")
    now = utc_now_iso()
    result = await db.accounting_period_anomalies.update_one(
        {"id": anomaly_id, "status": "OPEN"},
        {
            "$set": {
                "status": "RESOLVED",
                "resolution": resolution.strip(),
                "resolution_evidence_refs": refs,
                "resolved_by": actor_id,
                "resolved_at": now,
                "updated_at": now,
            }
        },
    )
    if result.modified_count != 1:
        raise ValueError("accounting anomaly changed concurrently")
    return {
        **row,
        "status": "RESOLVED",
        "resolution": resolution.strip(),
        "resolution_evidence_refs": refs,
        "resolved_by": actor_id,
        "resolved_at": now,
        "updated_at": now,
    }


async def period_close_gate(period_id: str) -> Dict[str, Any]:
    period = await db.accounting_periods.find_one({"id": period_id}, {"_id": 0})
    if not period:
        raise LookupError("accounting period not found")

    open_anomalies = await db.accounting_period_anomalies.find(
        {"period_id": period_id, "status": "OPEN"}, {"_id": 0}
    ).to_list(5000)
    payments = await db.payments.find(
        {
            "created_at": {
                "$gte": period["starts_at"],
                "$lt": period["ends_at"],
            }
        },
        {"_id": 0},
    ).to_list(100000)

    unreconciled: list[Dict[str, Any]] = []
    missing_invoices: list[str] = []
    for payment in payments:
        latest = await db.accounting_reconciliations.find_one(
            {"payment_id": payment["id"]},
            {"_id": 0},
            sort=[("checked_at", -1)],
        )
        if not latest or not latest.get("reconciled"):
            issues = (
                latest.get("issues", ["RECONCILIATION_MISSING"])
                if latest
                else ["RECONCILIATION_MISSING"]
            )
            unreconciled.append(
                {
                    "payment_id": payment["id"],
                    "status": payment.get("status"),
                    "reconciliation_id": latest.get("id") if latest else None,
                    "issues": issues,
                }
            )
        if payment.get("status") == "paid":
            invoice = await db.accounting_invoices.find_one(
                {"payment_id": payment["id"], "status": "ISSUED"},
                {"_id": 0, "id": 1},
            )
            if not invoice:
                missing_invoices.append(payment["id"])

    blockers: list[Dict[str, Any]] = []
    if open_anomalies:
        blockers.append({"code": "OPEN_ANOMALIES", "count": len(open_anomalies)})
    if unreconciled:
        blockers.append(
            {"code": "UNRECONCILED_PAYMENTS", "count": len(unreconciled)}
        )
    if missing_invoices:
        blockers.append(
            {
                "code": "MISSING_INVOICES_FOR_PAID_PAYMENTS",
                "count": len(missing_invoices),
            }
        )

    return {
        "period_id": period_id,
        "pass": not blockers,
        "blocking_count": sum(int(item["count"]) for item in blockers),
        "blockers": blockers,
        "open_anomalies": open_anomalies,
        "unreconciled_payments": unreconciled,
        "missing_invoice_payment_ids": missing_invoices,
        "supporting_documents_scope": (
            "ACC-007_NOT_YET_AUTOMATED; missing documents must be registered "
            "as period anomalies"
        ),
        "checked_at": utc_now_iso(),
    }


async def close_period(
    *,
    actor_id: str,
    period_id: str,
    evidence_refs: Iterable[str],
    review_note: str,
) -> Dict[str, Any]:
    row = await db.accounting_periods.find_one({"id": period_id}, {"_id": 0})
    if not row:
        raise LookupError("accounting period not found")
    if row["status"] == "CLOSED":
        return row
    refs = list(dict.fromkeys(evidence_refs))
    if not refs or not review_note.strip():
        raise ValueError("period closure requires review_note and evidence_refs")
    gate = await period_close_gate(period_id)
    if not gate["pass"]:
        raise ValueError("accounting period close gate failed")
    now = utc_now_iso()
    result = await db.accounting_periods.update_one(
        {"id": period_id, "status": "OPEN"},
        {
            "$set": {
                "status": "CLOSED",
                "closed_at": now,
                "closed_by": actor_id,
                "close_evidence_refs": refs,
                "close_review_note": review_note.strip(),
                "close_gate_snapshot": gate,
            }
        },
    )
    if result.modified_count != 1:
        raise ValueError("accounting period changed concurrently")
    return {
        **row,
        "status": "CLOSED",
        "closed_at": now,
        "closed_by": actor_id,
        "close_evidence_refs": refs,
        "close_review_note": review_note.strip(),
        "close_gate_snapshot": gate,
    }


async def register_account_mapping(
    *,
    actor_id: str,
    event_type: str,
    debit_account: str,
    credit_account: str,
    tax_code: Optional[str] = None,
    evidence_refs: Iterable[str] = (),
) -> Dict[str, Any]:
    """Legacy compatibility helper.

    The public API uses services.accounting_mappings, which versions mappings through
    XCP-008. Keep this helper only for old internal callers until they migrate.
    """
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
    invoices = await db.accounting_invoices.find(
        {"status": "ISSUED"}, {"_id": 0}
    ).to_list(100000)
    credits = await db.accounting_credit_notes.find(
        {"status": "ISSUED"}, {"_id": 0}
    ).to_list(100000)
    gross = sum(int(row["amount_cents"]) for row in invoices)
    credit_total = sum(int(row["amount_cents"]) for row in credits)
    mappings = await db.accounting_mappings.find(
        {"status": "ACTIVE"}, {"_id": 0}
    ).to_list(1000)
    return {
        "currency": "EUR",
        "gross_invoiced_cents": gross,
        "credit_notes_cents": credit_total,
        "net_invoiced_cents": gross - credit_total,
        "active_mappings": mappings,
        "tax_amounts": None,
        "tax_amounts_status": "NOT_COMPUTED_WITHOUT_VERIFIED_TAX_POLICY",
    }
