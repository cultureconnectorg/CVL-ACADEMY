"""Evidence-first Legal protocols (LEG-11/12/19/20/23/24).

The module extends canonical Risk, Governance Escalation, Policy Registry and
Regulatory Applicability primitives. It does not create parallel risk, escalation,
policy or regulatory-scope engines and never infers a legal conclusion from metadata.
"""

from __future__ import annotations

import uuid
from typing import Any, Dict, Iterable, Optional

from db import db, utc_now_iso
from services import authority_policy, governance_protocols, policy_registry
from services import professional_governance as governance

CONFIDENTIALITY_LEVELS = {
    "PUBLIC",
    "INTERNAL",
    "CONFIDENTIAL",
    "RESTRICTED",
    "PRIVILEGE_REVIEW_REQUIRED",
    "PRIVILEGED",
}
LEGAL_RESOURCE_COLLECTIONS = {
    "LEGAL_MATTER": "legal_matters",
    "LEGAL_DOCUMENT": "legal_documents",
    "LEGAL_CONTRACT": "legal_contracts",
}
RETENTION_ACTIONS = {"DELETE", "ARCHIVE", "REVIEW"}


def _id(prefix: str) -> str:
    return f"{prefix}-{uuid.uuid4()}"


def _refs(values: Iterable[str]) -> list[str]:
    return list(
        dict.fromkeys(str(value).strip() for value in values if str(value).strip())
    )


async def _effective_policy(version_id: str, policy_key: str) -> Dict[str, Any]:
    policy = await policy_registry.require_effective_version(version_id)
    if policy.get("policy_key") != policy_key:
        raise ValueError(f"control requires {policy_key} policy")
    return policy


async def classify_legal_risk(
    *,
    actor_id: str,
    risk_id: str,
    category: str,
    rationale: str,
    authority_ref: str,
    policy_version_id: str,
    evidence_refs: Iterable[str],
) -> Dict[str, Any]:
    """LEG-11: versioned classification layered on the canonical Risk Core."""
    risk = await db.risks.find_one({"id": risk_id}, {"_id": 0})
    if not risk or str(risk.get("domain", "")).upper() != "LEGAL":
        raise ValueError("legal risk classification requires canonical LEGAL risk")
    refs = _refs(evidence_refs)
    if not category.strip() or not rationale.strip() or not authority_ref.strip() or not refs:
        raise ValueError("legal risk classification requires category, rationale, authority and evidence")
    policy = await _effective_policy(policy_version_id, "LEGAL_RISK_CLASSIFICATION")
    previous = await db.legal_risk_classifications.find_one(
        {"risk_id": risk_id, "status": "CURRENT"}, {"_id": 0}
    )
    now = utc_now_iso()
    row = {
        "id": _id("LRCLASS"),
        "risk_id": risk_id,
        "category": category.strip().upper(),
        "rationale": rationale.strip(),
        "authority_ref": authority_ref.strip(),
        "policy_version_id": policy["id"],
        "policy_hash": policy["content_hash"],
        "evidence_refs": refs,
        "status": "CURRENT",
        "supersedes_id": previous["id"] if previous else None,
        "classified_by": actor_id,
        "classified_at": now,
    }
    if previous:
        result = await db.legal_risk_classifications.update_one(
            {"id": previous["id"], "status": "CURRENT"},
            {
                "$set": {
                    "status": "SUPERSEDED",
                    "superseded_by": row["id"],
                    "superseded_at": now,
                }
            },
        )
        if result.modified_count != 1:
            raise ValueError("legal risk classification changed concurrently")
    await db.legal_risk_classifications.insert_one(dict(row))
    await governance.audit_event(
        event_type="legal.risk.classified",
        actor_id=actor_id,
        resource_type="risk",
        resource_id=risk_id,
        before=previous,
        after=row,
        reason=rationale.strip(),
        result=row["category"],
        payload={
            "policy_version_id": policy["id"],
            "authority_ref": row["authority_ref"],
            "evidence_refs": refs,
        },
    )
    return row


