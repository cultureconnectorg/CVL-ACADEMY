"""MongoDB connection + shared helpers."""

import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict

from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / ".env")

MONGO_URL = os.environ["MONGO_URL"]
DB_NAME = os.environ["DB_NAME"]

if os.environ.get("MOCK_DB") == "1":
    # Preview/dev-only fallback — this sandbox has no outbound network
    # path to install or reach a real mongod (egress policy blocks both
    # the Docker Hub `mongo` image and the official MongoDB tarball), so
    # a real Motor connection can never be established here. `mongomock_
    # motor.AsyncMongoMockClient` implements the same async Motor API
    # surface already exercised by every test in `backend/tests/` — this
    # just wires the *app* to that same in-memory client instead of only
    # test fixtures, so the real FastAPI app + real frontend can be run
    # and clicked through for a live preview. In-memory, non-persistent
    # (data is lost on restart), never used unless this exact env var is
    # set — every other code path (including every existing test) is
    # untouched.
    from mongomock_motor import AsyncMongoMockClient

    client = AsyncMongoMockClient()
else:
    client: AsyncIOMotorClient[Dict[str, Any]] = AsyncIOMotorClient(MONGO_URL)
db = client[DB_NAME]


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


async def close_db():
    client.close()
