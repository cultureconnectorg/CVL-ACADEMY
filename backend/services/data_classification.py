"""Cross-cutting Data Classification Engine (XCP-002 / PRI-001).

Every Academy object, datum and provider classification is explicit. The engine reuses
``privacy_data_classes`` plus canonical policy versions and refuses a classification
that omits the founder-required operational context: purpose, legal basis when needed,
retention, owner, processor declaration, location and access policy.
"""

from __future__ import annotations

import hashlib
import json
import uuid
from typing import Any, Dict, Iterable, Optional

from db import db, utc_now_iso
from services import policy_registry
from services import professional_governance as governance

RESOURCE_KINDS = {"OBJECT", "DATA", "PROVIDER"}


def _id(prefix: str) -> str:
    return f"{prefix}-{uuid.uuid4()}"


def _hash(payload: Dict[str, Any]) -> str:
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def _normalise_refs(values: Iterable[str]) -> list[str]:
    return sorted({str(value).strip() for value in values if str(value).strip()})


async def declare_resource(
    *,
    actor_id: str,
    resource_kind: str,
    resource_type: str,
    resource_id: str,
    owner: str,
    source: str,
    metadata: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    kind = resource_kind.strip().upper()
    if kind not in RESOURCE_KINDS:
        raise ValueError("resource_kind must be OBJECT, DATA or PROVIDER")
    if not all(str(v).strip() for v in (resource_type, resource_id, owner, source)):
        raise ValueError("resource_type, resource_id, owner and source are required")
    key = {
        "resource_kind": kind,
        "resource_type": resource_type.strip().upper(),
        "resource_id": resource_id.strip(),
    }
    existing = await db.classification_resources.find_one(key, {"_id": 0})
    if existing:
        return existing
    row = {
        "id": _id("CRES"),
        **key,
        "owner": owner.strip(),
        "source": source.strip().upper(),
        "metadata": metadata or {},
        "metadata_hash": _hash(metadata or {}),
        "classification_status": "UNCLASSIFIED",
        "current_classification_id": None,
        "declared_by": actor_id,
        "declared_at": utc_now_iso(),
        "updated_at": utc_now_iso(),
    }
    await db.classification_resources.insert_one(dict(row))
    await governance.audit_event(
        event_type="classification.resource.declared",
        actor_id=actor_id,
        resource_type="classification_resource",
        resource_id=row["id"],
        payload={
            "resource_kind": kind,
            "resource_type": row["resource_type"],
            "resource_id": row["resource_id"],
        },
    )
    return row


async def classify_resource(
    *,
    actor_id: str,
    resource_record_id: str,
    data_class_code: str,
    policy_version_id: str,
    access_policy_version_id: str,
    purpose: str,
    legal_basis: Optional[str],
    retention_days: Optional[int],
    processor_refs: Iterable[str],
    locations: Iterable[str],
    rationale: str,
    evidence_refs: Iterable[str],
    handling_controls: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    resource = await db.classification_resources.find_one(
        {"id": resource_record_id}, {"_id": 0}
    )
    if not resource:
        raise LookupError("classification resource not found")
    code = data_class_code.strip().upper()
    data_class = await db.privacy_data_classes.find_one({"code": code}, {"_id": 0})
    if not data_class:
        raise LookupError("registered data class not found")
    if not purpose.strip() or not rationale.strip():
        raise ValueError("classification purpose and rationale are required")
    refs = _normalise_refs(evidence_refs)
    locations_list = _normalise_refs(locations)
    processors = _normalise_refs(processor_refs)
    if not refs or not locations_list:
        raise ValueError("classification requires evidence and at least one location")
    if bool(data_class.get("legal_basis_required", True)) and not str(legal_basis or "").strip():
        raise ValueError("legal basis is required for this data class")
    if retention_days is None or int(retention_days) < 0:
        raise ValueError("classification requires an explicit non-negative retention_days")

    policy = await policy_registry.require_effective_version(policy_version_id)
    if policy.get("policy_key") != "DATA_CLASSIFICATION":
        raise ValueError("policy version is not a DATA_CLASSIFICATION policy")
    access_policy = await policy_registry.require_effective_version(access_policy_version_id)
    if access_policy.get("policy_key") != "DATA_ACCESS":
        raise ValueError("access policy version is not a DATA_ACCESS policy")

    previous = await db.resource_classifications.find_one(
        {"resource_record_id": resource_record_id, "status": "CURRENT"}, {"_id": 0}
    )
    now = utc_now_iso()
    row = {
        "id": _id("CLASS"),
        "resource_record_id": resource_record_id,
        "resource_kind": resource["resource_kind"],
        "resource_type": resource["resource_type"],
        "resource_id": resource["resource_id"],
        "owner": resource["owner"],
        "data_class_code": code,
        "sensitivity": data_class.get("sensitivity"),
        "purpose": purpose.strip(),
        "legal_basis": str(legal_basis).strip() if legal_basis is not None else None,
        "legal_basis_required": bool(data_class.get("legal_basis_required", True)),
        "retention_days": int(retention_days),
        "processor_refs": processors,
        "locations": locations_list,
        "access_policy_version_id": access_policy["id"],
        "access_policy_hash": access_policy["content_hash"],
        "handling_controls": handling_controls or {},
        "rationale": rationale.strip(),
        "evidence_refs": refs,
        "policy_version_id": policy["id"],
        "policy_version": policy["version"],
        "policy_hash": policy["content_hash"],
        "supersedes_classification_id": previous["id"] if previous else None,
        "status": "CURRENT",
        "classified_by": actor_id,
        "classified_at": now,
    }
    row["classification_hash"] = _hash(row)
    if previous:
        result = await db.resource_classifications.update_one(
            {"id": previous["id"], "status": "CURRENT"},
            {"$set": {"status": "SUPERSEDED", "superseded_at": now, "superseded_by": row["id"]}},
        )
        if result.modified_count != 1:
            raise ValueError("classification changed concurrently")
    await db.resource_classifications.insert_one(dict(row))
    await db.classification_resources.update_one(
        {"id": resource_record_id},
        {"$set": {"classification_status": "CLASSIFIED", "current_classification_id": row["id"], "updated_at": now}},
    )
    await governance.audit_event(
        event_type="classification.resource.classified",
        actor_id=actor_id,
        resource_type="classification_resource",
        resource_id=resource_record_id,
        payload={
            "classification_id": row["id"],
            "data_class_code": code,
            "policy_version_id": policy["id"],
            "access_policy_version_id": access_policy["id"],
            "classification_hash": row["classification_hash"],
        },
    )
    return row


async def get_resource(resource_record_id: str) -> Dict[str, Any]:
    resource = await db.classification_resources.find_one(
        {"id": resource_record_id}, {"_id": 0}
    )
    if not resource:
        raise LookupError("classification resource not found")
    current = None
    if resource.get("current_classification_id"):
        current = await db.resource_classifications.find_one(
            {"id": resource["current_classification_id"]}, {"_id": 0}
        )
    return {**resource, "classification": current}


async def unclassified_gate(*, resource_kind: Optional[str] = None) -> Dict[str, Any]:
    query: Dict[str, Any] = {"classification_status": {"$ne": "CLASSIFIED"}}
    if resource_kind:
        kind = resource_kind.strip().upper()
        if kind not in RESOURCE_KINDS:
            raise ValueError("invalid resource_kind")
        query["resource_kind"] = kind
    rows = await db.classification_resources.find(query, {"_id": 0}).to_list(5000)
    return {
        "pass": len(rows) == 0,
        "unclassified_count": len(rows),
        "unclassified_resources": rows,
    }
