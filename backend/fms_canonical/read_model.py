"""ACA-0006 — canonical FMS read model.

Reads `db.fms_resources` (populated by the existing, untouched
`fms_import` pipeline) and assembles the structured
`CanonicalFormation`/`CanonicalModule`/`CanonicalSkillDefinition` views
this runtime binding is built on. **Never writes to `db.fms_resources`,
`db.formations`, or `db.progress`.**

See `fms_canonical/models.py`'s module docstring for why a module's
identity here (`canonical_module_code`, e.g. `FMS01-M01`) is derived
independently rather than read off `fms_resources.code` (which the
existing importer already normalizes to the legacy-shaped `FMS-01-M01`).
The module number itself is extracted from each resource's own
`source_file` using the exact same regex `fms_import/parser.py` already
uses internally to build that field (`MODULE_NUM_RE`) — reused, not
reinvented, so this stays a read-only, independent cross-check rather
than a second implementation that could drift from the first.
"""

from __future__ import annotations

import re
from typing import Dict, List, Optional

from db import db
from fms_import.parser import MODULE_NUM_RE

from .models import (
    CANONICAL_VERSION_CURRENT,
    CanonicalAssessmentRefs,
    CanonicalFormation,
    CanonicalModule,
    CanonicalPrerequisites,
    CanonicalSkillDefinition,
    is_learner_facing,
)
from .module_map_extract import extract_module_map_entries

# A genuine Skill ID is always a single digit after its bloc letter
# (confirmed against every real Skill IDs Registry read this session:
# FMS01-A1..F1, FMS02-A1..F1, etc.) — this excludes the false positives
# fms_import's own broader SKILL_ID_RE lets through (a métier's
# certification code, e.g. "FMS01-A01", 2 digits).
_SKILL_ID_SHAPE_RE = re.compile(r"^FMS\d{2}-[A-F]\d$")

# The six locked canonical métiers (FMS_BOUNDARIES_LOCKED) — never
# derived from a count, always this explicit, real list.
CANONICAL_FORMATION_CODES: List[str] = [
    "FMS-01",
    "FMS-02",
    "FMS-03",
    "FMS-04",
    "FMS-05",
    "FMS-06",
]


def _module_number_from_source_file(source_file: str) -> Optional[str]:
    m = MODULE_NUM_RE.search(source_file)
    return f"M{m.group(1)}" if m else None


def _canonical_module_code(formation_code: str, module_number: str) -> str:
    """`FMS-01`, "M01" -> `FMS01-M01` — the true canonical convention
    (no dash after the métier number), confirmed against every real
    Master Module Map's own `**ID**` field this session."""
    metier_no = formation_code.split("-")[-1]
    return f"FMS{metier_no}-M{module_number[1:]}"


def _metier_name_from_referentiel(title: str) -> str:
    """`# FMS — MÉTIER A : ARTIST DEVELOPMENT` -> `Artist Development`
    (real heading shape, confirmed against `01_FMS-A_Referentiel_...md`)."""
    name = title.rsplit(":", 1)[1].strip() if ":" in title else title.strip()
    return name.title() if name.isupper() else name


