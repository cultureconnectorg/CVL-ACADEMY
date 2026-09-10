"""Legal document registry and publication lifecycle (LEG-002/003, FD-L02/L04).

Legal document metadata is domain-specific, while every immutable content version
is stored through the shared Governance document-version registry. Publication is
an explicit A4 policy decision and never rewrites an old version.
"""

from __future__ import annotations

import hashlib
import re
import uuid
from typing import Any, Dict, Iterable, Optional

from db import db, utc_now_iso
from services import authority_policy, legal_policy
from services import professional_governance as governance


DOCUMENT_TYPES = {
    "CGU",
    "CGV",
    "PRIVACY",
    "CONTRACT",
    "POLICY",
    "IP",
    "PARTNER",
    "OTHER",
}
LIFECYCLE = {"DRAFT", "IN_REVIEW", "APPROVED", "SIGNED", "PUBLISHED", "SUPERSEDED"}
TRANSITIONS = {
    "DRAFT": {"IN_REVIEW"},
    "IN_REVIEW": {"DRAFT", "APPROVED"},
    "APPROVED": {"SIGNED"},
    "SIGNED": {"PUBLISHED"},
    "PUBLISHED": {"SUPERSEDED"},
    "SUPERSEDED": set(),
}
SHA256_RE = re.compile(r"^[0-9a-fA-F]{64}$")
VERIFIED_SIGNATURE_STATES = {"VERIFIED_FREK", "VERIFIED_FREK_BTC"}


def _id(prefix: str) -> str:
    return f"{prefix}-{uuid.uuid4()}"


def _refs(values: Iterable[str]) -> list[str]:
    return list(dict.fromkeys(str(value).strip() for value in values if str(value).strip()))


