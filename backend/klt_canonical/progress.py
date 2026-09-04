"""Canonical KLT learning progress — a separate collection
(`db.klt_canonical_progress`), same rationale as `fms_canonical/
progress.py`: never shares `db.progress`'s own `(user_id, module_code)`
namespace. Deliberately minimal: `content_viewed_at` is the one real
signal recorded this pass.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import List, Optional

from db import db

from .models import KLT_CANONICAL_VERSION_CURRENT, CanonicalKltModuleProgress

COLLECTION = "klt_canonical_progress"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


async def record_klt_content_viewed(
    user_id: str,
    klt_formation_code: str,
    module_code: str,
    *,
    canonical_version: str = KLT_CANONICAL_VERSION_CURRENT,
) -> CanonicalKltModuleProgress:
    now = _now()
    existing = await db[COLLECTION].find_one(
        {"user_id": user_id, "module_code": module_code}, {"_id": 0}
    )
    if existing and existing.get("content_viewed_at"):
        return CanonicalKltModuleProgress(**existing)

    record = CanonicalKltModuleProgress(
        user_id=user_id,
        klt_formation_code=klt_formation_code,
        module_code=module_code,
        canonical_version=canonical_version,
        content_viewed_at=now,
        updated_at=now,
    )
    await db[COLLECTION].update_one(
        {"user_id": user_id, "module_code": module_code},
        {"$set": record.model_dump()},
        upsert=True,
    )
    return record


async def get_user_klt_progress(
    user_id: str, *, klt_formation_code: Optional[str] = None
) -> List[CanonicalKltModuleProgress]:
    query = {"user_id": user_id}
    if klt_formation_code:
        query["klt_formation_code"] = klt_formation_code
    docs = await db[COLLECTION].find(query, {"_id": 0}).to_list(1000)
    return [CanonicalKltModuleProgress(**d) for d in docs]
