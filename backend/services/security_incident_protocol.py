"""Security disclosure and incident classification protocol (SEC-38..SEC-40).

This module does not create a second incident engine. Canonical incidents remain owned
by XCP-005 ``incident_core``. Security-specific records only classify or link evidence
back to that canonical incident. SEV-1..SEV-4 are treated as explicit ordinal labels;
no legal, regulatory, notification or response-time meaning is invented here.
"""

from __future__ import annotations

import uuid
from typing import Any, Dict, Iterable, Optional

from db import db, utc_now_iso
from services import professional_governance as governance

SEV_LEVELS = {"SEV-1": 1, "SEV-2": 2, "SEV-3": 3, "SEV-4": 4}
DISCLOSURE_STATES = {"RECEIVED", "TRIAGED", "ACCEPTED", "DUPLICATE", "REJECTED", "CLOSED"}


def _id(prefix: str) -> str:
    return f"{prefix}-{uuid.uuid4()}"


def _refs(values: Iterable[str]) -> list[str]:
    return list(dict.fromkeys(str(v).strip() for v in values if str(v).strip()))


async def record_vulnerability_disclosure(
    *,
    actor_id: str,
    summary: str,
    reporter_ref: str,
    channel: str,
    evidence_refs: Iterable[str],
    asset_id: Optional[str] = None,
    canonical_incident_id: Optional[str] = None,
) -> Dict[str, Any]:
    """SEC-38: evidence-backed intake without exposing source code or hidden findings."""
    refs = _refs(evidence_refs)
    if not summary.strip() or not reporter_ref.strip() or not channel.strip() or not refs:
        raise ValueError("disclosure requires summary, reporter, channel and evidence")
    if asset_id and not await db.security_assets.find_one({"id": asset_id}):
        raise LookupError("security asset not found")
    if canonical_incident_id:
        incident = await db.incidents.find_one({"id": canonical_incident_id}, {"_id": 0})
        if not incident:
            raise LookupError("canonical incident not found")
        if "SECURITY" not in set(incident.get("domains", [])):
            raise ValueError("canonical incident is not scoped to SECURITY")

    row = {
        "id": _id("VDISC"),
        "summary": summary.strip(),
        "reporter_ref": reporter_ref.strip(),
        "channel": channel.strip().upper(),
        "asset_id": asset_id,
        "canonical_incident_id": canonical_incident_id,
        "evidence_refs": refs,
        "status": "RECEIVED",
        "source_code_exposed": False,
        "created_by": actor_id,
        "created_at": utc_now_iso(),
        "updated_at": utc_now_iso(),
    }
    await db.security_vulnerability_disclosures.insert_one(dict(row))
    await governance.audit_event(
        event_type="security.disclosure.received",
        actor_id=actor_id,
        resource_type="security_vulnerability_disclosure",
        resource_id=row["id"],
        payload={
            "asset_id": asset_id,
            "canonical_incident_id": canonical_incident_id,
            "channel": row["channel"],
            "evidence_refs": refs,
        },
        result="RECEIVED",
    )
    return row


