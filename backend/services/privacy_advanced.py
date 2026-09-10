"""Advanced Privacy Core workflows (PRI-006/009/010/012/014).

The services are evidence-first and avoid false anonymisation/legal claims:
- rectification records requested change and verified before/after hashes;
- anonymisation produces a candidate first and needs an explicit verification step;
- commercial derived knowledge requires a VERIFIED_ANONYMISED source plus A5 policy;
- cross-border transfer decisions bind to an immutable policy version;
- privacy expert workspace is case-scoped through XCP-006 credentials.
"""

from __future__ import annotations

import hashlib
import json
import uuid
from typing import Any, Dict, Iterable, Optional

from db import db, utc_now_iso
from services import authority_policy, expert_access, policy_registry
from services import professional_governance as governance


RECTIFICATION_STATES = {"OPEN", "APPROVED", "EXECUTED", "REJECTED"}
ANON_OPS = {"DROP", "NULL", "GENERALIZE", "HASH_ONE_WAY"}


def _id(prefix: str) -> str:
    return f"{prefix}-{uuid.uuid4()}"


def _refs(values: Iterable[str]) -> list[str]:
    return list(dict.fromkeys(str(v).strip() for v in values if str(v).strip()))


def _hash(value: Any) -> str:
    raw = json.dumps(value, sort_keys=True, separators=(",", ":"), default=str)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


async def create_rectification_request(
    *,
    actor_id: str,
    user_id: str,
    resource_record_id: str,
    requested_changes: Dict[str, Any],
    rationale: str,
    evidence_refs: Iterable[str],
) -> Dict[str, Any]:
    refs = _refs(evidence_refs)
    if not requested_changes or not rationale.strip() or not refs:
        raise ValueError("rectification requires changes, rationale and evidence")
    resource = await db.classification_resources.find_one(
        {"id": resource_record_id, "classification_status": "CLASSIFIED"}, {"_id": 0}
    )
    if not resource:
        raise ValueError("rectification target must be an explicitly classified resource")
    row = {
        "id": _id("RECT"),
        "user_id": user_id,
        "resource_record_id": resource_record_id,
        "requested_changes": requested_changes,
        "requested_changes_hash": _hash(requested_changes),
        "rationale": rationale.strip(),
        "evidence_refs": refs,
        "status": "OPEN",
        "created_by": actor_id,
        "created_at": utc_now_iso(),
        "updated_at": utc_now_iso(),
    }
    await db.privacy_rectifications.insert_one(dict(row))
    await governance.audit_event(
        event_type="privacy.rectification.created",
        actor_id=actor_id,
        resource_type="privacy_rectification",
        resource_id=row["id"],
        payload={
            "resource_record_id": resource_record_id,
            "requested_changes_hash": row["requested_changes_hash"],
            "evidence_refs": refs,
        },
    )
    return row


async def approve_rectification(
    *, actor_id: str, rectification_id: str, evidence_refs: Iterable[str]
) -> Dict[str, Any]:
    refs = _refs(evidence_refs)
    if not refs:
        raise ValueError("rectification approval requires evidence")
    row = await db.privacy_rectifications.find_one(
        {"id": rectification_id}, {"_id": 0}
    )
    if not row:
        raise LookupError("rectification request not found")
    if row["status"] != "OPEN":
        raise ValueError("only OPEN rectifications can be approved")
    now = utc_now_iso()
    result = await db.privacy_rectifications.update_one(
        {"id": rectification_id, "status": "OPEN"},
        {
            "$set": {
                "status": "APPROVED",
                "approved_by": actor_id,
                "approved_at": now,
                "approval_evidence_refs": refs,
                "updated_at": now,
            }
        },
    )
    if result.modified_count != 1:
        raise ValueError("rectification approval lost race")
    return {**row, "status": "APPROVED", "approval_evidence_refs": refs}


