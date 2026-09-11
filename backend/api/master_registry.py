"""Admin runtime access to Academy master catalogue/economy/proof registries."""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel

from auth import require_role
from db import db
from models import User
from services.economy_importer import evaluate_sale_policy
from services.requirement_registry import promote_verified

router = APIRouter(prefix="/master", tags=["master-registry"])
Admin = Depends(require_role("admin", "super_admin", "founder"))


class VerificationPayload(BaseModel):
    evidence_ref: str


@router.get("/catalogue")
async def list_master_catalogue(
    domain: str | None = None,
    status: str | None = None,
    limit: int = Query(default=100, ge=1, le=1000),
    current: User = Admin,
):
    query = {}
    if domain:
        query["domain"] = domain
    if status:
        query["status"] = status
    return await db.academy_catalogue_master.find(query, {"_id": 0}).limit(limit).to_list(limit)


@router.get("/catalogue/{code}")
async def get_master_catalogue(code: str, current: User = Admin):
    row = await db.academy_catalogue_master.find_one({"code": code}, {"_id": 0})
    if not row:
        raise HTTPException(status_code=404, detail="catalogue row not found")
    return row


@router.get("/economy/{code}")
async def get_master_economy(code: str, current: User = Admin):
    row = await db.academy_economy_master.find_one({"code": code}, {"_id": 0})
    if not row:
        raise HTTPException(status_code=404, detail="economy row not found")
    return row


@router.get("/economy/{code}/sale-policy")
async def get_sale_policy(
    code: str,
    gates: list[str] = Query(default=[]),
    current: User = Admin,
):
    row = await db.academy_economy_master.find_one({"code": code}, {"_id": 0})
    if not row:
        raise HTTPException(status_code=404, detail="economy row not found")
    return {"code": code, **evaluate_sale_policy(row, set(gates))}


@router.get("/requirements")
async def requirement_summary(current: User = Admin):
    total = await db.academy_requirement_registry.count_documents({})
    verified = await db.academy_requirement_registry.count_documents({"verified": True})
    ingested = await db.academy_requirement_registry.count_documents({"status": "INGESTED_RUNTIME"})
    return {"total": total, "verified": verified, "ingested_runtime": ingested}


@router.get("/requirements/{requirement_id:path}")
async def get_requirement(requirement_id: str, current: User = Admin):
    row = await db.academy_requirement_registry.find_one(
        {"requirement_id": requirement_id}, {"_id": 0}
    )
    if not row:
        raise HTTPException(status_code=404, detail="requirement not found")
    return row


@router.post("/requirements/{requirement_id:path}/verify")
async def verify_requirement(
    requirement_id: str,
    payload: VerificationPayload,
    current: User = Admin,
):
    try:
        return await promote_verified(
            db, requirement_id, evidence_ref=payload.evidence_ref, actor_id=current.id
        )
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
