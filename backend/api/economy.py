"""Economy 3D traceability and canonical offer pricing API.

Traceability endpoints are staff-only. Offer pricing is public because it is
commercial catalogue data, not a payment or entitlement surface.
"""

from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query

from auth import require_role
from economy_3d import Economy3DError, commercial_class, record_by_code, records
from models import STAFF_ROLES, User
from pricing_catalog import economic_rules, offer_by_id, offers
from services.nvidia_runtime import accelerated_group_count

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

    # This is a real business path through the adaptive acceleration boundary.
    # The canonical workbook has only 812 records, so the default policy correctly
    # stays on CPU today; if this projection grows beyond the benchmarked threshold
    # on a qualified GPU worker, the same contract can switch to cuDF without
    # changing the endpoint's business semantics.
    projected = [{"commercial_class": commercial_class(record)} for record in items]
    observed_counts, engine, fallback_reason = accelerated_group_count(
        projected, "commercial_class"
    )
    expected_classes = (
        "PUBLIC_MARKET",
        "CROSS_ECOSYSTEM_PROGRAM",
        "INTERNAL_NOT_FOR_SALE",
        "BUNDLED_BRIDGE",
        "HOLD_FROM_SALE",
    )
    counts = {name: observed_counts.get(name, 0) for name in expected_classes}

    return {
        "status": "verified_projection",
        "source": "CVLN_Academy_Master_Economie_3D_DECIDE_V1.xlsx/Mapping_812",
        "records": len(items),
        "classes": counts,
        "aggregation_engine": engine,
        "acceleration_fallback_reason": fallback_reason,
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
