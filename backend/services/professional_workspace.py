"""Unified Professional Workspace Shell (GOV-003).

One case-scoped read model for all external expert domains. The shell does not grant
new authority: it reuses XCP-006 credentials/assignments and only exposes records
reachable from the assigned professional case. Domain-specific workspaces remain the
source for specialised actions.
"""

from __future__ import annotations

from typing import Any, Dict

from db import db
from services import expert_access

SUPPORTED_DOMAINS = {"LEGAL", "PRIVACY", "SECURITY", "ACCOUNTING", "RISK", "QUALITY"}


async def get_workspace(*, raw_key: str, case_id: str) -> Dict[str, Any]:
    context = await expert_access.authorize_case_scope(raw_key, case_id, "case:read")
    case = await db.professional_cases.find_one({"id": case_id}, {"_id": 0})
    if not case:
        raise LookupError("professional case not found")
    domain = str(case.get("domain") or "").upper()
    if domain not in SUPPORTED_DOMAINS:
        raise PermissionError("case domain is not exposed through professional workspace")

    assignment = context["assignment"]
    docs = await db.governance_document_versions.find(
        {"case_id": case_id}, {"_id": 0}
    ).sort("created_at", 1).to_list(1000)
    decisions = await db.governance_decisions.find(
        {"case_id": case_id}, {"_id": 0}
    ).sort("created_at", 1).to_list(1000)
    audit = await db.governance_audit_events.find(
        {"resource_id": case_id}, {"_id": 0}
    ).sort("created_at", -1).to_list(500)

    return {
        "workspace_type": "PROFESSIONAL_CASE_SCOPED",
        "domain": domain,
        "case": case,
        "expert": {
            "id": context["expert"]["id"],
            "display_name": context["expert"]["display_name"],
            "organisation": context["expert"].get("organisation"),
        },
        "assignment": {
            "id": assignment["id"],
            "authority_level": assignment.get("authority_level"),
            "scope": assignment.get("scope", []),
        },
        "queues": {
            "documents": docs,
            "decisions": decisions,
            "audit": audit,
        },
        "global_browse": False,
        "cross_case_access": False,
    }
