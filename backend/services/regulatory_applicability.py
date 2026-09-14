"""External regulatory applicability map (REG-01..REG-08).

The registry stores evidence-backed applicability decisions; it does not encode legal
advice or silently assert that a law applies. UNKNOWN/REVIEW_REQUIRED are first-class
states and production consumers can require a current reviewed record before acting.
"""

from __future__ import annotations

import uuid
from typing import Any, Dict, Iterable, Optional

from db import db, utc_now_iso
from services import professional_governance as governance

REGULATORY_AREAS = {
    "REG-01": "EU_FR_PRIVACY_DATA_PROTECTION",
    "REG-02": "COOKIES_ELECTRONIC_COMMUNICATIONS",
    "REG-03": "ECOMMERCE_CONSUMER",
    "REG-04": "ELECTRONIC_SIGNATURE_TRUST",
    "REG-05": "VOCATIONAL_TRAINING_QUALITY",
    "REG-06": "ACCOUNTING_INVOICING_TAX",
    "REG-07": "IP_COPYRIGHT_IMAGE_RIGHTS",
    "REG-08": "ACCESSIBILITY",
}
STATES = {
    "UNKNOWN",
    "REVIEW_REQUIRED",
    "APPLICABLE",
    "NOT_APPLICABLE",
    "SUPERSEDED",
}


def _id(prefix: str) -> str:
    return f"{prefix}-{uuid.uuid4()}"


def _refs(values: Iterable[str]) -> list[str]:
    return list(dict.fromkeys(str(v).strip() for v in values if str(v).strip()))


async def declare_scope(
    *,
    actor_id: str,
    regulatory_id: str,
    jurisdiction: str,
    activity: str,
    entity_ref: str,
    product_scope: str,
    evidence_refs: Iterable[str],
) -> Dict[str, Any]:
    reg = str(regulatory_id or "").upper()
    if reg not in REGULATORY_AREAS:
        raise ValueError("unknown regulatory area")
    refs = _refs(evidence_refs)
    required = (jurisdiction, activity, entity_ref, product_scope)
    if not all(str(v).strip() for v in required) or not refs:
        raise ValueError(
            "regulatory scope requires jurisdiction, activity, entity, product and evidence"
        )
    row = {
        "id": _id("REGSCOPE"),
        "regulatory_id": reg,
        "area": REGULATORY_AREAS[reg],
        "jurisdiction": jurisdiction.strip().upper(),
        "activity": activity.strip(),
        "entity_ref": entity_ref.strip(),
        "product_scope": product_scope.strip(),
        "status": "REVIEW_REQUIRED",
        "evidence_refs": refs,
        "declared_by": actor_id,
        "declared_at": utc_now_iso(),
        "current_decision_id": None,
    }
    await db.regulatory_scopes.insert_one(dict(row))
    await governance.audit_event(
        event_type="regulatory.scope.declared",
        actor_id=actor_id,
        resource_type="regulatory_scope",
        resource_id=row["id"],
        payload={"regulatory_id": reg, "jurisdiction": row["jurisdiction"]},
        result="REVIEW_REQUIRED",
    )
    return row


async def record_applicability_decision(
    *,
    actor_id: str,
    scope_id: str,
    outcome: str,
    rationale: str,
    authority_ref: str,
    source_refs: Iterable[str],
    effective_at: str,
    review_due_at: Optional[str] = None,
) -> Dict[str, Any]:
    scope = await db.regulatory_scopes.find_one({"id": scope_id}, {"_id": 0})
    if not scope:
        raise LookupError("regulatory scope not found")
    target = str(outcome or "").upper()
    if target not in {"APPLICABLE", "NOT_APPLICABLE"}:
        raise ValueError("applicability outcome must be APPLICABLE or NOT_APPLICABLE")
    refs = _refs(source_refs)
    if not rationale.strip() or not authority_ref.strip() or not refs:
        raise ValueError(
            "applicability decision requires rationale, authority and sources"
        )
    previous = None
    if scope.get("current_decision_id"):
        previous = await db.regulatory_applicability_decisions.find_one(
            {"id": scope["current_decision_id"]}, {"_id": 0}
        )
    row = {
        "id": _id("REGDEC"),
        "scope_id": scope_id,
        "regulatory_id": scope["regulatory_id"],
        "jurisdiction": scope["jurisdiction"],
        "outcome": target,
        "rationale": rationale.strip(),
        "authority_ref": authority_ref.strip(),
        "source_refs": refs,
        "effective_at": effective_at,
        "review_due_at": review_due_at,
        "supersedes_decision_id": previous["id"] if previous else None,
        "status": "CURRENT",
        "decided_by": actor_id,
        "decided_at": utc_now_iso(),
    }
    if previous:
        await db.regulatory_applicability_decisions.update_one(
            {"id": previous["id"], "status": "CURRENT"},
            {"$set": {"status": "SUPERSEDED", "superseded_by": row["id"]}},
        )
    await db.regulatory_applicability_decisions.insert_one(dict(row))
    await db.regulatory_scopes.update_one(
        {"id": scope_id},
        {"$set": {"status": target, "current_decision_id": row["id"]}},
    )
    await governance.audit_event(
        event_type="regulatory.applicability.decided",
        actor_id=actor_id,
        resource_type="regulatory_scope",
        resource_id=scope_id,
        payload={
            "decision_id": row["id"],
            "outcome": target,
            "authority_ref": authority_ref,
            "source_refs": refs,
        },
        reason=rationale.strip(),
        result=target,
    )
    return row


async def applicability_gate(
    *, regulatory_id: Optional[str] = None
) -> Dict[str, Any]:
    query: Dict[str, Any] = {
        "status": {"$in": ["UNKNOWN", "REVIEW_REQUIRED"]}
    }
    if regulatory_id:
        reg = regulatory_id.upper()
        if reg not in REGULATORY_AREAS:
            raise ValueError("unknown regulatory area")
        query["regulatory_id"] = reg
    rows = await db.regulatory_scopes.find(query, {"_id": 0}).to_list(10000)
    return {
        "pass": len(rows) == 0,
        "open_count": len(rows),
        "open_scopes": rows,
        "note": (
            "PASS means recorded applicability decisions exist; it does not certify "
            "legal correctness without the referenced authority evidence."
        ),
    }
