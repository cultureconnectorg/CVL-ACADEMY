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

    if os.environ.get("MOCK_DB") == "1":
        # Preview-only, additive: the real docs/kor and docs/klt trees
        # already live unpacked in this repo (no ZIP upload needed,
        # same rationale as their own import pipelines) — auto-import
        # them under MOCK_DB so a live click-through preview shows real
        # canonical content without a manual admin action first. Never
        # runs against a real MongoDB deployment (MOCK_DB is never set
        # there). FMS canonical is intentionally not auto-imported here:
        # it requires an uploaded ZIP this sandbox doesn't have.
        try:
            from kor_canonical.import_pipeline import import_kor_docs
            from klt_canonical.import_pipeline import import_klt_docs

            kor_report = await import_kor_docs()
            klt_report = await import_klt_docs()
            logger.info(
                "MOCK_DB preview import: KOR %s formations, KLT %s formations",
                kor_report.formations_found,
                klt_report.formations_found,
            )
        except Exception as e:  # noqa: BLE001
            logger.exception("MOCK_DB preview canonical import failed: %s", e)


@app.on_event("shutdown")
async def on_shutdown():
    client.close()
