"""Canonical native Trust & Signature service (TRU-01..TRU-14).

This service extends the existing FREK EvidencePackage bridge; it does not implement a
second cryptographic notary. It supports Legal, Quality and user-facing acknowledgements
with exact-version hashes, explicit signer identity/authority, intent, revocation,
delegation and multi-signature completion. FREK proof remains evidence and never creates
an eIDAS/legal-effect claim automatically.
"""

from __future__ import annotations

import uuid
from typing import Any, Dict, Iterable, Optional

from db import db, utc_now_iso
from services import evidence_graph, proof_bridge
from services import native_attestation_verifier
from services import professional_governance as governance

SIGNATURE_STATES = {"OPEN", "COMPLETE", "INVALIDATED", "CANCELLED"}
AUTH_STATES = {"AUTHORIZED", "REVOKED"}


def _id(prefix: str) -> str:
    return f"{prefix}-{uuid.uuid4()}"


def _refs(values: Iterable[str]) -> list[str]:
    return list(dict.fromkeys(str(v).strip() for v in values if str(v).strip()))


async def create_signature_request(
    *,
    actor_id: str,
    subject_type: str,
    subject_id: str,
    document_version_id: str,
    document_hash: str,
    required_signers: Iterable[Dict[str, Any]],
    evidence_refs: Iterable[str],
) -> Dict[str, Any]:
    digest = proof_bridge.validate_sha256(document_hash)
    refs = _refs(evidence_refs)
    signers = [dict(item) for item in required_signers]
    if not subject_type.strip() or not subject_id.strip() or not document_version_id.strip():
        raise ValueError("signature request requires subject and exact document version")
    if not refs or not signers:
        raise ValueError("signature request requires evidence and at least one signer")
    normalized = []
    identities = set()
    for signer in signers:
        user_id = str(signer.get("signer_user_id") or "").strip()
        frek_id = str(signer.get("signer_frek_id") or "").strip()
        role = str(signer.get("signer_role") or "").strip().upper()
        if not user_id or not frek_id or not role:
            raise ValueError("every signer requires user id, FREK id and role")
        key = (user_id, frek_id)
        if key in identities:
            raise ValueError("duplicate signer identity")
        identities.add(key)
        normalized.append(
            {"signer_user_id": user_id, "signer_frek_id": frek_id, "signer_role": role}
        )

    row = {
        "id": _id("SIGREQ"),
        "subject_type": subject_type.strip().upper(),
        "subject_id": subject_id.strip(),
        "document_version_id": document_version_id.strip(),
        "document_hash": digest,
        "required_signers": normalized,
        "evidence_refs": refs,
        "status": "OPEN",
        "created_by": actor_id,
        "created_at": utc_now_iso(),
        "completed_at": None,
    }
    await db.trust_signature_requests.insert_one(dict(row))
    for signer in normalized:
        auth = {
            "id": _id("TRUAUTH"),
            "signature_request_id": row["id"],
            **signer,
            "status": "AUTHORIZED",
            "delegated_from_authorization_id": None,
            "delegation_evidence_refs": [],
            "authorized_by": actor_id,
            "authorized_at": utc_now_iso(),
        }
        await db.trust_signer_authorizations.insert_one(auth)
    await governance.audit_event(
        event_type="trust.signature_request.created",
        actor_id=actor_id,
        resource_type=row["subject_type"],
        resource_id=row["subject_id"],
        payload={
            "signature_request_id": row["id"],
            "document_version_id": row["document_version_id"],
            "document_hash": digest,
            "required_signer_count": len(normalized),
        },
        reason="Exact document version opened for native signature",
        result="OPEN",
    )
    return row


async def delegate_signer_authority(
    *,
    actor_id: str,
    authorization_id: str,
    delegate_user_id: str,
    delegate_frek_id: str,
    delegate_role: str,
    evidence_refs: Iterable[str],
) -> Dict[str, Any]:
    original = await db.trust_signer_authorizations.find_one(
        {"id": authorization_id, "status": "AUTHORIZED"}, {"_id": 0}
    )
    if not original:
        raise LookupError("active signer authorization not found")
    request = await db.trust_signature_requests.find_one(
        {"id": original["signature_request_id"], "status": "OPEN"}, {"_id": 0}
    )
    if not request:
        raise ValueError("signature request is not open")
    refs = _refs(evidence_refs)
    if not refs:
        raise ValueError("delegated signature authority requires evidence")
    if not delegate_user_id.strip() or not delegate_frek_id.strip() or not delegate_role.strip():
        raise ValueError("delegate identity and role are required")
    row = {
        "id": _id("TRUAUTH"),
        "signature_request_id": original["signature_request_id"],
        "signer_user_id": delegate_user_id.strip(),
        "signer_frek_id": delegate_frek_id.strip(),
        "signer_role": delegate_role.strip().upper(),
        "status": "AUTHORIZED",
        "delegated_from_authorization_id": original["id"],
        "delegation_evidence_refs": refs,
        "authorized_by": actor_id,
        "authorized_at": utc_now_iso(),
    }
    await db.trust_signer_authorizations.insert_one(dict(row))
    await governance.audit_event(
        event_type="trust.signer_authority.delegated",
        actor_id=actor_id,
        resource_type="trust_signature_request",
        resource_id=original["signature_request_id"],
        payload={
            "from_authorization_id": original["id"],
            "to_authorization_id": row["id"],
            "evidence_refs": refs,
        },
        reason="Delegated signature authority with explicit evidence",
        result="AUTHORIZED",
    )
    return row


