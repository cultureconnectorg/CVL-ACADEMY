"""Assigned-only legal expert workspace (LEG-012 / FD-L01).

The workspace is a projection over existing canonical stores. It creates no parallel
matter/document/risk/deadline model and is only accessible through a scoped expert key.
"""

from __future__ import annotations

from typing import Any, Dict

from db import db
from services import expert_access

READ_SCOPE = "legal:workspace:read"


async def get_workspace(*, raw_key: str, case_id: str) -> Dict[str, Any]:
    context = await expert_access.authorize_case_scope(raw_key, case_id, READ_SCOPE)
    expert = context["expert"]
    case = await db.professional_cases.find_one({"id": case_id}, {"_id": 0})
    if not case:
        raise LookupError("professional case not found")
    if str(case.get("domain", "")).upper() != "LEGAL":
        raise PermissionError("legal workspace requires a LEGAL assigned case")
    if "LEGAL" not in {str(value).upper() for value in expert.get("domains", [])}:
        raise PermissionError("expert is not authorised for LEGAL domain")

    matters = await db.legal_matters.find({"case_id": case_id}, {"_id": 0}).to_list(1000)
    matter_ids = [row["id"] for row in matters]
    documents = await db.legal_documents.find(
        {"matter_id": {"$in": matter_ids}}, {"_id": 0}
    ).to_list(1000) if matter_ids else []
    risks = await db.risks.find(
        {"source_type": "LEGAL_MATTER", "source_id": {"$in": matter_ids}}, {"_id": 0}
    ).to_list(1000) if matter_ids else []
    deadlines = await db.legal_deadlines.find(
        {"matter_id": {"$in": matter_ids}}, {"_id": 0}
    ).to_list(1000) if matter_ids else []
    approvals = await db.legal_approvals.find(
        {"matter_id": {"$in": matter_ids}}, {"_id": 0}
    ).to_list(1000) if matter_ids else []
    rereview = await db.legal_rereview_queue.find(
        {"document_id": {"$in": [row["id"] for row in documents]}, "status": "OPEN"},
        {"_id": 0},
    ).to_list(1000) if documents else []

    return {
        "case": case,
        "expert": {
            "id": expert["id"],
            "display_name": expert.get("display_name"),
            "domains": expert.get("domains", []),
        },
        "assignment": {
            "id": context["assignment"]["id"],
            "scope": context["assignment"].get("scope", []),
            "authority_level": context["assignment"].get("authority_level"),
        },
        "matters": matters,
        "documents": documents,
        "risks": risks,
        "deadlines": deadlines,
        "approvals": approvals,
        "rereview_queue": rereview,
    }
