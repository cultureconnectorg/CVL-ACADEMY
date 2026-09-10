"""CVLN Academy proof bridge — EvidencePackage + FREK Notary.

This is a clean Academy implementation of two existing CVLN contracts:

* CVLN Intelligence OS EvidencePackage v1.1: content-addressed artefacts,
  ordered chain hash, independent verification fields, and ``legal_effect=none``.
* FREKCORE Notary: ``POST /api/v1/notary/notarize`` with an ``emit`` client.

The bridge deliberately does NOT fabricate a legal/eIDAS signature. A native Academy
attestation is cryptographic evidence of a user's signing intent and document digest;
it is not a qualified signature and does not by itself move a contract to SIGNED.
"""

from __future__ import annotations

import hashlib
import json
import os
import uuid
from typing import Any, Dict, Iterable, Optional

import httpx

from db import db, utc_now_iso


class FrekNotaryUnavailable(RuntimeError):
    """Raised when Academy cannot obtain a real FREK notary block."""


class InvalidEvidence(ValueError):
    """Raised when evidence inputs cannot be verified locally."""


def _id(prefix: str) -> str:
    return f"{prefix}-{uuid.uuid4()}"


def _canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, default=str
    ).encode("utf-8")


def sha256_hex(value: Any) -> str:
    raw = value if isinstance(value, bytes) else _canonical_bytes(value)
    return hashlib.sha256(raw).hexdigest()


def validate_sha256(digest: str) -> str:
    normalized = digest.strip().lower()
    if len(normalized) != 64:
        raise InvalidEvidence("digest must be a 64-character SHA-256 hex string")
    try:
        bytes.fromhex(normalized)
    except ValueError as exc:
        raise InvalidEvidence("digest must be hexadecimal") from exc
    return normalized


def build_evidence_package(
    *,
    subject: str,
    claims: Iterable[Dict[str, Any]],
    artefacts: Iterable[Dict[str, Any]],
    events: Iterable[str] = (),
    decisions: Iterable[str] = (),
    package_id: Optional[str] = None,
) -> Dict[str, Any]:
    """Build an unsigned EvidencePackage-shaped record.

    The chain hash is deterministic for the ordered evidence content. ``signature``
    remains ``None`` until a real signing authority provides one; FREK Notary anchoring
    is stored separately because a chain block is not the same thing as a signature.
    """
    normalized_artefacts = []
    for artefact in artefacts:
        digest = validate_sha256(str(artefact.get("hash", "")))
        normalized_artefacts.append(
            {
                **artefact,
                "hash": digest,
                "algorithm": str(artefact.get("algorithm") or "sha256").lower(),
            }
        )

    normalized_claims = [dict(item) for item in claims]
    ordered_events = list(events)
    ordered_decisions = list(decisions)
    chain_material = {
        "claims": normalized_claims,
        "artefacts": normalized_artefacts,
        "events": ordered_events,
        "decisions": ordered_decisions,
    }
    chain_hash = sha256_hex(chain_material)
    return {
        "package_id": package_id or _id("EPKG"),
        "subject": subject,
        "claims": normalized_claims,
        "artefacts": normalized_artefacts,
        "events": ordered_events,
        "decisions": ordered_decisions,
        "chain_hash": chain_hash,
        "signature": None,
        "anchored_at": None,
        "verification_status": "LOCAL_HASH_VERIFIED",
        "legal_effect": "none",
        "frek_notary": None,
        "created_at": utc_now_iso(),
    }


def verify_evidence_package(package: Dict[str, Any]) -> Dict[str, Any]:
    errors: list[str] = []
    for artefact in package.get("artefacts", []):
        try:
            validate_sha256(str(artefact.get("hash", "")))
        except InvalidEvidence as exc:
            errors.append(f"artefact_hash:{exc}")

    material = {
        "claims": package.get("claims", []),
        "artefacts": package.get("artefacts", []),
        "events": package.get("events", []),
        "decisions": package.get("decisions", []),
    }
    expected = sha256_hex(material)
    chain_ok = expected == package.get("chain_hash")
    if not chain_ok:
        errors.append("chain_hash_mismatch")

    # CVLN iOS requires signature verification as an independent step. Academy does
    # not claim that step when no external signer signature is present.
    signature_present = bool(package.get("signature"))
    notary = package.get("frek_notary") or {}
    notarized = bool(notary.get("block_hash") and notary.get("height") is not None)
    return {
        "valid_local_hashes": not errors,
        "chain_hash_valid": chain_ok,
        "signature_present": signature_present,
        "frek_notarized": notarized,
        "legal_effect": "none",
        "errors": errors,
    }


