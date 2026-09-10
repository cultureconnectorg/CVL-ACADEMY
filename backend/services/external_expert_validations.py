"""Scoped expert validation/correction actions for EXP-PRIV/ACC/RISK/QUAL.

These actions never create new domain truth engines. They attach external review
records to canonical Academy records after XCP-006 case/scope authorization.
"""

from __future__ import annotations

import uuid
from typing import Any, Dict, Iterable

from db import db, utc_now_iso
from services import expert_access
from services import professional_governance as governance


def _id(prefix: str) -> str:
    return f"{prefix}-{uuid.uuid4()}"


def _refs(values: Iterable[str]) -> list[str]:
    return list(dict.fromkeys(str(v).strip() for v in values if str(v).strip()))


async def accountant_review_reconciliation(
    *,
    raw_key: str,
    case_id: str,
    reconciliation_id: str,
    outcome: str,
    rationale: str,
    evidence_refs: Iterable[str],
) -> Dict[str, Any]:
    ctx = await expert_access.authorize_case_scope(
        raw_key, case_id, "accounting:reconciliation:review"
    )
    case = await db.professional_cases.find_one({"id": case_id}, {"_id": 0})
    recon = await db.accounting_reconciliations.find_one(
        {"id": reconciliation_id}, {"_id": 0}
    )
    if not case or str(case.get("domain", "")).upper() != "ACCOUNTING":
        raise PermissionError("reconciliation review requires ACCOUNTING case")
    if not recon:
        raise LookupError("accounting reconciliation not found")
    period_ids = list((case.get("metadata") or {}).get("accounting_period_ids", []))
    periods = await db.accounting_periods.find(
        {"id": {"$in": period_ids}}, {"_id": 0}
    ).to_list(500)
    payment = await db.payments.find_one({"id": recon["payment_id"]}, {"_id": 0})
    if not payment or not any(
        period["starts_at"] <= payment.get("created_at", "") < period["ends_at"]
        for period in periods
    ):
        raise PermissionError("reconciliation is outside assigned accounting periods")
    target = str(outcome or "").upper()
    if target not in {"VALIDATED", "REJECTED", "CORRECTION_REQUIRED"}:
        raise ValueError("invalid reconciliation review outcome")
    refs = _refs(evidence_refs)
    if not rationale.strip() or not refs:
        raise ValueError("reconciliation review requires rationale and evidence")
    row = {
        "id": _id("ACCREV"),
        "case_id": case_id,
        "reconciliation_id": reconciliation_id,
        "payment_id": recon["payment_id"],
        "outcome": target,
        "rationale": rationale.strip(),
        "evidence_refs": refs,
        "expert_id": ctx["expert"]["id"],
        "status": "EXTERNAL_ACCOUNTING_REVIEW",
        "created_at": utc_now_iso(),
    }
    await db.accounting_external_reviews.insert_one(dict(row))
    await governance.audit_event(
        event_type="accounting.external_reconciliation_review.recorded",
        actor_id=ctx["expert"]["id"],
        resource_type="accounting_reconciliation",
        resource_id=reconciliation_id,
        payload={"review_id": row["id"], "outcome": target, "evidence_refs": refs},
        reason=rationale.strip(),
        result=target,
    )
    return row


async def accountant_validate_tax_package(
    *,
    raw_key: str,
    case_id: str,
    tax_package_id: str,
    outcome: str,
    rationale: str,
    evidence_refs: Iterable[str],
) -> Dict[str, Any]:
    ctx = await expert_access.authorize_case_scope(
        raw_key, case_id, "accounting:tax:review"
    )
    case = await db.professional_cases.find_one({"id": case_id}, {"_id": 0})
    package = await db.accounting_tax_packages.find_one(
        {"id": tax_package_id}, {"_id": 0}
    )
    if not case or str(case.get("domain", "")).upper() != "ACCOUNTING":
        raise PermissionError("tax review requires ACCOUNTING case")
    if not package:
        raise LookupError("tax package not found")
    allowed_periods = set((case.get("metadata") or {}).get("accounting_period_ids", []))
    if package.get("period_id") not in allowed_periods:
        raise PermissionError("tax package is outside assigned accounting periods")
    target = str(outcome or "").upper()
    if target not in {"EXPERT_VALIDATED", "REJECTED", "CORRECTION_REQUIRED"}:
        raise ValueError("invalid tax package review outcome")
    refs = _refs(evidence_refs)
    if not rationale.strip() or not refs:
        raise ValueError("tax package review requires rationale and evidence")
    row = {
        "id": _id("TAXREV"),
        "case_id": case_id,
        "tax_package_id": tax_package_id,
        "period_id": package["period_id"],
        "outcome": target,
        "rationale": rationale.strip(),
        "evidence_refs": refs,
        "expert_id": ctx["expert"]["id"],
        "status": "EXTERNAL_TAX_REVIEW",
        "created_at": utc_now_iso(),
    }
    await db.accounting_tax_reviews.insert_one(dict(row))
    await db.accounting_tax_packages.update_one(
        {"id": tax_package_id},
        {
            "$set": {
                "external_review_id": row["id"],
                "external_review_outcome": target,
                "tax_validated": target == "EXPERT_VALIDATED",
                "tax_validation_status": (
                    "EXPERT_VALIDATED_WITH_EVIDENCE"
                    if target == "EXPERT_VALIDATED"
                    else target
                ),
            }
        },
    )
    await governance.audit_event(
        event_type="accounting.external_tax_review.recorded",
        actor_id=ctx["expert"]["id"],
        resource_type="accounting_tax_package",
        resource_id=tax_package_id,
        payload={"review_id": row["id"], "outcome": target, "evidence_refs": refs},
        reason=rationale.strip(),
        result=target,
    )
    return row


