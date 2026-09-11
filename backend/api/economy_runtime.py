"""Admin Economy 3D runtime: 812 line-level decisions and activation evidence."""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel

from auth import require_role
from db import db
from models import User
from services.canonical_convergence import get_canonical_authority_map
from services.economy_runtime import runtime_decisions, set_gate_state

router = APIRouter(prefix="/master/economy-runtime", tags=["master-registry"])
Admin = Depends(require_role("admin", "super_admin", "founder"))


class EconomyGatePayload(BaseModel):
    satisfied: bool
    evidence_ref: str = ""


@router.get("/summary")
async def economy_runtime_summary(current: User = Admin):
    rows = await db.academy_economy_master.find({}, {"_id": 0}).to_list(812)
    authority = await get_canonical_authority_map()
    decisions = await runtime_decisions(db, [row["code"] for row in rows], canonicalized_codes=set(authority))
    runtime = [item["runtime"] for item in decisions.values()]
    return {
        "rows": len(rows),
        "runtime_bound": len(runtime),
        "public_discovery_allowed": sum(1 for item in runtime if item["public_discovery_allowed"]),
        "sale_allowed_now": sum(1 for item in runtime if item["sale_allowed"]),
        "sale_blocked_now": sum(1 for item in runtime if not item["sale_allowed"]),
        "not_for_sale": sum(1 for row in rows if row.get("sale_policy") == "NOT_FOR_SALE"),
        "decided_hold": sum(1 for row in rows if row.get("economic_status") == "DECIDED_HOLD"),
        "with_missing_gates": sum(1 for item in runtime if item.get("missing_gates")),
    }


@router.get("")
async def list_economy_runtime(
    public: str | None = None,
    packaging_v1: str | None = None,
    economic_status: str | None = None,
    sale_allowed: bool | None = None,
    limit: int = Query(default=812, ge=1, le=812),
    current: User = Admin,
):
    query = {}
    if public:
        query["public"] = public
    if packaging_v1:
        query["packaging_v1"] = packaging_v1
    if economic_status:
        query["economic_status"] = economic_status
    rows = await db.academy_economy_master.find(query, {"_id": 0}).limit(limit).to_list(limit)
    authority = await get_canonical_authority_map()
    decisions = await runtime_decisions(db, [row["code"] for row in rows], canonicalized_codes=set(authority))
    result = list(decisions.values())
    if sale_allowed is not None:
        result = [row for row in result if row["runtime"]["sale_allowed"] is sale_allowed]
    return result


@router.get("/{code}")
async def get_economy_runtime(code: str, current: User = Admin):
    authority = await get_canonical_authority_map()
    decisions = await runtime_decisions(db, [code], canonicalized_codes=set(authority))
    if code not in decisions:
        raise HTTPException(status_code=404, detail="economy row not found")
    return decisions[code]


@router.put("/{code}/gates/{gate}")
async def put_economy_gate(code: str, gate: str, payload: EconomyGatePayload, current: User = Admin):
    try:
        return await set_gate_state(
            db,
            code=code,
            gate=gate,
            satisfied=payload.satisfied,
            evidence_ref=payload.evidence_ref,
            actor_id=current.id,
        )
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