async def record_rectification_execution(
    *,
    actor_id: str,
    rectification_id: str,
    adapter: str,
    before_hash: str,
    after_hash: str,
    evidence_refs: Iterable[str],
) -> Dict[str, Any]:
    refs = _refs(evidence_refs)
    if not adapter.strip() or not refs or len(before_hash) != 64 or len(after_hash) != 64:
        raise ValueError("rectification execution requires adapter, SHA-256 hashes and evidence")
    if before_hash == after_hash:
        raise ValueError("rectification execution must change the target state")
    row = await db.privacy_rectifications.find_one(
        {"id": rectification_id}, {"_id": 0}
    )
    if not row:
        raise LookupError("rectification request not found")
    if row["status"] != "APPROVED":
        raise ValueError("rectification must be APPROVED before execution")
    now = utc_now_iso()
    execution = {
        "adapter": adapter.strip(),
        "before_hash": before_hash.lower(),
        "after_hash": after_hash.lower(),
        "evidence_refs": refs,
        "executed_by": actor_id,
        "executed_at": now,
    }
    await db.privacy_rectifications.update_one(
        {"id": rectification_id, "status": "APPROVED"},
        {"$set": {"status": "EXECUTED", "execution": execution, "updated_at": now}},
    )
    await governance.audit_event(
        event_type="privacy.rectification.executed",
        actor_id=actor_id,
        resource_type="privacy_rectification",
        resource_id=rectification_id,
        payload=execution,
    )
    return {**row, "status": "EXECUTED", "execution": execution}


async def register_anonymisation_recipe(
    *,
    actor_id: str,
    data_class_code: str,
    operations: Dict[str, str],
    policy_version_id: str,
    evidence_refs: Iterable[str],
) -> Dict[str, Any]:
    refs = _refs(evidence_refs)
    if not operations or not refs:
        raise ValueError("anonymisation recipe requires operations and evidence")
    invalid = sorted({str(op).upper() for op in operations.values()} - ANON_OPS)
    if invalid:
        raise ValueError(f"invalid anonymisation operations: {', '.join(invalid)}")
    data_class = await db.privacy_data_classes.find_one(
        {"code": data_class_code.strip().upper()}, {"_id": 0}
    )
    if not data_class:
        raise LookupError("privacy data class not found")
    policy = await policy_registry.require_effective_version(policy_version_id)
    if policy.get("policy_key") != "ANONYMISATION":
        raise ValueError("anonymisation requires ANONYMISATION policy")
    row = {
        "id": _id("ANONR"),
        "data_class_code": data_class["code"],
        "operations": {k: str(v).upper() for k, v in operations.items()},
        "policy_version_id": policy["id"],
        "policy_hash": policy["content_hash"],
        "evidence_refs": refs,
        "status": "ACTIVE",
        "created_by": actor_id,
        "created_at": utc_now_iso(),
    }
    await db.privacy_anonymisation_recipes.insert_one(dict(row))
    return row


def apply_anonymisation_candidate(
    record: Dict[str, Any], operations: Dict[str, str]
) -> Dict[str, Any]:
    """Pure transformation; result is a candidate, not an anonymisation claim."""
    output = dict(record)
    for field, raw_operation in operations.items():
        operation = str(raw_operation).upper()
        if operation == "DROP":
            output.pop(field, None)
        elif operation == "NULL":
            if field in output:
                output[field] = None
        elif operation == "GENERALIZE":
            if field in output and output[field] is not None:
                value = str(output[field])
                output[field] = value[:1] + "*" * max(0, len(value) - 1)
        elif operation == "HASH_ONE_WAY":
            if field in output and output[field] is not None:
                output[field] = hashlib.sha256(str(output[field]).encode("utf-8")).hexdigest()
        else:
            raise ValueError("invalid anonymisation operation")
    return output


