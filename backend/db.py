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

client: AsyncIOMotorClient[Dict[str, Any]] = AsyncIOMotorClient(MONGO_URL)
db = client[DB_NAME]


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


async def close_db():
    client.close()
