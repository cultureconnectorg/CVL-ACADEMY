"""CVLN Academy OS — FastAPI entrypoint."""

from __future__ import annotations

import logging
import os

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from api import router
from db import client, db  # noqa
from fms_lineage import seed_initial_matrix
from infra_indexes import ensure_indexes
from seed import seed_if_empty
from services.integrations.subscribers import (
    register as register_integration_subscribers,
)
from template_engine import seed_default_definitions

app = FastAPI(title="CVLN Academy OS", version="0.1")
app.state.startup_ready = False
app.state.startup_error = None

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get("CORS_ORIGINS", "*").split(","),
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("cvln")


@app.on_event("startup")
async def on_startup():
    app.state.startup_ready = False
    app.state.startup_error = None
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
        app.state.startup_ready = True
        logger.info("Seed done; application ready.")
    except Exception as exc:  # noqa: BLE001
        app.state.startup_error = f"{type(exc).__name__}: {exc}"
        logger.exception("Startup initialization failed: %s", exc)


@app.on_event("shutdown")
async def on_shutdown():
    app.state.startup_ready = False
    client.close()
