"""CVLN Academy OS — FastAPI entrypoint."""

from __future__ import annotations

import logging
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from starlette.middleware.cors import CORSMiddleware

# Side-effect registration only: adds the optional Apps SDK widget/resource to
# the existing vendor-neutral public MCP server.
import apps_sdk  # noqa: E402,F401
from api import router
from api.mcp_oauth import router as mcp_oauth_router
from billing_config import assert_billing_production_ready
from db import client, db  # noqa
from fms_lineage import seed_initial_matrix
from infra_indexes import ensure_indexes
from mcp_indexes import ensure_mcp_indexes
from mcp_private import private_academy_mcp, private_mcp_http_app
import mcp_journey  # noqa: E402,F401
from mcp_server import academy_mcp, mcp_http_app
from seed import seed_if_empty
from services.integrations.subscribers import (
    register as register_integration_subscribers,
)
from services.workbook_runtime import ensure_workbook_runtimes
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

    # This gate intentionally runs outside the seed try/except. Production must
    # not accept paid Academy orders if legal invoice issuance is not configured.
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
        workbook_status = await ensure_workbook_runtimes(db)
        if not workbook_status["all_ready"]:
            raise RuntimeError("workbook runtime reconciliation incomplete")
        logger.info(
            "workbook runtimes ready; imported=%s",
            sorted(workbook_status["imported"]),
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


@app.middleware("http")
async def normalize_duplicate_leading_slashes(request: Request, call_next):
    """Normalize malformed leading // paths before Starlette route matching.

    This is a defensive compatibility layer for stale/browser-cached frontend
    bundles that may temporarily emit URLs such as //api/auth/register. The
    canonical frontend still emits /api/...; this prevents an avoidable 404
    while a deployment catches up without changing route semantics.
    """
    path = request.scope.get("path", "")
    if path.startswith("//"):
        normalized_path = "/" + path.lstrip("/")
        request.scope["path"] = normalized_path

        raw_path = request.scope.get("raw_path")
        if isinstance(raw_path, bytes) and raw_path.startswith(b"//"):
            request.scope["raw_path"] = b"/" + raw_path.lstrip(b"/")

        logger.warning("Normalized duplicate-leading-slash request: %s -> %s", path, normalized_path)

    return await call_next(request)


# 2026-09-14 main<->r35l31 reconciliation: r35l31 independently added a
# production CORS hard-gate that main never had -- ENVIRONMENT=production
# with an unset or wildcard CORS_ORIGINS is a security misconfiguration,
# not a default to silently serve. Restored here; main's own CORS_ORIGINS
# parsing/env var and every other middleware/route below is unchanged.
_ENVIRONMENT = os.environ.get("ENVIRONMENT", "development").strip().lower()
_cors_origins_raw = os.environ.get("CORS_ORIGINS", "*").strip()

if _ENVIRONMENT == "production":
    if not _cors_origins_raw or _cors_origins_raw == "*":
        raise RuntimeError(
            "ENVIRONMENT=production requires a real, explicit CORS_ORIGINS "
            "allowlist (comma-separated origins, e.g. "
            "\"https://academy.cvln.example,https://admin.cvln.example\") — "
            "an unset or wildcard CORS_ORIGINS in production is a security "
            "misconfiguration, not a default to silently fall back to."
        )
    _cors_origins = [o.strip() for o in _cors_origins_raw.split(",") if o.strip()]
else:
    _cors_origins = [o.strip() for o in _cors_origins_raw.split(",") if o.strip()] or ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=_cors_origins,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Mcp-Session-Id", "WWW-Authenticate"],
)

# OAuth discovery/endpoints live at root because MCP clients discover them via
# standardized /.well-known and /oauth URLs.
app.include_router(mcp_oauth_router)
app.include_router(router)

# Mount the more-specific OAuth-protected path first. Starlette Mount routes are
# prefix-based, so mounting /mcp first would swallow /mcp/private.
app.mount("/mcp/private", private_mcp_http_app)

# Existing public Streamable HTTP MCP endpoint: anonymous and read-only.
app.mount("/mcp", mcp_http_app)