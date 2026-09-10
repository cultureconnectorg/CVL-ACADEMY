"""Versioned accounting mappings (ACC-009) backed by XCP-008.

Accounting mappings are policy, not mutable configuration. Every change is stored as
an immutable governance policy version and the ``accounting_mappings`` collection is
only a current-view projection for existing accounting consumers.

This module does not validate tax law. ``tax_code`` is descriptive until an externally
validated tax policy is linked through evidence.
"""

from __future__ import annotations

from typing import Any, Dict, Iterable, Optional

from db import db, utc_now_iso
from services import policy_registry


def _policy_key(event_type: str) -> str:
    normalized = event_type.strip().upper()
    if not normalized:
        raise ValueError("event_type is required")
    return f"ACCOUNTING_MAPPING::{normalized}"


async def register_mapping_version(
    *,
    actor_id: str,
    event_type: str,
    debit_account: str,
    credit_account: str,
    version: str,
    effective_at: str,
    evidence_refs: Iterable[str],
    tax_code: Optional[str] = None,
    supersedes_version_id: Optional[str] = None,
) -> Dict[str, Any]:
    if not debit_account.strip() or not credit_account.strip():
        raise ValueError("debit_account and credit_account are required")
    refs = list(dict.fromkeys(evidence_refs))
    if not refs:
        raise ValueError("accounting mapping version requires evidence")

    event = event_type.strip().upper()
    policy = await policy_registry.register_version(
        actor_id=actor_id,
        policy_key=_policy_key(event),
        version=version,
        kind="POLICY",
        title=f"Accounting mapping — {event}",
        content={
            "event_type": event,
            "debit_account": debit_account.strip(),
            "credit_account": credit_account.strip(),
            "tax_code": tax_code,
            "tax_validation_status": "NOT_VALIDATED_BY_MAPPING",
        },
        effective_at=effective_at,
        evidence_refs=refs,
        supersedes_version_id=supersedes_version_id,
    )

    current_view = {
        "id": f"MAP::{event}",
        "event_type": event,
        "debit_account": debit_account.strip(),
        "credit_account": credit_account.strip(),
        "tax_code": tax_code,
        "policy_version_id": policy["id"],
        "policy_version": policy["version"],
        "policy_hash": policy["content_hash"],
        "effective_at": policy["effective_at"],
        "evidence_refs": refs,
        "tax_validation_status": "NOT_VALIDATED_BY_MAPPING",
        "status": "ACTIVE",
        "updated_by": actor_id,
        "updated_at": utc_now_iso(),
    }
    await db.accounting_mappings.update_one(
        {"event_type": event}, {"$set": current_view}, upsert=True
    )
    return {**current_view, "governance_policy": policy}


async def get_mapping(event_type: str) -> Dict[str, Any]:
    event = event_type.strip().upper()
    row = await db.accounting_mappings.find_one({"event_type": event}, {"_id": 0})
    if not row:
        raise LookupError("accounting mapping not found")
    version = await policy_registry.require_effective_version(row["policy_version_id"])
    if version["content_hash"] != row.get("policy_hash"):
        raise ValueError("accounting mapping projection integrity check failed")
    return row


async def list_mapping_history(event_type: str) -> list[Dict[str, Any]]:
    return await policy_registry.list_versions(_policy_key(event_type))