async def get_canonical_formation(
    formation_code: str, *, canonical_version: str = CANONICAL_VERSION_CURRENT
) -> Optional[CanonicalFormation]:
    if formation_code not in CANONICAL_FORMATION_CODES:
        return None

    module_map_doc = await db.fms_resources.find_one(
        {"type": "module_map", "formation_code": formation_code}
    )
    if not module_map_doc:
        return None  # this métier's canonical content hasn't been imported

    entries = extract_module_map_entries(module_map_doc.get("body_markdown", ""))
    # Order modules exactly as the Module Map's own module-number sequence
    # — never re-sorted or re-derived some other way.
    ordered_numbers = sorted(entries.keys(), key=lambda n: int(n[1:]))
    module_codes = [_canonical_module_code(formation_code, n) for n in ordered_numbers]

    referentiel_doc = await db.fms_resources.find_one(
        {"type": "referentiel", "formation_code": formation_code}
    )
    metier_name = (
        _metier_name_from_referentiel(referentiel_doc["title"])
        if referentiel_doc
        else formation_code
    )

    cas_fil_rouge_doc = await db.fms_resources.find_one(
        {"type": "cas_fil_rouge", "formation_code": formation_code}
    )
    pedagogical_case_title = None
    if cas_fil_rouge_doc:
        # Only FMS-01's filename names the case (Cas_Fil_Rouge_Anais_Solaine);
        # FMS-02..06 use a plain "Cas_Fil_Rouge.md" — real asymmetry, not
        # papered over (see docs/ACADEMY_FMS_CANONICAL_DELTA_MATRIX.md).
        stem = cas_fil_rouge_doc.get("source_file", "").rsplit("/", 1)[-1]
        stem = stem[: -len(".md")] if stem.lower().endswith(".md") else stem
        prefix = "Cas_Fil_Rouge_"
        if prefix in stem:
            name_part = stem.split(prefix, 1)[1]
            pedagogical_case_title = name_part.replace("_", " ").strip() or None

    has_dedicated_skill_registry = (
        await db.fms_resources.count_documents(
            {"type": "skill_ids_registry", "formation_code": formation_code}
        )
        > 0
    )
    has_infrastructure_doc = (
        await db.fms_resources.count_documents(
            {"type": "infrastructure", "formation_code": formation_code}
        )
        > 0
    )

    return CanonicalFormation(
        canonical_formation_code=formation_code,
        metier_number=formation_code.split("-")[-1],
        metier_name=metier_name,
        canonical_version=canonical_version,
        module_codes_in_order=module_codes,
        module_count=len(module_codes),
        pedagogical_case_title=pedagogical_case_title,
        has_dedicated_skill_registry=has_dedicated_skill_registry,
        has_infrastructure_doc=has_infrastructure_doc,
    )


async def list_canonical_formations(
    *,
    canonical_version: str = CANONICAL_VERSION_CURRENT,
) -> List[CanonicalFormation]:
    results = []
    for fc in CANONICAL_FORMATION_CODES:
        formation = await get_canonical_formation(
            fc, canonical_version=canonical_version
        )
        if formation:
            results.append(formation)
    return results


async def get_canonical_module(
    formation_code: str,
    module_code: str,
    *,
    canonical_version: str = CANONICAL_VERSION_CURRENT,
) -> Optional[CanonicalModule]:
    """Learner-safe: only ever returns content from
    `LEARNER_FACING_TYPES` resources. Returns `None` if the module isn't
    found — never a partially-fabricated result."""
    if formation_code not in CANONICAL_FORMATION_CODES:
        return None

    module_map_doc = await db.fms_resources.find_one(
        {"type": "module_map", "formation_code": formation_code}
    )
    if not module_map_doc:
        return None
    entries = extract_module_map_entries(module_map_doc.get("body_markdown", ""))
    ordered_numbers = sorted(entries.keys(), key=lambda n: int(n[1:]))

    target_number = None
    for n in ordered_numbers:
        if _canonical_module_code(formation_code, n) == module_code:
            target_number = n
            break
    if target_number is None:
        return None

    entry = entries[target_number]
    order_index = ordered_numbers.index(target_number)

    # Prerequisites: canonical codes, never bare "M03" tokens.
    if entry.prerequisite_status == "DEFINED":
        prereq = CanonicalPrerequisites(
            status="DEFINED",
            required_module_codes=[
                _canonical_module_code(formation_code, m)
                for m in entry.prerequisite_modules
            ],
        )
    else:
        prereq = CanonicalPrerequisites(status=entry.prerequisite_status)

    # Learner-facing content: only a real `module` (Contenu_Complet)
    # resource for this exact module number, matched via source_file —
    # never via the legacy-shaped `.code` field (see module docstring).
    content_markdown = None
    content_source_file = None
    skill_ids: List[str] = []
    async for doc in db.fms_resources.find(
        {"type": "module", "formation_code": formation_code}
    ):
        source_file = doc.get("source_file", "")
        if _module_number_from_source_file(source_file) == target_number:
            if is_learner_facing(doc.get("type", "")):
                content_markdown = doc.get("body_markdown")
                content_source_file = source_file
            skill_ids = doc.get("skill_ids", [])
            break

    return CanonicalModule(
        canonical_formation_code=formation_code,
        canonical_module_code=module_code,
        canonical_version=canonical_version,
        order_index=order_index,
        title=entry.title or module_code,
        bloc_competence=entry.bloc,
        niveau_progression=entry.niveau,
        prerequisites=prereq,
        skill_ids=skill_ids,
        assessment=CanonicalAssessmentRefs(
            n1_reference=entry.n1_reference,
            n2_reference=entry.n2_reference,
            n3_reference=entry.n3_reference,
        ),
        content_markdown=content_markdown,
        content_source_file=content_source_file,
    )


