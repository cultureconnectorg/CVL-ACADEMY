"""CVLN Academy OS — FastAPI entrypoint."""

from __future__ import annotations

import logging
import os

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from db import client, db  # noqa
from routes import router
from seed import seed_if_empty

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
    try:
        await seed_if_empty()
        logger.info("Seed done.")
    except Exception as e:  # noqa: BLE001
        logger.exception("Seed failed: %s", e)


@app.on_event("shutdown")
async def on_shutdown():
    client.close()
