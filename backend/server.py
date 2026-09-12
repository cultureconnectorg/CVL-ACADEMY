"""CVLN Academy OS — FastAPI entrypoint."""

from __future__ import annotations

from contextlib import asynccontextmanager
import logging
import os

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from api import router
from db import client, db  # noqa
from fms_lineage import seed_initial_matrix
from infra_indexes import ensure_indexes
from mcp_server import academy_mcp, mcp_http_app
from seed import seed_if_empty
from services.integrations.subscribers import (
    register as register_integration_subscribers,
)
from template_engine import seed_default_definitions


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("cvln")


@asynccontextmanager
async def lifespan(app: FastAPI):  # noqa: ARG001
    """Own Academy startup/shutdown and the mounted MCP session manager."""
    register_integration_subscribers()
    try:
        await ensure_indexes()
        await seed_if_empty()
        await seed_default_definitions()
        inserted, skipped = await seed_initial_matrix()
        logger.info(
            "module_lineage initial matrix: %d inserted, %d already present",
            inserted,
            skipped,
        )
        logger.info("Seed done.")
    except Exception as e:  # noqa: BLE001
        logger.exception("Seed failed: %s", e)

    # Mounted ASGI sub-app lifespans are not started by Starlette/FastAPI.
    # MCP requires its session manager to be entered by the host application.
    async with academy_mcp.session_manager.run():
        try:
            yield
        finally:
            client.close()


app = FastAPI(title="CVLN Academy OS", version="0.1", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get("CORS_ORIGINS", "*").split(","),
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Mcp-Session-Id"],
)

app.include_router(router)

# Public Streamable HTTP MCP endpoint. Business data remains read-only here;
# authenticated/private Academy operations stay behind the REST API.
app.mount("/mcp", mcp_http_app)
