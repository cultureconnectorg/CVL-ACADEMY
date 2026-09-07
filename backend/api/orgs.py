"""Organisations, cohorts and invitations — admin-managed.

Lets CVLN onboard an institutional partner (org) with its own cohorts
(e.g. one per intake/pole/territory) and invite members into a specific
role/org/cohort via a shareable code, consumed at signup
(`RegisterInput.invite_code`, see api/auth.py).
"""

from __future__ import annotations

import secrets
from datetime import datetime, timedelta, timezone
from typing import List

from fastapi import APIRouter, Depends, HTTPException

from auth import get_current_user, require_role
from db import db
from models import (
    ADMIN_ROLES,
    INVITER_ALLOWED_INVITED_ROLES,
    Cohort,
    CohortInput,
    Invitation,
    InvitationInput,
    Organisation,
    OrganisationInput,
    User,
)
from services.notifications import notifications

router = APIRouter(tags=["orgs"])


# ============ ORGANISATIONS ============
@router.get("/orgs", response_model=List[Organisation])
async def list_orgs(current: User = Depends(require_role(*ADMIN_ROLES))):
    docs = await db.organisations.find({}, {"_id": 0}).to_list(500)
    return [Organisation(**d) for d in docs]


@router.post("/orgs", response_model=Organisation)
async def create_org(
    inp: OrganisationInput, current: User = Depends(require_role(*ADMIN_ROLES))
):
    existing = await db.organisations.find_one({"slug": inp.slug}, {"_id": 0})
    if existing:
        raise HTTPException(status_code=400, detail="Slug déjà utilisé")
    org = Organisation(name=inp.name, slug=inp.slug)
    await db.organisations.insert_one(org.model_dump())
    return org


# ============ COHORTS ============
@router.get("/orgs/{org_id}/cohorts", response_model=List[Cohort])
async def list_cohorts(org_id: str, current: User = Depends(get_current_user)):
    # Staff of the org (or platform admins) can list its cohorts.
    if current.role not in ADMIN_ROLES and current.org_id != org_id:
        raise HTTPException(status_code=403, detail="Accès refusé à cette organisation")
    docs = await db.cohorts.find({"org_id": org_id}, {"_id": 0}).to_list(500)
    return [Cohort(**d) for d in docs]


@router.post("/orgs/{org_id}/cohorts", response_model=Cohort)
async def create_cohort(
    org_id: str, inp: CohortInput, current: User = Depends(require_role(*ADMIN_ROLES))
):
    org = await db.organisations.find_one({"id": org_id}, {"_id": 0})
    if not org:
        raise HTTPException(status_code=404, detail="Organisation introuvable")
    cohort = Cohort(org_id=org_id, **inp.model_dump())
    await db.cohorts.insert_one(cohort.model_dump())
    return cohort


# ============ INVITATIONS ============
@router.post("/invitations", response_model=Invitation)
async def create_invitation(
    inp: InvitationInput, current: User = Depends(require_role(*ADMIN_ROLES, "trainer"))
):
    # SEC-01 — server-enforced inviter_role -> allowed_invited_roles.
    # Never trust the client to only ever offer the "safe" roles in its
    # own UI; this is the actual privilege boundary.
    allowed_roles = INVITER_ALLOWED_INVITED_ROLES.get(current.role, ())
    if inp.role not in allowed_roles:
        raise HTTPException(
            status_code=403,
            detail=f"Le rôle '{inp.role}' ne peut pas être accordé par une invitation de type '{current.role}'.",
        )

    # SEC-01 — organisational scope. A non-admin inviter (today: trainer)
    # can only ever invite into their own organisation — never another
    # org, and never org-less. ADMIN_ROLES stay platform-wide, exactly
    # as before. The effective org_id is derived from the inviter's own
    # membership, never taken from the request body, so a spoofed
    # `org_id` in the payload can't widen scope.
    if current.role in ADMIN_ROLES:
        effective_org_id = inp.org_id
    else:
        if not current.org_id:
            raise HTTPException(
                status_code=400,
                detail="Vous devez appartenir à une organisation pour créer une invitation.",
            )
        if inp.org_id and inp.org_id != current.org_id:
            raise HTTPException(
                status_code=403,
                detail="Vous ne pouvez inviter que dans votre propre organisation.",
            )
        effective_org_id = current.org_id

    if effective_org_id:
        org = await db.organisations.find_one({"id": effective_org_id}, {"_id": 0})
        if not org:
            raise HTTPException(status_code=404, detail="Organisation introuvable")
    if inp.cohort_id:
        cohort = await db.cohorts.find_one({"id": inp.cohort_id}, {"_id": 0})
        if not cohort:
            raise HTTPException(status_code=404, detail="Cohorte introuvable")
        # A cohort belongs to exactly one org — an invitation naming both
        # must be internally consistent, never a cross-org cohort grant.
        if effective_org_id and cohort.get("org_id") != effective_org_id:
            raise HTTPException(
                status_code=400,
                detail="Cette cohorte n'appartient pas à l'organisation de l'invitation.",
            )

    invitation = Invitation(
        code=secrets.token_urlsafe(8),
        email=inp.email,
        role=inp.role,
        org_id=effective_org_id,
        cohort_id=inp.cohort_id,
        invited_by=current.id,
        expires_at=(
            datetime.now(timezone.utc) + timedelta(days=inp.expires_in_days)
        ).isoformat(),
    )
    await db.invitations.insert_one(invitation.model_dump())

    if inp.email:
        org_name = None
        if effective_org_id:
            org_doc = await db.organisations.find_one({"id": effective_org_id}, {"_id": 0})
            org_name = org_doc["name"] if org_doc else None
        await notifications.send_invitation(inp.email, invitation.code, org_name)

    return invitation


@router.get("/invitations/{code}")
async def get_invitation(code: str):
    """Public lookup so the signup UI can preview an invite before the user
    registers (role/org name — never leaks who invited them, and never
    leaks the target email either — SEC-02: possession of a leaked or
    guessed code must not let a stranger learn who the invitation was
    meant for. `email_required` is enough for the signup UI to say
    "this invitation is reserved for a specific address" without
    revealing what that address is."""
    inv = await db.invitations.find_one({"code": code}, {"_id": 0})
    if not inv:
        raise HTTPException(status_code=404, detail="Invitation introuvable")
    if inv.get("used_by"):
        raise HTTPException(status_code=400, detail="Invitation déjà utilisée")
    org_name = None
    if inv.get("org_id"):
        org_doc = await db.organisations.find_one({"id": inv["org_id"]}, {"_id": 0})
        org_name = org_doc["name"] if org_doc else None
    return {
        "role": inv["role"],
        "org_name": org_name,
        "expires_at": inv.get("expires_at"),
        "email_required": bool(inv.get("email")),
    }
