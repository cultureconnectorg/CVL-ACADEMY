"""Accounting protocol controls (ACC-05/06/16/18/21).

These controls extend the existing accounting stores. They do not invent tax treatment,
FEC compliance or revenue-recognition rules: mappings/policies and external validation
remain explicit evidence-bearing inputs.
"""

from __future__ import annotations

import uuid
from typing import Any, Dict, Iterable, Optional

from db import db, utc_now_iso
from services import policy_registry
from services import professional_governance as governance


def _id(prefix: str) -> str:
    return f"{prefix}-{uuid.uuid4()}"


def _refs(values: Iterable[str]) -> list[str]:
    return list(dict.fromkeys(str(v).strip() for v in values if str(v).strip()))


async def record_refund_accounting_event(
    *, actor_id: str, refund_ref: str, payment_id: str, amount_cents: int,
    currency: str, evidence_refs: Iterable[str], credit_note_id: Optional[str] = None
) -> Dict[str, Any]:
    refs = _refs(evidence_refs)
    if amount_cents <= 0 or not refund_ref.strip() or not refs:
        raise ValueError("refund accounting event requires positive amount, refund ref and evidence")
    payment = await db.payments.find_one({"id": payment_id}, {"_id": 0})
    if not payment:
        raise LookupError("payment not found")
    if credit_note_id:
        note = await db.accounting_credit_notes.find_one({"id": credit_note_id}, {"_id": 0})
        if not note:
            raise LookupError("credit note not found")
        if int(note.get("amount_cents", 0)) != int(amount_cents):
            raise ValueError("credit note amount does not match refund event")
    existing = await db.accounting_events.find_one({"source_type": "REFUND", "source_ref": refund_ref.strip()}, {"_id": 0})
    if existing:
        return existing
    row = {
        "id": _id("ACCEVT"), "event_type": "REFUND", "source_type": "REFUND",
        "source_ref": refund_ref.strip(), "payment_id": payment_id,
        "amount_cents": int(amount_cents), "currency": currency.strip().upper(),
        "credit_note_id": credit_note_id, "evidence_refs": refs,
        "posting_status": "UNMAPPED", "created_by": actor_id, "created_at": utc_now_iso(),
    }
    await db.accounting_events.insert_one(dict(row))
    return row


async def prepare_revenue_recognition(
    *, actor_id: str, source_ref: str, amount_cents: int, currency: str,
    recognition_date: str, policy_version_id: str, dimensions: Dict[str, Any],
    evidence_refs: Iterable[str]
) -> Dict[str, Any]:
    refs = _refs(evidence_refs)
    if amount_cents < 0 or not source_ref.strip() or not recognition_date.strip() or not refs:
        raise ValueError("revenue recognition preparation requires source, amount, date and evidence")
    policy = await policy_registry.require_effective_version(policy_version_id)
    if policy.get("policy_key") != "REVENUE_RECOGNITION":
        raise ValueError("revenue recognition requires REVENUE_RECOGNITION policy")
    row = {
        "id": _id("REVREC"), "source_ref": source_ref.strip(), "amount_cents": int(amount_cents),
        "currency": currency.strip().upper(), "recognition_date": recognition_date.strip(),
        "dimensions": dimensions, "policy_version_id": policy["id"], "policy_hash": policy["content_hash"],
        "evidence_refs": refs, "status": "PREPARED_NOT_VALIDATED",
        "prepared_by": actor_id, "prepared_at": utc_now_iso(),
    }
    await db.accounting_revenue_recognition.insert_one(dict(row))
    return row


