"""P0-G (Audit Chirurgical 2026-09-07) — CAN-01/CAN-02: canonical FMS
convergence.

ROOT_CAUSE this closes: every progression-facing read surface
(`GET /user/learning-path` in api/learning.py, `GET /frek/profile` and
`GET /progression/summary` in api/progression.py) read ONLY
`db.progress` (legacy per-module 7-phase progress) and `db.formations`
(legacy formation/module catalogue). A learner progressing entirely
through canonical content — FMS-canonical, Kiltikonet or KORA, each
with its OWN separate progress collection by design
(`canonical_progress`, `klt_canonical_progress`,
`kor_canonical_progress` — see each domain's own `progress.py`
docstring for why a shared collection was deliberately rejected) — was
invisible on every one of those three surfaces: 0% progression, 0
modules completed, no next action, regardless of how much real work
they had actually done. Three independent truth sources
(legacy + FMS-canonical + KLT-canonical + KOR-canonical, really four)
with no read path that ever looked at more than one of them is exactly
the "split-brain" the audit named.

FIX PRINCIPLE (binding, from the Founder's own directive):
`CURRICULUM_TRUTH = FMS ZIP`; `AUTO_PEDAGOGICAL_EQUIVALENCE = FORBIDDEN`.
This module is strictly ADDITIVE, never a merge or a replacement:
  - Legacy `db.progress`/`db.formations` reads in every caller stay
    byte-for-byte untouched.
  - Canonical progress is surfaced under its own, distinctly-named
    `canonical_*` fields, never folded into the legacy
    `modules_completed`/`completed_modules`/`global_pct` numbers —
    doing that would silently redefine what "completed" means for
    every existing legacy learner too.
  - `content_viewed_at` (canonical's one honest recorded signal today,
    per each domain's own progress.py docstring) is reported as
    *viewed*, never re-labeled *completed*: the legacy "completed"
    flag means quiz-passed + mini-mission-committed, a bar canonical's
    corpus doesn't yet have a mechanism to clear. Calling a viewed
    canonical module "completed" would be exactly the invented
    pedagogical equivalence the Founder's directive forbids.
"""

from __future__ import annotations

from typing import Any, Dict, List

import fms_canonical
import klt_canonical
import kor_canonical


async def _fms_summary(user_id: str) -> List[Dict[str, Any]]:
    formations = await fms_canonical.list_canonical_formations()
    progress = await fms_canonical.get_user_canonical_progress(user_id)
    viewed_by_formation: Dict[str, int] = {}
    for p in progress:
        if p.content_viewed_at:
            viewed_by_formation[p.canonical_formation_code] = (
                viewed_by_formation.get(p.canonical_formation_code, 0) + 1
            )
    return [
        {
            "domain": "FMS",
            "formation_code": f.canonical_formation_code,
            "formation_name": f.metier_name,
            "modules_total": f.module_count,
            "modules_viewed": viewed_by_formation.get(f.canonical_formation_code, 0),
        }
        for f in formations
    ]


async def _klt_summary(user_id: str) -> List[Dict[str, Any]]:
    formations = await klt_canonical.list_canonical_klt_formations()
    progress = await klt_canonical.get_user_klt_progress(user_id)
    viewed_by_formation: Dict[str, int] = {}
    for p in progress:
        if p.content_viewed_at:
            viewed_by_formation[p.klt_formation_code] = (
                viewed_by_formation.get(p.klt_formation_code, 0) + 1
            )
    return [
        {
            "domain": "KLT",
            "formation_code": f.klt_formation_code,
            "formation_name": f.title,
            "modules_total": f.module_count,
            "modules_viewed": viewed_by_formation.get(f.klt_formation_code, 0),
        }
        for f in formations
    ]


async def _kor_summary(user_id: str) -> List[Dict[str, Any]]:
    formations = await kor_canonical.list_canonical_kor_formations()
    progress = await kor_canonical.get_user_kor_progress(user_id)
    viewed_by_formation: Dict[str, int] = {}
    for p in progress:
        if p.content_viewed_at:
            viewed_by_formation[p.kor_formation_code] = (
                viewed_by_formation.get(p.kor_formation_code, 0) + 1
            )
    return [
        {
            "domain": "KOR",
            "formation_code": f.kor_formation_code,
            "formation_name": f.title,
            "modules_total": f.module_count,
            "modules_viewed": viewed_by_formation.get(f.kor_formation_code, 0),
        }
        for f in formations
    ]


async def get_canonical_progress_summary(user_id: str) -> Dict[str, Any]:
    """One converged, read-only view across all three canonical
    domains (FMS/KLT/KOR) for `user_id` — additive to, never replacing,
    the legacy view built from `db.progress`/`db.formations`.

    Every domain read here already runs in production today (the same
    `list_canonical_*_formations()`/`get_user_*_progress()` functions
    back `api/canonical.py`, `api/klt_canonical.py`, `api/kor_canonical.py`
    directly) — this is a convergence of existing, already-correct
    reads, not a new query surface.
    """
    fms, klt, kor = (
        await _fms_summary(user_id),
        await _klt_summary(user_id),
        await _kor_summary(user_id),
    )
    formations = fms + klt + kor
    modules_total = sum(f["modules_total"] for f in formations)
    modules_viewed = sum(f["modules_viewed"] for f in formations)
    return {
        "canonical_formations": formations,
        "canonical_modules_total": modules_total,
        "canonical_modules_viewed": modules_viewed,
        "canonical_progress_pct": (
            int((modules_viewed / modules_total) * 100) if modules_total else 0
        ),
    }
