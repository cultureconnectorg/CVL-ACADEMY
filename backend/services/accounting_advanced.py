"""Advanced accounting controls (ACC-001/002/004/005/007/008/010..014).

This module extends the existing accounting collections. It does not create a second
invoice/payment/mapping engine and it does not claim tax validation without an
explicit externally-evidenced policy decision.
"""

from __future__ import annotations

import csv
import io
import uuid
from typing import Any, Dict, Iterable, Optional

from db import db, utc_now_iso
from services import policy_registry
from services import professional_governance as governance


def _id(prefix: str) -> str:
    return f"{prefix}-{uuid.uuid4()}"


def _refs(values: Iterable[str]) -> list[str]:
    return list(dict.fromkeys(str(v).strip() for v in values if str(v).strip()))


async def register_accounting_entity(
    *,
    actor_id: str,
    code: str,
    legal_name: str,
    registration_ref: str,
    invoice_prefix: str,
    evidence_refs: Iterable[str],
) -> Dict[str, Any]:
    refs = _refs(evidence_refs)
    if not all(str(v).strip() for v in (code, legal_name, registration_ref, invoice_prefix)):
        raise ValueError("accounting entity requires code, legal_name, registration_ref and invoice_prefix")
    if not refs:
        raise ValueError("accounting entity requires evidence")
    key = code.strip().upper()
    existing = await db.accounting_entities.find_one({"code": key}, {"_id": 0})
    if existing:
        return existing
    row = {
        "id": _id("ACCENT"),
        "code": key,
        "legal_name": legal_name.strip(),
        "registration_ref": registration_ref.strip(),
        "invoice_prefix": invoice_prefix.strip().upper(),
        "evidence_refs": refs,
        "status": "ACTIVE",
        "created_by": actor_id,
        "created_at": utc_now_iso(),
    }
    await db.accounting_entities.insert_one(dict(row))
    await governance.audit_event(
        event_type="accounting.entity.registered",
        actor_id=actor_id,
        resource_type="accounting_entity",
        resource_id=row["id"],
        payload={"code": key, "registration_ref": row["registration_ref"], "evidence_refs": refs},
    )
    return row


async def attach_invoice_entity(
    *, actor_id: str, invoice_id: str, entity_id: str, evidence_refs: Iterable[str]
) -> Dict[str, Any]:
    refs = _refs(evidence_refs)
    invoice = await db.accounting_invoices.find_one({"id": invoice_id}, {"_id": 0})
    entity = await db.accounting_entities.find_one({"id": entity_id, "status": "ACTIVE"}, {"_id": 0})
    if not invoice:
        raise LookupError("invoice not found")
    if not entity:
        raise LookupError("active accounting entity not found")
    if not refs:
        raise ValueError("invoice entity binding requires evidence")
    if invoice.get("accounting_entity_id") and invoice["accounting_entity_id"] != entity_id:
        raise ValueError("issued invoice accounting entity cannot be silently replaced")
    update = {
        "accounting_entity_id": entity_id,
        "issuer_name": entity["legal_name"],
        "issuer_registration_ref": entity["registration_ref"],
        "entity_binding_evidence_refs": refs,
    }
    await db.accounting_invoices.update_one({"id": invoice_id}, {"$set": update})
    return {**invoice, **update}


