"""Verification gate for CVLN Academy native contract attestations.

This module follows the runtime contracts already implemented by FREKCORE and the
EvidencePackage verification discipline from CVLN Intelligence OS. Verification is
split into explicit steps and never changes a contract's legal state.
"""

from __future__ import annotations

import hashlib
import json
import os
import uuid
from typing import Any, Dict
from urllib.parse import quote

import httpx

from db import db, utc_now_iso
from services import proof_bridge


class FrekProofUnavailable(RuntimeError):
    """Raised when the independent FREK proof cannot be retrieved."""


def _id(prefix: str) -> str:
    return f"{prefix}-{uuid.uuid4()}"


def _canonical_json(data: dict) -> str:
    return json.dumps(data, sort_keys=True, separators=(",", ":"), default=str)


def _expected_notary_payload_hash(package: Dict[str, Any]) -> str:
    payload_data = {
        "subject": package["subject"],
        "chain_hash": package["chain_hash"],
        "legal_effect": "none",
    }
    return hashlib.sha256(_canonical_json(payload_data).encode("utf-8")).hexdigest()


def _expected_block_hash(block: Dict[str, Any]) -> str:
    event_id = block.get("event_id") or ""
    spec_version = block.get("spec_version") or "1.0.0"
    raw = (
        f"{block['height']}|{block['prev_hash']}|{block['payload_hash']}|"
        f"{block['payload_type']}|{block['payload_id']}|{block['timestamp']}|"
        f"{event_id}|{spec_version}"
    )
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def _frek_base_url() -> str:
    base = (os.environ.get("FREK_CORE_BASE_URL") or "").rstrip("/")
    if not base:
        raise FrekProofUnavailable("FREK_CORE_BASE_URL is required for proof verification")
    return base


async def fetch_frek_proof(package_id: str) -> Dict[str, Any]:
    """Fetch FREK's public proof endpoint for one Academy evidence package."""
    base = _frek_base_url()
    try:
        async with httpx.AsyncClient(timeout=8.0) as client:
            response = await client.get(
                f"{base}/api/v1/notary/proof/{quote(package_id, safe='')}"
            )
    except httpx.HTTPError as exc:
        raise FrekProofUnavailable(
            f"FREK proof network error: {type(exc).__name__}"
        ) from exc
    if response.status_code == 404:
        raise FrekProofUnavailable("FREK proof not found for evidence package")
    if response.status_code >= 400:
        raise FrekProofUnavailable(f"FREK proof request failed: HTTP {response.status_code}")
    try:
        proof = response.json()
    except ValueError as exc:
        raise FrekProofUnavailable("FREK proof endpoint returned non-JSON response") from exc
    if not isinstance(proof, dict) or not isinstance(proof.get("block"), dict):
        raise FrekProofUnavailable("FREK proof response missing block")
    return proof


async def list_contract_attestations(contract_id: str) -> list[Dict[str, Any]]:
    if not await db.legal_contracts.find_one({"id": contract_id}):
        raise LookupError("contract not found")
    return await db.native_signature_attestations.find(
        {"contract_id": contract_id}, {"_id": 0}
    ).sort("created_at", 1).to_list(200)


async def verify_native_attestation(
    *,
    actor_id: str,
    attestation_id: str,
    require_btc_anchor: bool = False,
) -> Dict[str, Any]:
    """Run local + remote FREK verification and persist an immutable audit result.

    PASS means the Academy package is internally consistent and independently resolves
    to the same FREK block. If ``require_btc_anchor`` is true, FREK must additionally
    report Bitcoin anchoring. PASS still has ``legal_effect=none`` and does not imply an
    eIDAS-qualified signature or mutate the contract lifecycle.
    """
    attestation = await db.native_signature_attestations.find_one(
        {"id": attestation_id}, {"_id": 0}
    )
    if not attestation:
        raise LookupError("native attestation not found")

    package = attestation.get("evidence_package") or {}
    local = proof_bridge.verify_evidence_package(package)
    errors = list(local.get("errors") or [])

    remote = await fetch_frek_proof(str(package.get("package_id") or ""))
    block = remote.get("block") or {}
    chain_proof = remote.get("chain_proof") or {}
    stored_notary = package.get("frek_notary") or {}

    expected_payload_hash = _expected_notary_payload_hash(package)
    checks = {
        "local_chain_hash": bool(local.get("chain_hash_valid")),
        "local_artefact_hashes": bool(local.get("valid_local_hashes")),
        "package_has_no_claimed_legal_effect": package.get("legal_effect") == "none",
        "remote_payload_id": remote.get("payload_id") == package.get("package_id"),
        "remote_payload_type": block.get("payload_type") == "academy_evidence_package",
        "remote_payload_hash": block.get("payload_hash") == expected_payload_hash,
        "stored_block_height": block.get("height") == stored_notary.get("height"),
        "stored_block_hash": block.get("block_hash") == stored_notary.get("block_hash"),
        "stored_payload_hash": block.get("payload_hash") == stored_notary.get("payload_hash"),
        "chain_proof_height": chain_proof.get("height") == block.get("height"),
        "chain_proof_block_hash": chain_proof.get("block_hash") == block.get("block_hash"),
        "chain_proof_payload_hash": chain_proof.get("payload_hash") == block.get("payload_hash"),
        "block_hash_recomputed": False,
        "btc_anchor_requirement": bool(remote.get("btc_anchored")) if require_btc_anchor else True,
    }

    try:
        checks["block_hash_recomputed"] = _expected_block_hash(block) == block.get("block_hash")
    except (KeyError, TypeError, ValueError):
        checks["block_hash_recomputed"] = False

    errors.extend(name for name, passed in checks.items() if not passed)
    passed = not errors
    btc_anchored = bool(remote.get("btc_anchored"))
    status = (
        "VERIFIED_FREK_BTC"
        if passed and btc_anchored
        else "VERIFIED_FREK"
        if passed
        else "FAILED"
    )
    result = {
        "id": _id("NSIGVER"),
        "attestation_id": attestation_id,
        "contract_id": attestation["contract_id"],
        "status": status,
        "checks": checks,
        "errors": list(dict.fromkeys(errors)),
        "require_btc_anchor": require_btc_anchor,
        "btc_anchored": btc_anchored,
        "btc_attestation": remote.get("btc_attestation"),
        "verification_url": remote.get("verification_url"),
        "frek_block": {
            "height": block.get("height"),
            "block_hash": block.get("block_hash"),
            "payload_hash": block.get("payload_hash"),
            "timestamp": block.get("timestamp"),
            "spec_version": block.get("spec_version"),
        },
        "legal_effect": "none",
        "verified_by": actor_id,
        "verified_at": utc_now_iso(),
    }
    await db.native_signature_verifications.insert_one(dict(result))
    return result
