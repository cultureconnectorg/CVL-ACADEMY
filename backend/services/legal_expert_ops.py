"""Scoped legal-expert write operations (FD-L01).

A legal expert may modify a legal matter directly only when all of the following
are true at the same time:
- the inbound professional credential is active and grants legal:matter:write;
- the professional case is LEGAL and the matter belongs to that exact case;
- the expert identity declares the LEGAL domain;
- the canonical Authority Policy Engine returns ALLOW for the requested action;
- every mutation is recorded as an append-only change record and governance audit.

This module deliberately exposes an allow-list of mutable fields. Identity,
case linkage, creator metadata and lifecycle state cannot be rewritten through
this direct expert-edit path.
"""

from __future__ import annotations

import hashlib
import json
import uuid
from typing import Any, Dict, Iterable

from db import db, utc_now_iso
from services import authority_policy, expert_access
from services import professional_governance as governance


WRITE_SCOPE = "legal:matter:write"
MUTABLE_FIELDS = {"title", "jurisdiction", "owner_id", "risk_ids", "evidence_refs"}
PROTECTED_FIELDS = {
    "id",
    "case_id",
    "matter_type",
    "status",
    "created_by",
    "created_at",
    "updated_by",
    "updated_at",
}


def _id(prefix: str) -> str:
    return f"{prefix}-{uuid.uuid4()}"


def _hash(payload: Dict[str, Any]) -> str:
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def _normalise_patch(patch: Dict[str, Any]) -> Dict[str, Any]:
    if not patch:
        raise ValueError("legal expert modification requires at least one field")
    forbidden = sorted(set(patch) & PROTECTED_FIELDS)
    unknown = sorted(set(patch) - MUTABLE_FIELDS - PROTECTED_FIELDS)
    if forbidden:
        raise PermissionError(f"protected legal fields cannot be modified: {', '.join(forbidden)}")
    if unknown:
        raise ValueError(f"unsupported legal matter fields: {', '.join(unknown)}")

    result: Dict[str, Any] = {}
    for key, value in patch.items():
        if key == "title":
            title = str(value or "").strip()
            if not title:
                raise ValueError("title cannot be empty")
            result[key] = title
        elif key in {"risk_ids", "evidence_refs"}:
            if value is None:
                result[key] = []
            elif not isinstance(value, (list, tuple, set)):
                raise ValueError(f"{key} must be a list")
            else:
                result[key] = list(dict.fromkeys(str(item) for item in value if str(item)))
        elif key in {"jurisdiction", "owner_id"}:
            result[key] = str(value).strip() if value is not None else None
    return result


async def modify_legal_matter(
    *,
    raw_key: str,
    case_id: str,
    matter_id: str,
    patch: Dict[str, Any],
    policy_version_id: str,
    rationale: str,
    evidence_refs: Iterable[str],
) -> Dict[str, Any]:
    """Apply one direct expert edit with scope, policy and evidence gates."""
    rationale = (rationale or "").strip()
    refs = list(dict.fromkeys(str(ref) for ref in evidence_refs if str(ref)))
    if not rationale:
        raise ValueError("expert modification rationale is required")
    if not refs:
        raise ValueError("expert modification requires evidence")
    if not policy_version_id.strip():
        raise ValueError("policy_version_id is required")

    changes = _normalise_patch(patch)
    context = await expert_access.authorize_case_scope(raw_key, case_id, WRITE_SCOPE)
    expert = context["expert"]
    assignment = context["assignment"]

    if "LEGAL" not in {str(domain).upper() for domain in expert.get("domains", [])}:
        raise PermissionError("expert identity is not authorised for LEGAL domain")

    case = await db.professional_cases.find_one({"id": case_id}, {"_id": 0})
    if not case:
        raise LookupError("professional case not found")
    if str(case.get("domain", "")).upper() != "LEGAL":
        raise PermissionError("direct legal modification requires a LEGAL professional case")

    matter = await db.legal_matters.find_one({"id": matter_id}, {"_id": 0})
    if not matter:
        raise LookupError("legal matter not found")
    if matter.get("case_id") != case_id:
        raise PermissionError("legal matter is outside the assigned professional case")

    authority = await authority_policy.evaluate_authority(
        actor_id=expert["id"],
        actor_role="EXTERNAL_EXPERT",
        action="LEGAL_EXPERT_MODIFY",
        context={
            "domain": "LEGAL",
            "jurisdiction": matter.get("jurisdiction") or case.get("metadata", {}).get("jurisdiction"),
            "sensitivity": case.get("sensitivity", "INTERNAL"),
            "authority_level": assignment.get("authority_level", "A3_EXTERNAL_EXPERT"),
            "case_id": case_id,
            "matter_id": matter_id,
        },
        policy_version_id=policy_version_id,
    )
    if authority["decision"] != "ALLOW":
        raise PermissionError(
            f"authority policy did not allow legal expert modification: {authority['decision']}"
        )

    before = {field: matter.get(field) for field in changes}
    after = {**before, **changes}
    if before == after:
        raise ValueError("expert modification does not change the legal matter")

    now = utc_now_iso()
    change = {
        "id": _id("LEXCHG"),
        "case_id": case_id,
        "matter_id": matter_id,
        "expert_id": expert["id"],
        "assignment_id": assignment["id"],
        "credential_key_id": context["key"]["id"],
        "scope": WRITE_SCOPE,
        "before": before,
        "after": after,
        "rationale": rationale,
        "evidence_refs": refs,
        "authority_decision_id": authority["id"],
        "policy_version_id": authority["policy_version_id"],
        "policy_content_hash": authority["policy_content_hash"],
        "created_at": now,
    }
    change["change_hash"] = _hash(change)

    result = await db.legal_matters.update_one(
        {
            "id": matter_id,
            "case_id": case_id,
            "updated_at": matter.get("updated_at"),
        },
        {
            "$set": {
                **changes,
                "updated_at": now,
                "updated_by": expert["id"],
                "last_expert_change_id": change["id"],
            }
        },
    )
    if result.modified_count != 1:
        raise ValueError("legal matter changed concurrently; expert edit was not applied")

    await db.legal_expert_changes.insert_one(dict(change))
    await governance.audit_event(
        event_type="legal.expert.matter_modified",
        actor_id=expert["id"],
        resource_type="legal_matter",
        resource_id=matter_id,
        payload={
            "case_id": case_id,
            "assignment_id": assignment["id"],
            "change_id": change["id"],
            "change_hash": change["change_hash"],
            "changed_fields": sorted(changes),
            "authority_decision_id": authority["id"],
            "policy_version_id": authority["policy_version_id"],
            "evidence_refs": refs,
        },
    )

    updated = await db.legal_matters.find_one({"id": matter_id}, {"_id": 0})
    return {"matter": updated, "change": change, "authority": authority}