async def privacy_validate_processing_activity(
    *,
    raw_key: str,
    case_id: str,
    activity_id: str,
    outcome: str,
    rationale: str,
    evidence_refs: Iterable[str],
) -> Dict[str, Any]:
    ctx = await expert_access.authorize_case_scope(
        raw_key, case_id, "privacy:processing:review"
    )
    case = await db.professional_cases.find_one({"id": case_id}, {"_id": 0})
    activity = await db.privacy_processing_activities.find_one(
        {"id": activity_id}, {"_id": 0}
    )
    if not case or str(case.get("domain", "")).upper() != "PRIVACY":
        raise PermissionError("processing review requires PRIVACY case")
    if not activity:
        raise LookupError("processing activity not found")
    allowed = set((case.get("metadata") or {}).get("processing_activity_ids", []))
    if activity_id not in allowed:
        raise PermissionError("processing activity is outside assigned privacy case")
    target = str(outcome or "").upper()
    if target not in {"VALIDATED", "REJECTED", "CORRECTION_REQUIRED"}:
        raise ValueError("invalid processing activity review outcome")
    refs = _refs(evidence_refs)
    if not rationale.strip() or not refs:
        raise ValueError("processing review requires rationale and evidence")
    row = {
        "id": _id("DPOREV"),
        "case_id": case_id,
        "processing_activity_id": activity_id,
        "outcome": target,
        "rationale": rationale.strip(),
        "evidence_refs": refs,
        "expert_id": ctx["expert"]["id"],
        "status": "EXTERNAL_PRIVACY_REVIEW",
        "created_at": utc_now_iso(),
    }
    await db.privacy_processing_external_reviews.insert_one(dict(row))
    await governance.audit_event(
        event_type="privacy.external_processing_review.recorded",
        actor_id=ctx["expert"]["id"],
        resource_type="processing_activity",
        resource_id=activity_id,
        payload={"review_id": row["id"], "outcome": target, "evidence_refs": refs},
        reason=rationale.strip(),
        result=target,
    )
    return row


async def broker_record_recommendation(
    *,
    raw_key: str,
    case_id: str,
    risk_id: str,
    recommendation: str,
    rationale: str,
    evidence_refs: Iterable[str],
) -> Dict[str, Any]:
    ctx = await expert_access.authorize_case_scope(
        raw_key, case_id, "risk:recommendation:write"
    )
    case = await db.professional_cases.find_one({"id": case_id}, {"_id": 0})
    risk = await db.risks.find_one({"id": risk_id}, {"_id": 0})
    if not case or str(case.get("domain", "")).upper() != "RISK":
        raise PermissionError("broker recommendation requires RISK case")
    allowed = set((case.get("metadata") or {}).get("risk_ids", []))
    if risk_id not in allowed or not risk:
        raise PermissionError("risk is outside assigned broker case")
    refs = _refs(evidence_refs)
    if not recommendation.strip() or not rationale.strip() or not refs:
        raise ValueError("broker recommendation requires recommendation, rationale and evidence")
    row = {
        "id": _id("BROKERREC"),
        "case_id": case_id,
        "risk_id": risk_id,
        "recommendation": recommendation.strip(),
        "rationale": rationale.strip(),
        "evidence_refs": refs,
        "expert_id": ctx["expert"]["id"],
        "status": "EXTERNAL_RECOMMENDATION_ONLY",
        "created_at": utc_now_iso(),
    }
    await db.risk_broker_recommendations.insert_one(dict(row))
    return row


async def quality_record_correction(
    *,
    raw_key: str,
    case_id: str,
    evidence_id: str,
    correction: Dict[str, Any],
    rationale: str,
    evidence_refs: Iterable[str],
) -> Dict[str, Any]:
    ctx = await expert_access.authorize_case_scope(
        raw_key, case_id, "quality:evidence:correct"
    )
    case = await db.professional_cases.find_one({"id": case_id}, {"_id": 0})
    source = await db.quality_learner_evidence.find_one({"id": evidence_id}, {"_id": 0})
    if not case or str(case.get("domain", "")).upper() != "QUALITY":
        raise PermissionError("quality correction requires QUALITY case")
    if not source:
        raise LookupError("quality evidence not found")
    scope_ids = list((case.get("metadata") or {}).get("quality_scope_ids", []))
    scopes = await db.quality_scopes.find(
        {"id": {"$in": scope_ids}, "status": "ACTIVE"}, {"_id": 0}
    ).to_list(500)
    formations = {scope["formation_code"] for scope in scopes}
    if source.get("formation_code") not in formations:
        raise PermissionError("quality evidence is outside assigned case")
    refs = _refs(evidence_refs)
    if not correction or not rationale.strip() or not refs:
        raise ValueError("quality correction requires patch, rationale and evidence")
    row = {
        "id": _id("QCORR"),
        "case_id": case_id,
        "quality_evidence_id": evidence_id,
        "correction": correction,
        "rationale": rationale.strip(),
        "evidence_refs": refs,
        "expert_id": ctx["expert"]["id"],
        "status": "PROPOSED_CORRECTION",
        "created_at": utc_now_iso(),
    }
    await db.quality_external_corrections.insert_one(dict(row))
    await governance.audit_event(
        event_type="quality.external_correction.recorded",
        actor_id=ctx["expert"]["id"],
        resource_type="quality_evidence",
        resource_id=evidence_id,
        payload={"correction_id": row["id"], "evidence_refs": refs},
        reason=rationale.strip(),
        result="PROPOSED_CORRECTION",
    )
    return row
