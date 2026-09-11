"""Institutional Bridge API.

This surface enriches existing organisations instead of replacing them. All
mutating funding operations remain admin-only until a dedicated institution
role/permission policy is explicitly approved. Preparation endpoints never
submit data to an external institution.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query

from auth import get_current_user, require_role
from db import db
from models import ADMIN_ROLES, STAFF_ROLES, User
from services.institutional_bridge.models import (
    Capability,
    ConnectorDescriptor,
    FundingCase,
    FundingCaseInput,
    InstitutionProfile,
    InstitutionProfileInput,
    PreparedEnvelope,
)
from services.institutional_bridge.registry import (
    UnknownConnector,
    UnsupportedCapability,
    connector_registry,
    describe_connectors,
    prepare_case,
)

router = APIRouter(prefix="/institutional", tags=["institutional"])


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


@router.get("/connectors", response_model=List[ConnectorDescriptor])
async def list_connectors(
    current: User = Depends(require_role(*ADMIN_ROLES)),
):
    return list(describe_connectors())


@router.put("/orgs/{org_id}/profile", response_model=InstitutionProfile)
async def upsert_institution_profile(
    org_id: str,
    inp: InstitutionProfileInput,
    current: User = Depends(require_role(*ADMIN_ROLES)),
):
    org = await db.organisations.find_one({"id": org_id}, {"_id": 0})
    if not org:
        raise HTTPException(status_code=404, detail="Organisation introuvable")

    unknown = [code for code in inp.connector_codes if code not in connector_registry]
    if unknown:
        raise HTTPException(
            status_code=400,
            detail={"message": "Connecteur institutionnel inconnu", "codes": unknown},
        )

    existing = await db.institution_profiles.find_one({"org_id": org_id}, {"_id": 0})
    profile = InstitutionProfile(
        org_id=org_id,
        **inp.model_dump(),
        created_at=existing.get("created_at", _now()) if existing else _now(),
        updated_at=_now(),
    )
    await db.institution_profiles.replace_one(
        {"org_id": org_id},
        profile.model_dump(),
        upsert=True,
    )
    return profile


@router.get("/orgs/{org_id}/profile", response_model=InstitutionProfile)
async def get_institution_profile(
    org_id: str,
    current: User = Depends(get_current_user),
):
    is_admin = current.role in ADMIN_ROLES
    is_org_staff = current.role in STAFF_ROLES and current.org_id == org_id
    if not is_admin and not is_org_staff:
        raise HTTPException(status_code=403, detail="Accès refusé à cette organisation")

    profile = await db.institution_profiles.find_one({"org_id": org_id}, {"_id": 0})
    if not profile:
        raise HTTPException(status_code=404, detail="Profil institutionnel introuvable")
    return InstitutionProfile(**profile)


@router.post("/funding-cases", response_model=FundingCase)
async def create_funding_case(
    inp: FundingCaseInput,
    current: User = Depends(require_role(*ADMIN_ROLES)),
):
    org = await db.organisations.find_one({"id": inp.org_id}, {"_id": 0})
    if not org:
        raise HTTPException(status_code=404, detail="Organisation introuvable")

    formation = await db.formations.find_one(
        {"code": inp.formation_code},
        {"_id": 0, "code": 1},
    )
    if not formation:
        raise HTTPException(status_code=404, detail="Formation introuvable")

    if inp.beneficiary_user_id:
        beneficiary = await db.users.find_one(
            {"id": inp.beneficiary_user_id},
            {"_id": 0, "id": 1},
        )
        if not beneficiary:
            raise HTTPException(status_code=404, detail="Bénéficiaire introuvable")

    funding_case = FundingCase(**inp.model_dump())
    await db.funding_cases.insert_one(funding_case.model_dump())
    return funding_case


@router.get("/funding-cases", response_model=List[FundingCase])
async def list_funding_cases(
    org_id: Optional[str] = Query(default=None),
    current: User = Depends(require_role(*ADMIN_ROLES)),
):
    query = {"org_id": org_id} if org_id else {}
    docs = (
        await db.funding_cases.find(query, {"_id": 0})
        .sort("created_at", -1)
        .to_list(500)
    )
    return [FundingCase(**doc) for doc in docs]


@router.get("/funding-cases/{case_id}", response_model=FundingCase)
async def get_funding_case(
    case_id: str,
    current: User = Depends(require_role(*ADMIN_ROLES)),
):
    doc = await db.funding_cases.find_one({"id": case_id}, {"_id": 0})
    if not doc:
        raise HTTPException(status_code=404, detail="Dossier de financement introuvable")
    return FundingCase(**doc)


@router.post(
    "/funding-cases/{case_id}/prepare/{connector_code}",
    response_model=PreparedEnvelope,
)
async def prepare_funding_case(
    case_id: str,
    connector_code: str,
    capability: Capability = Query(default="APPLICATION_PREPARE"),
    current: User = Depends(require_role(*ADMIN_ROLES)),
):
    doc = await db.funding_cases.find_one({"id": case_id}, {"_id": 0})
    if not doc:
        raise HTTPException(status_code=404, detail="Dossier de financement introuvable")

    try:
        return prepare_case(FundingCase(**doc), connector_code, capability)
    except UnknownConnector as exc:
        raise HTTPException(
            status_code=404,
            detail="Connecteur institutionnel inconnu",
        ) from exc
    except UnsupportedCapability as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
