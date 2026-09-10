"""ACC-015 — case-scoped accounting workspace for external accountants.

The workspace reuses Professional Governance assignments and expert credentials.
It exposes only Academy accounting records attached to the accounting periods named in
one assigned professional case. It never exposes other CVLN systems or global Academy
records by default.
"""

from __future__ import annotations

from typing import Any, Dict

from db import db
from services import accounting_core, expert_access


async def get_workspace(*, raw_key: str, case_id: str) -> Dict[str, Any]:
    context = await expert_access.authorize_case_scope(raw_key, case_id, "accounting:read")
    case = await db.professional_cases.find_one({"id": case_id}, {"_id": 0})
    if not case:
        raise LookupError("professional case not found")
    if str(case.get("domain", "")).upper() != "ACCOUNTING":
        raise PermissionError("case is not an accounting workspace")

    period_ids = list(dict.fromkeys((case.get("metadata") or {}).get("accounting_period_ids", [])))
    if not period_ids:
        raise PermissionError("accounting case has no explicit period scope")

    periods = await db.accounting_periods.find(
        {"id": {"$in": period_ids}}, {"_id": 0}
    ).to_list(len(period_ids))
    if len(periods) != len(period_ids):
        raise PermissionError("accounting case references an unknown period")

    period_by_id = {row["id"]: row for row in periods}
    ordered_periods = [period_by_id[period_id] for period_id in period_ids]
    period_ranges = [(row["starts_at"], row["ends_at"]) for row in ordered_periods]

    payments: list[Dict[str, Any]] = []
    for starts_at, ends_at in period_ranges:
        rows = await db.payments.find(
            {"created_at": {"$gte": starts_at, "$lt": ends_at}}, {"_id": 0}
        ).to_list(100000)
        payments.extend(rows)
    payment_ids = list(dict.fromkeys(row["id"] for row in payments))

    invoices = []
    reconciliations = []
    if payment_ids:
        invoices = await db.accounting_invoices.find(
            {"payment_id": {"$in": payment_ids}}, {"_id": 0}
        ).to_list(100000)
        reconciliations = await db.accounting_reconciliations.find(
            {"payment_id": {"$in": payment_ids}}, {"_id": 0}
        ).to_list(100000)

    invoice_ids = [row["id"] for row in invoices]
    credit_notes = []
    if invoice_ids:
        credit_notes = await db.accounting_credit_notes.find(
            {"invoice_id": {"$in": invoice_ids}}, {"_id": 0}
        ).to_list(100000)

    anomalies = await db.accounting_period_anomalies.find(
        {"period_id": {"$in": period_ids}}, {"_id": 0}
    ).to_list(10000)
    gates = [await accounting_core.period_close_gate(period_id) for period_id in period_ids]

    gross_cents = sum(int(row.get("amount_cents", 0)) for row in invoices if row.get("status") == "ISSUED")
    credit_cents = sum(int(row.get("amount_cents", 0)) for row in credit_notes if row.get("status") == "ISSUED")

    return {
        "workspace_type": "ACADEMY_ACCOUNTING_ONLY",
        "case": {
            "id": case["id"],
            "title": case["title"],
            "domain": case["domain"],
            "status": case["status"],
            "accounting_period_ids": period_ids,
        },
        "expert": {
            "id": context["expert"]["id"],
            "display_name": context["expert"]["display_name"],
        },
        "granted_scope": context["assignment"].get("scope", []),
        "periods": ordered_periods,
        "period_close_gates": gates,
        "payments": payments,
        "invoices": invoices,
        "credit_notes": credit_notes,
        "reconciliations": reconciliations,
        "anomalies": anomalies,
        "summary": {
            "payment_count": len(payments),
            "invoice_count": len(invoices),
            "gross_invoiced_cents": gross_cents,
            "credit_notes_cents": credit_cents,
            "net_invoiced_cents": gross_cents - credit_cents,
            "open_anomaly_count": sum(1 for row in anomalies if row.get("status") == "OPEN"),
        },
        "external_system_data": None,
    }
