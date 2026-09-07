"""Canonical KORA read model. Reads `db.kor_resources` (populated by
`import_pipeline.import_kor_docs`, itself a direct read of the real
`docs/kor/` tree). **Never writes to `db.kor_resources`, `db.formations`,
or `db.progress`.**

`fully_complete` is computed here, live, never hardcoded — see
`models.py`'s module docstring for why KOR's own corpus gives this
package a different real invariant to check than KLT's BUILT/BLOCKED
column: a formation is `fully_complete` only when its skill registry has
been imported AND every skill row's module reference actually resolves
to a module that was itself imported for that same formation. A skill
row naming a module that isn't there (partial import, or a corpus gap)
makes `fully_complete=False` and lists that skill in
`unresolved_skill_ids` — never silently ignored.
"""

from __future__ import annotations

from typing import List, Optional

from db import db

from .models import (KOR_CANONICAL_VERSION_CURRENT, KOR_CONTEXTS,
                     KOR_FORMATION_CODES, CanonicalKorFormation,
                     CanonicalKorModule, CanonicalKorSkill, is_learner_facing)
from .parser import canonical_module_code


async def _get_referentiel_doc(formation_code: str) -> Optional[dict]:
    return await db.kor_resources.find_one(
        {"type": "referentiel_blueprints", "formation_code": formation_code}
    )


def _friendly_title(referentiel_title: Optional[str], formation_code: str) -> str:
    """ "KOR-01 — Blueprints canoniques (14 modules)" -> "Blueprints
    canoniques (14 modules)" — real heading shape, confirmed against
    `00_BLUEPRINTS.md`. Falls back to the bare formation code when no
    referentiel doc is present or the heading doesn't split cleanly —
    never fabricated."""
    if not referentiel_title:
        return formation_code
    parts = [p.strip() for p in referentiel_title.split("—", 1)]
    return parts[1] if len(parts) == 2 and parts[1] else referentiel_title


async def get_canonical_kor_formation(
    formation_code: str, *, canonical_version: str = KOR_CANONICAL_VERSION_CURRENT
) -> Optional[CanonicalKorFormation]:
    if formation_code not in KOR_FORMATION_CODES:
        return None

    registry_doc = await db.kor_resources.find_one(
        {"type": "skill_id_registry", "formation_code": formation_code}
    )
    if not registry_doc:
        return None  # this formation hasn't been imported yet

    module_docs = await db.kor_resources.find(
        {"type": "module", "formation_code": formation_code}
    ).to_list(100)
    ordered_codes = sorted(
        (d["module_code"] for d in module_docs if d.get("module_code")),
        key=lambda code: int(code.rsplit("-M", 1)[-1]),
    )

    skill_rows = registry_doc.get("skill_rows", [])
    unresolved_skill_ids: List[str] = []
    for row in skill_rows:
        module_code_raw = row.get("module_code_raw")
        resolved = (
            canonical_module_code(formation_code, module_code_raw)
            if module_code_raw
            else None
        )
        if not resolved or resolved not in ordered_codes:
            unresolved_skill_ids.append(row["skill_id"])
    fully_complete = len(skill_rows) > 0 and len(unresolved_skill_ids) == 0

    referentiel_doc = await _get_referentiel_doc(formation_code)
    title = _friendly_title(
        referentiel_doc.get("title") if referentiel_doc else None, formation_code
    )

    case_doc = await db.kor_resources.find_one(
        {"type": "case_fil_rouge", "formation_code": formation_code}
    )
    pedagogical_case_title = None
    if case_doc and case_doc.get("title"):
        # "# KOR-01 — Cas fil rouge : L'Antenne Lanbi — Épisode 0, ..."
        # -> everything after the first "—" (real heading shape,
        # confirmed against docs/kor/kor01/case/CAS_FIL_ROUGE.md).
        _, _, rest = case_doc["title"].partition("—")
        pedagogical_case_title = rest.strip() or None

    return CanonicalKorFormation(
        kor_formation_code=formation_code,
        title=title,
        canonical_version=canonical_version,
        fully_complete=fully_complete,
        unresolved_skill_ids=unresolved_skill_ids,
        contexts=KOR_CONTEXTS.get(formation_code, []),
        module_codes_in_order=ordered_codes,
        module_count=len(ordered_codes),
        skill_count=len(skill_rows),
        pedagogical_case_title=pedagogical_case_title,
        certification_scope="FULL" if fully_complete else "PARTIAL",
    )