async def register_missing_supporting_document(
    *, actor_id: str, period_id: str, expected_document_type: str,
    source_ref: str, owner: str, due_at: str, evidence_refs: Iterable[str]
) -> Dict[str, Any]:
    period = await db.accounting_periods.find_one({"id": period_id}, {"_id": 0})
    if not period:
        raise LookupError("accounting period not found")
    refs = _refs(evidence_refs)
    if not all(str(v).strip() for v in (expected_document_type, source_ref, owner, due_at)) or not refs:
        raise ValueError("missing-document record requires type, source, owner, due date and evidence")
    row = {
        "id": _id("MISSDOC"), "period_id": period_id,
        "expected_document_type": expected_document_type.strip().upper(),
        "source_ref": source_ref.strip(), "owner": owner.strip(), "due_at": due_at.strip(),
        "evidence_refs": refs, "status": "OPEN", "resolved_document_id": None,
        "created_by": actor_id, "created_at": utc_now_iso(), "updated_at": utc_now_iso(),
    }
    await db.accounting_missing_documents.insert_one(dict(row))
    return row


async def resolve_missing_supporting_document(
    *, actor_id: str, missing_document_id: str, supporting_document_id: str,
    evidence_refs: Iterable[str]
) -> Dict[str, Any]:
    row = await db.accounting_missing_documents.find_one({"id": missing_document_id}, {"_id": 0})
    doc = await db.accounting_supporting_documents.find_one({"id": supporting_document_id}, {"_id": 0})
    if not row or not doc:
        raise LookupError("missing-document record or supporting document not found")
    refs = _refs(evidence_refs)
    if not refs:
        raise ValueError("missing-document resolution requires evidence")
    now = utc_now_iso()
    update = {"status": "RESOLVED", "resolved_document_id": supporting_document_id,
              "resolution_evidence_refs": refs, "resolved_by": actor_id, "resolved_at": now, "updated_at": now}
    await db.accounting_missing_documents.update_one({"id": missing_document_id, "status": "OPEN"}, {"$set": update})
    return {**row, **update}


async def fec_readiness_gate(*, period_id: str) -> Dict[str, Any]:
    """ACC-18 readiness only. This never claims a legally valid FEC file."""
    if not await db.accounting_periods.find_one({"id": period_id}):
        raise LookupError("accounting period not found")
    missing_docs = await db.accounting_missing_documents.find({"period_id": period_id, "status": "OPEN"}, {"_id": 0}).to_list(10000)
    unmapped = await db.accounting_events.find({"period_id": period_id, "posting_status": "UNMAPPED"}, {"_id": 0}).to_list(10000)
    mapping_errors = await db.accounting_period_anomalies.find({"period_id": period_id, "status": "OPEN"}, {"_id": 0}).to_list(10000)
    blockers = len(missing_docs) + len(unmapped) + len(mapping_errors)
    return {
        "period_id": period_id, "pass": blockers == 0, "blocking_count": blockers,
        "missing_documents": missing_docs, "unmapped_events": unmapped,
        "open_anomalies": mapping_errors, "fec_generated": False,
        "legal_compliance_claimed": False,
    }


async def register_financial_retention_policy(
    *, actor_id: str, record_type: str, retention_days: int,
    trigger: str, policy_version_id: str, evidence_refs: Iterable[str]
) -> Dict[str, Any]:
    refs = _refs(evidence_refs)
    if retention_days < 0 or not record_type.strip() or not trigger.strip() or not refs:
        raise ValueError("financial retention requires record type, retention, trigger and evidence")
    policy = await policy_registry.require_effective_version(policy_version_id)
    if policy.get("policy_key") != "FINANCIAL_RETENTION":
        raise ValueError("financial retention requires FINANCIAL_RETENTION policy")
    row = {
        "id": _id("ACCRET"), "record_type": record_type.strip().upper(),
        "retention_days": int(retention_days), "trigger": trigger.strip().upper(),
        "policy_version_id": policy["id"], "policy_hash": policy["content_hash"],
        "evidence_refs": refs, "status": "ACTIVE", "created_by": actor_id,
        "created_at": utc_now_iso(),
    }
    await db.accounting_retention_policies.update_one(
        {"record_type": row["record_type"], "status": "ACTIVE"}, {"$set": row}, upsert=True
    )
    await governance.audit_event(
        event_type="accounting.retention_policy.registered", actor_id=actor_id,
        resource_type="accounting_retention_policy", resource_id=row["id"],
        payload={"record_type": row["record_type"], "retention_days": row["retention_days"], "policy_version_id": policy["id"]}
    )
    return row