async def escalate_legal_matter(
    *,
    actor_id: str,
    matter_id: str,
    severity: str,
    target_authority_level: str,
    reason: str,
    evidence_refs: Iterable[str],
) -> Dict[str, Any]:
    """LEG-12: Legal wrapper over the single GOV-13 escalation primitive."""
    matter = await db.legal_matters.find_one({"id": matter_id}, {"_id": 0})
    if not matter:
        raise LookupError("legal matter not found")
    return await governance_protocols.create_escalation(
        actor_id=actor_id,
        source_type="LEGAL_MATTER",
        source_id=matter_id,
        case_id=matter.get("case_id"),
        domain="LEGAL",
        severity=severity,
        target_authority_level=target_authority_level,
        reason=reason,
        evidence_refs=evidence_refs,
    )


async def classify_privilege_confidentiality(
    *,
    actor_id: str,
    resource_type: str,
    resource_id: str,
    classification: str,
    rationale: str,
    authority_ref: str,
    policy_version_id: str,
    evidence_refs: Iterable[str],
) -> Dict[str, Any]:
    """LEG-19: reviewed classification record, not an automatic legal conclusion."""
    resource_kind = str(resource_type or "").strip().upper()
    collection_name = LEGAL_RESOURCE_COLLECTIONS.get(resource_kind)
    if not collection_name:
        raise ValueError("unsupported legal confidentiality resource type")
    collection = getattr(db, collection_name)
    if not await collection.find_one({"id": resource_id}):
        raise LookupError("legal confidentiality resource not found")
    level = str(classification or "").strip().upper()
    if level not in CONFIDENTIALITY_LEVELS:
        raise ValueError("invalid legal confidentiality classification")
    refs = _refs(evidence_refs)
    if not rationale.strip() or not authority_ref.strip() or not refs:
        raise ValueError("confidentiality classification requires rationale, authority and evidence")
    policy = await _effective_policy(
        policy_version_id, "LEGAL_PRIVILEGE_CONFIDENTIALITY"
    )
    previous = await db.legal_confidentiality_classifications.find_one(
        {
            "resource_type": resource_kind,
            "resource_id": resource_id,
            "status": "CURRENT",
        },
        {"_id": 0},
    )
    now = utc_now_iso()
    row = {
        "id": _id("LCONF"),
        "resource_type": resource_kind,
        "resource_id": resource_id,
        "classification": level,
        "rationale": rationale.strip(),
        "authority_ref": authority_ref.strip(),
        "policy_version_id": policy["id"],
        "policy_hash": policy["content_hash"],
        "evidence_refs": refs,
        "legal_effect": "RECORDED_CLASSIFICATION_NOT_AUTOMATIC_LEGAL_DETERMINATION",
        "status": "CURRENT",
        "supersedes_id": previous["id"] if previous else None,
        "classified_by": actor_id,
        "classified_at": now,
    }
    if previous:
        result = await db.legal_confidentiality_classifications.update_one(
            {"id": previous["id"], "status": "CURRENT"},
            {
                "$set": {
                    "status": "SUPERSEDED",
                    "superseded_by": row["id"],
                    "superseded_at": now,
                }
            },
        )
        if result.modified_count != 1:
            raise ValueError("confidentiality classification changed concurrently")
    await db.legal_confidentiality_classifications.insert_one(dict(row))
    await governance.audit_event(
        event_type="legal.confidentiality.classified",
        actor_id=actor_id,
        resource_type=resource_kind.lower(),
        resource_id=resource_id,
        before=previous,
        after=row,
        reason=rationale.strip(),
        result=level,
        payload={
            "policy_version_id": policy["id"],
            "authority_ref": authority_ref.strip(),
            "evidence_refs": refs,
        },
    )
    return row


