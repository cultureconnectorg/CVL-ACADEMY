"""Evidence-first Privacy protocols (PRI-04/05/09/10/16/22/29/31/33/34/35).

This module closes protocol-level controls without inventing legal conclusions. It
reuses canonical processing activities, classifications, incidents, policy versions
and the Evidence Graph. Legal-basis, jurisdiction and minor-user records are reviewed
facts, not automatic statements of law. FREK references are proof references only;
they are never promoted to verified proof without canonical verification evidence.
"""

from __future__ import annotations

import hashlib
import json
import uuid
from typing import Any, Dict, Iterable

from db import db, utc_now_iso
from services import evidence_graph, policy_registry

PRIVACY_REQUEST_TYPES = {"RESTRICTION", "OBJECTION"}
PRIVACY_REQUEST_STATES = {
    "OPEN",
    "IDENTITY_VERIFIED",
    "IN_REVIEW",
    "APPROVED",
    "REJECTED",
    "EXECUTED",
    "CLOSED",
}
PSEUDONYMISATION_OPERATIONS = {"TOKENIZE", "HMAC", "VAULT_REFERENCE"}
MINOR_STATES = {"REVIEW_REQUIRED", "ALLOWED", "BLOCKED"}
BREACH_STATES = {"OPEN", "INVESTIGATING", "CONTAINED", "ASSESSED", "CLOSED"}


def _id(prefix: str) -> str:
    return f"{prefix}-{uuid.uuid4()}"


def _refs(values: Iterable[str]) -> list[str]:
    return list(
        dict.fromkeys(str(value).strip() for value in values if str(value).strip())
    )


def _hash(payload: Dict[str, Any]) -> str:
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


