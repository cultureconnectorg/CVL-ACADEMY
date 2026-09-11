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


def _parse_expiry(value: str) -> datetime:
    expires_at = datetime.fromisoformat(value)
    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=timezone.utc)
    return expires_at


async def _membership_for(user: User) -> dict:
    membership = await db.stakeholder_memberships.find_one(
        {"user_id": user.id}, {"_id": 0}
    )
    if not membership:
        raise HTTPException(
            status_code=403, detail="Aucun accès partenaire/institution"
        )
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
    if _parse_expiry(invitation["expires_at"]) < _now():
        raise HTTPException(status_code=410, detail="Invitation expirée")

    org = await db.organisations.find_one({"id": invitation["org_id"]}, {"_id": 0})
    return {
        "stakeholder_type": invitation["stakeholder_type"],
        "org_name": org.get("name") if org else None,
        "email": invitation.get("email"),
        "expires_at": invitation["expires_at"],
    }


@router.post("/invitations/{code}/claim")
async def claim_stakeholder_invitation(
    code: str, current: User = Depends(get_current_user)
):
    invitation = await db.stakeholder_invitations.find_one({"code": code}, {"_id": 0})
    if not invitation or invitation.get("used_by"):
        raise HTTPException(status_code=404, detail="Invitation introuvable")
    if _parse_expiry(invitation["expires_at"]) < _now():
        raise HTTPException(status_code=410, detail="Invitation expirée")
    if invitation.get("email") and invitation["email"] != current.email.lower():
        raise HTTPException(
            status_code=403, detail="Invitation réservée à une autre adresse"
        )

    existing = await db.stakeholder_memberships.find_one(
        {"user_id": current.id}, {"_id": 0}
    )
    if existing:
        if (
            existing.get("org_id") == invitation["org_id"]
            and existing.get("stakeholder_type") == invitation["stakeholder_type"]
        ):
            return {"membership": existing, "already_member": True}
        raise HTTPException(
            status_code=409,
            detail="Ce compte possède déjà une adhésion partenaire/institution active",
        )

    claimed_at = _iso(_now())
    result = await db.stakeholder_invitations.update_one(
        {"code": code, "used_by": None},
        {"$set": {"used_by": current.id, "used_at": claimed_at}},
    )
    if result.modified_count != 1:
        raise HTTPException(status_code=409, detail="Invitation déjà utilisée")

    membership = {
        "user_id": current.id,
        "org_id": invitation["org_id"],
        "stakeholder_type": invitation["stakeholder_type"],
        "granted_by": invitation["invited_by"],
        "created_at": claimed_at,
    }
    await db.stakeholder_memberships.insert_one(membership.copy())
    await db.users.update_one(
        {"id": current.id}, {"$set": {"org_id": invitation["org_id"]}}
    )
    return {"membership": membership, "already_member": False}


@router.get("/me")
async def stakeholder_me(current: User = Depends(get_current_user)):
    membership = await _membership_for(current)
    org = await db.organisations.find_one({"id": membership["org_id"]}, {"_id": 0})
    return {"membership": membership, "organisation": org}


@router.get("/overview")
async def stakeholder_overview(current: User = Depends(get_current_user)):
    membership = await _membership_for(current)
    org_id = membership["org_id"]

    cohorts = await db.cohorts.find({"org_id": org_id}, {"_id": 0}).to_list(500)
    learner_count = await db.users.count_documents(
        {"org_id": org_id, "role": "student"}
    )
    trainer_count = await db.users.count_documents(
        {"org_id": org_id, "role": "trainer"}
    )

    cohort_rows = []
    for cohort in cohorts:
        learner_ids = await db.users.distinct(
            "id", {"org_id": org_id, "cohort_id": cohort["id"], "role": "student"}
        )
        active_ids = []
        if learner_ids:
            active_ids = await db.module_progress.distinct(
                "user_id", {"user_id": {"$in": learner_ids}}
            )
        cohort_rows.append(
            {
                "id": cohort["id"],
                "name": cohort["name"],
                "pole": cohort.get("pole"),
                "starts_at": cohort.get("starts_at"),
                "ends_at": cohort.get("ends_at"),
                "learner_count": len(learner_ids),
                "active_learners": len(active_ids),
            }
        )

    return {
        "stakeholder_type": membership["stakeholder_type"],
        "org_id": org_id,
        "cohort_count": len(cohorts),
        "learner_count": learner_count,
        "trainer_count": trainer_count,
        "cohorts": cohort_rows,
    }