async def register_legal_retention_rule(
    *,
    actor_id: str,
    record_type: str,
    jurisdiction: str,
    retention_days: int,
    trigger: str,
    action: str,
    policy_version_id: str,
    authority_decision_id: str,
    evidence_refs: Iterable[str],
) -> Dict[str, Any]:
    """LEG-20: bind retention configuration to one versioned authority policy."""
    target_action = str(action or "").strip().upper()
    refs = _refs(evidence_refs)
    if target_action not in RETENTION_ACTIONS:
        raise ValueError("invalid legal retention action")
    if retention_days < 0:
        raise ValueError("retention_days must be >= 0")
    required = (record_type, jurisdiction, trigger)
    if not all(str(value).strip() for value in required) or not refs:
        raise ValueError("legal retention requires record, jurisdiction, trigger and evidence")
    policy = await _effective_policy(policy_version_id, "LEGAL_RETENTION")
    decision = await authority_policy.get_decision(authority_decision_id)
    if decision.get("decision") != "ALLOW":
        raise PermissionError("legal retention configuration requires ALLOW authority")
    if str(decision.get("action", "")).upper() != "LEGAL_RETENTION_CONFIGURE":
        raise ValueError("authority decision action does not configure legal retention")
    if decision.get("policy_version_id") != policy["id"]:
        raise ValueError("authority decision did not use the supplied retention policy")
    context = decision.get("context") or {}
    if str(context.get("domain", "")).upper() != "LEGAL":
        raise ValueError("legal retention authority decision must be scoped to LEGAL")

    now = utc_now_iso()
    query = {
        "record_type": record_type.strip().upper(),
        "jurisdiction": jurisdiction.strip().upper(),
        "trigger": trigger.strip().upper(),
        "status": "ACTIVE",
    }
    previous = await db.legal_retention_rules.find_one(query, {"_id": 0})
    row = {
        "id": _id("LRET"),
        "record_type": query["record_type"],
        "jurisdiction": query["jurisdiction"],
        "retention_days": int(retention_days),
        "trigger": query["trigger"],
        "action": target_action,
        "policy_version_id": policy["id"],
        "policy_hash": policy["content_hash"],
        "authority_decision_id": decision["id"],
        "authority_decision_hash": decision.get("decision_hash"),
        "evidence_refs": refs,
        "status": "ACTIVE",
        "supersedes_id": previous["id"] if previous else None,
        "created_by": actor_id,
        "created_at": now,
    }
    if previous:
        result = await db.legal_retention_rules.update_one(
            {"id": previous["id"], "status": "ACTIVE"},
            {
                "$set": {
                    "status": "SUPERSEDED",
                    "superseded_by": row["id"],
                    "superseded_at": now,
                }
            },
        )
        if result.modified_count != 1:
            raise ValueError("legal retention rule changed concurrently")
    await db.legal_retention_rules.insert_one(dict(row))
    await governance.audit_event(
        event_type="legal.retention.rule_registered",
        actor_id=actor_id,
        resource_type="legal_retention_rule",
        resource_id=row["id"],
        before=previous,
        after=row,
        result="ACTIVE",
        payload={
            "policy_version_id": policy["id"],
            "authority_decision_id": decision["id"],
            "evidence_refs": refs,
        },
    )
    return row


async def map_jurisdiction(
    *,
    actor_id: str,
    matter_id: str,
    jurisdiction: str,
    regulatory_scope_ids: Iterable[str],
    rationale: str,
    evidence_refs: Iterable[str],
) -> Dict[str, Any]:
    """LEG-23: map a matter only to reviewed canonical regulatory scopes."""
    matter = await db.legal_matters.find_one({"id": matter_id}, {"_id": 0})
    if not matter:
        raise LookupError("legal matter not found")
    jurisdiction_key = jurisdiction.strip().upper()
    scope_ids = _refs(regulatory_scope_ids)
    refs = _refs(evidence_refs)
    if not jurisdiction_key or not scope_ids or not rationale.strip() or not refs:
        raise ValueError("jurisdiction mapping requires scopes, rationale and evidence")
    scopes = await db.regulatory_scopes.find(
        {"id": {"$in": scope_ids}}, {"_id": 0}
    ).to_list(len(scope_ids))
    if len(scopes) != len(scope_ids):
        raise LookupError("one or more regulatory scopes are missing")
    for scope in scopes:
        if scope.get("status") not in {"APPLICABLE", "NOT_APPLICABLE"}:
            raise ValueError("jurisdiction mapping refuses unresolved regulatory scope")
        if str(scope.get("jurisdiction", "")).upper() != jurisdiction_key:
            raise ValueError("regulatory scope jurisdiction does not match mapping")
        if not scope.get("current_decision_id"):
            raise ValueError("reviewed regulatory scope is missing current decision")

    previous = await db.legal_jurisdiction_mappings.find_one(
        {"matter_id": matter_id, "status": "CURRENT"}, {"_id": 0}
    )
    now = utc_now_iso()
    row = {
        "id": _id("LJUR"),
        "matter_id": matter_id,
        "jurisdiction": jurisdiction_key,
        "regulatory_scope_ids": scope_ids,
        "rationale": rationale.strip(),
        "evidence_refs": refs,
        "status": "CURRENT",
        "supersedes_id": previous["id"] if previous else None,
        "mapped_by": actor_id,
        "mapped_at": now,
    }
    if previous:
        result = await db.legal_jurisdiction_mappings.update_one(
            {"id": previous["id"], "status": "CURRENT"},
            {
                "$set": {
                    "status": "SUPERSEDED",
                    "superseded_by": row["id"],
                    "superseded_at": now,
                }
            },
        )
        if result.modified_count != 1:
            raise ValueError("jurisdiction mapping changed concurrently")
    await db.legal_jurisdiction_mappings.insert_one(dict(row))
    await governance.audit_event(
        event_type="legal.jurisdiction.mapped",
        actor_id=actor_id,
        resource_type="legal_matter",
        resource_id=matter_id,
        before=previous,
        after=row,
        reason=rationale.strip(),
        result="CURRENT",
        payload={"regulatory_scope_ids": scope_ids, "evidence_refs": refs},
    )
    return row


