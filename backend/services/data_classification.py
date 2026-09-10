"""Cross-cutting Data Classification Engine (XCP-002).

Excel target: classify every object, datum and provider explicitly, and detect
unclassified resources. This module deliberately reuses the existing
``privacy_data_classes`` registry and XCP-008 policy versions; it does not create
another taxonomy or silently infer sensitive classifications from raw content.
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
    if not rationale.strip():
        raise ValueError("classification rationale is required")
    refs = list(dict.fromkeys(evidence_refs))
    if not refs:
        raise ValueError("classification requires evidence")

    policy = await policy_registry.require_effective_version(policy_version_id)
    if policy.get("policy_key") != "DATA_CLASSIFICATION":
        raise ValueError("policy version is not a DATA_CLASSIFICATION policy")

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
        "data_class_code": code,
        "sensitivity": data_class.get("sensitivity"),
        "legal_basis_required": bool(data_class.get("legal_basis_required", True)),
        "retention_days": data_class.get("retention_days"),
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
