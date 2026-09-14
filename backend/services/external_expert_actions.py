"""Scoped write actions for external experts (EXP-*).

Every action reuses XCP-006 credentials and case assignments. The service exposes no
global browsing and never upgrades external advice into CVL authority automatically.
"""

from __future__ import annotations

import uuid
from typing import Any, Dict, Iterable, Optional

from db import db, utc_now_iso
from services import accounting_mappings, expert_access, risk_advanced
from services import professional_governance as governance


def _id(prefix: str) -> str:
    return f"{prefix}-{uuid.uuid4()}"


def _refs(values: Iterable[str]) -> list[str]:
    return list(dict.fromkeys(str(v).strip() for v in values if str(v).strip()))


async def privacy_review_processor(
    *,
    raw_key: str,
    case_id: str,
    processor_id: str,
    recommendation: str,
    rationale: str,
    evidence_refs: Iterable[str],
) -> Dict[str, Any]:
    context = await expert_access.authorize_case_scope(raw_key, case_id, "privacy:processor:review")
    case = await db.professional_cases.find_one({"id": case_id}, {"_id": 0})
    processor = await db.privacy_processors.find_one({"id": processor_id}, {"_id": 0})
    if not case or str(case.get("domain", "")).upper() != "PRIVACY":
        raise PermissionError("expert action requires PRIVACY case")
    allowed = set((case.get("metadata") or {}).get("processor_ids", []))
    if processor_id not in allowed or not processor:
        raise PermissionError("processor is outside assigned privacy case")
    refs = _refs(evidence_refs)
    decision = str(recommendation or "").upper()
    if decision not in {"APPROVE", "REJECT", "REVIEW"}:
        raise ValueError("invalid processor recommendation")
    if not rationale.strip() or not refs:
        raise ValueError("processor review requires rationale and evidence")
    row = {
        "id": _id("EXPREV"),
        "case_id": case_id,
        "processor_id": processor_id,
        "recommendation": decision,
        "rationale": rationale.strip(),
        "evidence_refs": refs,
        "expert_id": context["expert"]["id"],
        "status": "EXTERNAL_RECOMMENDATION_ONLY",
        "created_at": utc_now_iso(),
    }
    await db.privacy_external_reviews.insert_one(dict(row))
    await governance.audit_event(
        event_type="privacy.external_processor_review.recorded",
        actor_id=context["expert"]["id"],
        resource_type="privacy_processor",
        resource_id=processor_id,
        payload={"review_id": row["id"], "recommendation": decision, "evidence_refs": refs},
        reason=rationale.strip(),
        result="EXTERNAL_RECOMMENDATION_ONLY",
    )
    return row


async def submit_pentest_finding(
    *,
    raw_key: str,
    case_id: str,
    title: str,
    severity: str,
    attack_surface: str,
    evidence_refs: Iterable[str],
    remediation_recommendation: str,
) -> Dict[str, Any]:
    context = await expert_access.authorize_case_scope(raw_key, case_id, "security:pentest:submit")
    case = await db.professional_cases.find_one({"id": case_id}, {"_id": 0})
    if not case or str(case.get("domain", "")).upper() != "SECURITY":
        raise PermissionError("pentest submission requires SECURITY case")
    sev = str(severity or "").upper()
    if sev not in {"LOW", "MEDIUM", "HIGH", "CRITICAL"}:
        raise ValueError("invalid finding severity")
    refs = _refs(evidence_refs)
    if not title.strip() or not attack_surface.strip() or not refs:
        raise ValueError("pentest finding requires title, attack surface and evidence")
    row = {
        "id": _id("PENTESTF"),
        "case_id": case_id,
        "title": title.strip(),
        "severity": sev,
        "attack_surface": attack_surface.strip(),
        "evidence_refs": refs,
        "remediation_recommendation": remediation_recommendation.strip(),
        "expert_id": context["expert"]["id"],
        "status": "SUBMITTED_EXTERNAL",
        "created_at": utc_now_iso(),
    }
    await db.external_pentest_findings.insert_one(dict(row))
    await governance.audit_event(
        event_type="security.external_pentest_finding.submitted",
        actor_id=context["expert"]["id"],
        resource_type="professional_case",
        resource_id=case_id,
        payload={"finding_id": row["id"], "severity": sev, "evidence_refs": refs},
        result="SUBMITTED_EXTERNAL",
    )
    return row


async def submit_pentest_retest(
    *,
    raw_key: str,
    case_id: str,
    finding_id: str,
    outcome: str,
    evidence_refs: Iterable[str],
) -> Dict[str, Any]:
    context = await expert_access.authorize_case_scope(raw_key, case_id, "security:pentest:retest")
    finding = await db.external_pentest_findings.find_one(
        {"id": finding_id, "case_id": case_id}, {"_id": 0}
    )
    if not finding:
        raise LookupError("external pentest finding not found in assigned case")
    result = str(outcome or "").upper()
    if result not in {"PASS", "FAIL"}:
        raise ValueError("retest outcome must be PASS or FAIL")
    refs = _refs(evidence_refs)
    if not refs:
        raise ValueError("retest requires evidence")
    row = {
        "id": _id("PENTESTRT"),
        "case_id": case_id,
        "finding_id": finding_id,
        "outcome": result,
        "evidence_refs": refs,
        "expert_id": context["expert"]["id"],
        "created_at": utc_now_iso(),
    }
    await db.external_pentest_retests.insert_one(dict(row))
    await governance.audit_event(
        event_type="security.external_pentest_retest.submitted",
        actor_id=context["expert"]["id"],
        resource_type="external_pentest_finding",
        resource_id=finding_id,
        payload={"retest_id": row["id"], "outcome": result, "evidence_refs": refs},
        result=result,
    )
    return row


