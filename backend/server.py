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
from services import architecture_reuse
from services.integrations.subscribers import (
    register as register_integration_subscribers,
)
from template_engine import seed_default_definitions

app = FastAPI(title="CVLN Academy OS", version="0.1")

ENVIRONMENT = os.environ.get("ENVIRONMENT", "development").strip().lower()
_cors_origins_raw = os.environ.get("CORS_ORIGINS", "*").strip()

if ENVIRONMENT == "production":
    if not _cors_origins_raw or _cors_origins_raw == "*":
        raise RuntimeError(
            "ENVIRONMENT=production requires a real, explicit CORS_ORIGINS "
            "allowlist (comma-separated origins, e.g. "
            "\"https://academy.cvln.example,https://admin.cvln.example\") — "
            "an unset or wildcard CORS_ORIGINS in production is a security "
            "misconfiguration, not a default to silently fall back to."
        )
    cors_origins = [o.strip() for o in _cors_origins_raw.split(",") if o.strip()]
else:
    cors_origins = [o.strip() for o in _cors_origins_raw.split(",") if o.strip()] or ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=cors_origins,
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
    register_integration_subscribers()

    # Correctness/security invariants fail closed. Database indexes and the locked
    # PG-13 reuse manifest are part of the runtime contract, not best-effort demo data.
    await ensure_indexes()
    manifest = await architecture_reuse.sync_manifest(actor_id="SYSTEM_STARTUP")
    if manifest.get("status") != "LOCKED":
        raise RuntimeError("PG-13 deduplication manifest failed to lock")

    # Seed/demo/catalogue data is best effort and does not weaken correctness gates.
    try:
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

    if os.environ.get("MOCK_DB") == "1":
        try:
            from kor_canonical.import_pipeline import import_kor_docs
            from klt_canonical.import_pipeline import import_klt_docs
            from frk_canonical.import_pipeline import import_frk_docs

            kor_report = await import_kor_docs()
            klt_report = await import_klt_docs()
            frk_report = await import_frk_docs()
            logger.info(
                "MOCK_DB preview import: KOR %s formations, KLT %s formations, "
                "FRK %s formations",
                kor_report.formations_found,
                klt_report.formations_found,
                frk_report.formations_found,
            )
        except Exception as e:  # noqa: BLE001
            logger.exception("MOCK_DB preview canonical import failed: %s", e)


@app.on_event("shutdown")
async def on_shutdown():
    client.close()
