"""Canonical KOR learning progress — a **separate collection**
(`db.kor_canonical_progress`), not a reuse of `db.progress`, for the same
reason `fms_canonical`/`klt_canonical` each keep their own: `db.progress`'s
own unique index is `(user_id, module_code)` — a single global namespace
for module codes. A separate collection makes the coexistence structural
instead of incidental.

Deliberately minimal this pass, same as the other two canonical
packages: `content_viewed_at` is the one real, honest signal recorded.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import List, Optional

from db import db

from .models import KOR_CANONICAL_VERSION_CURRENT, CanonicalKorModuleProgress

COLLECTION = "kor_canonical_progress"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


async def record_content_viewed(
    user_id: str,
    kor_formation_code: str,
    module_code: str,
    *,
    canonical_version: str = KOR_CANONICAL_VERSION_CURRENT,
) -> CanonicalKorModuleProgress:
    now = _now()
    existing = await db[COLLECTION].find_one(
        {"user_id": user_id, "module_code": module_code},
        {"_id": 0},
    )
    if existing and existing.get("content_viewed_at"):
        # Already recorded — idempotent, never overwrite the original
        # timestamp with a later one just because the page was revisited.
        return CanonicalKorModuleProgress(**existing)

    record = CanonicalKorModuleProgress(
        user_id=user_id,
        kor_formation_code=kor_formation_code,
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


async def get_user_kor_progress(
    user_id: str, *, kor_formation_code: Optional[str] = None
) -> List[CanonicalKorModuleProgress]:
    query = {"user_id": user_id}
    if kor_formation_code:
        query["kor_formation_code"] = kor_formation_code
    docs = await db[COLLECTION].find(query, {"_id": 0}).to_list(1000)
    return [CanonicalKorModuleProgress(**d) for d in docs]