async def revoke_signer_authority(
    *, actor_id: str, authorization_id: str, evidence_refs: Iterable[str]
) -> Dict[str, Any]:
    row = await db.trust_signer_authorizations.find_one(
        {"id": authorization_id}, {"_id": 0}
    )
    if not row:
        raise LookupError("signer authorization not found")
    refs = _refs(evidence_refs)
    if not refs:
        raise ValueError("signature revocation requires evidence")
    if row["status"] == "REVOKED":
        return row
    now = utc_now_iso()
    update = {
        "status": "REVOKED",
        "revocation_evidence_refs": refs,
        "revoked_by": actor_id,
        "revoked_at": now,
    }
    result = await db.trust_signer_authorizations.update_one(
        {"id": authorization_id, "status": "AUTHORIZED"}, {"$set": update}
    )
    if result.modified_count != 1:
        raise ValueError("signer authorization changed concurrently")
    await governance.audit_event(
        event_type="trust.signer_authority.revoked",
        actor_id=actor_id,
        resource_type="trust_signer_authorization",
        resource_id=authorization_id,
        payload={"signature_request_id": row["signature_request_id"], "evidence_refs": refs},
        reason="Signer authority revoked",
        result="REVOKED",
    )
    return {**row, **update}


async def sign_intent(
    *,
    actor_id: str,
    actor_frek_id: str,
    signature_request_id: str,
    document_hash: str,
    intent: str,
    evidence_refs: Iterable[str] = (),
) -> Dict[str, Any]:
    if str(intent or "").upper() != "SIGN":
        raise ValueError("explicit SIGN intent is required")
    request = await db.trust_signature_requests.find_one(
        {"id": signature_request_id, "status": "OPEN"}, {"_id": 0}
    )
    if not request:
        raise LookupError("open signature request not found")
    digest = proof_bridge.validate_sha256(document_hash)
    if digest != request["document_hash"]:
        raise ValueError("document hash differs from exact signature request version")
    auth = await db.trust_signer_authorizations.find_one(
        {
            "signature_request_id": signature_request_id,
            "signer_user_id": actor_id,
            "signer_frek_id": actor_frek_id,
            "status": "AUTHORIZED",
        },
        {"_id": 0},
    )
    if not auth:
        raise PermissionError("actor has no active signer authority for this request")
    existing = await db.trust_signatures.find_one(
        {
            "signature_request_id": signature_request_id,
            "authorization_id": auth["id"],
            "document_hash": digest,
            "status": "FREK_NOTARIZED",
        },
        {"_id": 0},
    )
    if existing:
        return existing

    refs = _refs(evidence_refs)
    package = proof_bridge.build_evidence_package(
        subject=f"academy:signature:{signature_request_id}:{auth['id']}",
        claims=[
            {
                "statement": "Authorized signer explicitly asserted SIGN intent for exact digest",
                "status": "OBSERVED",
                "evidence_ref": auth["id"],
            }
        ],
        artefacts=[
            {
                "type": request["subject_type"],
                "id": request["document_version_id"],
                "hash": digest,
                "algorithm": "sha256",
            }
        ],
        events=[f"actor:{actor_id}:SIGN", f"frek:{actor_frek_id}"],
        decisions=[auth["id"], *refs],
    )
    notarized = await proof_bridge.notarize_package(package)
    row = {
        "id": _id("TRUSIG"),
        "signature_request_id": signature_request_id,
        "authorization_id": auth["id"],
        "signer_user_id": actor_id,
        "signer_frek_id": actor_frek_id,
        "document_version_id": request["document_version_id"],
        "document_hash": digest,
        "intent": "SIGN",
        "evidence_package": notarized,
        "status": "FREK_NOTARIZED",
        "verification_status": "PENDING_INDEPENDENT_VERIFICATION",
        "legal_effect": "none",
        "created_at": utc_now_iso(),
    }
    await db.trust_signatures.insert_one(dict(row))
    return row


