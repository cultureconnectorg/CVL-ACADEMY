"""Poles + formations catalogue, governed by Economy 3D line policy."""
from __future__ import annotations

from typing import Dict, Optional

from fastapi import APIRouter, Depends, HTTPException

from auth import get_current_user_optional, require_role
from db import db
from lx import (
    compute_status,
    is_formation_unlocked,
    is_module_unlocked,
    phase_completion_flags,
)
from models import ADMIN_ROLES, STAFF_ROLES, ContentStatusInput, User
from services.canonical_convergence import get_canonical_authority_map
from services.economy_runtime import runtime_decisions

router = APIRouter(tags=["formations"])


@router.get("/poles")
async def list_poles():
    return await db.poles.find({}, {"_id": 0}).to_list(50)


def _economy_public_payload(economy: dict | None) -> dict | None:
    if not economy:
        return None
    runtime = economy.get("runtime") or {}
    return {
        "code": economy.get("code"),
        "public": economy.get("public"),
        "monetization_v1": economy.get("monetization_v1"),
        "packaging_v1": economy.get("packaging_v1"),
        "public_price_v1": economy.get("public_price_v1"),
        "channel": economy.get("channel"),
        "economic_status": economy.get("economic_status"),
        "sale_allowed": runtime.get("sale_allowed", False),
        "sale_reason": runtime.get("sale_reason"),
        "missing_gates": runtime.get("missing_gates", []),
        "allowed_offer_ids": runtime.get("allowed_offer_ids", []),
    }


@router.get("/formations")
async def list_formations(
    limit: int = 200,
    skip: int = 0,
    current: Optional[User] = Depends(get_current_user_optional),
):
    staff = bool(current and current.role in STAFF_ROLES)
    content_filter = {} if staff else {"content_status": "published"}
    docs = (
        await db.formations.find(content_filter, {"_id": 0})
        .skip(skip)
        .limit(limit)
        .to_list(limit)
    )
    authority_map = await get_canonical_authority_map()
    codes = [doc["code"] for doc in docs]
    economy = await runtime_decisions(
        db,
        codes,
        canonicalized_codes=set(authority_map),
    )

    # Economy 3D `Public ?` is an actual discovery rule. Legacy formations
    # with no Economy row preserve their former behavior. Staff sees all.
    if not staff:
        docs = [
            doc
            for doc in docs
            if doc["code"] not in economy
            or economy[doc["code"]]["runtime"]["public_discovery_allowed"]
        ]

    return [
        {
            "code": doc["code"],
            "name": doc["name"],
            "pole": doc["pole"],
            "pole_name": doc.get("pole_name"),
            "pole_color": doc.get("pole_color"),
            "duration_h": doc["duration_h"],
            "stades": doc["stades"],
            "cc": doc["cc"],
            "badge_name": doc["badge_name"],
            "description": doc.get("description", ""),
            "contexts": doc.get("contexts", []),
            "audience_levels": doc.get("audience_levels", []),
            "bridge_entities": doc.get("bridge_entities", []),
            "positioning_note": doc.get("positioning_note", ""),
            "primary_job": (doc.get("cartography") or {}).get("primary_job"),
            "reconstruction_status": doc.get("reconstruction_status"),
            "needs_external_calibration": doc.get(
                "needs_external_calibration",
                True,
            ),
            "delivery_formats": (doc.get("cartography") or {}).get(
                "delivery_formats",
                [],
            ),
            "market_job_title": doc.get("market_job_title"),
            "calibration_confidence": doc.get("calibration_confidence"),
            "calibration_date": doc.get("calibration_date"),
            "reconciliation_flags": doc.get("reconciliation_flags", []),
            "modules_count": len(doc.get("modules", [])),
            "content_status": doc.get("content_status", "published"),
            "canonical_authority": authority_map.get(doc["code"]),
            "economy": _economy_public_payload(economy.get(doc["code"])),
        }
        for doc in docs
    ]


@router.get("/formations/{code}")
async def get_formation(
    code: str,
    current: Optional[User] = Depends(get_current_user_optional),
):
    doc = await db.formations.find_one({"code": code}, {"_id": 0})
    if not doc:
        raise HTTPException(status_code=404, detail="Formation introuvable")
    staff = bool(current and current.role in STAFF_ROLES)
    if doc.get("content_status", "published") != "published" and not staff:
        raise HTTPException(status_code=404, detail="Formation introuvable")

    authority_map = await get_canonical_authority_map()
    econ_map = await runtime_decisions(
        db,
        [code],
        canonicalized_codes=set(authority_map),
    )
    econ = econ_map.get(code)
    if (
        econ
        and not staff
        and not econ["runtime"]["public_discovery_allowed"]
    ):
        raise HTTPException(status_code=404, detail="Formation introuvable")

    doc["canonical_authority"] = authority_map.get(code)
    doc["economy"] = _economy_public_payload(econ)

    if not current:
        for module in doc.get("modules", []):
            module["is_unlocked"] = True
            module["status"] = "available"
            module["phase_flags"] = phase_completion_flags(None)
        doc["is_unlocked"] = True
        doc["lock_reason"] = ""
        return doc

    progress_docs = await db.progress.find(
        {"user_id": current.id},
        {"_id": 0},
    ).to_list(1000)
    prog_by_mod: Dict[str, Dict] = {
        progress["module_code"]: progress
        for progress in progress_docs
    }
    all_formations = await db.formations.find({}, {"_id": 0}).to_list(200)
    is_unlocked, reason = is_formation_unlocked(
        current.metier_vise,
        doc,
        all_formations,
        prog_by_mod,
    )
    doc["is_unlocked"] = is_unlocked
    doc["lock_reason"] = reason
    for module in doc.get("modules", []):
        module["is_unlocked"] = is_unlocked and is_module_unlocked(
            doc,
            module["code"],
            prog_by_mod,
        )
        progress = prog_by_mod.get(module["code"])
        module["status"] = compute_status(progress)
        module["phase_flags"] = phase_completion_flags(progress)
        module["course_progress_pct"] = int(
            (progress or {}).get("course_progress_pct", 0)
        )
        module["quiz_score"] = float(
            (progress or {}).get("quiz_score", 0.0)
        )
    return doc


@router.patch("/admin/formations/{code}/status")
async def set_formation_status(
    code: str,
    inp: ContentStatusInput,
    current: User = Depends(require_role(*ADMIN_ROLES)),
):
    result = await db.formations.update_one(
        {"code": code},
        {"$set": {"content_status": inp.content_status}},
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Formation introuvable")
    return {
        "ok": True,
        "code": code,
        "content_status": inp.content_status,
    }
