"""Versioned legal clause library, usage graph and change impact (LEG-004/005/006)."""

from __future__ import annotations

import re
import uuid
from typing import Any, Dict, Iterable, Optional

from db import db, utc_now_iso
from services import professional_governance as governance

SHA256_RE = re.compile(r"^[0-9a-fA-F]{64}$")


def _id(prefix: str) -> str:
    return f"{prefix}-{uuid.uuid4()}"


def _refs(values: Iterable[str]) -> list[str]:
    return list(dict.fromkeys(str(v).strip() for v in values if str(v).strip()))


async def create_clause(
    *,
    actor_id: str,
    case_id: str,
    code: str,
    title: str,
    context_tags: Iterable[str],
    content_hash: str,
    evidence_refs: Iterable[str],
) -> Dict[str, Any]:
    if not SHA256_RE.fullmatch(content_hash or ""):
        raise ValueError("content_hash must be SHA-256")
    refs = _refs(evidence_refs)
    if not refs:
        raise ValueError("clause creation requires evidence")
    case = await db.professional_cases.find_one({"id": case_id}, {"_id": 0})
    if not case or str(case.get("domain", "")).upper() != "LEGAL":
        raise ValueError("clause library requires a LEGAL case")
    normalized_code = str(code or "").strip().upper()
    if not normalized_code or await db.legal_clauses.find_one({"code": normalized_code}):
        raise ValueError("clause code is required and must be unique")
    clause = {
        "id": _id("LCL"),
        "case_id": case_id,
        "code": normalized_code,
        "title": str(title or "").strip(),
        "context_tags": sorted({str(v).strip().upper() for v in context_tags if str(v).strip()}),
        "current_version_id": None,
        "status": "ACTIVE",
        "created_by": actor_id,
        "created_at": utc_now_iso(),
        "updated_at": utc_now_iso(),
    }
    if not clause["title"]:
        raise ValueError("clause title is required")
    await db.legal_clauses.insert_one(dict(clause))
    version = await governance.register_document_version(
        actor_id=actor_id,
        case_id=case_id,
        document_type="LEGAL_CLAUSE",
        title=clause["title"],
        content_hash=content_hash,
        metadata={
            "clause_id": clause["id"],
            "clause_code": normalized_code,
            "context_tags": clause["context_tags"],
            "evidence_refs": refs,
        },
    )
    await db.legal_clauses.update_one(
        {"id": clause["id"]}, {"$set": {"current_version_id": version["id"]}}
    )
    return {**clause, "current_version_id": version["id"], "version": version}


async def add_clause_version(
    *, actor_id: str, clause_id: str, content_hash: str, evidence_refs: Iterable[str]
) -> Dict[str, Any]:
    if not SHA256_RE.fullmatch(content_hash or ""):
        raise ValueError("content_hash must be SHA-256")
    refs = _refs(evidence_refs)
    if not refs:
        raise ValueError("clause version requires evidence")
    clause = await db.legal_clauses.find_one({"id": clause_id, "status": "ACTIVE"}, {"_id": 0})
    if not clause:
        raise LookupError("active clause not found")
    previous = await db.governance_document_versions.find_one(
        {"id": clause["current_version_id"]}, {"_id": 0}
    )
    if not previous:
        raise ValueError("current clause version missing")
    if previous["content_hash"] == content_hash.lower():
        raise ValueError("new clause version must change content")
    version = await governance.register_document_version(
        actor_id=actor_id,
        case_id=clause["case_id"],
        document_type="LEGAL_CLAUSE",
        title=clause["title"],
        content_hash=content_hash,
        parent_version_id=previous["id"],
        metadata={
            "clause_id": clause_id,
            "clause_code": clause["code"],
            "context_tags": clause["context_tags"],
            "evidence_refs": refs,
        },
    )
    result = await db.legal_clauses.update_one(
        {"id": clause_id, "current_version_id": previous["id"]},
        {"$set": {"current_version_id": version["id"], "updated_at": utc_now_iso()}},
    )
    if result.modified_count != 1:
        raise ValueError("clause changed concurrently")
    await _queue_change_impact(
        actor_id=actor_id,
        clause_id=clause_id,
        old_version_id=previous["id"],
        new_version_id=version["id"],
        evidence_refs=refs,
    )
    return version