async def verify_signature(*, actor_id: str, signature_id: str) -> Dict[str, Any]:
    signature = await db.trust_signatures.find_one({"id": signature_id}, {"_id": 0})
    if not signature:
        raise LookupError("trust signature not found")
    package = signature["evidence_package"]
    local = proof_bridge.verify_evidence_package(package)
    remote = await native_attestation_verifier.fetch_frek_proof(package["package_id"])
    block = remote.get("block") or {}
    stored = package.get("frek_notary") or {}
    checks = {
        "local_chain_hash": bool(local.get("chain_hash_valid")),
        "local_artefact_hashes": bool(local.get("valid_local_hashes")),
        "remote_payload_id": remote.get("payload_id") == package.get("package_id"),
        "stored_block_hash": block.get("block_hash") == stored.get("block_hash"),
        "stored_payload_hash": block.get("payload_hash") == stored.get("payload_hash"),
        "authorization_active": bool(
            await db.trust_signer_authorizations.find_one(
                {"id": signature["authorization_id"], "status": "AUTHORIZED"}
            )
        ),
    }
    passed = all(checks.values())
    row = {
        "id": _id("TRUSIGVER"),
        "signature_id": signature_id,
        "signature_request_id": signature["signature_request_id"],
        "status": "VERIFIED_FREK" if passed else "FAILED",
        "checks": checks,
        "verified_by": actor_id,
        "verified_at": utc_now_iso(),
        "legal_effect": "none",
    }
    await db.trust_signature_verifications.insert_one(dict(row))
    await db.trust_signatures.update_one(
        {"id": signature_id}, {"$set": {"verification_status": row["status"]}}
    )
    return row


async def evaluate_multisignature(signature_request_id: str) -> Dict[str, Any]:
    request = await db.trust_signature_requests.find_one(
        {"id": signature_request_id}, {"_id": 0}
    )
    if not request:
        raise LookupError("signature request not found")
    required = {
        (item["signer_user_id"], item["signer_frek_id"])
        for item in request["required_signers"]
    }
    verified_signatures = await db.trust_signatures.find(
        {"signature_request_id": signature_request_id, "verification_status": "VERIFIED_FREK"},
        {"_id": 0},
    ).to_list(1000)
    verified = {
        (item["signer_user_id"], item["signer_frek_id"])
        for item in verified_signatures
        if await db.trust_signer_authorizations.find_one(
            {"id": item["authorization_id"], "status": "AUTHORIZED"}
        )
    }
    missing = sorted(required - verified)
    complete = not missing
    if complete and request["status"] == "OPEN":
        now = utc_now_iso()
        await db.trust_signature_requests.update_one(
            {"id": signature_request_id, "status": "OPEN"},
            {"$set": {"status": "COMPLETE", "completed_at": now}},
        )
    return {
        "signature_request_id": signature_request_id,
        "pass": complete,
        "required_count": len(required),
        "verified_count": len(required & verified),
        "missing_signers": [
            {"signer_user_id": item[0], "signer_frek_id": item[1]} for item in missing
        ],
    }


async def invalidate_document_version(
    *,
    actor_id: str,
    signature_request_id: str,
    replacement_version_id: Optional[str],
    replacement_hash: Optional[str],
    evidence_refs: Iterable[str],
) -> Dict[str, Any]:
    request = await db.trust_signature_requests.find_one(
        {"id": signature_request_id}, {"_id": 0}
    )
    if not request:
        raise LookupError("signature request not found")
    refs = _refs(evidence_refs)
    if not refs:
        raise ValueError("document invalidation requires evidence")
    digest = proof_bridge.validate_sha256(replacement_hash) if replacement_hash else None
    now = utc_now_iso()
    update = {
        "status": "INVALIDATED",
        "invalidated_by": actor_id,
        "invalidated_at": now,
        "invalidation_evidence_refs": refs,
        "replacement_version_id": replacement_version_id,
        "replacement_hash": digest,
    }
    await db.trust_signature_requests.update_one(
        {"id": signature_request_id}, {"$set": update}
    )
    await db.trust_signer_authorizations.update_many(
        {"signature_request_id": signature_request_id, "status": "AUTHORIZED"},
        {"$set": {"status": "REVOKED", "revoked_at": now, "revoked_by": actor_id}},
    )
    await governance.audit_event(
        event_type="trust.document_version.invalidated",
        actor_id=actor_id,
        resource_type=request["subject_type"],
        resource_id=request["subject_id"],
        payload={
            "signature_request_id": signature_request_id,
            "old_hash": request["document_hash"],
            "replacement_hash": digest,
            "evidence_refs": refs,
        },
        reason="Signed document version invalidated; old signer authority revoked",
        result="INVALIDATED",
    )
    return {**request, **update}


async def create_signature_evidence_pack(
    *,
    actor_id: str,
    signature_request_id: str,
    evidence_node_ids: Iterable[str],
    evidence_refs: Iterable[str],
) -> Dict[str, Any]:
    request = await db.trust_signature_requests.find_one(
        {"id": signature_request_id}, {"_id": 0}
    )
    if not request:
        raise LookupError("signature request not found")
    return await evidence_graph.create_pack(
        actor_id=actor_id,
        title=f"Signature evidence — {signature_request_id}",
        consumer="GOVERNANCE",
        node_ids=evidence_node_ids,
        purpose="Native signature verification and audit evidence",
        evidence_refs=[signature_request_id, *_refs(evidence_refs)],
    )
