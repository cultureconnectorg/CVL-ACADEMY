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

from typing import Any, Dict, List, Optional

import fms_canonical
import frk_canonical
import klt_canonical
import kor_canonical

# CANONICAL_CURRICULUM_RUNTIME = AUTHORITATIVE (Founder decision,
# ACA-0019, 2026-09-07) — the one place the "which of three frontend
# route prefixes" knowledge lives. Every caller (formations catalogue,
# formation detail, module journey, next_action, Dashboard) asks this
# module instead of re-deriving it, so the three prefixes can never
# drift apart across call sites.
CANONICAL_ROUTE_PREFIX: Dict[str, str] = {
    "FMS": "/canonical",
    "KLT": "/kiltikonet-canonical",
    "KOR": "/kora-canonical",
    "FRK": "/frek-canonical",
}


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
            "route": f"{CANONICAL_ROUTE_PREFIX['FMS']}/{f.canonical_formation_code}",
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
            "route": f"{CANONICAL_ROUTE_PREFIX['KLT']}/{f.klt_formation_code}",
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
            "route": f"{CANONICAL_ROUTE_PREFIX['KOR']}/{f.kor_formation_code}",
        }
        for f in formations
    ]


async def _frk_summary(user_id: str) -> List[Dict[str, Any]]:
    formations = await frk_canonical.list_canonical_frk_formations()
    progress = await frk_canonical.get_user_frk_progress(user_id)
    viewed_by_formation: Dict[str, int] = {}
    for p in progress:
        if p.content_viewed_at:
            viewed_by_formation[p.frk_formation_code] = (
                viewed_by_formation.get(p.frk_formation_code, 0) + 1
            )
    return [
        {
            "domain": "FRK",
            "formation_code": f.frk_formation_code,
            "formation_name": f.title,
            "modules_total": f.module_count,
            "modules_viewed": viewed_by_formation.get(f.frk_formation_code, 0),
            "route": f"{CANONICAL_ROUTE_PREFIX['FRK']}/{f.frk_formation_code}",
        }
        for f in formations
    ]


async def get_canonical_authority_map() -> Dict[str, Dict[str, str]]:
    """CANONICAL_CURRICULUM_RUNTIME = AUTHORITATIVE (Founder decision,
    ACA-0019, 2026-09-07) — every real canonical formation_code across
    all three domains, mapped to `{domain, route}`. For any
    formation_code present here, the canonical route is now THE single
    active pedagogical source a learner is routed to; legacy content at
    the same code (`db.formations`/`db.progress`) is never deleted,
    never auto-merged, never auto-credited — it stays real,
    queryable READ_ONLY_HISTORY, simply no longer where navigation
    points. A formation_code absent from this map has no canonical
    counterpart yet and keeps using the existing legacy runtime
    unchanged, exactly as before this decision.

    Deliberately progress-free (unlike `get_canonical_progress_summary`
    above) — routing authority never depends on any one user's
    progress, so this is cheap to call from request paths that don't
    otherwise need a user's canonical progress (the formations
    catalogue, formation detail).
    """
    fms = await fms_canonical.list_canonical_formations()
    klt = await klt_canonical.list_canonical_klt_formations()
    kor = await kor_canonical.list_canonical_kor_formations()
    result: Dict[str, Dict[str, str]] = {}
    for f in fms:
        result[f.canonical_formation_code] = {
            "domain": "FMS",
            "route": f"{CANONICAL_ROUTE_PREFIX['FMS']}/{f.canonical_formation_code}",
        }
    for klt_f in klt:
        result[klt_f.klt_formation_code] = {
            "domain": "KLT",
            "route": f"{CANONICAL_ROUTE_PREFIX['KLT']}/{klt_f.klt_formation_code}",
        }
    for kor_f in kor:
        result[kor_f.kor_formation_code] = {
            "domain": "KOR",
            "route": f"{CANONICAL_ROUTE_PREFIX['KOR']}/{kor_f.kor_formation_code}",
        }
    return result


async def get_canonical_authority(formation_code: str) -> Optional[Dict[str, str]]:
    """Single-formation convenience wrapper over
    `get_canonical_authority_map` — for call sites (e.g. one formation's
    detail page) that only need one code, not the full map."""
    return (await get_canonical_authority_map()).get(formation_code)