async def register_supporting_document(
    *,
    actor_id: str,
    document_type: str,
    document_ref: str,
    content_hash: str,
    vendor_id: Optional[str] = None,
    invoice_id: Optional[str] = None,
    period_id: Optional[str] = None,
    amount_cents: Optional[int] = None,
    evidence_refs: Iterable[str],
) -> Dict[str, Any]:
    refs = _refs(evidence_refs)
    digest = content_hash.strip().lower()
    if len(digest) != 64:
        raise ValueError("supporting document content_hash must be SHA-256")
    try:
        bytes.fromhex(digest)
    except ValueError as exc:
        raise ValueError("supporting document content_hash must be hexadecimal") from exc
    if not document_ref.strip() or not refs:
        raise ValueError("supporting document requires document_ref and evidence")
    if invoice_id and not await db.accounting_invoices.find_one({"id": invoice_id}):
        raise LookupError("invoice not found")
    if period_id and not await db.accounting_periods.find_one({"id": period_id}):
        raise LookupError("accounting period not found")
    if amount_cents is not None and amount_cents < 0:
        raise ValueError("supporting document amount cannot be negative")
    row = {
        "id": _id("ACCDOC"),
        "document_type": document_type.strip().upper(),
        "document_ref": document_ref.strip(),
        "content_hash": digest,
        "vendor_id": vendor_id,
        "invoice_id": invoice_id,
        "period_id": period_id,
        "amount_cents": amount_cents,
        "evidence_refs": refs,
        "status": "REGISTERED",
        "created_by": actor_id,
        "created_at": utc_now_iso(),
    }
    await db.accounting_supporting_documents.insert_one(dict(row))
    await governance.audit_event(
        event_type="accounting.supporting_document.registered",
        actor_id=actor_id,
        resource_type="accounting_supporting_document",
        resource_id=row["id"],
        payload={
            "document_type": row["document_type"],
            "invoice_id": invoice_id,
            "period_id": period_id,
            "content_hash": digest,
        },
    )
    return row


async def register_connector(
    *,
    actor_id: str,
    connector_type: str,
    provider_name: str,
    account_ref: str,
    mode: str,
    evidence_refs: Iterable[str],
) -> Dict[str, Any]:
    refs = _refs(evidence_refs)
    normalized_mode = mode.strip().upper()
    if normalized_mode not in {"MANUAL_IMPORT", "API_READ", "API_SYNC"}:
        raise ValueError("invalid accounting connector mode")
    if not provider_name.strip() or not account_ref.strip() or not refs:
        raise ValueError("connector requires provider, account_ref and evidence")
    row = {
        "id": _id("ACCCONN"),
        "connector_type": connector_type.strip().upper(),
        "provider_name": provider_name.strip(),
        "account_ref": account_ref.strip(),
        "mode": normalized_mode,
        "evidence_refs": refs,
        "status": "REGISTERED_NOT_VERIFIED",
        "created_by": actor_id,
        "created_at": utc_now_iso(),
    }
    await db.accounting_connectors.insert_one(dict(row))
    return row


async def record_cost_line(
    *,
    actor_id: str,
    cost_type: str,
    amount_cents: int,
    source_ref: str,
    formation_code: Optional[str] = None,
    cohort_id: Optional[str] = None,
    pole: Optional[str] = None,
    entity_id: Optional[str] = None,
    learner_id: Optional[str] = None,
    expert_id: Optional[str] = None,
    period_id: Optional[str] = None,
    evidence_refs: Iterable[str],
) -> Dict[str, Any]:
    refs = _refs(evidence_refs)
    if amount_cents < 0 or not cost_type.strip() or not source_ref.strip() or not refs:
        raise ValueError("cost line requires non-negative amount, type, source and evidence")
    row = {
        "id": _id("ACCCOST"),
        "cost_type": cost_type.strip().upper(),
        "amount_cents": int(amount_cents),
        "source_ref": source_ref.strip(),
        "formation_code": formation_code,
        "cohort_id": cohort_id,
        "pole": pole,
        "entity_id": entity_id,
        "learner_id": learner_id,
        "expert_id": expert_id,
        "period_id": period_id,
        "evidence_refs": refs,
        "created_by": actor_id,
        "created_at": utc_now_iso(),
    }
    await db.accounting_cost_lines.insert_one(dict(row))
    return row


async def profitability_summary(
    *,
    formation_code: Optional[str] = None,
    cohort_id: Optional[str] = None,
    pole: Optional[str] = None,
    entity_id: Optional[str] = None,
    learner_id: Optional[str] = None,
    expert_id: Optional[str] = None,
    period_id: Optional[str] = None,
) -> Dict[str, Any]:
    dimensions = {
        "formation_code": formation_code,
        "cohort_id": cohort_id,
        "pole": pole,
        "entity_id": entity_id,
        "learner_id": learner_id,
        "expert_id": expert_id,
        "period_id": period_id,
    }
    query = {key: value for key, value in dimensions.items() if value is not None}
    costs = await db.accounting_cost_lines.find(query, {"_id": 0}).to_list(100000)
    revenue_query = dict(query)
    revenues = await db.accounting_revenue_lines.find(revenue_query, {"_id": 0}).to_list(100000)
    total_revenue = sum(int(row.get("amount_cents", 0)) for row in revenues)
    total_cost = sum(int(row.get("amount_cents", 0)) for row in costs)
    by_type: Dict[str, int] = {}
    for row in costs:
        key = row["cost_type"]
        by_type[key] = by_type.get(key, 0) + int(row["amount_cents"])
    return {
        "scope": query,
        "revenue_cents": total_revenue,
        "cost_cents": total_cost,
        "margin_cents": total_revenue - total_cost,
        "cost_by_type": by_type,
        "status": "COMPUTED_FROM_REGISTERED_LINES",
    }


