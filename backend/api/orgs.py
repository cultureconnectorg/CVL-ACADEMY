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


@router.get("/orgs/{org_id}/cohorts", response_model=List[Cohort])
async def list_cohorts(org_id: str, current: User = Depends(get_current_user)):
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


@router.post("/invitations", response_model=Invitation)
async def create_invitation(
    inp: InvitationInput, current: User = Depends(require_role(*ADMIN_ROLES, "trainer"))
):
    # Trainers can only invite learners into their own organisation. Role and
    # tenant boundaries are enforced server-side, never trusted from the UI.
    if current.role == "trainer":
        if inp.role != "student":
            raise HTTPException(status_code=403, detail="Un formateur ne peut inviter que des apprenants")
        if not current.org_id or inp.org_id != current.org_id:
            raise HTTPException(status_code=403, detail="Invitation limitée à votre organisation")

    if inp.org_id:
        org = await db.organisations.find_one({"id": inp.org_id}, {"_id": 0})
        if not org:
            raise HTTPException(status_code=404, detail="Organisation introuvable")
    if inp.cohort_id:
        cohort = await db.cohorts.find_one({"id": inp.cohort_id}, {"_id": 0})
        if not cohort:
            raise HTTPException(status_code=404, detail="Cohorte introuvable")
        if inp.org_id and cohort.get("org_id") != inp.org_id:
            raise HTTPException(status_code=400, detail="La cohorte n'appartient pas à cette organisation")

    invitation = Invitation(
        code=secrets.token_urlsafe(8),
        email=inp.email,
        role=inp.role,
        org_id=inp.org_id,
        cohort_id=inp.cohort_id,
        invited_by=current.id,
        expires_at=(datetime.now(timezone.utc) + timedelta(days=inp.expires_in_days)).isoformat(),
    )
    await db.invitations.insert_one(invitation.model_dump())

    if inp.email:
        org_name = None
        if inp.org_id:
            org_doc = await db.organisations.find_one({"id": inp.org_id}, {"_id": 0})
            org_name = org_doc["name"] if org_doc else None
        await notifications.send_invitation(inp.email, invitation.code, org_name)

    return invitation


@router.get("/invitations/{code}")
async def get_invitation(code: str):
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
        "email": inv.get("email"),
    }