async def transition_vulnerability_disclosure(
    *,
    actor_id: str,
    disclosure_id: str,
    status: str,
    rationale: str,
    evidence_refs: Iterable[str],
    finding_id: Optional[str] = None,
) -> Dict[str, Any]:
    row = await db.security_vulnerability_disclosures.find_one(
        {"id": disclosure_id}, {"_id": 0}
    )
    if not row:
        raise LookupError("vulnerability disclosure not found")
    target = str(status or "").strip().upper()
    if target not in DISCLOSURE_STATES - {"RECEIVED"}:
        raise ValueError("invalid vulnerability disclosure state")
    refs = _refs(evidence_refs)
    if not rationale.strip() or not refs:
        raise ValueError("disclosure transition requires rationale and evidence")
    if finding_id and not await db.security_findings.find_one({"id": finding_id}):
        raise LookupError("security finding not found")
    if target == "ACCEPTED" and not finding_id and not row.get("canonical_incident_id"):
        raise ValueError("accepted disclosure must link to a finding or canonical incident")

    now = utc_now_iso()
    update = {
        "status": target,
        "finding_id": finding_id or row.get("finding_id"),
        "last_rationale": rationale.strip(),
        "last_evidence_refs": refs,
        "updated_by": actor_id,
        "updated_at": now,
    }
    await db.security_vulnerability_disclosures.update_one(
        {"id": disclosure_id}, {"$set": update}
    )
    await governance.audit_event(
        event_type="security.disclosure.state_changed",
        actor_id=actor_id,
        resource_type="security_vulnerability_disclosure",
        resource_id=disclosure_id,
        before={"status": row["status"], "finding_id": row.get("finding_id")},
        after={"status": target, "finding_id": update["finding_id"]},
        reason=rationale.strip(),
        result=target,
        payload={"evidence_refs": refs},
    )
    return {**row, **update}


async def classify_security_incident(
    *,
    actor_id: str,
    incident_id: str,
    sev_level: str,
    rationale: str,
    evidence_refs: Iterable[str],
) -> Dict[str, Any]:
    """SEC-39/40: bind a SEV label to one XCP-005 SECURITY incident.

    The canonical incident's LOW/MEDIUM/HIGH/CRITICAL severity is left untouched. This
    prevents a hidden conversion rule between two taxonomies.
    """
    incident = await db.incidents.find_one({"id": incident_id}, {"_id": 0})
    if not incident:
        raise LookupError("canonical incident not found")
    if "SECURITY" not in set(incident.get("domains", [])):
        raise ValueError("incident is not scoped to SECURITY")
    target = str(sev_level or "").strip().upper()
    if target not in SEV_LEVELS:
        raise ValueError("security incident severity must be SEV-1..SEV-4")
    refs = _refs(evidence_refs)
    if not rationale.strip() or not refs:
        raise ValueError("security incident classification requires rationale and evidence")

    previous = await db.security_incident_classifications.find_one(
        {"incident_id": incident_id, "status": "CURRENT"}, {"_id": 0}
    )
    now = utc_now_iso()
    row = {
        "id": _id("SEVCLASS"),
        "incident_id": incident_id,
        "sev_level": target,
        "ordinal": SEV_LEVELS[target],
        "canonical_severity": incident.get("severity"),
        "rationale": rationale.strip(),
        "evidence_refs": refs,
        "status": "CURRENT",
        "supersedes_classification_id": previous["id"] if previous else None,
        "classified_by": actor_id,
        "classified_at": now,
    }
    if previous:
        result = await db.security_incident_classifications.update_one(
            {"id": previous["id"], "status": "CURRENT"},
            {"$set": {"status": "SUPERSEDED", "superseded_by": row["id"], "superseded_at": now}},
        )
        if result.modified_count != 1:
            raise ValueError("security incident classification changed concurrently")
    await db.security_incident_classifications.insert_one(dict(row))
    await db.incidents.update_one(
        {"id": incident_id},
        {"$set": {"metadata.security_sev_classification_id": row["id"], "updated_at": now}},
    )
    await governance.audit_event(
        event_type="security.incident.classified",
        actor_id=actor_id,
        resource_type="incident",
        resource_id=incident_id,
        payload={
            "classification_id": row["id"],
            "sev_level": target,
            "canonical_severity": incident.get("severity"),
            "evidence_refs": refs,
        },
        reason=rationale.strip(),
        result=target,
    )
    return row


async def get_current_security_incident_classification(incident_id: str) -> Dict[str, Any]:
    row = await db.security_incident_classifications.find_one(
        {"incident_id": incident_id, "status": "CURRENT"}, {"_id": 0}
    )
    if not row:
        raise LookupError("current security incident classification not found")
    return row