async def record_revenue_line(
    *,
    actor_id: str,
    amount_cents: int,
    source_ref: str,
    formation_code: Optional[str] = None,
    cohort_id: Optional[str] = None,
    pole: Optional[str] = None,
    entity_id: Optional[str] = None,
    learner_id: Optional[str] = None,
    period_id: Optional[str] = None,
    evidence_refs: Iterable[str],
) -> Dict[str, Any]:
    refs = _refs(evidence_refs)
    if amount_cents < 0 or not source_ref.strip() or not refs:
        raise ValueError("revenue line requires non-negative amount, source and evidence")
    row = {
        "id": _id("ACCREV"),
        "amount_cents": int(amount_cents),
        "source_ref": source_ref.strip(),
        "formation_code": formation_code,
        "cohort_id": cohort_id,
        "pole": pole,
        "entity_id": entity_id,
        "learner_id": learner_id,
        "expert_id": None,
        "period_id": period_id,
        "evidence_refs": refs,
        "created_by": actor_id,
        "created_at": utc_now_iso(),
    }
    await db.accounting_revenue_lines.insert_one(dict(row))
    return row


async def prepare_tax_package(
    *,
    actor_id: str,
    period_id: str,
    policy_version_id: str,
    evidence_refs: Iterable[str],
) -> Dict[str, Any]:
    refs = _refs(evidence_refs)
    if not refs:
        raise ValueError("tax preparation requires evidence")
    period = await db.accounting_periods.find_one({"id": period_id}, {"_id": 0})
    if not period:
        raise LookupError("accounting period not found")
    policy = await policy_registry.require_effective_version(policy_version_id)
    if policy.get("policy_key") != "ACCOUNTING_TAX_PREPARATION":
        raise ValueError("tax preparation requires ACCOUNTING_TAX_PREPARATION policy")
    invoices = await db.accounting_invoices.find(
        {"issued_at": {"$gte": period["starts_at"], "$lt": period["ends_at"]}},
        {"_id": 0},
    ).to_list(100000)
    gross = sum(int(row.get("amount_cents", 0)) for row in invoices if row.get("status") == "ISSUED")
    row = {
        "id": _id("TAXPKG"),
        "period_id": period_id,
        "policy_version_id": policy["id"],
        "policy_hash": policy["content_hash"],
        "gross_invoiced_cents": gross,
        "evidence_refs": refs,
        "status": "PREPARED",
        "tax_validated": False,
        "prepared_by": actor_id,
        "prepared_at": utc_now_iso(),
    }
    await db.accounting_tax_packages.insert_one(dict(row))
    return row


async def export_period_csv(period_id: str) -> Dict[str, Any]:
    period = await db.accounting_periods.find_one({"id": period_id}, {"_id": 0})
    if not period:
        raise LookupError("accounting period not found")
    invoices = await db.accounting_invoices.find(
        {"issued_at": {"$gte": period["starts_at"], "$lt": period["ends_at"]}},
        {"_id": 0},
    ).sort("issued_at", 1).to_list(100000)
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["number", "payment_id", "amount_cents", "currency", "issued_at"])
    for invoice in invoices:
        writer.writerow(
            [
                invoice.get("number"),
                invoice.get("payment_id"),
                invoice.get("amount_cents"),
                invoice.get("currency"),
                invoice.get("issued_at"),
            ]
        )
    text = output.getvalue()
    return {
        "period_id": period_id,
        "format": "CSV",
        "row_count": len(invoices),
        "content": text,
        "status": "EXPORT_GENERATED",
    }