async def record_anonymisation_run(
    *,
    actor_id: str,
    recipe_id: str,
    resource_record_id: str,
    before_hash: str,
    candidate_hash: str,
    adapter: str,
    evidence_refs: Iterable[str],
    metrics: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    refs = _refs(evidence_refs)
    if not refs or not adapter.strip() or len(before_hash) != 64 or len(candidate_hash) != 64:
        raise ValueError("anonymisation run requires adapter, hashes and evidence")
    if before_hash == candidate_hash:
        raise ValueError("anonymisation candidate must differ from source")
    recipe = await db.privacy_anonymisation_recipes.find_one(
        {"id": recipe_id, "status": "ACTIVE"}, {"_id": 0}
    )
    resource = await db.classification_resources.find_one(
        {"id": resource_record_id, "classification_status": "CLASSIFIED"}, {"_id": 0}
    )
    if not recipe or not resource:
        raise LookupError("active anonymisation recipe or classified resource not found")
    row = {
        "id": _id("ANONRUN"),
        "recipe_id": recipe_id,
        "resource_record_id": resource_record_id,
        "before_hash": before_hash.lower(),
        "candidate_hash": candidate_hash.lower(),
        "adapter": adapter.strip(),
        "metrics": metrics or {},
        "evidence_refs": refs,
        "status": "ANONYMISATION_CANDIDATE",
        "verified_anonymised": False,
        "created_by": actor_id,
        "created_at": utc_now_iso(),
    }
    await db.privacy_anonymisation_runs.insert_one(dict(row))
    return row


async def verify_anonymisation(
    *,
    actor_id: str,
    run_id: str,
    rationale: str,
    residual_reidentification_risk: str,
    evidence_refs: Iterable[str],
) -> Dict[str, Any]:
    refs = _refs(evidence_refs)
    if not rationale.strip() or not residual_reidentification_risk.strip() or not refs:
        raise ValueError("anonymisation verification requires rationale, residual risk and evidence")
    run = await db.privacy_anonymisation_runs.find_one({"id": run_id}, {"_id": 0})
    if not run:
        raise LookupError("anonymisation run not found")
    if run["status"] != "ANONYMISATION_CANDIDATE":
        raise ValueError("only anonymisation candidates can be verified")
    now = utc_now_iso()
    update = {
        "status": "VERIFIED_ANONYMISED",
        "verified_anonymised": True,
        "verification_rationale": rationale.strip(),
        "residual_reidentification_risk": residual_reidentification_risk.strip().upper(),
        "verification_evidence_refs": refs,
        "verified_by": actor_id,
        "verified_at": now,
    }
    await db.privacy_anonymisation_runs.update_one(
        {"id": run_id, "status": "ANONYMISATION_CANDIDATE"}, {"$set": update}
    )
    await governance.audit_event(
        event_type="privacy.anonymisation.verified",
        actor_id=actor_id,
        resource_type="privacy_anonymisation_run",
        resource_id=run_id,
        payload={
            "candidate_hash": run["candidate_hash"],
            "residual_reidentification_risk": update["residual_reidentification_risk"],
            "evidence_refs": refs,
        },
    )
    return {**run, **update}


async def approve_derived_knowledge_asset(
    *,
    actor_id: str,
    actor_role: str,
    authority_level: str,
    anonymisation_run_id: str,
    asset_name: str,
    policy_version_id: str,
    evidence_refs: Iterable[str],
) -> Dict[str, Any]:
    refs = _refs(evidence_refs)
    run = await db.privacy_anonymisation_runs.find_one(
        {"id": anonymisation_run_id}, {"_id": 0}
    )
    if not run or run.get("status") != "VERIFIED_ANONYMISED":
        raise ValueError("commercial asset requires VERIFIED_ANONYMISED source")
    if not asset_name.strip() or not refs:
        raise ValueError("commercial asset requires name and evidence")
    decision = await authority_policy.evaluate_authority(
        actor_id=actor_id,
        actor_role=actor_role,
        action="COMMERCIALISE_DERIVED_KNOWLEDGE",
        context={
            "domain": "PRIVACY",
            "authority_level": authority_level,
            "source_state": "VERIFIED_ANONYMISED",
            "source_run_id": run["id"],
        },
        policy_version_id=policy_version_id,
    )
    if decision["policy_key"] != "DERIVED_KNOWLEDGE_COMMERCIALISATION":
        raise ValueError("commercialisation requires DERIVED_KNOWLEDGE_COMMERCIALISATION policy")
    if decision["decision"] != "ALLOW":
        raise PermissionError("authority policy did not allow derived knowledge commercialisation")
    row = {
        "id": _id("DKA"),
        "asset_name": asset_name.strip(),
        "asset_class": "COMMERCIAL_ASSET",
        "personal_archive": False,
        "source_anonymisation_run_id": run["id"],
        "source_candidate_hash": run["candidate_hash"],
        "authority_decision_id": decision["id"],
        "policy_version_id": decision["policy_version_id"],
        "evidence_refs": refs,
        "status": "APPROVED",
        "created_by": actor_id,
        "created_at": utc_now_iso(),
    }
    await db.privacy_derived_knowledge_assets.insert_one(dict(row))
    return {**row, "authority": decision}


async def assess_cross_border_transfer(
    *,
    actor_id: str,
    actor_role: str,
    authority_level: str,
    processor_id: str,
    destination_region: str,
    transfer_mechanism: str,
    policy_version_id: str,
    evidence_refs: Iterable[str],
) -> Dict[str, Any]:
    refs = _refs(evidence_refs)
    processor = await db.privacy_processors.find_one(
        {"id": processor_id}, {"_id": 0}
    )
    if not processor:
        raise LookupError("processor not found")
    if processor.get("status") != "APPROVED":
        raise ValueError("cross-border transfer requires an APPROVED processor")
    if not destination_region.strip() or not transfer_mechanism.strip() or not refs:
        raise ValueError("transfer requires destination, mechanism and evidence")
    decision = await authority_policy.evaluate_authority(
        actor_id=actor_id,
        actor_role=actor_role,
        action="PRIVACY_CROSS_BORDER_TRANSFER",
        context={
            "domain": "PRIVACY",
            "authority_level": authority_level,
            "processor_id": processor_id,
            "source_regions": processor.get("regions", []),
            "destination_region": destination_region.strip().upper(),
            "transfer_mechanism": transfer_mechanism.strip().upper(),
        },
        policy_version_id=policy_version_id,
    )
    if decision["policy_key"] != "CROSS_BORDER_TRANSFER":
        raise ValueError("transfer requires CROSS_BORDER_TRANSFER policy")
    status = "APPROVED" if decision["decision"] == "ALLOW" else "BLOCKED"
    row = {
        "id": _id("XFER"),
        "processor_id": processor_id,
        "destination_region": destination_region.strip().upper(),
        "transfer_mechanism": transfer_mechanism.strip().upper(),
        "authority_decision_id": decision["id"],
        "policy_version_id": decision["policy_version_id"],
        "evidence_refs": refs,
        "status": status,
        "created_by": actor_id,
        "created_at": utc_now_iso(),
    }
    await db.privacy_transfer_assessments.insert_one(dict(row))
    return {**row, "authority": decision}


async def get_privacy_workspace(*, raw_key: str, case_id: str) -> Dict[str, Any]:
    context = await expert_access.authorize_case_scope(raw_key, case_id, "privacy:case:read")
    case = await db.professional_cases.find_one({"id": case_id}, {"_id": 0})
    if not case:
        raise LookupError("professional case not found")
    if str(case.get("domain", "")).upper() != "PRIVACY":
        raise PermissionError("privacy workspace only exposes PRIVACY cases")
    expert = context["expert"]
    if "PRIVACY" not in {str(v).upper() for v in expert.get("domains", [])}:
        raise PermissionError("expert identity is not authorised for PRIVACY domain")

    dsar_ids = list(case.get("metadata", {}).get("dsar_ids", []))
    incident_ids = list(case.get("metadata", {}).get("incident_ids", []))
    processor_ids = list(case.get("metadata", {}).get("processor_ids", []))
    dsars = await db.privacy_dsar.find({"id": {"$in": dsar_ids}}, {"_id": 0}).to_list(500)
    incidents = await db.incidents.find({"id": {"$in": incident_ids}}, {"_id": 0}).to_list(500)
    processors = await db.privacy_processors.find(
        {"id": {"$in": processor_ids}}, {"_id": 0}
    ).to_list(500)
    return {
        "case": case,
        "expert": {"id": expert["id"], "display_name": expert["display_name"]},
        "granted_scope": context["assignment"].get("scope", []),
        "dsars": dsars,
        "incidents": incidents,
        "processors": processors,
    }
