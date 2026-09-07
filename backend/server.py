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

# OPS-02 (Audit Chirurgical 2026-09-07) — a wildcard CORS_ORIGINS with
# allow_credentials=True let ANY site make credentialed (cookie/
# Authorization-header) requests against this API. The previous version
# defaulted straight to "*" with no distinction between a local/preview
# checkout (where that convenience is fine and expected — zero .env
# config to get a fresh clone running) and a real production
# deployment (where it is a real, silent security misconfiguration).
# ENVIRONMENT defaults to "development" so every existing checkout that
# never set it keeps booting exactly as before; only ENVIRONMENT=
# production changes behavior, and it fails CLOSED (raises at import,
# same fail-closed philosophy as ensure_indexes() in on_startup() below
# and the same pattern db.py already uses for its own required env
# vars) rather than silently falling back to a wildcard.
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

    # OPS-01 (Audit Chirurgical 2026-09-07) — fail CLOSED, not open.
    # ensure_indexes() creates every unique/partial index this session's
    # atomicity fixes actually depend on for their real guarantee
    # (wallet-ledger idempotency, badge dedup, physical-enrollment
    # dedup, FMS provenance dedup, ...). The previous version wrapped
    # this in the same broad try/except as the seed calls below, so an
    # index that failed to create (a conflicting pre-existing document,
    # a transient Mongo error) logged an exception and let the app boot
    # anyway — serving real traffic with none of those DB-enforced
    # guarantees in place, while every code path that assumes them
    # (DuplicateKeyError handlers, CAS filters) would misbehave in ways
    # invisible until the exact race they exist to prevent actually
    # happens. Left unguarded here on purpose: FastAPI/uvicorn treats an
    # exception raised from a startup event as a hard boot failure —
    # exactly what an orchestrator's health/readiness check should see
    # instead of a silently degraded instance.
    await ensure_indexes()

    # Seed data (catalogue/demo content, template definitions, the
    # module-lineage matrix) is NOT a correctness/security invariant —
    # a failure here means some optional content is missing, never that
    # a guarantee this app makes to a user is broken. Deliberately still
    # best-effort/logged-not-fatal, unlike ensure_indexes() above.
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
