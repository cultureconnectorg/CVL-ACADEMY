"""ACA-0006 — canonical learning progress.

A **separate collection** (`db.canonical_progress`), not a reuse of
`db.progress`, and deliberately so: `db.progress`'s own unique index is
`(user_id, module_code)` — a single global namespace for module codes.
Writing canonical progress there under `FMS01-M01` would be *safe today*
only because that string happens to differ from legacy's `FMS-01-M01` by
one character; a separate collection makes the coexistence structural
instead of incidental, and makes "did this write ever touch
`db.progress`" trivially provable by grep (it doesn't — this file has no
reference to that collection at all).

Deliberately minimal this pass (mission §4): `content_viewed_at` is the
one real, honest signal recorded — the runtime binding report explains
why the legacy 7-phase shape (hook/objectives/course/workshop/
deliverable/quiz/mini_mission) is not force-fit onto canonical content.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import List, Optional

from db import db

from .models import CANONICAL_VERSION_CURRENT, CanonicalModuleProgress

COLLECTION = "canonical_progress"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


async def record_content_viewed(
    user_id: str,
    canonical_formation_code: str,
    canonical_module_code: str,
    *,
    canonical_version: str = CANONICAL_VERSION_CURRENT,
) -> CanonicalModuleProgress:
    now = _now()
    existing = await db[COLLECTION].find_one(
        {"user_id": user_id, "canonical_module_code": canonical_module_code},
        {"_id": 0},
    )
    if existing and existing.get("content_viewed_at"):
        # Already recorded — idempotent, never overwrite the original
        # timestamp with a later one just because the page was revisited.
        return CanonicalModuleProgress(**existing)

    record = CanonicalModuleProgress(
        user_id=user_id,
        canonical_formation_code=canonical_formation_code,
        canonical_module_code=canonical_module_code,
        canonical_version=canonical_version,
        content_viewed_at=now,
        updated_at=now,
    )
    await db[COLLECTION].update_one(
        {"user_id": user_id, "canonical_module_code": canonical_module_code},
        {"$set": record.model_dump()},
        upsert=True,
    )
    return record


async def get_user_canonical_progress(
    user_id: str, *, canonical_formation_code: Optional[str] = None
) -> List[CanonicalModuleProgress]:
    query = {"user_id": user_id}
    if canonical_formation_code:
        query["canonical_formation_code"] = canonical_formation_code
    docs = await db[COLLECTION].find(query, {"_id": 0}).to_list(1000)
    return [CanonicalModuleProgress(**d) for d in docs]
