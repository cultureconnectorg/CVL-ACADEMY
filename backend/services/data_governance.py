"""Academy data governance primitives (DAT-01..DAT-14).

Data truth is explicit, provenance-bearing and append-only where lineage/history matters.
This service reuses XCP-002 classification and XCP-008 policies. It never converts
personal data into a commercial asset by assertion: commercial eligibility requires an
explicit anonymised-derived asset plus authority/policy evidence.
"""

from __future__ import annotations

import uuid
from typing import Any, Dict, Iterable, Optional

from db import db, utc_now_iso
from services import authority_policy, data_classification, policy_registry
from services import professional_governance as governance
from services.proof_bridge import validate_sha256

LIFECYCLE = {"ACTIVE", "ARCHIVED", "WITHDRAWN", "DELETED"}


def _id(prefix: str) -> str:
    return f"{prefix}-{uuid.uuid4()}"


def _refs(values: Iterable[str]) -> list[str]:
    return list(dict.fromkeys(str(v).strip() for v in values if str(v).strip()))


async def register_dataset(
    *,
    actor_id: str,
    name: str,
    source_system: str,
    source_ref: str,
    content_hash: str,
    owner: str,
    evidence_refs: Iterable[str],
    classification_resource_id: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    digest = validate_sha256(content_hash)
    refs = _refs(evidence_refs)
    if not all(str(v).strip() for v in (name, source_system, source_ref, owner)) or not refs:
        raise ValueError("dataset requires name, source, owner and evidence")
    if classification_resource_id:
        classification = await data_classification.get_resource(classification_resource_id)
        if classification.get("classification_status") != "CLASSIFIED":
            raise ValueError("dataset classification resource is not classified")
    row = {
        "id": _id("DATASET"),
        "name": name.strip(),
        "source_system": source_system.strip().upper(),
        "source_ref": source_ref.strip(),
        "content_hash": digest,
        "owner": owner.strip(),
        "classification_resource_id": classification_resource_id,
        "metadata": metadata or {},
        "evidence_refs": refs,
        "status": "ACTIVE",
        "created_by": actor_id,
        "created_at": utc_now_iso(),
        "updated_at": utc_now_iso(),
    }
    await db.data_datasets.insert_one(dict(row))
    await governance.audit_event(
        event_type="data.dataset.registered",
        actor_id=actor_id,
        resource_type="dataset",
        resource_id=row["id"],
        payload={"source_system": row["source_system"], "content_hash": digest},
        after=row,
        reason="Dataset registered from explicit source of truth",
        result="ACTIVE",
    )
    return row


async def record_lineage(
    *,
    actor_id: str,
    parent_dataset_id: str,
    child_dataset_id: str,
    transformation: str,
    code_or_job_ref: str,
    evidence_refs: Iterable[str],
) -> Dict[str, Any]:
    if parent_dataset_id == child_dataset_id:
        raise ValueError("dataset cannot derive from itself")
    docs = await db.data_datasets.find(
        {"id": {"$in": [parent_dataset_id, child_dataset_id]}}, {"_id": 0}
    ).to_list(2)
    if len(docs) != 2:
        raise LookupError("lineage dataset not found")
    refs = _refs(evidence_refs)
    if not transformation.strip() or not code_or_job_ref.strip() or not refs:
        raise ValueError("lineage requires transformation, job ref and evidence")
    existing = await db.data_lineage.find_one(
        {"parent_dataset_id": parent_dataset_id, "child_dataset_id": child_dataset_id},
        {"_id": 0},
    )
    if existing:
        return existing
    row = {
        "id": _id("LINEAGE"),
        "parent_dataset_id": parent_dataset_id,
        "child_dataset_id": child_dataset_id,
        "transformation": transformation.strip(),
        "code_or_job_ref": code_or_job_ref.strip(),
        "evidence_refs": refs,
        "created_by": actor_id,
        "created_at": utc_now_iso(),
    }
    await db.data_lineage.insert_one(dict(row))
    return row


async def archive_dataset(
    *, actor_id: str, dataset_id: str, archive_ref: str, archive_hash: str, evidence_refs: Iterable[str]
) -> Dict[str, Any]:
    row = await db.data_datasets.find_one({"id": dataset_id}, {"_id": 0})
    if not row:
        raise LookupError("dataset not found")
    if row["status"] != "ACTIVE":
        raise ValueError("only ACTIVE dataset can be archived")
    digest = validate_sha256(archive_hash)
    refs = _refs(evidence_refs)
    if not archive_ref.strip() or not refs:
        raise ValueError("archive requires reference and evidence")
    now = utc_now_iso()
    update = {
        "status": "ARCHIVED",
        "archive_ref": archive_ref.strip(),
        "archive_hash": digest,
        "archive_evidence_refs": refs,
        "archived_by": actor_id,
        "archived_at": now,
        "updated_at": now,
    }
    result = await db.data_datasets.update_one(
        {"id": dataset_id, "status": "ACTIVE"}, {"$set": update}
    )
    if result.modified_count != 1:
        raise ValueError("dataset lifecycle changed concurrently")
    return {**row, **update}


async def register_anonymised_derived_asset(
    *,
    actor_id: str,
    source_dataset_id: str,
    derived_dataset_id: str,
    anonymisation_execution_ref: str,
    evidence_refs: Iterable[str],
) -> Dict[str, Any]:
    source = await db.data_datasets.find_one({"id": source_dataset_id}, {"_id": 0})
    derived = await db.data_datasets.find_one({"id": derived_dataset_id}, {"_id": 0})
    if not source or not derived:
        raise LookupError("source or derived dataset not found")
    refs = _refs(evidence_refs)
    if not anonymisation_execution_ref.strip() or not refs:
        raise ValueError("anonymised derived asset requires execution proof")
    execution = await db.privacy_anonymisation_executions.find_one(
        {"id": anonymisation_execution_ref, "status": "VERIFIED_ANONYMISED"}, {"_id": 0}
    )
    if not execution:
        raise ValueError("verified anonymisation execution not found")
    row = {
        "id": _id("DERIVED"),
        "source_dataset_id": source_dataset_id,
        "derived_dataset_id": derived_dataset_id,
        "anonymisation_execution_ref": anonymisation_execution_ref,
        "evidence_refs": refs,
        "personal_data_excluded": True,
        "commercial_eligibility": "NOT_DECIDED",
        "created_by": actor_id,
        "created_at": utc_now_iso(),
    }
    await db.data_derived_assets.insert_one(dict(row))
    return row


async def decide_commercial_eligibility(
    *,
    actor_id: str,
    actor_role: str,
    authority_level: str,
    derived_asset_id: str,
    policy_version_id: str,
    eligible: bool,
    rationale: str,
    evidence_refs: Iterable[str],
) -> Dict[str, Any]:
    asset = await db.data_derived_assets.find_one({"id": derived_asset_id}, {"_id": 0})
    if not asset:
        raise LookupError("derived asset not found")
    if not asset.get("personal_data_excluded"):
        raise ValueError("personal data exclusion is not proven")
    refs = _refs(evidence_refs)
    if not rationale.strip() or not refs:
        raise ValueError("commercial eligibility requires rationale and evidence")
    decision = await authority_policy.evaluate_authority(
        actor_id=actor_id,
        actor_role=actor_role,
        action="DATA_COMMERCIAL_ELIGIBILITY",
        context={
            "domain": "PRIVACY",
            "authority_level": authority_level,
            "derived_asset_id": derived_asset_id,
            "eligible_requested": bool(eligible),
        },
        policy_version_id=policy_version_id,
    )
    if decision["decision"] != "ALLOW":
        raise PermissionError("authority policy did not allow commercial eligibility decision")
    status = "ELIGIBLE" if eligible else "NOT_ELIGIBLE"
    now = utc_now_iso()
    update = {
        "commercial_eligibility": status,
        "eligibility_decision_id": decision["id"],
        "eligibility_policy_version_id": decision["policy_version_id"],
        "eligibility_rationale": rationale.strip(),
        "eligibility_evidence_refs": refs,
        "updated_at": now,
    }
    await db.data_derived_assets.update_one({"id": derived_asset_id}, {"$set": update})
    return {**asset, **update}


async def issue_dataset_license(
    *,
    actor_id: str,
    derived_asset_id: str,
    licensee_id: str,
    purpose: str,
    starts_at: str,
    ends_at: str,
    policy_version_id: str,
    evidence_refs: Iterable[str],
) -> Dict[str, Any]:
    asset = await db.data_derived_assets.find_one(
        {"id": derived_asset_id, "commercial_eligibility": "ELIGIBLE"}, {"_id": 0}
    )
    if not asset:
        raise ValueError("dataset is not commercially eligible")
    policy = await policy_registry.require_effective_version(policy_version_id)
    if policy.get("policy_key") != "DATASET_LICENSING":
        raise ValueError("dataset license requires DATASET_LICENSING policy")
    refs = _refs(evidence_refs)
    if not licensee_id.strip() or not purpose.strip() or not refs:
        raise ValueError("dataset license requires licensee, purpose and evidence")
    row = {
        "id": _id("DLIC"),
        "derived_asset_id": derived_asset_id,
        "licensee_id": licensee_id.strip(),
        "purpose": purpose.strip(),
        "starts_at": starts_at,
        "ends_at": ends_at,
        "policy_version_id": policy["id"],
        "policy_hash": policy["content_hash"],
        "evidence_refs": refs,
        "status": "ACTIVE",
        "created_by": actor_id,
        "created_at": utc_now_iso(),
    }
    await db.data_dataset_licenses.insert_one(dict(row))
    return row


async def withdraw_dataset_license(
    *, actor_id: str, license_id: str, reason: str, evidence_refs: Iterable[str]
) -> Dict[str, Any]:
    row = await db.data_dataset_licenses.find_one({"id": license_id}, {"_id": 0})
    if not row:
        raise LookupError("dataset license not found")
    refs = _refs(evidence_refs)
    if not reason.strip() or not refs:
        raise ValueError("license withdrawal requires reason and evidence")
    if row["status"] == "WITHDRAWN":
        return row
    now = utc_now_iso()
    update = {
        "status": "WITHDRAWN",
        "withdrawal_reason": reason.strip(),
        "withdrawal_evidence_refs": refs,
        "withdrawn_by": actor_id,
        "withdrawn_at": now,
    }
    await db.data_dataset_licenses.update_one({"id": license_id}, {"$set": update})
    return {**row, **update}


async def audit_data_access(
    *,
    actor_id: str,
    dataset_id: str,
    action: str,
    purpose: str,
    decision: str,
    evidence_refs: Iterable[str],
) -> Dict[str, Any]:
    if not await db.data_datasets.find_one({"id": dataset_id}):
        raise LookupError("dataset not found")
    outcome = str(decision or "").upper()
    if outcome not in {"ALLOW", "DENY"}:
        raise ValueError("data access audit decision must be ALLOW or DENY")
    refs = _refs(evidence_refs)
    if not action.strip() or not purpose.strip() or not refs:
        raise ValueError("data access audit requires action, purpose and evidence")
    row = {
        "id": _id("DATAACCESS"),
        "dataset_id": dataset_id,
        "actor_id": actor_id,
        "action": action.strip().upper(),
        "purpose": purpose.strip(),
        "decision": outcome,
        "evidence_refs": refs,
        "created_at": utc_now_iso(),
    }
    await db.data_access_audit.insert_one(dict(row))
    return row