async def accountant_define_mapping(
    *,
    raw_key: str,
    case_id: str,
    event_type: str,
    debit_account: str,
    credit_account: str,
    version: str,
    effective_at: str,
    evidence_refs: Iterable[str],
    tax_code: Optional[str] = None,
    supersedes_version_id: Optional[str] = None,
) -> Dict[str, Any]:
    context = await expert_access.authorize_case_scope(raw_key, case_id, "accounting:mapping:write")
    case = await db.professional_cases.find_one({"id": case_id}, {"_id": 0})
    if not case or str(case.get("domain", "")).upper() != "ACCOUNTING":
        raise PermissionError("mapping action requires ACCOUNTING case")
    allowed = {str(v).upper() for v in (case.get("metadata") or {}).get("allowed_event_types", [])}
    event = str(event_type or "").upper()
    if allowed and event not in allowed:
        raise PermissionError("accounting event type outside assigned case")
    return await accounting_mappings.register_mapping_version(
        actor_id=context["expert"]["id"],
        event_type=event,
        debit_account=debit_account,
        credit_account=credit_account,
        version=version,
        effective_at=effective_at,
        evidence_refs=evidence_refs,
        tax_code=tax_code,
        supersedes_version_id=supersedes_version_id,
    )


async def broker_review_coverage(
    *,
    raw_key: str,
    case_id: str,
    link_id: str,
    coverage_confirmed: bool,
    rationale: str,
    evidence_refs: Iterable[str],
) -> Dict[str, Any]:
    context = await expert_access.authorize_case_scope(raw_key, case_id, "risk:coverage:review")
    case = await db.professional_cases.find_one({"id": case_id}, {"_id": 0})
    link = await db.risk_insurance_links.find_one({"id": link_id}, {"_id": 0})
    if not case or str(case.get("domain", "")).upper() != "RISK":
        raise PermissionError("coverage review requires RISK case")
    allowed_risks = set((case.get("metadata") or {}).get("risk_ids", []))
    if not link or link.get("risk_id") not in allowed_risks:
        raise PermissionError("coverage link outside assigned risk case")
    return await risk_advanced.review_coverage_link(
        actor_id=context["expert"]["id"],
        link_id=link_id,
        coverage_confirmed=coverage_confirmed,
        rationale=rationale,
        evidence_refs=evidence_refs,
    )


async def quality_review_evidence(
    *,
    raw_key: str,
    case_id: str,
    evidence_id: str,
    outcome: str,
    rationale: str,
    evidence_refs: Iterable[str],
) -> Dict[str, Any]:
    context = await expert_access.authorize_case_scope(raw_key, case_id, "quality:evidence:review")
    case = await db.professional_cases.find_one({"id": case_id}, {"_id": 0})
    if not case or str(case.get("domain", "")).upper() != "QUALITY":
        raise PermissionError("quality review requires QUALITY case")
    source = await db.quality_learner_evidence.find_one({"id": evidence_id}, {"_id": 0})
    if not source:
        raise LookupError("quality evidence not found")
    allowed_scope_ids = set((case.get("metadata") or {}).get("quality_scope_ids", []))
    scopes = await db.quality_scopes.find(
        {"id": {"$in": list(allowed_scope_ids)}, "status": "ACTIVE"}, {"_id": 0}
    ).to_list(500)
    allowed_formations = {scope["formation_code"] for scope in scopes}
    if source.get("formation_code") not in allowed_formations:
        raise PermissionError("quality evidence outside assigned case")
    target = str(outcome or "").upper()
    if target not in {"ACCEPT", "CORRECT", "REJECT"}:
        raise ValueError("invalid quality review outcome")
    refs = _refs(evidence_refs)
    if not rationale.strip() or not refs:
        raise ValueError("quality review requires rationale and evidence")
    row = {
        "id": _id("QEXTREV"),
        "case_id": case_id,
        "quality_evidence_id": evidence_id,
        "outcome": target,
        "rationale": rationale.strip(),
        "evidence_refs": refs,
        "expert_id": context["expert"]["id"],
        "status": "EXTERNAL_QUALITY_REVIEW",
        "created_at": utc_now_iso(),
    }
    await db.quality_external_reviews.insert_one(dict(row))
    await governance.audit_event(
        event_type="quality.external_review.recorded",
        actor_id=context["expert"]["id"],
        resource_type="quality_evidence",
        resource_id=evidence_id,
        payload={"review_id": row["id"], "outcome": target, "evidence_refs": refs},
        reason=rationale.strip(),
        result=target,
    )
    return row
