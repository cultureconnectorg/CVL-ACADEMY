"""Cross-domain critical decision proof (FD-005 / GOV-007 / GOV-008 / PG-09).

This is not a second signature engine. It reuses the existing EvidencePackage/FREK
Notary bridge to bind one canonical authority decision, one resource digest, and the
exact governing policy version. A notarized proof is evidence, never a legal-effect
claim by itself.
"""

from __future__ import annotations

import uuid
from typing import Any, Dict, Iterable

from db import db, utc_now_iso
from services import policy_registry, proof_bridge
from services import professional_governance as governance

CRITICAL_DOMAINS = {"GOVERNANCE", "LEGAL", "PRIVACY", "SECURITY", "ACCOUNTING", "RISK", "QUALITY"}


def _id(prefix: str) -> str:
    return f"{prefix}-{uuid.uuid4()}"


def _refs(values: Iterable[str]) -> list[str]:
    return list(dict.fromkeys(str(v).strip() for v in values if str(v).strip()))


async def create_critical_decision_proof(
    *,
    actor_id: str,
    domain: str,
    resource_type: str,
    resource_id: str,
    resource_hash: str,
    authority_decision_id: str,
    policy_version_id: str,
    evidence_refs: Iterable[str],
) -> Dict[str, Any]:
    target_domain = str(domain or "").upper()
    if target_domain not in CRITICAL_DOMAINS:
        raise ValueError("invalid critical proof domain")
    digest = proof_bridge.validate_sha256(resource_hash)
    refs = _refs(evidence_refs)
    if not resource_type.strip() or not resource_id.strip() or not refs:
        raise ValueError("critical proof requires resource, id and evidence")

    authority = await db.authority_decisions.find_one(
        {"id": authority_decision_id}, {"_id": 0}
    )
    if not authority:
        raise LookupError("authority decision not found")
    if authority.get("decision") != "ALLOW":
        raise ValueError("critical proof requires an ALLOW authority decision")
    if str((authority.get("context") or {}).get("domain", "")).upper() != target_domain:
        raise ValueError("authority decision domain does not match proof domain")
    if authority.get("policy_version_id") != policy_version_id:
        raise ValueError("authority decision and proof must use the same policy version")

    policy = await policy_registry.require_effective_version(policy_version_id)
    if policy["content_hash"] != authority.get("policy_content_hash"):
        raise ValueError("authority policy hash mismatch")

    existing = await db.critical_decision_proofs.find_one(
        {
            "domain": target_domain,
            "resource_type": resource_type.strip().upper(),
            "resource_id": resource_id.strip(),
            "resource_hash": digest,
            "authority_decision_id": authority_decision_id,
            "status": "FREK_NOTARIZED",
        },
        {"_id": 0},
    )
    if existing:
        return existing

    package = proof_bridge.build_evidence_package(
        subject=f"academy:{target_domain.lower()}:{resource_type}:{resource_id}:critical-decision",
        claims=[
            {
                "statement": "Canonical authority decision was bound to this exact resource digest",
                "status": "OBSERVED",
                "evidence_ref": authority_decision_id,
            }
        ],
        artefacts=[
            {
                "type": resource_type.strip().upper(),
                "id": resource_id.strip(),
                "hash": digest,
                "algorithm": "sha256",
            }
        ],
        decisions=[authority_decision_id, policy_version_id],
        events=refs,
    )
    notarized = await proof_bridge.notarize_package(package)
    row = {
        "id": _id("CRITPROOF"),
        "domain": target_domain,
        "resource_type": resource_type.strip().upper(),
        "resource_id": resource_id.strip(),
        "resource_hash": digest,
        "authority_decision_id": authority_decision_id,
        "policy_version_id": policy_version_id,
        "policy_content_hash": policy["content_hash"],
        "evidence_refs": refs,
        "evidence_package": notarized,
        "frek_block_hash": notarized["frek_notary"]["block_hash"],
        "status": "FREK_NOTARIZED",
        "legal_effect": "none",
        "created_by": actor_id,
        "created_at": utc_now_iso(),
    }
    await db.critical_decision_proofs.insert_one(dict(row))
    await governance.audit_event(
        event_type="governance.critical_decision.frek_notarized",
        actor_id=actor_id,
        resource_type=row["resource_type"],
        resource_id=row["resource_id"],
        payload={
            "critical_proof_id": row["id"],
            "domain": target_domain,
            "authority_decision_id": authority_decision_id,
            "policy_version_id": policy_version_id,
            "frek_block_hash": row["frek_block_hash"],
        },
        reason="Critical decision proof anchored through canonical FREK bridge",
        result="FREK_NOTARIZED",
    )
    return row


async def proof_gate(
    *, domain: str, resource_type: str, resource_id: str, resource_hash: str
) -> Dict[str, Any]:
    digest = proof_bridge.validate_sha256(resource_hash)
    proof = await db.critical_decision_proofs.find_one(
        {
            "domain": str(domain).upper(),
            "resource_type": str(resource_type).upper(),
            "resource_id": resource_id,
            "resource_hash": digest,
            "status": "FREK_NOTARIZED",
        },
        {"_id": 0},
        sort=[("created_at", -1)],
    )
    return {
        "pass": bool(proof),
        "critical_proof_id": proof["id"] if proof else None,
        "frek_block_hash": proof.get("frek_block_hash") if proof else None,
    }
