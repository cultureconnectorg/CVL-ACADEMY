"""Canonical Doctrine / Policy Version Registry (XCP-008).

One cross-cutting registry is shared by authority, legal, privacy, security, risk
and quality. Version content and effective date are immutable. Supersession is
recorded as lifecycle metadata so historical decisions keep the exact version
and hash that governed them.
"""

from __future__ import annotations

import hashlib
import json
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, Optional

from db import db, utc_now_iso
from services import professional_governance as governance


KINDS = {"DOCTRINE", "POLICY", "PROTOCOL", "RULE", "STANDARD"}


def _id(prefix: str) -> str:
    return f"{prefix}-{uuid.uuid4()}"


def _canonical_hash(payload: Dict[str, Any]) -> str:
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def parse_instant(value: str) -> datetime:
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except (TypeError, ValueError) as exc:
        raise ValueError("effective_at must be ISO-8601") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ValueError("effective_at must include timezone")
    return parsed.astimezone(timezone.utc)


def _content_envelope(
    *, policy_key: str, version: str, kind: str, title: str, content: Dict[str, Any], effective_at: str
) -> Dict[str, Any]:
    return {
        "policy_key": policy_key,
        "version": version,
        "kind": kind,
        "title": title,
        "content": content,
        "effective_at": effective_at,
    }


async def register_version(
    *,
    actor_id: str,
    policy_key: str,
    version: str,
    kind: str,
    title: str,
    content: Dict[str, Any],
    effective_at: str,
    evidence_refs: Iterable[str],
    supersedes_version_id: Optional[str] = None,
) -> Dict[str, Any]:
    key = policy_key.strip().upper()
    ver = version.strip()
    normalized_kind = kind.strip().upper()
    refs = list(dict.fromkeys(evidence_refs))
    if not key or not ver or not title.strip():
        raise ValueError("policy_key, version and title are required")
    if normalized_kind not in KINDS:
        raise ValueError("invalid doctrine/policy kind")
    if not refs:
        raise ValueError("policy version requires evidence")
    parse_instant(effective_at)
    if await db.governance_policy_versions.find_one({"policy_key": key, "version": ver}):
        raise ValueError("policy version already exists")

    active = await db.governance_policy_versions.find_one(
        {"policy_key": key, "status": "ACTIVE"}, {"_id": 0}
    )
    superseded = None
    if active:
        if not supersedes_version_id:
            raise ValueError("existing active version must be explicitly superseded")
        if active["id"] != supersedes_version_id:
            raise ValueError("supersedes_version_id is not the active version")
        superseded = active
    elif supersedes_version_id:
        raise ValueError("cannot supersede a policy with no active version")

    envelope = _content_envelope(
        policy_key=key,
        version=ver,
        kind=normalized_kind,
        title=title.strip(),
        content=content,
        effective_at=effective_at,
    )
    now = utc_now_iso()
    row = {
        "id": _id("POLV"),
        **envelope,
        "content_hash": _canonical_hash(envelope),
        "evidence_refs": refs,
        "status": "ACTIVE",
        "supersedes_version_id": supersedes_version_id,
        "superseded_by_version_id": None,
        "superseded_at": None,
        "content_immutable": True,
        "created_by": actor_id,
        "created_at": now,
    }

    if superseded:
        result = await db.governance_policy_versions.update_one(
            {"id": superseded["id"], "status": "ACTIVE"},
            {
                "$set": {
                    "status": "SUPERSEDED",
                    "superseded_by_version_id": row["id"],
                    "superseded_at": now,
                }
            },
        )
        if result.modified_count != 1:
            raise ValueError("active policy changed during supersession")

    await db.governance_policy_versions.insert_one(dict(row))
    await governance.audit_event(
        event_type="governance.policy_version.registered",
        actor_id=actor_id,
        resource_type="governance_policy_version",
        resource_id=row["id"],
        payload={
            "policy_key": key,
            "version": ver,
            "kind": normalized_kind,
            "content_hash": row["content_hash"],
            "supersedes_version_id": supersedes_version_id,
        },
    )
    return row


async def get_version(version_id: str) -> Dict[str, Any]:
    row = await db.governance_policy_versions.find_one({"id": version_id}, {"_id": 0})
    if not row:
        raise LookupError("policy version not found")
    return row


async def verify_version_integrity(version: Dict[str, Any]) -> bool:
    envelope = _content_envelope(
        policy_key=version["policy_key"],
        version=version["version"],
        kind=version["kind"],
        title=version["title"],
        content=version["content"],
        effective_at=version["effective_at"],
    )
    return _canonical_hash(envelope) == version.get("content_hash")


async def require_effective_version(version_id: str, *, at: Optional[datetime] = None) -> Dict[str, Any]:
    row = await get_version(version_id)
    if row.get("status") != "ACTIVE" or not row.get("content_immutable"):
        raise ValueError("policy version is not active and immutable")
    if not await verify_version_integrity(row):
        raise ValueError("policy version integrity check failed")
    moment = at or datetime.now(timezone.utc)
    if parse_instant(row["effective_at"]) > moment.astimezone(timezone.utc):
        raise ValueError("policy version is not yet effective")
    return row


async def list_versions(policy_key: Optional[str] = None) -> list[Dict[str, Any]]:
    query: Dict[str, Any] = {}
    if policy_key:
        query["policy_key"] = policy_key.strip().upper()
    return await db.governance_policy_versions.find(query, {"_id": 0}).sort("created_at", -1).to_list(1000)
