"""Canonical Kiltikonet read model. Reads `db.klt_resources` (populated
by `import_pipeline.import_klt_docs`, itself a direct read of the real
`docs/klt/` tree). **Never writes to `db.klt_resources`, `db.formations`,
or `db.progress`.**

`fully_complete` (see `models.py`'s module docstring) is computed here,
live, from the formation's own `skill_id_registry` resource — the one
place in this whole package where that invariant could silently drift
if it were hardcoded instead. It isn't.
"""

from __future__ import annotations

import re
from typing import List, Optional

from db import db

from .models import (KLT_CANONICAL_VERSION_CURRENT, KLT_CONTEXTS,
                     KLT_FORMATION_CODES, CanonicalKltFormation,
                     CanonicalKltModule, CanonicalKltSkill, is_learner_facing)

# KLT-01..05 keep a legacy badge_name (DISPLAY_ONLY_LEGACY, seed_data.py,
# untouched by this package) — KLT-06..08 have none (KLT_0001 §1: no
# legacy trace at all). A real, fixed corpus fact, not a per-import
# guess.
_LEGACY_BADGE_FORMATIONS = frozenset({"KLT-01", "KLT-02", "KLT-03", "KLT-04", "KLT-05"})

_CASE_TITLE_RE = re.compile(r"Cas fil rouge\s*:\s*(.+?)\s*$")


def _friendly_title(referentiel_title: Optional[str]) -> Optional[str]:
    """ "KLT-06 — Analyste Observatory / Cultural Data Analyst —
    Référentiel canonique + Blueprints" -> "Analyste Observatory /
    Cultural Data Analyst" — real heading shape, confirmed across every
    `00_REFERENTIEL_ET_BLUEPRINTS.md`/`00_BLUEPRINTS.md` this session
    wrote or reused."""
    if not referentiel_title:
        return None
    parts = [p.strip() for p in referentiel_title.split("—")]
    # parts[0] is the "KLT-XX" code; the trailing part(s) are
    # "Référentiel canonique..." — the formation name is everything
    # between, joined back with " — " for names that themselves contain
    # an em-dash (none currently do, but this stays correct if one did).
    if len(parts) < 3:
        return parts[-1] if parts else referentiel_title
    return " — ".join(parts[1:-1])


async def _get_referentiel_doc(formation_code: str) -> Optional[dict]:
    return await db.klt_resources.find_one(
        {"type": "referentiel_blueprints", "formation_code": formation_code}
    )


async def get_canonical_klt_formation(
    formation_code: str, *, canonical_version: str = KLT_CANONICAL_VERSION_CURRENT
) -> Optional[CanonicalKltFormation]:
    if formation_code not in KLT_FORMATION_CODES:
        return None

    registry_doc = await db.klt_resources.find_one(
        {"type": "skill_id_registry", "formation_code": formation_code}
    )
    if not registry_doc:
        return None  # this formation hasn't been imported yet

    skill_rows = registry_doc.get("skill_rows", [])
    built_skill_count = sum(1 for r in skill_rows if r.get("status") == "BUILT")
    blocked_skill_ids = [
        r["skill_id"] for r in skill_rows if r.get("status") == "BLOCKED"
    ]
    fully_complete = len(blocked_skill_ids) == 0

    referentiel_doc = await _get_referentiel_doc(formation_code)
    title = (
        _friendly_title(referentiel_doc.get("title"))
        if referentiel_doc
        else formation_code
    ) or formation_code

    module_docs = await db.klt_resources.find(
        {"type": "module", "formation_code": formation_code}
    ).to_list(100)
    ordered_codes = sorted(
        (d["module_code"] for d in module_docs if d.get("module_code")),
        key=lambda code: int(code.rsplit("-M", 1)[-1]),
    )

    case_title = None
    case_doc = await db.klt_resources.find_one(
        {
            "type": {"$in": ["case_fil_rouge", "case_angle"]},
            "formation_code": formation_code,
        }
    )
    if case_doc and case_doc.get("title"):
        m = _CASE_TITLE_RE.search(case_doc["title"])
        if m:
            case_title = m.group(1)

    has_legacy_badge = formation_code in _LEGACY_BADGE_FORMATIONS

    return CanonicalKltFormation(
        klt_formation_code=formation_code,
        title=title,
        canonical_version=canonical_version,
        structural_status="COMPLETE" if fully_complete else "PARTIAL",
        fully_complete=fully_complete,
        blocked_skill_ids=blocked_skill_ids,
        contexts=KLT_CONTEXTS.get(formation_code, []),
        module_codes_in_order=ordered_codes,
        module_count=len(ordered_codes),
        skill_count=len(skill_rows),
        built_skill_count=built_skill_count,
        pedagogical_case_title=case_title,
        has_legacy_badge=has_legacy_badge,
        certification_scope="FULL" if fully_complete else "PARTIAL",
    )


