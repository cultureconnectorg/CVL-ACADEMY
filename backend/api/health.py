"""Health, liveness and readiness endpoints."""

from __future__ import annotations

from fastapi import APIRouter, Request, status
from fastapi.responses import JSONResponse

from db import db
from services.agent_factory import agent_factory
from services.frek_core import frek_core

router = APIRouter(tags=["health"])


@router.get("/")
async def root():
    return {
        "app": "CVLN Academy OS",
        "version": "0.1",
        "frek_core_remote": frek_core.is_remote_enabled(),
        "agent_factory_remote": agent_factory.is_remote_enabled(),
    }


@router.get("/health/live")
async def live():
    """Process-level liveness probe; does not depend on external systems."""
    return {"status": "alive"}


@router.get("/health/ready")
async def ready(request: Request):
    """Readiness probe requiring startup initialization and MongoDB connectivity."""
    startup_ready = bool(getattr(request.app.state, "startup_ready", False))
    startup_failed = bool(getattr(request.app.state, "startup_error", None))

    mongo_ready = False
    try:
        await db.command("ping")
        mongo_ready = True
    except Exception:  # noqa: BLE001
        # Do not expose database exception details on a public probe.
        pass

    payload = {
        "status": "ready" if startup_ready and mongo_ready else "not_ready",
        "startup_ready": startup_ready,
        "startup_failed": startup_failed,
        "mongo_ready": mongo_ready,
        "frek_core_remote": frek_core.is_remote_enabled(),
        "agent_factory_remote": agent_factory.is_remote_enabled(),
    }

    if not (startup_ready and mongo_ready):
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content=payload,
        )
    return payload