async def _first_unviewed_fms(user_id: str) -> Any:
    formations = await fms_canonical.list_canonical_formations()
    progress = await fms_canonical.get_user_canonical_progress(user_id)
    viewed = {p.canonical_module_code for p in progress if p.content_viewed_at}
    for f in formations:
        for module_code in f.module_codes_in_order:
            if module_code not in viewed:
                module = await fms_canonical.get_canonical_module(
                    f.canonical_formation_code, module_code
                )
                return {
                    "domain": "FMS",
                    "formation_code": f.canonical_formation_code,
                    "formation_name": f.metier_name,
                    "module_code": module_code,
                    "module_name": module.title if module else module_code,
                    "route": f"{CANONICAL_ROUTE_PREFIX['FMS']}/{f.canonical_formation_code}/{module_code}",
                }
    return None


async def _first_unviewed_klt(user_id: str) -> Any:
    formations = await klt_canonical.list_canonical_klt_formations()
    progress = await klt_canonical.get_user_klt_progress(user_id)
    viewed = {p.module_code for p in progress if p.content_viewed_at}
    for f in formations:
        for module_code in f.module_codes_in_order:
            if module_code not in viewed:
                module = await klt_canonical.get_canonical_klt_module(
                    f.klt_formation_code, module_code
                )
                return {
                    "domain": "KLT",
                    "formation_code": f.klt_formation_code,
                    "formation_name": f.title,
                    "module_code": module_code,
                    "module_name": module.title if module else module_code,
                    "route": f"{CANONICAL_ROUTE_PREFIX['KLT']}/{f.klt_formation_code}/{module_code}",
                }
    return None


async def _first_unviewed_kor(user_id: str) -> Any:
    formations = await kor_canonical.list_canonical_kor_formations()
    progress = await kor_canonical.get_user_kor_progress(user_id)
    viewed = {p.module_code for p in progress if p.content_viewed_at}
    for f in formations:
        for module_code in f.module_codes_in_order:
            if module_code not in viewed:
                module = await kor_canonical.get_canonical_kor_module(
                    f.kor_formation_code, module_code
                )
                return {
                    "domain": "KOR",
                    "formation_code": f.kor_formation_code,
                    "formation_name": f.title,
                    "module_code": module_code,
                    "module_name": module.title if module else module_code,
                    "route": f"{CANONICAL_ROUTE_PREFIX['KOR']}/{f.kor_formation_code}/{module_code}",
                }
    return None


async def _first_unviewed_frk(user_id: str) -> Any:
    formations = await frk_canonical.list_canonical_frk_formations()
    progress = await frk_canonical.get_user_frk_progress(user_id)
    viewed = {p.module_code for p in progress if p.content_viewed_at}
    for f in formations:
        for module_code in f.module_codes_in_order:
            if module_code not in viewed:
                module = await frk_canonical.get_canonical_frk_module(
                    f.frk_formation_code, module_code
                )
                return {
                    "domain": "FRK",
                    "formation_code": f.frk_formation_code,
                    "formation_name": f.title,
                    "module_code": module_code,
                    "module_name": module.title if module else module_code,
                    "route": f"{CANONICAL_ROUTE_PREFIX['FRK']}/{f.frk_formation_code}/{module_code}",
                }
    return None


async def get_first_unviewed_canonical_module(user_id: str) -> Any:
    """CONVERGENCE_RUNTIME — the canonical equivalent of legacy's
    `next_action` in `GET /user/learning-path`. Tried FMS, then KLT,
    then KOR, then FRK, in that order (mirrors `check_certification_
    eligibility`'s own domain-precedence in `certification/service.py`;
    FRK tried last — added after the other three were already the
    established precedence, and never meant to preempt them for an
    existing learner mid-way through one of them); returns the first
    canonical module across the four domains this user hasn't yet
    viewed, or `None` if every domain is either exhausted or has no
    content imported at all. Deliberately a real, precomputed `route`
    string rather than a bare formation/module code pair — the four
    canonical domains live under four different frontend route
    prefixes (`/canonical`, `/kiltikonet-canonical`, `/kora-canonical`,
    `/frek-canonical`), unlike legacy's single `/formations/:code/
    modules/:code` — a caller building the URL itself would have to
    already know which domain produced the result, exactly the kind of
    split-brain knowledge this convergence module exists to keep out of
    every caller.
    """
    for finder in (
        _first_unviewed_fms,
        _first_unviewed_klt,
        _first_unviewed_kor,
        _first_unviewed_frk,
    ):
        result = await finder(user_id)
        if result:
            return result
    return None


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
    fms, klt, kor, frk = (
        await _fms_summary(user_id),
        await _klt_summary(user_id),
        await _kor_summary(user_id),
        await _frk_summary(user_id),
    )
    formations = fms + klt + kor + frk
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
