"""Threat-model registry and attack-case evidence for CVLN Academy.

This is a defensive registry: assets, threats, mitigations and regression-test
references. It does not execute attacks. A threat can only be marked VERIFIED
when concrete test/evidence references are recorded.
"""

from __future__ import annotations

import uuid
from typing import Any, Dict, Iterable, Optional

from db import db, utc_now_iso


THREAT_STATES = {"OPEN", "MITIGATING", "VERIFIED", "ACCEPTED", "CLOSED"}


def _id(prefix: str) -> str:
    return f"{prefix}-{uuid.uuid4()}"


async def create_threat(
    *,
    actor_id: str,
    title: str,
    category: str,
    asset_id: Optional[str],
    attack_surface: str,
    abuse_case: str,
    severity: str,
    mitigations: Iterable[str] = (),
    test_refs: Iterable[str] = (),
) -> Dict[str, Any]:
    sev = severity.upper()
    if sev not in {"LOW", "MEDIUM", "HIGH", "CRITICAL"}:
        raise ValueError("invalid threat severity")
    if asset_id and not await db.security_assets.find_one({"id": asset_id}):
        raise LookupError("security asset not found")
    tests = list(test_refs)
    row = {
        "id": _id("THREAT"),
        "title": title,
        "category": category.upper(),
        "asset_id": asset_id,
        "attack_surface": attack_surface,
        "abuse_case": abuse_case,
        "severity": sev,
        "mitigations": list(mitigations),
        "test_refs": tests,
        "status": "OPEN",
        "created_by": actor_id,
        "created_at": utc_now_iso(),
        "updated_at": utc_now_iso(),
    }
    await db.security_threats.insert_one(dict(row))
    return row


async def add_threat_evidence(
    *,
    actor_id: str,
    threat_id: str,
    mitigation: Optional[str] = None,
    test_ref: Optional[str] = None,
    evidence_ref: Optional[str] = None,
) -> Dict[str, Any]:
    threat = await db.security_threats.find_one({"id": threat_id}, {"_id": 0})
    if not threat:
        raise LookupError("threat not found")
    update: Dict[str, Any] = {"updated_at": utc_now_iso(), "last_actor_id": actor_id}
    pushes: Dict[str, Any] = {}
    if mitigation:
        pushes["mitigations"] = mitigation
    if test_ref:
        pushes["test_refs"] = test_ref
    if evidence_ref:
        pushes["evidence_refs"] = evidence_ref
    mongo_update: Dict[str, Any] = {"$set": update}
    if pushes:
        mongo_update["$push"] = pushes
    await db.security_threats.update_one({"id": threat_id}, mongo_update)
    return await db.security_threats.find_one({"id": threat_id}, {"_id": 0})


async def transition_threat(
    *, actor_id: str, threat_id: str, status: str
) -> Dict[str, Any]:
    target = status.upper()
    if target not in THREAT_STATES:
        raise ValueError("invalid threat status")
    threat = await db.security_threats.find_one({"id": threat_id}, {"_id": 0})
    if not threat:
        raise LookupError("threat not found")
    if target == "VERIFIED":
        if not threat.get("mitigations") or not threat.get("test_refs"):
            raise ValueError("verified threat requires mitigation and regression-test evidence")
    now = utc_now_iso()
    await db.security_threats.update_one(
        {"id": threat_id},
        {"$set": {"status": target, "updated_at": now, "last_actor_id": actor_id}},
    )
    return {**threat, "status": target, "updated_at": now}


async def threat_release_gate() -> Dict[str, Any]:
    blockers = await db.security_threats.find(
        {
            "severity": {"$in": ["HIGH", "CRITICAL"]},
            "status": {"$nin": ["VERIFIED", "ACCEPTED", "CLOSED"]},
        },
        {"_id": 0},
    ).to_list(1000)
    return {
        "pass": len(blockers) == 0,
        "blocking_count": len(blockers),
        "blocking_threats": blockers,
    }