async def register_regulatory_requirement(
    *,
    actor_id: str,
    requirement_key: str,
    scope_id: str,
    title: str,
    requirement: str,
    authority_ref: str,
    source_refs: Iterable[str],
    effective_at: str,
    review_due_at: Optional[str] = None,
) -> Dict[str, Any]:
    """LEG-24: canonical Legal requirement registry over reviewed REG scopes."""
    scope = await db.regulatory_scopes.find_one({"id": scope_id}, {"_id": 0})
    if not scope:
        raise LookupError("regulatory scope not found")
    if scope.get("status") not in {"APPLICABLE", "NOT_APPLICABLE"}:
        raise ValueError("regulatory requirement requires reviewed applicability scope")
    decision_id = scope.get("current_decision_id")
    decision = await db.regulatory_applicability_decisions.find_one(
        {"id": decision_id, "status": "CURRENT"}, {"_id": 0}
    )
    if not decision:
        raise ValueError("regulatory scope current applicability decision is missing")
    refs = _refs(source_refs)
    key = requirement_key.strip().upper()
    required = (key, title, requirement, authority_ref, effective_at)
    if not all(str(value).strip() for value in required) or not refs:
        raise ValueError("regulatory requirement requires key, content, authority, date and sources")

    previous = await db.legal_regulatory_requirements.find_one(
        {"requirement_key": key, "status": "CURRENT"}, {"_id": 0}
    )
    now = utc_now_iso()
    row = {
        "id": _id("LREG"),
        "requirement_key": key,
        "scope_id": scope_id,
        "regulatory_id": scope.get("regulatory_id"),
        "jurisdiction": scope.get("jurisdiction"),
        "applicability_decision_id": decision["id"],
        "applicability_outcome": decision.get("outcome"),
        "title": title.strip(),
        "requirement": requirement.strip(),
        "authority_ref": authority_ref.strip(),
        "source_refs": refs,
        "effective_at": effective_at.strip(),
        "review_due_at": review_due_at,
        "status": "CURRENT",
        "supersedes_id": previous["id"] if previous else None,
        "registered_by": actor_id,
        "registered_at": now,
    }
    if previous:
        result = await db.legal_regulatory_requirements.update_one(
            {"id": previous["id"], "status": "CURRENT"},
            {
                "$set": {
                    "status": "SUPERSEDED",
                    "superseded_by": row["id"],
                    "superseded_at": now,
                }
            },
        )
        if result.modified_count != 1:
            raise ValueError("regulatory requirement changed concurrently")
    await db.legal_regulatory_requirements.insert_one(dict(row))
    await governance.audit_event(
        event_type="legal.regulatory_requirement.registered",
        actor_id=actor_id,
        resource_type="legal_regulatory_requirement",
        resource_id=row["id"],
        before=previous,
        after=row,
        result="CURRENT",
        payload={
            "scope_id": scope_id,
            "applicability_decision_id": decision["id"],
            "authority_ref": authority_ref.strip(),
            "source_refs": refs,
        },
    )
    return row