async def create_document(
    *,
    actor_id: str,
    case_id: str,
    matter_id: str,
    document_type: str,
    title: str,
    jurisdiction: Optional[str],
    content_hash: str,
    evidence_refs: Iterable[str],
    metadata: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    dtype = str(document_type or "").upper()
    refs = _refs(evidence_refs)
    if dtype not in DOCUMENT_TYPES:
        raise ValueError("invalid legal document type")
    if not SHA256_RE.fullmatch(str(content_hash or "")):
        raise ValueError("content_hash must be SHA-256")
    if not refs:
        raise ValueError("legal document requires evidence")
    case = await db.professional_cases.find_one({"id": case_id}, {"_id": 0})
    matter = await db.legal_matters.find_one({"id": matter_id}, {"_id": 0})
    if not case or str(case.get("domain", "")).upper() != "LEGAL":
        raise ValueError("legal document requires a LEGAL professional case")
    if not matter or matter.get("case_id") != case_id:
        raise ValueError("legal document matter must belong to the same case")

    doc = {
        "id": _id("LDOC"),
        "case_id": case_id,
        "matter_id": matter_id,
        "document_type": dtype,
        "title": str(title).strip(),
        "jurisdiction": jurisdiction,
        "status": "DRAFT",
        "current_version_id": None,
        "published_version_id": None,
        "metadata": metadata or {},
        "created_by": actor_id,
        "created_at": utc_now_iso(),
        "updated_at": utc_now_iso(),
    }
    if not doc["title"]:
        raise ValueError("legal document title is required")
    await db.legal_documents.insert_one(dict(doc))
    version = await governance.register_document_version(
        actor_id=actor_id,
        case_id=case_id,
        document_type=f"LEGAL_{dtype}",
        title=doc["title"],
        content_hash=content_hash,
        metadata={
            "legal_document_id": doc["id"],
            "matter_id": matter_id,
            "jurisdiction": jurisdiction,
            "evidence_refs": refs,
            "domain": "LEGAL",
        },
    )
    await db.legal_documents.update_one(
        {"id": doc["id"]},
        {"$set": {"current_version_id": version["id"], "updated_at": utc_now_iso()}},
    )
    await governance.audit_event(
        event_type="legal.document.created",
        actor_id=actor_id,
        resource_type="legal_document",
        resource_id=doc["id"],
        payload={"version_id": version["id"], "evidence_refs": refs},
    )
    return {**doc, "current_version_id": version["id"], "version": version}


async def add_version(
    *,
    actor_id: str,
    document_id: str,
    content_hash: str,
    evidence_refs: Iterable[str],
) -> Dict[str, Any]:
    refs = _refs(evidence_refs)
    if not SHA256_RE.fullmatch(str(content_hash or "")):
        raise ValueError("content_hash must be SHA-256")
    if not refs:
        raise ValueError("new legal version requires evidence")
    doc = await db.legal_documents.find_one({"id": document_id}, {"_id": 0})
    if not doc:
        raise LookupError("legal document not found")
    if doc["status"] not in {"DRAFT", "IN_REVIEW"}:
        raise ValueError("new versions require DRAFT or IN_REVIEW document")
    current = await db.governance_document_versions.find_one(
        {"id": doc["current_version_id"]}, {"_id": 0}
    )
    if not current:
        raise ValueError("current governance document version is missing")
    if current["content_hash"] == content_hash.lower():
        raise ValueError("new legal version must change content hash")

    version = await governance.register_document_version(
        actor_id=actor_id,
        case_id=doc["case_id"],
        document_type=f"LEGAL_{doc['document_type']}",
        title=doc["title"],
        content_hash=content_hash,
        parent_version_id=current["id"],
        metadata={
            "legal_document_id": document_id,
            "matter_id": doc["matter_id"],
            "jurisdiction": doc.get("jurisdiction"),
            "evidence_refs": refs,
            "domain": "LEGAL",
        },
    )
    now = utc_now_iso()
    result = await db.legal_documents.update_one(
        {"id": document_id, "current_version_id": current["id"]},
        {"$set": {"current_version_id": version["id"], "updated_at": now}},
    )
    if result.modified_count != 1:
        raise ValueError("legal document changed concurrently")
    return version


async def _verified_signature_for_current_version(
    *, document_id: str, version: Dict[str, Any], refs: list[str]
) -> Dict[str, Any] | None:
    if not refs:
        return None
    attestation = await db.native_signature_attestations.find_one(
        {
            "id": {"$in": refs},
            "document_hash": version["content_hash"],
            "$or": [
                {"legal_document_id": document_id},
                {"legal_document_id": {"$exists": False}},
            ],
        },
        {"_id": 0},
    )
    if not attestation:
        return None
    verification = await db.native_signature_verifications.find_one(
        {
            "attestation_id": attestation["id"],
            "status": {"$in": sorted(VERIFIED_SIGNATURE_STATES)},
        },
        {"_id": 0},
        sort=[("verified_at", -1)],
    )
    if not verification:
        return None
    return {"attestation": attestation, "verification": verification}


async def transition_document(
    *,
    actor_id: str,
    document_id: str,
    status: str,
    evidence_refs: Iterable[str] = (),
) -> Dict[str, Any]:
    target = str(status or "").upper()
    doc = await db.legal_documents.find_one({"id": document_id}, {"_id": 0})
    if not doc:
        raise LookupError("legal document not found")
    if target not in LIFECYCLE or target not in TRANSITIONS[doc["status"]]:
        raise ValueError(f"invalid legal document transition {doc['status']}->{target}")
    refs = _refs(evidence_refs)

    if target == "APPROVED":
        approvals = await legal_policy.approval_state(doc["matter_id"])
        if not approvals["internal_approved"]:
            raise ValueError("APPROVED requires INTERNAL_APPROVED evidence")
        matter = await db.legal_matters.find_one({"id": doc["matter_id"]}, {"_id": 0})
        if matter.get("external_review_required") and not approvals["external_legal_approved"]:
            raise ValueError("external review is required but not externally approved")
    if target in {"SIGNED", "SUPERSEDED"} and not refs:
        raise ValueError(f"{target} transition requires evidence")
    if target == "SIGNED":
        version = await db.governance_document_versions.find_one(
            {"id": doc["current_version_id"]}, {"_id": 0}
        )
        if not version:
            raise ValueError("current governance document version is missing")
        verified = await _verified_signature_for_current_version(
            document_id=document_id, version=version, refs=refs
        )
        if not verified:
            raise ValueError("SIGNED requires verified native signature evidence")

    now = utc_now_iso()
    result = await db.legal_documents.update_one(
        {"id": document_id, "status": doc["status"]},
        {"$set": {"status": target, "updated_at": now, "updated_by": actor_id}},
    )
    if result.modified_count != 1:
        raise ValueError("legal document transition lost race")
    await governance.audit_event(
        event_type="legal.document.state_changed",
        actor_id=actor_id,
        resource_type="legal_document",
        resource_id=document_id,
        payload={"from": doc["status"], "to": target, "evidence_refs": refs},
    )
    return {**doc, "status": target, "updated_at": now, "updated_by": actor_id}


async def publish_document(
    *,
    actor_id: str,
    actor_role: str,
    authority_level: str,
    document_id: str,
    policy_version_id: str,
    evidence_refs: Iterable[str],
) -> Dict[str, Any]:
    refs = _refs(evidence_refs)
    if not refs:
        raise ValueError("publication requires evidence")
    doc = await db.legal_documents.find_one({"id": document_id}, {"_id": 0})
    if not doc:
        raise LookupError("legal document not found")
    if doc["status"] != "SIGNED":
        raise ValueError("only SIGNED legal documents can be published")
    version = await db.governance_document_versions.find_one(
        {"id": doc["current_version_id"]}, {"_id": 0}
    )
    if not version:
        raise ValueError("current governance document version is missing")

    authority = await authority_policy.evaluate_authority(
        actor_id=actor_id,
        actor_role=actor_role,
        action="LEGAL_DOCUMENT_PUBLISH",
        context={
            "domain": "LEGAL",
            "jurisdiction": doc.get("jurisdiction"),
            "authority_level": authority_level,
            "resource_type": doc["document_type"],
            "document_id": document_id,
            "version_id": version["id"],
        },
        policy_version_id=policy_version_id,
    )
    if authority["policy_key"] != "LEGAL_PUBLICATION_AUTHORITY":
        raise ValueError("publication requires LEGAL_PUBLICATION_AUTHORITY policy")
    if authority["decision"] != "ALLOW":
        raise PermissionError("authority policy did not allow legal publication")

    now = utc_now_iso()
    result = await db.legal_documents.update_one(
        {"id": document_id, "status": "SIGNED", "current_version_id": version["id"]},
        {
            "$set": {
                "status": "PUBLISHED",
                "published_version_id": version["id"],
                "published_at": now,
                "published_by": actor_id,
                "publication_authority_decision_id": authority["id"],
                "updated_at": now,
            }
        },
    )
    if result.modified_count != 1:
        raise ValueError("legal publication lost race")
    publication = {
        "id": _id("LPUB"),
        "document_id": document_id,
        "version_id": version["id"],
        "content_hash": version["content_hash"],
        "authority_decision_id": authority["id"],
        "policy_version_id": authority["policy_version_id"],
        "policy_content_hash": authority["policy_content_hash"],
        "evidence_refs": refs,
        "published_by": actor_id,
        "published_at": now,
    }
    publication["publication_hash"] = hashlib.sha256(
        repr(sorted(publication.items())).encode("utf-8")
    ).hexdigest()
    await db.legal_publications.insert_one(dict(publication))
    await governance.audit_event(
        event_type="legal.document.published",
        actor_id=actor_id,
        resource_type="legal_document",
        resource_id=document_id,
        payload={
            "publication_id": publication["id"],
            "version_id": version["id"],
            "content_hash": version["content_hash"],
            "authority_decision_id": authority["id"],
            "evidence_refs": refs,
        },
    )
    return {"document": {**doc, "status": "PUBLISHED"}, "publication": publication}