async def register_usage(
    *,
    actor_id: str,
    clause_id: str,
    document_id: str,
    version_id: Optional[str],
    evidence_refs: Iterable[str],
) -> Dict[str, Any]:
    refs = _refs(evidence_refs)
    if not refs:
        raise ValueError("clause usage requires evidence")
    clause = await db.legal_clauses.find_one({"id": clause_id}, {"_id": 0})
    doc = await db.legal_documents.find_one({"id": document_id}, {"_id": 0})
    if not clause or not doc:
        raise LookupError("clause or legal document not found")
    clause_version_id = version_id or clause["current_version_id"]
    version = await db.governance_document_versions.find_one(
        {"id": clause_version_id, "metadata.clause_id": clause_id}, {"_id": 0}
    )
    if not version:
        raise ValueError("clause version does not belong to clause")
    existing = await db.legal_clause_usages.find_one(
        {
            "clause_id": clause_id,
            "clause_version_id": clause_version_id,
            "document_id": document_id,
            "document_version_id": doc["current_version_id"],
            "status": "ACTIVE",
        },
        {"_id": 0},
    )
    if existing:
        return existing
    row = {
        "id": _id("LCU"),
        "clause_id": clause_id,
        "clause_version_id": clause_version_id,
        "document_id": document_id,
        "document_version_id": doc["current_version_id"],
        "evidence_refs": refs,
        "status": "ACTIVE",
        "created_by": actor_id,
        "created_at": utc_now_iso(),
    }
    await db.legal_clause_usages.insert_one(dict(row))
    return row


async def _queue_change_impact(
    *,
    actor_id: str,
    clause_id: str,
    old_version_id: str,
    new_version_id: str,
    evidence_refs: list[str],
) -> list[Dict[str, Any]]:
    usages = await db.legal_clause_usages.find(
        {"clause_id": clause_id, "clause_version_id": old_version_id, "status": "ACTIVE"},
        {"_id": 0},
    ).to_list(1000)
    queued: list[Dict[str, Any]] = []
    for usage in usages:
        existing = await db.legal_rereview_queue.find_one(
            {
                "document_id": usage["document_id"],
                "cause_clause_version_id": new_version_id,
                "status": "OPEN",
            },
            {"_id": 0},
        )
        if existing:
            queued.append(existing)
            continue
        row = {
            "id": _id("LRR"),
            "document_id": usage["document_id"],
            "document_version_id": usage["document_version_id"],
            "clause_id": clause_id,
            "previous_clause_version_id": old_version_id,
            "cause_clause_version_id": new_version_id,
            "status": "OPEN",
            "evidence_refs": evidence_refs,
            "created_by": actor_id,
            "created_at": utc_now_iso(),
        }
        await db.legal_rereview_queue.insert_one(dict(row))
        queued.append(row)
    await governance.audit_event(
        event_type="legal.clause.impact_queued",
        actor_id=actor_id,
        resource_type="legal_clause",
        resource_id=clause_id,
        payload={
            "previous_version_id": old_version_id,
            "new_version_id": new_version_id,
            "affected_document_ids": sorted({row["document_id"] for row in queued}),
            "evidence_refs": evidence_refs,
        },
    )
    return queued


async def impact_for_version(version_id: str) -> Dict[str, Any]:
    rows = await db.legal_rereview_queue.find(
        {"cause_clause_version_id": version_id}, {"_id": 0}
    ).to_list(1000)
    return {
        "clause_version_id": version_id,
        "affected_document_ids": sorted({row["document_id"] for row in rows}),
        "queue": rows,
    }
