"""Economy 3D traceability and canonical offer pricing API.

Traceability endpoints are staff-only. Offer pricing is public because it is
commercial catalogue data, not a payment or entitlement surface.
"""

from __future__ import annotations

from typing import Optional

from auth import require_role
from economy_3d import Economy3DError, commercial_class, record_by_code, records
from fastapi import APIRouter, Depends, HTTPException, Query
from models import STAFF_ROLES, User
from pricing_catalog import economic_rules, offer_by_id, offers

router = APIRouter(prefix="/economy", tags=["economy"])


@router.get("/offers")
async def list_offers(public_only: bool = Query(default=False)):
    return {
        "source": "CVLN_Academy_Master_Economie_3D_DECIDE_V1.xlsx",
        "commercial_runtime": "PRICING_CATALOG_ONLY",
        "checkout_runtime": "NOT_IMPLEMENTED_HERE",
        "items": offers(public_only=public_only),
        "rules": economic_rules(),
    }


@router.get("/offers/{offer_id}")
async def get_offer(offer_id: str):
    try:
        return offer_by_id(offer_id)
    except KeyError as exc:
        raise HTTPException(
            status_code=404, detail="Offre économique introuvable"
        ) from exc


@router.get("/3d/health")
async def economy_3d_health(current: User = Depends(require_role(*STAFF_ROLES))):
    del current
    try:
        items = records()
    except Economy3DError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc

    counts = {
        "PUBLIC_MARKET": 0,
        "CROSS_ECOSYSTEM_PROGRAM": 0,
        "INTERNAL_NOT_FOR_SALE": 0,
        "BUNDLED_BRIDGE": 0,
        "HOLD_FROM_SALE": 0,
    }
    for record in items:
        counts[commercial_class(record)] += 1
    return {
        "status": "verified_projection",
        "source": "CVLN_Academy_Master_Economie_3D_DECIDE_V1.xlsx/Mapping_812",
        "records": len(items),
        "classes": counts,
        "commercial_runtime": "TRACEABILITY_PLUS_PRICING_CATALOG",
    }


@router.get("/3d")
async def list_economy_3d(
    commercial_class_filter: Optional[str] = Query(default=None, alias="class"),
    limit: int = Query(default=100, ge=1, le=812),
    skip: int = Query(default=0, ge=0),
    current: User = Depends(require_role(*STAFF_ROLES)),
):
    del current
    items = records()
    if commercial_class_filter:
        normalized = commercial_class_filter.strip().upper()
        items = [r for r in items if commercial_class(r) == normalized]
    selected = items[skip : skip + limit]
    return {
        "total": len(items),
        "skip": skip,
        "limit": limit,
        "items": [
            {**record, "commercial_class": commercial_class(record)}
            for record in selected
        ],
    }


@router.get("/3d/{code}")
async def get_economy_3d(
    code: str,
    current: User = Depends(require_role(*STAFF_ROLES)),
):
    del current
    try:
        record = record_by_code(code)
    except KeyError as exc:
        raise HTTPException(
            status_code=404, detail="Economy 3D code introuvable"
        ) from exc
    return {**record, "commercial_class": commercial_class(record)}
