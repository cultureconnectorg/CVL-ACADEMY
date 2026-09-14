"""Assurance Core for CVLN Academy.

Concrete P0 primitives derived from the Academy integration masters for
LEGAL, PRIVACY, SECURITY and RISK. The module deliberately records policy,
review and evidence state; it does not pretend to replace lawyers, DPOs,
security auditors, insurers or external authorities.
"""

from __future__ import annotations

import hashlib
import json
import uuid
from typing import Any, Dict, Iterable, Optional

from db import db, utc_now_iso


LEGAL_DOC_STATES = {"DRAFT", "REVIEW", "APPROVED", "SIGNED", "PUBLISHED", "SUPERSEDED"}
DSAR_STATES = {"OPEN", "IDENTITY_CHECK", "IN_REVIEW", "READY", "COMPLETED", "REJECTED"}
PRIVACY_INCIDENT_STATES = {"OPEN", "CONTAINED", "ASSESSED", "CLOSED"}
SECURITY_FINDING_STATES = {"OPEN", "REMEDIATING", "RETEST", "RESOLVED", "ACCEPTED"}
RISK_TREATMENTS = {"ACCEPT", "MITIGATE", "TRANSFER_INSURE", "ESCALATE", "BLOCK"}
RISK_STATES = {"OPEN", "TREATING", "ACCEPTED", "MITIGATED", "TRANSFERRED", "BLOCKED", "CLOSED"}


def _id(prefix: str) -> str:
    return f"{prefix}-{uuid.uuid4()}"


def _hash(payload: Dict[str, Any]) -> str:
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str)
    return hashlib.sha256(raw.encode()).hexdigest()


async def _audit(event_type: str, actor_id: str, resource_type: str, resource_id: str, payload: Dict[str, Any]) -> None:
    event = {
        "id": _id("AUD"),
        "event_type": event_type,
        "actor_id": actor_id,
        "resource_type": resource_type,
        "resource_id": resource_id,
        "payload": payload,
        "payload_hash": _hash(payload),
        "created_at": utc_now_iso(),
    }
    await db.governance_audit_events.insert_one(event)


