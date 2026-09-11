"""Health / service-status endpoint."""

from __future__ import annotations

from fastapi import APIRouter

from services.agent_factory import agent_factory
from services.frek_core import frek_core

router = APIRouter(tags=["health"])


@router.get("/")
async def root():
    return {
        "app": "CVLN Academy OS",
        "version": "0.1",
        "frek_core_remote": frek_core.is_remote_enabled(),
        "frek_core_identity_authority": frek_core.identity_authority(),
        "frek_core_sovereign_identity": frek_core.is_sovereign_identity_enabled(),
        "agent_factory_remote": agent_factory.is_remote_enabled(),
    }
