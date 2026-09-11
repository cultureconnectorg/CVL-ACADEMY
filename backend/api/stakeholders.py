"""Partner and institution portal API.

Stakeholder access is additive to the existing Academy identity/role model:
a user keeps their FREK-ID and pedagogical role, while an organisation-scoped
membership grants access to a partner or institution portal. This avoids
turning external relationships into global platform roles.
"""

from __future__ import annotations

import secrets
from datetime import datetime, timedelta, timezone
from typing import Literal, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr, Field

from auth import get_current_user, require_role
from db import db
from models import ADMIN_ROLES, User

router = APIRouter(prefix="/stakeholders", tags=["stakeholders"])

StakeholderType = Literal["partner", "institution"]


class StakeholderInvitationInput(BaseModel):
    org_id: str
    stakeholder_type: StakeholderType
    email: Optional[EmailStr] = None
    expires_in_days: int = Field(default=14, ge=1, le=90)


class StakeholderInvitation(BaseModel):
    code: str
    org_id: str
    stakeholder_type: StakeholderType
    email: Optional[str] = None
    invited_by: str
    expires_at: str
    used_by: Optional[str] = None
    used_at: Optional[str] = None
    created_at: str


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _iso(dt: datetime) -> str:
    return dt.isoformat()


async def _membership_for(user: User) -> dict:
    membership = await db.stakeholder_memberships.find_one(
        {"user_id": user.id}, {"_id": 0}
    )
    if not membership:
        raise HTTPException(status_code=403, detail="Aucun accès partenaire/institution")
    if membership.get("org_id") != user.org_id:
        raise HTTPException(status_code=403, detail="Contexte organisation invalide")
    return membership


@router.post("/invitations", response_model=StakeholderInvitation)
async def create_stakeholder_invitation(
    inp: StakeholderInvitationInput,
    current: User = Depends(require_role(*ADMIN_ROLES)),
):
    org = await db.organisations.find_one({"id": inp.org_id}, {"_id": 0})
    if not org:
        raise HTTPException(status_code=404, detail="Organisation introuvable")

    invitation = {
        "code": secrets.token_urlsafe(18),
        "org_id": inp.org_id,
        "stakeholder_type": inp.stakeholder_type,
        "email": str(inp.email).lower() if inp.email else None,
        "invited_by": current.id,
        "expires_at": _iso(_now() + timedelta(days=inp.expires_in_days)),
        "used_by": None,
        "used_at": None,
        "created_at": _iso(_now()),
    }
    await db.stakeholder_invitations.insert_one(invitation.copy())
    return StakeholderInvitation(**invitation)


@router.get("/invitations/{code}")
async def preview_stakeholder_invitation(code: str):
    invitation = await db.stakeholder_invitations.find_one({"code": code}, {"_id": 0})
    if not invitation or invitation.get("used_by"):
        raise HTTPException(status_code=404, detail="Invitation introuvable")

    expires_at = datetime.fromisoformat(invitation["expires_at"])
    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=timezone.utc)
    if expires_at < _now():
        raise HTTPException(status_code=410, detail="Invitation expirée")

    org = await db.organisations.find_one({"id": invitation["org_id"]}, {"_id": 0})
    return {
        "stakeholder_type": invitation["stakeholder_type"],
        "org_name": org.get("name") if org else None,
        "email": invitation.get("email"),
        "expires_at": invitation["expires_at"],
    }


@router.get("/me")
async def stakeholder_me(current: User = Depends(get_current_user)):
    membership = await _membership_for(current)
    org = await db.organisations.find_one({"id": membership["org_id"]}, {"_id": 0})
    return {
        "membership": membership,
        "organisation": org,
    }


@router.get("/overview")
async def stakeholder_overview(current: User = Depends(get_current_user)):
    membership = await _membership_for(current)
    org_id = membership["org_id"]

    cohorts = await db.cohorts.find({"org_id": org_id}, {"_id": 0}).to_list(500)
    cohort_ids = [c["id"] for c in cohorts]
    learner_count = await db.users.count_documents({"org_id": org_id, "role": "student"})
    trainer_count = await db.users.count_documents({"org_id": org_id, "role": "trainer"})

    progress_pipeline = [
        {"$match": {"cohort_id": {"$in": cohort_ids}}},
        {"$group": {"_id": "$cohort_id", "learners": {"$addToSet": "$user_id"}}},
    ] if cohort_ids else []
    progress_rows = []
    if progress_pipeline:
        progress_rows = await db.module_progress.aggregate(progress_pipeline).to_list(500)
    active_by_cohort = {row["_id"]: len(row.get("learners", [])) for row in progress_rows}

    return {
        "stakeholder_type": membership["stakeholder_type"],
        "org_id": org_id,
        "cohort_count": len(cohorts),
        "learner_count": learner_count,
        "trainer_count": trainer_count,
        "cohorts": [
            {
                "id": c["id"],
                "name": c["name"],
                "pole": c.get("pole"),
                "starts_at": c.get("starts_at"),
                "ends_at": c.get("ends_at"),
                "active_learners": active_by_cohort.get(c["id"], 0),
            }
            for c in cohorts
        ],
    }