# ---------------- LEGAL ----------------
async def create_legal_document(
    *, actor_id: str, title: str, document_type: str, case_id: Optional[str] = None,
    jurisdiction: Optional[str] = None, metadata: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    doc = {
        "id": _id("LDOC"), "title": title, "document_type": document_type.upper(),
        "case_id": case_id, "jurisdiction": jurisdiction, "state": "DRAFT",
        "current_version_id": None, "metadata": metadata or {}, "created_by": actor_id,
        "created_at": utc_now_iso(), "updated_at": utc_now_iso(),
    }
    await db.legal_documents.insert_one(dict(doc))
    await _audit("legal.document.created", actor_id, "legal_document", doc["id"], {"type": doc["document_type"]})
    return doc


async def transition_legal_document(*, actor_id: str, document_id: str, state: str) -> Dict[str, Any]:
    target = state.upper()
    if target not in LEGAL_DOC_STATES:
        raise ValueError("invalid legal document state")
    doc = await db.legal_documents.find_one({"id": document_id}, {"_id": 0})
    if not doc:
        raise LookupError("legal document not found")
    allowed = {
        "DRAFT": {"REVIEW"}, "REVIEW": {"DRAFT", "APPROVED"}, "APPROVED": {"SIGNED", "SUPERSEDED"},
        "SIGNED": {"PUBLISHED", "SUPERSEDED"}, "PUBLISHED": {"SUPERSEDED"}, "SUPERSEDED": set(),
    }
    if target not in allowed[doc["state"]]:
        raise ValueError(f"invalid legal transition {doc['state']}->{target}")
    now = utc_now_iso()
    await db.legal_documents.update_one({"id": document_id}, {"$set": {"state": target, "updated_at": now}})
    await _audit("legal.document.state_changed", actor_id, "legal_document", document_id, {"from": doc["state"], "to": target})
    return {**doc, "state": target, "updated_at": now}


async def register_clause(*, actor_id: str, code: str, title: str, text_hash: str, version: int, tags: Iterable[str] = ()) -> Dict[str, Any]:
    clause = {
        "id": _id("CLAUSE"), "code": code.upper(), "title": title, "text_hash": text_hash.lower(),
        "version": version, "tags": sorted(set(tags)), "status": "ACTIVE", "created_by": actor_id,
        "created_at": utc_now_iso(),
    }
    await db.legal_clauses.insert_one(dict(clause))
    await _audit("legal.clause.registered", actor_id, "legal_clause", clause["id"], {"code": clause["code"], "version": version})
    return clause


async def link_clause_usage(*, actor_id: str, document_id: str, clause_id: str) -> Dict[str, Any]:
    if not await db.legal_documents.find_one({"id": document_id}):
        raise LookupError("legal document not found")
    if not await db.legal_clauses.find_one({"id": clause_id}):
        raise LookupError("clause not found")
    usage = {"id": _id("CLUS"), "document_id": document_id, "clause_id": clause_id, "linked_at": utc_now_iso(), "linked_by": actor_id}
    await db.legal_clause_usage.insert_one(dict(usage))
    return usage


async def clause_impact(clause_id: str) -> list[Dict[str, Any]]:
    return await db.legal_clause_usage.find({"clause_id": clause_id}, {"_id": 0}).to_list(1000)


# ---------------- PRIVACY ----------------
async def register_data_class(*, actor_id: str, code: str, name: str, sensitivity: str, retention_days: Optional[int], legal_basis_required: bool = True) -> Dict[str, Any]:
    row = {
        "id": _id("DCLASS"), "code": code.upper(), "name": name, "sensitivity": sensitivity.upper(),
        "retention_days": retention_days, "legal_basis_required": legal_basis_required,
        "created_by": actor_id, "created_at": utc_now_iso(),
    }
    await db.privacy_data_classes.update_one({"code": row["code"]}, {"$set": row}, upsert=True)
    await _audit("privacy.data_class.registered", actor_id, "privacy_data_class", row["id"], {"code": row["code"]})
    return row


async def register_processing_activity(*, actor_id: str, name: str, purpose: str, data_classes: Iterable[str], legal_basis: str, processors: Iterable[str] = (), regions: Iterable[str] = ()) -> Dict[str, Any]:
    row = {
        "id": _id("ROPA"), "name": name, "purpose": purpose, "data_classes": sorted(set(data_classes)),
        "legal_basis": legal_basis, "processors": sorted(set(processors)), "regions": sorted(set(regions)),
        "status": "ACTIVE", "created_by": actor_id, "created_at": utc_now_iso(), "updated_at": utc_now_iso(),
    }
    await db.privacy_processing_activities.insert_one(dict(row))
    await _audit("privacy.processing_activity.registered", actor_id, "processing_activity", row["id"], {"legal_basis": legal_basis})
    return row


async def record_consent(*, actor_id: str, user_id: str, purpose: str, policy_version: str, granted: bool, evidence: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    row = {
        "id": _id("CONSENT"), "user_id": user_id, "purpose": purpose, "policy_version": policy_version,
        "granted": granted, "evidence": evidence or {}, "recorded_by": actor_id, "recorded_at": utc_now_iso(),
    }
    row["evidence_hash"] = _hash(row["evidence"])
    await db.privacy_consents.insert_one(dict(row))
    await _audit("privacy.consent.recorded", actor_id, "user", user_id, {"purpose": purpose, "granted": granted, "policy_version": policy_version})
    return row


async def current_consents(user_id: str) -> Dict[str, bool]:
    rows = await db.privacy_consents.find({"user_id": user_id}, {"_id": 0}).sort("recorded_at", 1).to_list(5000)
    current: Dict[str, bool] = {}
    for row in rows:
        current[row["purpose"]] = bool(row["granted"])
    return current


async def create_dsar(*, actor_id: str, user_id: str, request_type: str) -> Dict[str, Any]:
    row = {"id": _id("DSAR"), "user_id": user_id, "request_type": request_type.upper(), "status": "OPEN", "created_by": actor_id, "created_at": utc_now_iso(), "updated_at": utc_now_iso()}
    await db.privacy_dsar.insert_one(dict(row))
    await _audit("privacy.dsar.created", actor_id, "dsar", row["id"], {"user_id": user_id, "request_type": row["request_type"]})
    return row


async def create_privacy_incident(*, actor_id: str, title: str, severity: str, data_classes: Iterable[str], description: str) -> Dict[str, Any]:
    row = {"id": _id("PINC"), "title": title, "severity": severity.upper(), "data_classes": sorted(set(data_classes)), "description": description, "status": "OPEN", "created_by": actor_id, "created_at": utc_now_iso()}
    await db.privacy_incidents.insert_one(dict(row))
    await _audit("privacy.incident.created", actor_id, "privacy_incident", row["id"], {"severity": row["severity"], "data_classes": row["data_classes"]})
    return row


# ---------------- SECURITY ----------------
async def create_security_asset(*, actor_id: str, name: str, asset_type: str, owner: str, exposure: str, criticality: str) -> Dict[str, Any]:
    row = {"id": _id("ASSET"), "name": name, "asset_type": asset_type.upper(), "owner": owner, "exposure": exposure.upper(), "criticality": criticality.upper(), "created_by": actor_id, "created_at": utc_now_iso()}
    await db.security_assets.insert_one(dict(row))
    return row


async def create_security_finding(*, actor_id: str, title: str, severity: str, asset_id: Optional[str], evidence_refs: Iterable[str], remediation: str) -> Dict[str, Any]:
    sev = severity.upper()
    if sev not in {"LOW", "MEDIUM", "HIGH", "CRITICAL"}:
        raise ValueError("invalid severity")
    row = {"id": _id("FIND"), "title": title, "severity": sev, "asset_id": asset_id, "evidence_refs": list(evidence_refs), "remediation": remediation, "status": "OPEN", "created_by": actor_id, "created_at": utc_now_iso(), "updated_at": utc_now_iso()}
    await db.security_findings.insert_one(dict(row))
    await _audit("security.finding.created", actor_id, "security_finding", row["id"], {"severity": sev, "asset_id": asset_id})
    return row


async def accept_security_risk(*, actor_id: str, finding_id: str, rationale: str, expires_at: str) -> Dict[str, Any]:
    finding = await db.security_findings.find_one({"id": finding_id}, {"_id": 0})
    if not finding:
        raise LookupError("security finding not found")
    row = {"id": _id("RACC"), "finding_id": finding_id, "rationale": rationale, "accepted_by": actor_id, "expires_at": expires_at, "created_at": utc_now_iso()}
    await db.security_risk_acceptances.insert_one(dict(row))
    await db.security_findings.update_one({"id": finding_id}, {"$set": {"status": "ACCEPTED", "updated_at": utc_now_iso()}})
    await _audit("security.risk.accepted", actor_id, "security_finding", finding_id, {"acceptance_id": row["id"], "expires_at": expires_at})
    return row


async def release_security_gate() -> Dict[str, Any]:
    blockers = await db.security_findings.find({"severity": {"$in": ["HIGH", "CRITICAL"]}, "status": {"$nin": ["RESOLVED", "ACCEPTED"]}}, {"_id": 0}).to_list(1000)
    return {"pass": len(blockers) == 0, "blocking_findings": blockers, "blocking_count": len(blockers)}


# ---------------- RISK ----------------
def score_risk(impact: int, probability: int, control_effectiveness: int = 0) -> int:
    if not all(1 <= x <= 5 for x in (impact, probability)) or not 0 <= control_effectiveness <= 5:
        raise ValueError("risk inputs out of range")
    raw = impact * probability
    adjusted = max(1, raw - control_effectiveness)
    if adjusted <= 4:
        return 1
    if adjusted <= 8:
        return 2
    if adjusted <= 12:
        return 3
    if adjusted <= 18:
        return 4
    return 5


async def create_risk(*, actor_id: str, title: str, domain: str, impact: int, probability: int, control_effectiveness: int = 0, owner: Optional[str] = None, mitigation: Optional[str] = None, deadline: Optional[str] = None, evidence_refs: Iterable[str] = ()) -> Dict[str, Any]:
    level = score_risk(impact, probability, control_effectiveness)
    row = {"id": _id("RISK"), "title": title, "domain": domain.upper(), "impact": impact, "probability": probability, "control_effectiveness": control_effectiveness, "level": level, "owner": owner, "mitigation": mitigation, "deadline": deadline, "evidence_refs": list(evidence_refs), "treatment": None, "status": "OPEN", "created_by": actor_id, "created_at": utc_now_iso(), "updated_at": utc_now_iso()}
    await db.risks.insert_one(dict(row))
    await _audit("risk.created", actor_id, "risk", row["id"], {"level": level, "domain": row["domain"]})
    return row


async def set_risk_treatment(*, actor_id: str, risk_id: str, treatment: str) -> Dict[str, Any]:
    target = treatment.upper().replace("-", "_")
    if target not in RISK_TREATMENTS:
        raise ValueError("invalid risk treatment")
    risk = await db.risks.find_one({"id": risk_id}, {"_id": 0})
    if not risk:
        raise LookupError("risk not found")
    state_map = {"ACCEPT": "ACCEPTED", "MITIGATE": "TREATING", "TRANSFER_INSURE": "TRANSFERRED", "ESCALATE": "OPEN", "BLOCK": "BLOCKED"}
    status = state_map[target]
    await db.risks.update_one({"id": risk_id}, {"$set": {"treatment": target, "status": status, "updated_at": utc_now_iso()}})
    await _audit("risk.treatment.set", actor_id, "risk", risk_id, {"treatment": target, "status": status})
    return {**risk, "treatment": target, "status": status}


async def critical_risk_gate() -> Dict[str, Any]:
    rows = await db.risks.find({"level": {"$gte": 4}, "status": {"$nin": ["MITIGATED", "TRANSFERRED", "CLOSED"]}}, {"_id": 0}).to_list(1000)
    blockers = [r for r in rows if not (r.get("owner") and r.get("mitigation") and r.get("deadline") and r.get("evidence_refs"))]
    return {"pass": len(blockers) == 0, "blocking_risks": blockers, "blocking_count": len(blockers)}
