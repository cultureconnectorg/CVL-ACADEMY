"""Scoped external-expert authentication for Professional Governance.

API keys are issued by professional_governance.py and stored only as SHA-256
hashes. This module turns issuance into an enforceable access path: active key
+ active assignment + matching case + required scope are all required.
"""

from __future__ import annotations

import hashlib
from typing import Any, Dict, Iterable

from db import db, utc_now_iso


def _hash(raw: str) -> str:
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def _allows(granted: Iterable[str], required: str) -> bool:
    scopes = set(granted)
    return "*" in scopes or required in scopes


async def authenticate_expert_key(raw_key: str) -> Dict[str, Any]:
    if not raw_key or not raw_key.startswith("cvln_exp_"):
        raise PermissionError("invalid expert credential")
    key = await db.governance_api_keys.find_one(
        {"token_hash": _hash(raw_key), "status": "ACTIVE"}, {"_id": 0}
    )
    if not key:
        raise PermissionError("invalid or revoked expert credential")
    assignment = await db.governance_expert_assignments.find_one(
        {"id": key["assignment_id"], "status": "ACTIVE"}, {"_id": 0}
    )
    if not assignment:
        raise PermissionError("expert assignment is inactive")
    if assignment["expert_id"] != key["expert_id"] or assignment["case_id"] != key["case_id"]:
        raise PermissionError("expert credential assignment mismatch")
    return {"key": key, "assignment": assignment}


async def authorize_case_scope(raw_key: str, case_id: str, required_scope: str) -> Dict[str, Any]:
    context = await authenticate_expert_key(raw_key)
    key = context["key"]
    assignment = context["assignment"]
    if case_id != assignment["case_id"]:
        raise PermissionError("credential is not assigned to this case")
    # Require both the key snapshot and current assignment to allow the scope.
    # This means narrowing an assignment immediately narrows old keys too.
    if not _allows(key.get("scope", []), required_scope):
        raise PermissionError("credential scope denied")
    if not _allows(assignment.get("scope", []), required_scope):
        raise PermissionError("assignment scope denied")
    expert = await db.governance_experts.find_one(
        {"id": assignment["expert_id"], "status": "ACTIVE"}, {"_id": 0}
    )
    if not expert:
        raise PermissionError("expert identity is inactive")
    return {**context, "expert": expert}


async def revoke_expert_api_key(*, actor_id: str, key_id: str) -> Dict[str, Any]:
    key = await db.governance_api_keys.find_one({"id": key_id}, {"_id": 0})
    if not key:
        raise LookupError("expert API key not found")
    if key["status"] == "REVOKED":
        return key
    now = utc_now_iso()
    await db.governance_api_keys.update_one(
        {"id": key_id, "status": "ACTIVE"},
        {"$set": {"status": "REVOKED", "revoked_at": now, "revoked_by": actor_id}},
    )
    return {**key, "status": "REVOKED", "revoked_at": now, "revoked_by": actor_id}