async def list_canonical_klt_formations(
    *, canonical_version: str = KLT_CANONICAL_VERSION_CURRENT
) -> List[CanonicalKltFormation]:
    results = []
    for fc in KLT_FORMATION_CODES:
        formation = await get_canonical_klt_formation(
            fc, canonical_version=canonical_version
        )
        if formation:
            results.append(formation)
    return results


async def get_canonical_klt_module(
    formation_code: str,
    module_code: str,
    *,
    canonical_version: str = KLT_CANONICAL_VERSION_CURRENT,
) -> Optional[CanonicalKltModule]:
    """Learner-safe: only ever returns the module's own body (a `module`
    resource is always learner-facing — see `models.RESOURCE_AUDIENCE`).
    Returns `None` if not found — never a partially-fabricated result."""
    if formation_code not in KLT_FORMATION_CODES:
        return None

    doc = await db.klt_resources.find_one(
        {
            "type": "module",
            "formation_code": formation_code,
            "module_code": module_code,
        }
    )
    if not doc:
        return None

    formation = await get_canonical_klt_formation(
        formation_code, canonical_version=canonical_version
    )
    order_index = (
        formation.module_codes_in_order.index(module_code)
        if formation and module_code in formation.module_codes_in_order
        else 0
    )

    return CanonicalKltModule(
        klt_formation_code=formation_code,
        module_code=module_code,
        canonical_version=canonical_version,
        order_index=order_index,
        title=doc.get("title") or module_code,
        competency_id=doc.get("competency_id"),
        competency_label=doc.get("competency_label"),
        prerequisites_raw=doc.get("prerequisites_raw"),
        assessment_level=doc.get("assessment_level"),
        kiltikonet_dependency=doc.get("kiltikonet_dependency"),
        role_boundaries=doc.get("role_boundaries"),
        frek_proof_mapping=doc.get("frek_proof_mapping"),
        origin=doc.get("origin"),
        content_markdown=(
            doc.get("body_markdown") if is_learner_facing("module") else None
        ),
        content_source_file=doc.get("source_file"),
    )


async def list_canonical_klt_modules(
    formation_code: str, *, canonical_version: str = KLT_CANONICAL_VERSION_CURRENT
) -> List[CanonicalKltModule]:
    formation = await get_canonical_klt_formation(
        formation_code, canonical_version=canonical_version
    )
    if not formation:
        return []
    modules = []
    for code in formation.module_codes_in_order:
        module = await get_canonical_klt_module(
            formation_code, code, canonical_version=canonical_version
        )
        if module:
            modules.append(module)
    return modules


async def list_canonical_klt_skills(
    formation_code: str, *, canonical_version: str = KLT_CANONICAL_VERSION_CURRENT
) -> List[CanonicalKltSkill]:
    if formation_code not in KLT_FORMATION_CODES:
        return []
    registry_doc = await db.klt_resources.find_one(
        {"type": "skill_id_registry", "formation_code": formation_code}
    )
    if not registry_doc:
        return []
    return [
        CanonicalKltSkill(
            skill_id=row["skill_id"],
            klt_formation_code=formation_code,
            label=row["label"],
            module_code=row.get("module_code"),
            status=row["status"],
            blocked_reason=row.get("blocked_reason"),
        )
        for row in registry_doc.get("skill_rows", [])
    ]