async def list_canonical_modules(
    formation_code: str, *, canonical_version: str = CANONICAL_VERSION_CURRENT
) -> List[CanonicalModule]:
    formation = await get_canonical_formation(
        formation_code, canonical_version=canonical_version
    )
    if not formation:
        return []
    modules = []
    for code in formation.module_codes_in_order:
        module = await get_canonical_module(
            formation_code, code, canonical_version=canonical_version
        )
        if module:
            modules.append(module)
    return modules


async def list_canonical_skill_definitions(
    formation_code: str, *, canonical_version: str = CANONICAL_VERSION_CURRENT
) -> List[CanonicalSkillDefinition]:
    """Mission §9: `REGISTER_SKILL_DEFINITION = ALLOWED`. Deterministic
    extraction only — every distinct Skill ID already indexed by
    `fms_import`'s own `extract_skill_ids` (`fms_resources.skill_ids`) is
    unioned across every resource for this formation. Never credits a
    skill to any user — this is a catalogue read, not a progress write."""
    if formation_code not in CANONICAL_FORMATION_CODES:
        return []

    metier_no = formation_code.split("-")[-1]
    own_prefix = f"FMS{metier_no}-"

    seen: Dict[str, CanonicalSkillDefinition] = {}
    async for doc in db.fms_resources.find({"formation_code": formation_code}):
        for skill_id in doc.get("skill_ids", []):
            if not skill_id.startswith(own_prefix):
                # A cross-métier mention (e.g. FMS-02's content discussing
                # a frontier or the continuing case's prior FMS-01 step
                # names an FMS-01 Skill ID) — real text, but not this
                # formation's own skill catalogue. Confirmed present in
                # the real archive this session (FMS-02's own resources
                # cite FMS01-B2/C1/E1/F1) — excluded deliberately, not a
                # guess.
                continue
            if not _SKILL_ID_SHAPE_RE.match(skill_id):
                # fms_import/parser.py's own SKILL_ID_RE (\bFMS0\d-[A-F]\d+\b)
                # over-matches a métier's certification code (e.g.
                # "FMS01-A01") as if its "A01" were a skill number under
                # bloc A — confirmed against every real Skill IDs
                # Registry this session read: every genuine skill number
                # is exactly one digit (A1..F4 range), never two.
                # fms_import itself is untouched; this filter is local to
                # the canonical read model's own registration step.
                continue
            if skill_id not in seen:
                seen[skill_id] = CanonicalSkillDefinition(
                    skill_id=skill_id,
                    canonical_formation_code=formation_code,
                    canonical_version=canonical_version,
                    source="inline_extraction",
                )

    # Richer metadata where a dedicated registry exists (FMS-01/02/03 —
    # see docs/ACADEMY_FMS_CANONICAL_DELTA_MATRIX.md §3). Table rows in
    # that file are real Markdown; only the ID itself is trusted enough
    # to reconcile against `seen` — label/bloc extraction from that
    # table's free-form prose is left for a future pass rather than
    # risking a wrong field-to-ID pairing here.
    registry_doc = await db.fms_resources.find_one(
        {"type": "skill_ids_registry", "formation_code": formation_code}
    )
    if registry_doc:
        for skill_id in registry_doc.get("skill_ids", []):
            if skill_id in seen:
                seen[skill_id].source = "skill_ids_registry"

    return sorted(seen.values(), key=lambda s: s.skill_id)
