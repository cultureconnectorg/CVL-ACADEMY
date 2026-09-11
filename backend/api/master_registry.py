"""Admin runtime access to Academy master and proof registries."""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel

from auth import require_role
from db import db
from models import User
from services.cartography_2d_runtime import SHEET_ROW_COUNTS
from services.economy_importer import evaluate_sale_policy
from services.protocol_master_runtime import EXPECTED_DOMAINS, EXPECTED_ROWS, evaluate_protocol_control
from services.requirement_registry import promote_verified

router = APIRouter(prefix="/master", tags=["master-registry"])
Admin = Depends(require_role("admin", "super_admin", "founder"))


class VerificationPayload(BaseModel):
    evidence_ref: str


class ProtocolExecutionPayload(BaseModel):
    context: dict = {}


@router.get("/catalogue")
async def list_master_catalogue(domain: str | None = None, status: str | None = None, limit: int = Query(default=100, ge=1, le=1000), current: User = Admin):
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
async def get_sale_policy(code: str, gates: list[str] = Query(default=[]), current: User = Admin):
    row = await db.academy_economy_master.find_one({"code": code}, {"_id": 0})
    if not row:
        raise HTTPException(status_code=404, detail="economy row not found")
    return {"code": code, **evaluate_sale_policy(row, set(gates))}


@router.get("/cartography-2d/summary")
async def cartography_2d_summary(current: User = Admin):
    manifest = await db.academy_cartography_2d_manifest.find_one({"kind": "CARTOGRAPHY_2D_WORKBOOK"}, {"_id": 0})
    runtime_rows = await db.academy_cartography_2d_rows.count_documents({})
    proof_rows = await db.academy_requirement_registry.count_documents({"family": "CARTOGRAPHY_2D"})
    return {"expected_rows": sum(SHEET_ROW_COUNTS.values()), "expected_sheets": len(SHEET_ROW_COUNTS), "runtime_rows": runtime_rows, "proof_rows": proof_rows, "sheet_row_counts": SHEET_ROW_COUNTS, "manifest": manifest}


@router.get("/cartography-2d/sheets")
async def cartography_2d_sheets(current: User = Admin):
    return [{"sheet": sheet, "expected_rows": count} for sheet, count in SHEET_ROW_COUNTS.items()]


@router.get("/cartography-2d/sheet/{sheet}")
async def cartography_2d_sheet(sheet: str, limit: int = Query(default=100, ge=1, le=2000), current: User = Admin):
    if sheet not in SHEET_ROW_COUNTS:
        raise HTTPException(status_code=404, detail="unknown cartography 2D sheet")
    return await db.academy_cartography_2d_rows.find({"sheet": sheet}, {"_id": 0}).sort("excel_row", 1).limit(limit).to_list(limit)


@router.get("/cartography-2d/sheet/{sheet}/row/{excel_row}")
async def cartography_2d_row(sheet: str, excel_row: int, current: User = Admin):
    if sheet not in SHEET_ROW_COUNTS:
        raise HTTPException(status_code=404, detail="unknown cartography 2D sheet")
    row = await db.academy_cartography_2d_rows.find_one({"sheet": sheet, "excel_row": excel_row}, {"_id": 0})
    if not row:
        raise HTTPException(status_code=404, detail="cartography 2D row not found")
    return row


@router.get("/protocols/summary")
async def protocol_master_summary(current: User = Admin):
    runtime_rows = await db.academy_protocol_controls.count_documents({})
    proof_rows = await db.academy_requirement_registry.count_documents({"family": "PROTOCOL_MASTER"})
    manifest = await db.academy_protocol_manifest.find_one({"kind": "PROTOCOL_MASTER_WORKBOOK"}, {"_id": 0})
    return {"expected_rows": EXPECTED_ROWS, "runtime_rows": runtime_rows, "proof_rows": proof_rows, "domain_counts": EXPECTED_DOMAINS, "manifest": manifest}


@router.get("/protocols")
async def list_protocol_controls(domain: str | None = None, limit: int = Query(default=227, ge=1, le=227), current: User = Admin):
    query = {"domain": domain} if domain else {}
    return await db.academy_protocol_controls.find(query, {"_id": 0}).sort("excel_row", 1).limit(limit).to_list(limit)


@router.get("/protocols/{control_id}")
async def get_protocol_control(control_id: str, current: User = Admin):
    row = await db.academy_protocol_controls.find_one({"control_id": control_id}, {"_id": 0})
    if not row:
        raise HTTPException(status_code=404, detail="protocol control not found")
    return row


@router.post("/protocols/{control_id}/execute")
async def execute_protocol_control(control_id: str, payload: ProtocolExecutionPayload, current: User = Admin):
    row = await db.academy_protocol_controls.find_one({"control_id": control_id}, {"_id": 0})
    if not row:
        raise HTTPException(status_code=404, detail="protocol control not found")
    context = dict(payload.context)
    context.setdefault("actor_id", current.id)
    decision = evaluate_protocol_control(row, context)
    await db.academy_protocol_executions.insert_one({**decision, "context_keys": sorted(context.keys())})
    return decision


@router.get("/requirements")
async def requirement_summary(current: User = Admin):
    total = await db.academy_requirement_registry.count_documents({})
    verified = await db.academy_requirement_registry.count_documents({"verified": True})
    ingested = await db.academy_requirement_registry.count_documents({"status": "INGESTED_RUNTIME"})
    return {"total": total, "verified": verified, "ingested_runtime": ingested}


@router.get("/requirements/{requirement_id:path}")
async def get_requirement(requirement_id: str, current: User = Admin):
    row = await db.academy_requirement_registry.find_one({"requirement_id": requirement_id}, {"_id": 0})
    if not row:
        raise HTTPException(status_code=404, detail="requirement not found")
    return row


@router.post("/requirements/{requirement_id:path}/verify")
async def verify_requirement(requirement_id: str, payload: VerificationPayload, current: User = Admin):
    try:
        return await promote_verified(db, requirement_id, evidence_ref=payload.evidence_ref, actor_id=current.id)
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