async def register_legal_basis(
    *,
    actor_id: str,
    code: str,
    label: str,
    jurisdiction: str,
    authority_ref: str,
    rationale: str,
    evidence_refs: Iterable[str],
) -> Dict[str, Any]:
    refs = _refs(evidence_refs)
    key = str(code or "").strip().upper()
    required_values = (key, label, jurisdiction, authority_ref, rationale)
    if not all(str(value).strip() for value in required_values) or not refs:
        raise ValueError(
            "legal basis requires code, label, jurisdiction, authority, rationale "
            "and evidence"
        )
    jurisdiction_key = jurisdiction.strip().upper()
    previous = await db.privacy_legal_bases.find_one(
        {"code": key, "jurisdiction": jurisdiction_key, "status": "CURRENT"},
        {"_id": 0},
    )
    now = utc_now_iso()
    row = {
        "id": _id("LBASIS"),
        "code": key,
        "label": label.strip(),
        "jurisdiction": jurisdiction_key,
        "authority_ref": authority_ref.strip(),
        "rationale": rationale.strip(),
        "evidence_refs": refs,
        "status": "CURRENT",
        "supersedes_id": previous["id"] if previous else None,
        "created_by": actor_id,
        "created_at": now,
    }
    if previous:
        result = await db.privacy_legal_bases.update_one(
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
            raise ValueError("legal basis changed concurrently")
    await db.privacy_legal_bases.insert_one(dict(row))
    return row


async def assess_purpose_limitation(
    *,
    actor_id: str,
    processing_activity_id: str,
    requested_purpose: str,
    compatible: bool,
    rationale: str,
    evidence_refs: Iterable[str],
) -> Dict[str, Any]:
    activity = await db.privacy_processing_activities.find_one(
        {"id": processing_activity_id}, {"_id": 0}
    )
    if not activity:
        raise LookupError("processing activity not found")
    refs = _refs(evidence_refs)
    if not requested_purpose.strip() or not rationale.strip() or not refs:
        raise ValueError(
            "purpose limitation assessment requires purpose, rationale and evidence"
        )
    decision = (
        "ALLOW_WITHIN_RECORDED_PURPOSE"
        if compatible
        else "BLOCK_NEW_PROCESSING_PENDING_REVIEW"
    )
    row = {
        "id": _id("PURPOSE"),
        "processing_activity_id": processing_activity_id,
        "registered_purpose": activity.get("purpose"),
        "requested_purpose": requested_purpose.strip(),
        "compatible": bool(compatible),
        "rationale": rationale.strip(),
        "evidence_refs": refs,
        "decision": decision,
        "assessed_by": actor_id,
        "assessed_at": utc_now_iso(),
    }
    await db.privacy_purpose_assessments.insert_one(dict(row))
    return row


async def assess_data_minimisation(
    *,
    actor_id: str,
    processing_activity_id: str,
    required_fields: Iterable[str],
    collected_fields: Iterable[str],
    rationale: str,
    evidence_refs: Iterable[str],
) -> Dict[str, Any]:
    activity = await db.privacy_processing_activities.find_one(
        {"id": processing_activity_id}, {"_id": 0}
    )
    if not activity:
        raise LookupError("processing activity not found")
    required = sorted(
        {str(value).strip() for value in required_fields if str(value).strip()}
    )
    collected = sorted(
        {str(value).strip() for value in collected_fields if str(value).strip()}
    )
    refs = _refs(evidence_refs)
    if not required or not collected or not rationale.strip() or not refs:
        raise ValueError(
            "minimisation assessment requires required/collected fields, rationale "
            "and evidence"
        )
    excess = sorted(set(collected) - set(required))
    row = {
        "id": _id("MIN"),
        "processing_activity_id": processing_activity_id,
        "required_fields": required,
        "collected_fields": collected,
        "excess_fields": excess,
        "pass": not excess,
        "rationale": rationale.strip(),
        "evidence_refs": refs,
        "assessed_by": actor_id,
        "assessed_at": utc_now_iso(),
    }
    await db.privacy_minimisation_assessments.insert_one(dict(row))
    return row


async def record_consent_frek_proof(
    *,
    actor_id: str,
    consent_id: str,
    frek_proof_ref: str,
    proof_status: str,
    evidence_refs: Iterable[str],
) -> Dict[str, Any]:
    consent = await db.privacy_consents.find_one({"id": consent_id}, {"_id": 0})
    if not consent:
        raise LookupError("consent not found")
    refs = _refs(evidence_refs)
    status = str(proof_status or "").strip().upper()
    if status not in {"PENDING_VERIFICATION", "VERIFIED", "FAILED"}:
        raise ValueError("invalid FREK consent proof status")
    if not frek_proof_ref.strip() or not refs:
        raise ValueError("FREK consent proof requires reference and evidence")
    canonical_verification = any(ref.startswith("FREK_VERIFY:") for ref in refs)
    if status == "VERIFIED" and not canonical_verification:
        raise ValueError(
            "VERIFIED FREK consent proof requires canonical verification evidence"
        )
    row = {
        "id": _id("CFREK"),
        "consent_id": consent_id,
        "frek_proof_ref": frek_proof_ref.strip(),
        "proof_status": status,
        "evidence_refs": refs,
        "legal_effect": "none",
        "recorded_by": actor_id,
        "recorded_at": utc_now_iso(),
    }
    await db.privacy_consent_frek_proofs.insert_one(dict(row))
    await db.privacy_consents.update_one(
        {"id": consent_id}, {"$set": {"frek_proof_record_id": row["id"]}}
    )
    return row


async def create_restriction_or_objection(
    *,
    actor_id: str,
    user_id: str,
    request_type: str,
    processing_activity_id: str,
    rationale: str,
    evidence_refs: Iterable[str],
) -> Dict[str, Any]:
    kind = str(request_type or "").strip().upper()
    if kind not in PRIVACY_REQUEST_TYPES:
        raise ValueError("request_type must be RESTRICTION or OBJECTION")
    activity = await db.privacy_processing_activities.find_one(
        {"id": processing_activity_id}, {"_id": 0}
    )
    if not activity:
        raise LookupError("processing activity not found")
    refs = _refs(evidence_refs)
    if not rationale.strip() or not refs:
        raise ValueError("privacy request requires rationale and evidence")
    row = {
        "id": _id("PRREQ"),
        "user_id": user_id,
        "request_type": kind,
        "processing_activity_id": processing_activity_id,
        "rationale": rationale.strip(),
        "evidence_refs": refs,
        "status": "OPEN",
        "created_by": actor_id,
        "created_at": utc_now_iso(),
        "updated_at": utc_now_iso(),
    }
    await db.privacy_restriction_objection_requests.insert_one(dict(row))
    return row


async def transition_restriction_or_objection(
    *,
    actor_id: str,
    request_id: str,
    status: str,
    evidence_refs: Iterable[str],
) -> Dict[str, Any]:
    row = await db.privacy_restriction_objection_requests.find_one(
        {"id": request_id}, {"_id": 0}
    )
    if not row:
        raise LookupError("privacy request not found")
    target = str(status or "").strip().upper()
    allowed = {
        "OPEN": {"IDENTITY_VERIFIED", "REJECTED"},
        "IDENTITY_VERIFIED": {"IN_REVIEW", "REJECTED"},
        "IN_REVIEW": {"APPROVED", "REJECTED"},
        "APPROVED": {"EXECUTED"},
        "EXECUTED": {"CLOSED"},
        "REJECTED": {"CLOSED"},
        "CLOSED": set(),
    }
    if target not in PRIVACY_REQUEST_STATES or target not in allowed[row["status"]]:
        raise ValueError(f"invalid privacy request transition {row['status']}->{target}")
    refs = _refs(evidence_refs)
    if not refs:
        raise ValueError("privacy request transition requires evidence")
    now = utc_now_iso()
    update = {
        "status": target,
        "last_evidence_refs": refs,
        "updated_by": actor_id,
        "updated_at": now,
    }
    result = await db.privacy_restriction_objection_requests.update_one(
        {"id": request_id, "status": row["status"]}, {"$set": update}
    )
    if result.modified_count != 1:
        raise ValueError("privacy request changed concurrently")
    return {**row, **update}


async def register_pseudonymisation_policy(
    *,
    actor_id: str,
    name: str,
    operation: str,
    key_or_vault_ref: str,
    policy_version_id: str,
    evidence_refs: Iterable[str],
) -> Dict[str, Any]:
    operation_key = str(operation or "").strip().upper()
    refs = _refs(evidence_refs)
    if operation_key not in PSEUDONYMISATION_OPERATIONS:
        raise ValueError("invalid pseudonymisation operation")
    if not name.strip() or not key_or_vault_ref.strip() or not refs:
        raise ValueError(
            "pseudonymisation policy requires name, protected key/vault reference "
            "and evidence"
        )
    policy = await policy_registry.require_effective_version(policy_version_id)
    if policy.get("policy_key") != "PSEUDONYMISATION":
        raise ValueError("pseudonymisation requires PSEUDONYMISATION policy")
    row = {
        "id": _id("PSEUDO"),
        "name": name.strip(),
        "operation": operation_key,
        "key_or_vault_ref": key_or_vault_ref.strip(),
        "secret_material_stored": False,
        "policy_version_id": policy["id"],
        "policy_hash": policy["content_hash"],
        "evidence_refs": refs,
        "status": "ACTIVE",
        "created_by": actor_id,
        "created_at": utc_now_iso(),
    }
    await db.privacy_pseudonymisation_policies.insert_one(dict(row))
    return row


async def register_data_residency_rule(
    *,
    actor_id: str,
    data_class_code: str,
    allowed_regions: Iterable[str],
    prohibited_regions: Iterable[str],
    policy_version_id: str,
    evidence_refs: Iterable[str],
) -> Dict[str, Any]:
    allowed = sorted(
        {str(value).strip().upper() for value in allowed_regions if str(value).strip()}
    )
    prohibited = sorted(
        {
            str(value).strip().upper()
            for value in prohibited_regions
            if str(value).strip()
        }
    )
    refs = _refs(evidence_refs)
    data_class_key = data_class_code.strip().upper()
    if not await db.privacy_data_classes.find_one({"code": data_class_key}):
        raise LookupError("privacy data class not found")
    if not allowed or set(allowed) & set(prohibited) or not refs:
        raise ValueError(
            "residency rule requires non-conflicting allowed regions and evidence"
        )
    policy = await policy_registry.require_effective_version(policy_version_id)
    if policy.get("policy_key") != "DATA_RESIDENCY":
        raise ValueError("residency rule requires DATA_RESIDENCY policy")
    row = {
        "id": _id("RESID"),
        "data_class_code": data_class_key,
        "allowed_regions": allowed,
        "prohibited_regions": prohibited,
        "policy_version_id": policy["id"],
        "policy_hash": policy["content_hash"],
        "evidence_refs": refs,
        "status": "ACTIVE",
        "created_by": actor_id,
        "created_at": utc_now_iso(),
    }
    await db.privacy_residency_rules.insert_one(dict(row))
    return row


async def open_breach_investigation(
    *,
    actor_id: str,
    incident_id: str,
    hypothesis: str,
    evidence_refs: Iterable[str],
) -> Dict[str, Any]:
    incident = await db.incidents.find_one({"id": incident_id}, {"_id": 0})
    if not incident or "PRIVACY" not in set(incident.get("domains", [])):
        raise ValueError("breach investigation requires canonical PRIVACY incident")
    refs = _refs(evidence_refs)
    if not hypothesis.strip() or not refs:
        raise ValueError("breach investigation requires hypothesis and evidence")
    row = {
        "id": _id("BREACH"),
        "incident_id": incident_id,
        "hypothesis": hypothesis.strip(),
        "evidence_refs": refs,
        "status": "OPEN",
        "findings": [],
        "created_by": actor_id,
        "created_at": utc_now_iso(),
        "updated_at": utc_now_iso(),
    }
    await db.privacy_breach_investigations.insert_one(dict(row))
    return row


async def record_breach_finding(
    *,
    actor_id: str,
    investigation_id: str,
    finding: str,
    evidence_refs: Iterable[str],
    status: str = "INVESTIGATING",
) -> Dict[str, Any]:
    row = await db.privacy_breach_investigations.find_one(
        {"id": investigation_id}, {"_id": 0}
    )
    if not row:
        raise LookupError("breach investigation not found")
    target = str(status or "").strip().upper()
    if target not in BREACH_STATES:
        raise ValueError("invalid breach investigation status")
    refs = _refs(evidence_refs)
    if not finding.strip() or not refs:
        raise ValueError("breach finding requires text and evidence")
    item = {
        "id": _id("BFIND"),
        "finding": finding.strip(),
        "evidence_refs": refs,
        "recorded_by": actor_id,
        "recorded_at": utc_now_iso(),
    }
    now = utc_now_iso()
    await db.privacy_breach_investigations.update_one(
        {"id": investigation_id},
        {"$push": {"findings": item}, "$set": {"status": target, "updated_at": now}},
    )
    return {"investigation_id": investigation_id, "status": target, "finding": item}


async def assess_minor_user(
    *,
    actor_id: str,
    user_id: str,
    jurisdiction: str,
    age_or_age_band: str,
    outcome: str,
    authority_ref: str,
    rationale: str,
    evidence_refs: Iterable[str],
) -> Dict[str, Any]:
    target = str(outcome or "").strip().upper()
    refs = _refs(evidence_refs)
    required = (jurisdiction, age_or_age_band, authority_ref, rationale)
    valid_required = all(str(value).strip() for value in required)
    if target not in MINOR_STATES or not valid_required or not refs:
        raise ValueError(
            "minor-user assessment requires valid outcome, jurisdiction, age evidence, "
            "authority, rationale and evidence"
        )
    row = {
        "id": _id("MINOR"),
        "user_id": user_id,
        "jurisdiction": jurisdiction.strip().upper(),
        "age_or_age_band": age_or_age_band.strip(),
        "outcome": target,
        "authority_ref": authority_ref.strip(),
        "rationale": rationale.strip(),
        "evidence_refs": refs,
        "assessed_by": actor_id,
        "assessed_at": utc_now_iso(),
    }
    await db.privacy_minor_assessments.insert_one(dict(row))
    return row


async def create_jurisdiction_pack(
    *,
    actor_id: str,
    jurisdiction: str,
    regulatory_scope_ids: Iterable[str],
    policy_version_ids: Iterable[str],
    evidence_refs: Iterable[str],
) -> Dict[str, Any]:
    scope_ids = _refs(regulatory_scope_ids)
    policy_ids = _refs(policy_version_ids)
    refs = _refs(evidence_refs)
    if not jurisdiction.strip() or not scope_ids or not policy_ids or not refs:
        raise ValueError(
            "jurisdiction pack requires jurisdiction, regulatory scopes, policies "
            "and evidence"
        )
    scopes = await db.regulatory_scopes.find(
        {"id": {"$in": scope_ids}}, {"_id": 0}
    ).to_list(len(scope_ids))
    if len(scopes) != len(scope_ids):
        raise LookupError("one or more regulatory scopes are missing")
    unresolved = {"UNKNOWN", "REVIEW_REQUIRED"}
    if any(scope.get("status") in unresolved for scope in scopes):
        raise ValueError(
            "jurisdiction pack cannot close with unresolved regulatory scope"
        )
    policies = []
    for policy_id in policy_ids:
        policies.append(await policy_registry.require_effective_version(policy_id))
    row = {
        "id": _id("JPACK"),
        "jurisdiction": jurisdiction.strip().upper(),
        "regulatory_scope_ids": scope_ids,
        "regulatory_decision_ids": [
            scope.get("current_decision_id") for scope in scopes
        ],
        "policy_versions": [
            {
                "id": policy["id"],
                "key": policy["policy_key"],
                "hash": policy["content_hash"],
            }
            for policy in policies
        ],
        "evidence_refs": refs,
        "status": "COMPOSED_FROM_REVIEWED_SOURCES",
        "created_by": actor_id,
        "created_at": utc_now_iso(),
    }
    row["pack_hash"] = _hash(row)
    await db.privacy_jurisdiction_packs.insert_one(dict(row))
    return row


async def create_privacy_evidence_pack(
    *,
    actor_id: str,
    title: str,
    evidence_node_ids: Iterable[str],
    evidence_refs: Iterable[str],
) -> Dict[str, Any]:
    """PRI-35: compose evidence by reference through canonical XCP-004 only."""
    return await evidence_graph.create_pack(
        actor_id=actor_id,
        title=title,
        consumer="PRIVACY",
        node_ids=evidence_node_ids,
        purpose=(
            "Privacy controls, requests, incidents, reviews and jurisdiction evidence"
        ),
        evidence_refs=evidence_refs,
    )
