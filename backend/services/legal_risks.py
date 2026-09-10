"""Legal risk bridge (LEG-008 / FD-L12).

Legal risk records never implement a second scoring engine. They reuse the canonical
Academy Risk Core and bind each resulting risk back to the legal matter that caused it.
"""

from __future__ import annotations

from typing import Any, Dict, Iterable, Optional

from db import db, utc_now_iso
from services import assurance_core
from services import professional_governance as governance


async def register_legal_risk(
    *,
    actor_id: str,
    matter_id: str,
    title: str,
    impact: int,
    probability: int,
    control_effectiveness: int = 0,
    owner: Optional[str] = None,
    mitigation: Optional[str] = None,
    deadline: Optional[str] = None,
    evidence_refs: Iterable[str],
) -> Dict[str, Any]:
    refs = list(dict.fromkeys(str(ref).strip() for ref in evidence_refs if str(ref).strip()))
    if not refs:
        raise ValueError("legal risk requires evidence")
    matter = await db.legal_matters.find_one({"id": matter_id}, {"_id": 0})
    if not matter:
        raise LookupError("legal matter not found")

    existing = await db.risks.find_one(
        {"source_type": "LEGAL_MATTER", "source_id": matter_id, "title": title},
        {"_id": 0},
    )
    if existing:
        return existing

    risk = await assurance_core.create_risk(
        actor_id=actor_id,
        title=title,
        domain="LEGAL",
        impact=impact,
        probability=probability,
        control_effectiveness=control_effectiveness,
        owner=owner,
        mitigation=mitigation,
        deadline=deadline,
        evidence_refs=[matter_id, *refs],
    )
    now = utc_now_iso()
    await db.risks.update_one(
        {"id": risk["id"]},
        {
            "$set": {
                "source_type": "LEGAL_MATTER",
                "source_id": matter_id,
                "updated_at": now,
            }
        },
    )
    await db.legal_matters.update_one(
        {"id": matter_id},
        {
            "$addToSet": {"risk_ids": risk["id"]},
            "$set": {"updated_at": now},
        },
    )
    await governance.audit_event(
        event_type="legal.risk.registered",
        actor_id=actor_id,
        resource_type="legal_matter",
        resource_id=matter_id,
        payload={
            "risk_id": risk["id"],
            "level": risk["level"],
            "evidence_refs": refs,
        },
    )
    return {**risk, "source_type": "LEGAL_MATTER", "source_id": matter_id}


async def list_matter_risks(matter_id: str) -> list[Dict[str, Any]]:
    if not await db.legal_matters.find_one({"id": matter_id}):
        raise LookupError("legal matter not found")
    return await db.risks.find(
        {"source_type": "LEGAL_MATTER", "source_id": matter_id}, {"_id": 0}
    ).sort("created_at", 1).to_list(1000)
