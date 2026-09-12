"""CVLN Academy OS — FastAPI entrypoint."""

from __future__ import annotations

import logging
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from api import router
from api.mcp_oauth import router as mcp_oauth_router
from billing_config import assert_billing_production_ready
from db import client, db  # noqa
from fms_lineage import seed_initial_matrix
from infra_indexes import ensure_indexes
from mcp_indexes import ensure_mcp_indexes
from mcp_private import private_academy_mcp, private_mcp_http_app
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
async def lifespan(app: FastAPI):
    """Own Academy startup/shutdown and both MCP session managers."""
    app.state.startup_ready = False
    app.state.startup_error = None

    billing_status = assert_billing_production_ready()
    logger.info(
        "billing production readiness: required=%s ready=%s environment=%s",
        billing_status["required"],
        billing_status["ready"],
        billing_status["environment"],
    )

    register_integration_subscribers()
    try:
        await ensure_indexes()
        await ensure_mcp_indexes()
        await seed_if_empty()
        await seed_default_definitions()
        inserted, skipped = await seed_initial_matrix()
        logger.info(
            "module_lineage initial matrix: %d inserted, %d already present",
            inserted,
            skipped,
        )
        app.state.startup_ready = True
        logger.info("Seed done; application ready.")
    except Exception as exc:  # noqa: BLE001
        app.state.startup_error = f"{type(exc).__name__}: {exc}"
        logger.exception("Startup initialization failed: %s", exc)

    async with academy_mcp.session_manager.run(), private_academy_mcp.session_manager.run():
        try:
            yield
        finally:
            app.state.startup_ready = False
            client.close()


app = FastAPI(title="CVLN Academy OS", version="0.2", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get("CORS_ORIGINS", "*").split(","),
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Mcp-Session-Id", "WWW-Authenticate"],
)

# OAuth discovery/endpoints live at root because MCP clients discover them via
# standardized /.well-known and /oauth URLs.
app.include_router(mcp_oauth_router)
app.include_router(router)

# Existing public Streamable HTTP MCP endpoint: anonymous and read-only.
app.mount("/mcp", mcp_http_app)

# OAuth-protected MCP endpoint: connected-user data and scoped write actions.
app.mount("/mcp/private", private_mcp_http_app)
