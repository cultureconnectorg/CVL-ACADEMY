"""Retention Executor API (XCP-003 / PRI-008)."""

from __future__ import annotations

from typing import Any, Dict, List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from auth import require_role
from models import User
from services import retention_executor

router = APIRouter(prefix="/retention", tags=["privacy-retention"])
Admin = Depends(require_role("admin", "super_admin", "founder"))


class HoldCreate(BaseModel):
    resource_record_id: str = Field(min_length=1, max_length=240)
    reason: str = Field(min_length=3, max_length=4000)
    evidence_refs: List[str] = Field(min_length=1)


class HoldRelease(BaseModel):
    evidence_refs: List[str] = Field(min_length=1)


class RetentionJobCreate(BaseModel):
    resource_record_id: str = Field(min_length=1, max_length=240)
    trigger: str = Field(min_length=2, max_length=120)
    trigger_at: str = Field(min_length=10, max_length=64)
    policy_version_id: str = Field(min_length=1, max_length=240)


class ExecutionReceipt(BaseModel):
    adapter: str = Field(min_length=1, max_length=240)
    evidence_ref: str = Field(min_length=1, max_length=500)
    outcome: str = Field(min_length=4, max_length=20)
    details: Dict[str, Any] = Field(default_factory=dict)


class RetryRequest(BaseModel):
    evidence_refs: List[str] = Field(min_length=1)


class ReplayRequest(BaseModel):
    reason: str = Field(min_length=3, max_length=2000)
    evidence_refs: List[str] = Field(min_length=1)


def _translate(exc: Exception):
    if isinstance(exc, LookupError):
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.post("/holds")
async def create_hold(payload: HoldCreate, current: User = Admin):
    try:
        return await retention_executor.create_legal_hold(
            actor_id=current.id, **payload.model_dump()
        )
    except (LookupError, ValueError) as exc:
        _translate(exc)


@router.patch("/holds/{hold_id}/release")
async def release_hold(hold_id: str, payload: HoldRelease, current: User = Admin):
    try:
        return await retention_executor.release_legal_hold(
            actor_id=current.id,
            hold_id=hold_id,
            evidence_refs=payload.evidence_refs,
        )
    except (LookupError, ValueError) as exc:
        _translate(exc)


@router.post("/jobs")
async def create_job(payload: RetentionJobCreate, current: User = Admin):
    try:
        return await retention_executor.schedule_job(
            actor_id=current.id, **payload.model_dump()
        )
    except (LookupError, ValueError) as exc:
        _translate(exc)


@router.get("/jobs/due")
async def due_jobs(limit: int = 200, current: User = Admin):
    return await retention_executor.list_due_jobs(limit=limit)


@router.get("/jobs/{job_id}")
async def get_job(job_id: str, current: User = Admin):
    try:
        return await retention_executor.refresh_job(job_id)
    except LookupError as exc:
        _translate(exc)


@router.post("/jobs/{job_id}/dry-run")
async def dry_run(job_id: str, current: User = Admin):
    try:
        return await retention_executor.dry_run_job(job_id)
    except (LookupError, ValueError) as exc:
        _translate(exc)


@router.post("/jobs/{job_id}/begin")
async def begin_execution(job_id: str, current: User = Admin):
    try:
        return await retention_executor.begin_execution(
            actor_id=current.id, job_id=job_id
        )
    except (LookupError, ValueError) as exc:
        _translate(exc)


@router.post("/jobs/{job_id}/execution")
async def record_execution(
    job_id: str, payload: ExecutionReceipt, current: User = Admin
):
    try:
        return await retention_executor.record_execution(
            actor_id=current.id, job_id=job_id, **payload.model_dump()
        )
    except (LookupError, ValueError) as exc:
        _translate(exc)


@router.post("/jobs/{job_id}/retry")
async def retry_job(job_id: str, payload: RetryRequest, current: User = Admin):
    try:
        return await retention_executor.retry_failed_job(
            actor_id=current.id,
            job_id=job_id,
            evidence_refs=payload.evidence_refs,
        )
    except (LookupError, ValueError) as exc:
        _translate(exc)


@router.post("/jobs/{job_id}/replay")
async def replay_job(job_id: str, payload: ReplayRequest, current: User = Admin):
    try:
        return await retention_executor.replay_verified_job(
            actor_id=current.id,
            job_id=job_id,
            **payload.model_dump(),
        )
    except (LookupError, ValueError) as exc:
        _translate(exc)


@router.get("/execution-gate")
async def execution_gate(current: User = Admin):
    return await retention_executor.execution_gate()
