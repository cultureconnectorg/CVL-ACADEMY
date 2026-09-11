"""PG-13 / GOV-18 canonical no-duplicate architecture manifest.

The manifest records Founder-approved REUSE/EXTEND/BUILD-ONCE decisions. Runtime
registration rejects conflicting component choices and the gate also scans stored
records so a legacy/manual conflicting write cannot silently pass production closure.
"""

from __future__ import annotations

from typing import Any, Dict

from db import db, utc_now_iso
from services import professional_governance as governance

MANIFEST = [
    {
        "theme": "Expert Identity & Assignment",
        "decision": "EXTEND",
        "canonical_owner": "Academy Auth/RBAC",
        "must_not_create": "Separate expert auth system",
    },
    {
        "theme": "Event / Workflow Triggers",
        "decision": "EXTEND",
        "canonical_owner": "Academy Event Bus",
        "must_not_create": "Legal/Security/Quality event buses",
    },
    {
        "theme": "Notifications",
        "decision": "EXTEND",
        "canonical_owner": "NotificationService",
        "must_not_create": "New notification core per domain",
    },
    {
        "theme": "Provider / Ecosystem Registry",
        "decision": "EXTEND",
        "canonical_owner": "Integration Registry",
        "must_not_create": "Parallel vendor/provider registry",
    },
    {
        "theme": "FREK Proof Adapter",
        "decision": "CONNECT/EXTEND",
        "canonical_owner": "Academy→FREK adapter",
        "must_not_create": "Domain-specific FREK clients",
    },
    {
        "theme": "Commerce",
        "decision": "REUSE",
        "canonical_owner": "Commerce Core",
        "must_not_create": "Accounting commerce engine",
    },
    {
        "theme": "Payments",
        "decision": "REUSE/EXTEND",
        "canonical_owner": "Payments Core",
        "must_not_create": "Accounting payment engine",
    },
    {
        "theme": "Academy Internal Wallet",
        "decision": "REUSE",
        "canonical_owner": "Academy Wallet",
        "must_not_create": "Accounting wallet clone",
    },
    {
        "theme": "Certification",
        "decision": "REUSE",
        "canonical_owner": "Certification Core",
        "must_not_create": "Quality certification database",
    },
    {
        "theme": "Physical sessions / attendance",
        "decision": "REUSE",
        "canonical_owner": "Physical Delivery Core",
        "must_not_create": "Quality attendance clone",
    },
    {
        "theme": "Learning / Progression Evidence",
        "decision": "COMPOSE",
        "canonical_owner": "Academy Learning Runtime",
        "must_not_create": "Quality evidence DB copying records",
    },
    {
        "theme": "AI / Orchestration",
        "decision": "CONNECT",
        "canonical_owner": "Existing AI/Agent infrastructure",
        "must_not_create": "New Academy AI engine",
    },
    {
        "theme": "Audit Trail",
        "decision": "EXTEND",
        "canonical_owner": "Professional Governance AuditEvent",
        "must_not_create": "Domain-specific audit stores",
    },
    {
        "theme": "Signature",
        "decision": "BUILD ONCE",
        "canonical_owner": "Trust & Signature Service",
        "must_not_create": "Legal/Quality/Privacy signature engines",
    },
    {
        "theme": "Documents / Versioning",
        "decision": "BUILD ONCE",
        "canonical_owner": "Professional Governance Document Registry",
        "must_not_create": "Legal/Privacy/Quality document stores",
    },
    {
        "theme": "Incidents",
        "decision": "BUILD ONCE",
        "canonical_owner": "Professional Governance Incident Core",
        "must_not_create": "Separate incident source per domain",
    },
]


def _allowed_decisions(expected: str) -> set[str]:
    value = str(expected).upper()
    allowed = {value}
    if value == "REUSE/EXTEND":
        allowed |= {"REUSE", "EXTEND"}
    if value == "CONNECT/EXTEND":
        allowed |= {"CONNECT", "EXTEND"}
    return allowed


async def sync_manifest(*, actor_id: str) -> Dict[str, Any]:
    for index, entry in enumerate(MANIFEST, start=1):
        row = {
            "id": f"REUSE-{index:02d}",
            **entry,
            "status": "LOCKED",
            "updated_by": actor_id,
            "updated_at": utc_now_iso(),
        }
        await db.architecture_reuse_manifest.update_one(
            {"id": row["id"]}, {"$set": row}, upsert=True
        )
    return {"count": len(MANIFEST), "status": "LOCKED"}


async def register_build_decision(
    *,
    actor_id: str,
    theme: str,
    component: str,
    decision: str,
    canonical_owner: str,
    evidence_ref: str,
) -> Dict[str, Any]:
    manifest = await db.architecture_reuse_manifest.find_one(
        {"theme": theme, "status": "LOCKED"}, {"_id": 0}
    )
    if not manifest:
        raise LookupError("deduplication manifest theme not found")
    normalized = decision.strip().upper()
    if normalized not in _allowed_decisions(manifest["decision"]):
        raise ValueError("build decision conflicts with locked deduplication manifest")
    if canonical_owner.strip() != manifest["canonical_owner"]:
        raise ValueError("component points to wrong canonical owner")
    if not component.strip() or not evidence_ref.strip():
        raise ValueError("component and evidence_ref are required")
    row = {
        "theme": theme,
        "component": component.strip(),
        "decision": normalized,
        "canonical_owner": canonical_owner.strip(),
        "manifest_id": manifest["id"],
        "evidence_ref": evidence_ref.strip(),
        "recorded_by": actor_id,
        "recorded_at": utc_now_iso(),
    }
    await db.architecture_build_decisions.insert_one(dict(row))
    await governance.audit_event(
        event_type="governance.architecture.build_decision_recorded",
        actor_id=actor_id,
        resource_type="architecture_build_decision",
        resource_id=f"{manifest['id']}:{row['component']}",
        after=row,
        reason="GOV-18 no-duplicate architecture decision",
        result=normalized,
        payload={
            "manifest_id": manifest["id"],
            "theme": theme,
            "canonical_owner": row["canonical_owner"],
            "evidence_ref": row["evidence_ref"],
        },
    )
    return row


async def gate() -> Dict[str, Any]:
    manifest = await db.architecture_reuse_manifest.find({}, {"_id": 0}).to_list(1000)
    unlocked = [row for row in manifest if row.get("status") != "LOCKED"]
    by_id = {row.get("id"): row for row in manifest}
    decisions = await db.architecture_build_decisions.find({}, {"_id": 0}).to_list(10000)
    conflicts = []
    for decision in decisions:
        owner = by_id.get(decision.get("manifest_id"))
        reason = None
        if not owner:
            reason = "MANIFEST_REFERENCE_MISSING"
        elif decision.get("canonical_owner") != owner.get("canonical_owner"):
            reason = "CANONICAL_OWNER_MISMATCH"
        elif str(decision.get("decision", "")).upper() not in _allowed_decisions(
            owner.get("decision", "")
        ):
            reason = "DECISION_CONFLICT"
        if reason:
            conflicts.append({**decision, "conflict_reason": reason})
    return {
        "pass": len(manifest) == len(MANIFEST) and not unlocked and not conflicts,
        "manifest_count": len(manifest),
        "expected_count": len(MANIFEST),
        "unlocked": unlocked,
        "conflict_count": len(conflicts),
        "conflicts": conflicts,
    }
