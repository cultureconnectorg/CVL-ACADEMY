"""Canonical Incident Core (XCP-005).

One incident ID is the source of truth. Domain records in Privacy, Security, Legal and
Risk are projections that retain the canonical incident id. Severity is never silently
converted into a risk score; risk impact/probability remain explicit Human Authority
inputs.
"""

from __future__ import annotations

import uuid
from typing import Any, Dict, Iterable, Optional

from db import db, utc_now_iso
from services import assurance_core, legal_ops
from services import professional_governance as governance

DOMAINS = {"PRIVACY", "SECURITY", "LEGAL", "RISK"}
STATUSES = {"OPEN", "CONTAINED", "INVESTIGATING", "RESOLVED", "CLOSED"}
TRANSITIONS = {
    "OPEN": {"CONTAINED", "INVESTIGATING"},
    "CONTAINED": {"INVESTIGATING", "RESOLVED"},
    "INVESTIGATING": {"CONTAINED", "RESOLVED"},
    "RESOLVED": {"CLOSED", "INVESTIGATING"},
    "CLOSED": set(),
}
SEVERITIES = {"LOW", "MEDIUM", "HIGH", "CRITICAL"}


def _id(prefix: str) -> str:
    return f"{prefix}-{uuid.uuid4()}"


async def create_incident(
    *,
    actor_id: str,
    title: str,
    description: str,
    severity: str,
    domains: Iterable[str],
    evidence_refs: Iterable[str],
    data_classes: Iterable[str] = (),
    asset_id: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    sev = severity.strip().upper()
    target_domains = sorted({d.strip().upper() for d in domains if d.strip()})
    refs = list(dict.fromkeys(evidence_refs))
    if sev not in SEVERITIES:
        raise ValueError("invalid incident severity")
    if not target_domains or any(domain not in DOMAINS for domain in target_domains):
        raise ValueError("incident requires valid projection domains")
    if not refs:
        raise ValueError("incident requires evidence")
    row = {
        "id": _id("INC"),
        "title": title.strip(),
        "description": description.strip(),
        "severity": sev,
        "domains": target_domains,
        "data_classes": sorted({item.upper() for item in data_classes}),
        "asset_id": asset_id,
        "evidence_refs": refs,
        "metadata": metadata or {},
        "status": "OPEN",
        "projections": {},
        "created_by": actor_id,
        "created_at": utc_now_iso(),
        "updated_at": utc_now_iso(),
    }
    await db.incidents.insert_one(dict(row))
    await governance.audit_event(
        event_type="incident.created",
        actor_id=actor_id,
        resource_type="incident",
        resource_id=row["id"],
        payload={"severity": sev, "domains": target_domains},
    )
    return row


async def transition_incident(
    *, actor_id: str, incident_id: str, status: str, evidence_refs: Iterable[str]
) -> Dict[str, Any]:
    incident = await db.incidents.find_one({"id": incident_id}, {"_id": 0})
    if not incident:
        raise LookupError("incident not found")
    target = status.strip().upper()
    if target not in STATUSES or target not in TRANSITIONS[incident["status"]]:
        raise ValueError(f"invalid incident transition {incident['status']}->{target}")
    refs = list(dict.fromkeys(evidence_refs))
    if target in {"RESOLVED", "CLOSED"} and not refs:
        raise ValueError(f"{target.lower()} transition requires evidence")
    now = utc_now_iso()
    update = {"status": target, "updated_at": now, "last_transition_evidence_refs": refs}
    await db.incidents.update_one({"id": incident_id}, {"$set": update})
    await governance.audit_event(
        event_type="incident.status_changed",
        actor_id=actor_id,
        resource_type="incident",
        resource_id=incident_id,
        payload={"from": incident["status"], "to": target, "evidence_refs": refs},
    )
    return {**incident, **update}


async def _remember_projection(incident_id: str, domain: str, projection: Dict[str, Any]) -> None:
    await db.incidents.update_one(
        {"id": incident_id},
        {"$set": {f"projections.{domain}": projection["id"], "updated_at": utc_now_iso()}},
    )


async def project_privacy(*, actor_id: str, incident: Dict[str, Any]) -> Dict[str, Any]:
    existing_id = incident.get("projections", {}).get("PRIVACY")
    if existing_id:
        existing = await db.privacy_incidents.find_one({"id": existing_id}, {"_id": 0})
        if existing:
            return existing
    row = await assurance_core.create_privacy_incident(
        actor_id=actor_id,
        title=incident["title"],
        severity=incident["severity"],
        data_classes=incident.get("data_classes", []),
        description=incident["description"],
    )
    await db.privacy_incidents.update_one(
        {"id": row["id"]}, {"$set": {"canonical_incident_id": incident["id"]}}
    )
    row = {**row, "canonical_incident_id": incident["id"]}
    await _remember_projection(incident["id"], "PRIVACY", row)
    return row


async def project_security(
    *, actor_id: str, incident: Dict[str, Any], remediation: str
) -> Dict[str, Any]:
    existing_id = incident.get("projections", {}).get("SECURITY")
    if existing_id:
        existing = await db.security_findings.find_one({"id": existing_id}, {"_id": 0})
        if existing:
            return existing
    if not remediation.strip():
        raise ValueError("security projection requires remediation")
    row = await assurance_core.create_security_finding(
        actor_id=actor_id,
        title=incident["title"],
        severity=incident["severity"],
        asset_id=incident.get("asset_id"),
        evidence_refs=[incident["id"], *incident["evidence_refs"]],
        remediation=remediation,
    )
    await db.security_findings.update_one(
        {"id": row["id"]}, {"$set": {"canonical_incident_id": incident["id"]}}
    )
    row = {**row, "canonical_incident_id": incident["id"]}
    await _remember_projection(incident["id"], "SECURITY", row)
    return row


async def project_legal(
    *, actor_id: str, incident: Dict[str, Any], jurisdiction: Optional[str] = None
) -> Dict[str, Any]:
    existing_id = incident.get("projections", {}).get("LEGAL")
    if existing_id:
        existing = await db.legal_matters.find_one({"id": existing_id}, {"_id": 0})
        if existing:
            return existing
    row = await legal_ops.create_legal_matter(
        actor_id=actor_id,
        title=f"Incident legal matter — {incident['title']}",
        matter_type="INCIDENT",
        jurisdiction=jurisdiction,
        case_id=incident["id"],
        evidence_refs=[incident["id"], *incident["evidence_refs"]],
    )
    await _remember_projection(incident["id"], "LEGAL", row)
    return row


async def project_risk(
    *,
    actor_id: str,
    incident: Dict[str, Any],
    impact: int,
    probability: int,
    owner: Optional[str] = None,
    mitigation: Optional[str] = None,
    deadline: Optional[str] = None,
) -> Dict[str, Any]:
    existing_id = incident.get("projections", {}).get("RISK")
    if existing_id:
        existing = await db.risks.find_one({"id": existing_id}, {"_id": 0})
        if existing:
            return existing
    row = await assurance_core.create_risk(
        actor_id=actor_id,
        title=f"Incident risk — {incident['title']}",
        domain="INCIDENT",
        impact=impact,
        probability=probability,
        owner=owner,
        mitigation=mitigation,
        deadline=deadline,
        evidence_refs=[incident["id"], *incident["evidence_refs"]],
    )
    await db.risks.update_one(
        {"id": row["id"]},
        {"$set": {"source_type": "INCIDENT", "source_id": incident["id"]}},
    )
    row = {**row, "source_type": "INCIDENT", "source_id": incident["id"]}
    await _remember_projection(incident["id"], "RISK", row)
    return row


async def project_incident(
    *,
    actor_id: str,
    incident_id: str,
    security_remediation: Optional[str] = None,
    jurisdiction: Optional[str] = None,
    risk_impact: Optional[int] = None,
    risk_probability: Optional[int] = None,
    risk_owner: Optional[str] = None,
    risk_mitigation: Optional[str] = None,
    risk_deadline: Optional[str] = None,
) -> Dict[str, Any]:
    incident = await db.incidents.find_one({"id": incident_id}, {"_id": 0})
    if not incident:
        raise LookupError("incident not found")
    result: Dict[str, Any] = {}
    for domain in incident["domains"]:
        current = await db.incidents.find_one({"id": incident_id}, {"_id": 0})
        if domain == "PRIVACY":
            result[domain] = await project_privacy(actor_id=actor_id, incident=current)
        elif domain == "SECURITY":
            result[domain] = await project_security(
                actor_id=actor_id, incident=current, remediation=security_remediation or ""
            )
        elif domain == "LEGAL":
            result[domain] = await project_legal(
                actor_id=actor_id, incident=current, jurisdiction=jurisdiction
            )
        elif domain == "RISK":
            if risk_impact is None or risk_probability is None:
                raise ValueError("risk projection requires explicit impact and probability")
            result[domain] = await project_risk(
                actor_id=actor_id,
                incident=current,
                impact=risk_impact,
                probability=risk_probability,
                owner=risk_owner,
                mitigation=risk_mitigation,
                deadline=risk_deadline,
            )
    return {"incident_id": incident_id, "projections": result}


async def get_incident(incident_id: str) -> Dict[str, Any]:
    incident = await db.incidents.find_one({"id": incident_id}, {"_id": 0})
    if not incident:
        raise LookupError("incident not found")
    return incident
