"""NVIDIA accelerator observability and controlled runtime self-test."""

from __future__ import annotations

import time

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from auth import require_role
from models import User
from services.nvidia_runtime import (
    accelerated_group_count,
    accelerated_runtime_status,
    public_accelerator_status,
)

router = APIRouter(prefix="/accelerators", tags=["accelerators"])


class AcceleratorSelfTestInput(BaseModel):
    rows: int = Field(default=100_000, ge=1, le=1_000_000)
    require_gpu: bool = False


@router.get("/status")
async def accelerator_status():
    """Public coarse status; never returns API keys or full host details."""
    return public_accelerator_status()


@router.get("/diagnostics")
async def accelerator_diagnostics(
    current: User = Depends(require_role("admin", "super_admin", "founder")),
):
    """Operator diagnostics with hardware/software evidence."""
    del current
    return accelerated_runtime_status()


@router.post("/self-test")
async def accelerator_self_test(
    inp: AcceleratorSelfTestInput,
    current: User = Depends(require_role("admin", "super_admin", "founder")),
):
    """Execute a bounded group-by path and report the engine actually used.

    ``require_gpu=true`` is deliberately fail-closed. It is the runtime proof
    endpoint operators can use on a GPU host to demonstrate that the request
    reached cuDF instead of the CPU fallback.
    """
    del current
    records = ({"bucket": index % 17, "value": index} for index in range(inp.rows))
    started = time.perf_counter()
    counts, engine, fallback_reason = accelerated_group_count(
        records,
        "bucket",
        min_rows=0 if inp.require_gpu else None,
        require_gpu=inp.require_gpu,
    )
    elapsed_ms = (time.perf_counter() - started) * 1000

    return {
        "rows": inp.rows,
        "engine": engine,
        "fallback_reason": fallback_reason,
        "checksum": sum(counts.values()),
        "bucket_count": len(counts),
        "elapsed_ms": round(elapsed_ms, 3),
        "verified": sum(counts.values()) == inp.rows,
    }