def _frek_config() -> tuple[str, str]:
    base_url = (os.environ.get("FREK_CORE_BASE_URL") or "").rstrip("/")
    api_key = (os.environ.get("FREK_CORE_API_KEY") or "").strip()
    if not base_url or not api_key:
        raise FrekNotaryUnavailable(
            "FREK_CORE_BASE_URL and FREK_CORE_API_KEY are required for native attestation"
        )
    return base_url, api_key


async def notarize_package(package: Dict[str, Any]) -> Dict[str, Any]:
    """Create a real FREK-Chain block. Never falls back to a fake local proof."""
    base_url, api_key = _frek_config()
    payload = {
        "payload_type": "academy_evidence_package",
        "payload_id": package["package_id"],
        "payload_data": {
            "subject": package["subject"],
            "chain_hash": package["chain_hash"],
            "legal_effect": "none",
        },
        "metadata": {
            "source": "CVLN_ACADEMY",
            "evidence_package_version": "1.1",
        },
    }
    try:
        async with httpx.AsyncClient(timeout=8.0) as client:
            response = await client.post(
                f"{base_url}/api/v1/notary/notarize",
                json=payload,
                headers={"Authorization": f"Bearer {api_key}"},
            )
    except httpx.HTTPError as exc:
        raise FrekNotaryUnavailable(f"FREK Notary network error: {type(exc).__name__}") from exc

    if response.status_code >= 400:
        raise FrekNotaryUnavailable(f"FREK Notary rejected request: HTTP {response.status_code}")
    try:
        block = response.json()
    except ValueError as exc:
        raise FrekNotaryUnavailable("FREK Notary returned non-JSON response") from exc

    required = {"height", "payload_id", "payload_hash", "block_hash", "timestamp"}
    if not required.issubset(block):
        raise FrekNotaryUnavailable("FREK Notary response missing required block fields")
    if block["payload_id"] != package["package_id"]:
        raise FrekNotaryUnavailable("FREK Notary payload_id mismatch")

    updated = {
        **package,
        "anchored_at": block["timestamp"],
        "verification_status": "FREK_NOTARIZED",
        "frek_notary": {
            "height": block["height"],
            "payload_hash": block["payload_hash"],
            "block_hash": block["block_hash"],
            "timestamp": block["timestamp"],
            "btc_anchored": bool(block.get("btc_anchored", False)),
            "btc_block_height": block.get("btc_block_height"),
        },
    }
    return updated


async def create_contract_native_attestation(
    *,
    actor_id: str,
    actor_frek_id: str,
    contract_id: str,
    document_hash: str,
    intent: str,
    evidence_refs: Iterable[str] = (),
) -> Dict[str, Any]:
    """Evidence-first native signing intent bound to FREK identity and document hash.

    The contract must already be APPROVED. The caller's explicit intent is preserved in
    the package. Success means FREK_NOTARIZED, not LEGALLY_SIGNED. Contract state is not
    changed here; that transition remains subject to the Academy legal workflow.
    """
    contract = await db.legal_contracts.find_one({"id": contract_id}, {"_id": 0})
    if not contract:
        raise LookupError("contract not found")
    if contract.get("status") != "APPROVED":
        raise ValueError("native attestation requires an APPROVED contract")
    normalized_hash = validate_sha256(document_hash)
    if intent.strip().upper() != "SIGN":
        raise ValueError("explicit SIGN intent is required")

    existing = await db.native_signature_attestations.find_one(
        {
            "contract_id": contract_id,
            "actor_id": actor_id,
            "document_hash": normalized_hash,
            "status": "FREK_NOTARIZED",
        },
        {"_id": 0},
    )
    if existing:
        return existing

    package = build_evidence_package(
        subject=f"academy:contract:{contract_id}:signing-intent",
        claims=[
            {
                "statement": "Actor explicitly asserted SIGN intent for this document digest",
                "status": "OBSERVED",
                "evidence_ref": normalized_hash,
            }
        ],
        artefacts=[
            {
                "type": "contract_document",
                "id": contract.get("document_id") or contract_id,
                "hash": normalized_hash,
                "algorithm": "sha256",
            }
        ],
        events=[f"actor:{actor_id}:SIGN"],
        decisions=list(evidence_refs),
    )
    package = await notarize_package(package)
    row = {
        "id": _id("NSIG"),
        "contract_id": contract_id,
        "actor_id": actor_id,
        "actor_frek_id": actor_frek_id,
        "document_hash": normalized_hash,
        "intent": "SIGN",
        "evidence_package": package,
        "status": "FREK_NOTARIZED",
        "signature_level": "CVLN_NATIVE_ATTESTATION",
        "legal_effect": "none",
        "created_at": utc_now_iso(),
    }
    await db.native_signature_attestations.insert_one(dict(row))
    return row
