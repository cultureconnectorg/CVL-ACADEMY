"""Partner and institution portal API.

This surface is intentionally read-first. External stakeholders get visibility
into the organisation they belong to, never platform-wide data. The tenant
boundary is the authenticated user's ``org_id`` and every query is scoped to it.

CVLN remains the authority for organisation/cohort creation and invitations.
Partners/institutions can observe cohorts and member-level operational status
without receiving learner private pedagogy, wallet data, or unrestricted admin
capabilities.
"""

from __future__ import annotations

from collections import Counter
from typing import Any, Dict, List

from fastapi import APIRouter, Depends, HTTPException

from auth import require_role
from db import db
from models import ADMIN_ROLES, User

router = APIRouter(prefix="/stakeholders", tags=["stakeholders"])

PORTAL_ROLES = ("partner", "institution", *ADMIN_ROLES)


def _require_org(current: User) -> str:
    if not current.org_id:
        raise HTTPException(
            status_code=409,
            detail="Ce compte doit être rattaché à une organisation avant d'utiliser cet espace",
        )
    return current.org_id


@router.get("/overview")
async def stakeholder_overview(
    current: User = Depends(require_role(*PORTAL_ROLES)),
) -> Dict[str, Any]:
    """Return the minimum organisation-scoped dataset needed by the portal."""
    org_id = _require_org(current)

    organisation = await db.organisations.find_one({"id": org_id}, {"_id": 0})
    if not organisation:
        raise HTTPException(status_code=404, detail="Organisation introuvable")

    cohorts = await db.cohorts.find({"org_id": org_id}, {"_id": 0}).to_list(500)
    members = await db.users.find(
        {"org_id": org_id},
        {
            "_id": 0,
            "id": 1,
            "display_name": 1,
            "role": 1,
            "cohort_id": 1,
            "onboarding_completed": 1,
            "email_verified": 1,
            "created_at": 1,
        },
    ).to_list(5000)

    role_counts = Counter(member.get("role", "unknown") for member in members)
    cohort_counts = Counter(
        member.get("cohort_id") for member in members if member.get("cohort_id")
    )

    cohort_summaries: List[Dict[str, Any]] = []
    for cohort in cohorts:
        cohort_summaries.append(
            {
                **cohort,
                "member_count": cohort_counts.get(cohort["id"], 0),
            }
        )

    return {
        "organisation": organisation,
        "viewer": {
            "role": current.role,
            "display_name": current.display_name,
        },
        "counts": {
            "members": len(members),
            "students": role_counts.get("student", 0),
            "trainers": role_counts.get("trainer", 0),
            "cohorts": len(cohorts),
        },
        "cohorts": cohort_summaries,
        "members": members,
        "data_scope": "organisation",
    }