async def list_canonical_kor_formations(
    *, canonical_version: str = KOR_CANONICAL_VERSION_CURRENT
) -> List[CanonicalKorFormation]:
    results = []
    for fc in KOR_FORMATION_CODES:
        formation = await get_canonical_kor_formation(
            fc, canonical_version=canonical_version
        )
        if formation:
            results.append(formation)
    return results


async def get_canonical_kor_module(
    formation_code: str,
    module_code: str,
    *,
    canonical_version: str = KOR_CANONICAL_VERSION_CURRENT,
) -> Optional[CanonicalKorModule]:
    """Learner-safe: only ever returns the module's own body (a `module`
    resource is always learner-facing). Returns `None` if not found —
    never a partially-fabricated result."""
    if formation_code not in KOR_FORMATION_CODES:
        return None

    doc = await db.kor_resources.find_one(
        {
            "type": "module",
            "formation_code": formation_code,
            "module_code": module_code,
        }
    )
    if not doc:
        return None

    formation = await get_canonical_kor_formation(
        formation_code, canonical_version=canonical_version
    )
    order_index = (
        formation.module_codes_in_order.index(module_code)
        if formation and module_code in formation.module_codes_in_order
        else 0
    )

    return CanonicalKorModule(
        kor_formation_code=formation_code,
        module_code=module_code,
        canonical_version=canonical_version,
        order_index=order_index,
        title=doc.get("title") or module_code,
        competency_id=doc.get("competency_id"),
        competency_label=doc.get("competency_label"),
        prerequisites_raw=doc.get("prerequisites_raw"),
        prerequisite_module_code=doc.get("prerequisite_module_code"),
        assessment_level=doc.get("assessment_level"),
        kora_dependency=doc.get("kora_dependency"),
        role_boundaries=doc.get("role_boundaries"),
        frek_proof_mapping=doc.get("frek_proof_mapping"),
        origin=doc.get("origin"),
        content_markdown=(
            doc.get("body_markdown") if is_learner_facing("module") else None
        ),
        content_source_file=doc.get("source_file"),
    )


async def list_canonical_kor_modules(
    formation_code: str, *, canonical_version: str = KOR_CANONICAL_VERSION_CURRENT
) -> List[CanonicalKorModule]:
    formation = await get_canonical_kor_formation(
        formation_code, canonical_version=canonical_version
    )
    if not formation:
        return []
    modules = []
    for code in formation.module_codes_in_order:
        module = await get_canonical_kor_module(
            formation_code, code, canonical_version=canonical_version
        )
        if module:
            modules.append(module)
    return modules


async def list_canonical_kor_skills(
    formation_code: str, *, canonical_version: str = KOR_CANONICAL_VERSION_CURRENT
) -> List[CanonicalKorSkill]:
    if formation_code not in KOR_FORMATION_CODES:
        return []
    registry_doc = await db.kor_resources.find_one(
        {"type": "skill_id_registry", "formation_code": formation_code}
    )
    if not registry_doc:
        return []
    skills = []
    for row in registry_doc.get("skill_rows", []):
        module_code_raw = row.get("module_code_raw")
        canonical_code = (
            canonical_module_code(formation_code, module_code_raw)
            if module_code_raw
            else None
        )
        skills.append(
            CanonicalKorSkill(
                skill_id=row["skill_id"],
                kor_formation_code=formation_code,
                label=row["label"],
                module_code_raw=module_code_raw,
                canonical_module_code=canonical_code,
                assessment_ref_raw=row.get("assessment_ref_raw"),
                evidence_expected=row.get("evidence_expected"),
            )
        )
    return skills
