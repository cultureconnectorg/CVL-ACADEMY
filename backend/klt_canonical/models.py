"""Canonical Kiltikonet runtime models — "branchage complet de
Kiltikonet" (Founder authorization, 2026-09-04, following the exact
non-destructive pattern already used and proven for FMS in
`fms_canonical/` — ACA-0006).

**Source of truth**: `docs/klt/klt01/` through `docs/klt/klt08/` —
already-unpacked Markdown, not a ZIP upload (unlike FMS). The import
pipeline scans that directory tree directly on the server filesystem;
see `import_pipeline.py`.

**The one invariant this whole package exists to enforce structurally,
not just assert in prose** (Founder, 2026-09-04: "on ne doit pas
déclarer KLT-06/07/08 FULLY_COMPLETE" tant que leurs compétences
bloquées ne sont pas réellement connectées) — `CanonicalKltFormation.
fully_complete` is **derived at import time from each formation's own
`skills/SKILL_ID_REGISTRY.md`**, never hardcoded: a formation is
`fully_complete=True` only if every skill row in that real file carries
no `BLOCKED` status. KLT-01→05's registries have no status column at
all (5 columns, every skill built) — `fully_complete=True` for those.
KLT-06/07/08's registries have an explicit 6th status column with real
`BLOCKED` rows — `fully_complete=False` for those, and stays False
until a future re-import finds the registry rewritten with no more
`BLOCKED` rows (which itself only happens when a human writes that
content after a real Observatory/Network/Compliance connection exists —
this package never manufactures that).
"""

from __future__ import annotations

from typing import List, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field

KLT_CANONICAL_VERSION_CURRENT = "KLT_20260904_V1"

# The 8 formations named in KLT_MASTER_MAP_v1 (docs/KILTIKONET_KLT0001_
# CANONICAL_EDUCATION_MAP.md §2) — never derived from a directory listing
# count, always this explicit, real list, exactly like FMS's
# CANONICAL_FORMATION_CODES.
KLT_FORMATION_CODES: List[str] = [
    "KLT-01",
    "KLT-02",
    "KLT-03",
    "KLT-04",
    "KLT-05",
    "KLT-06",
    "KLT-07",
    "KLT-08",
]

# Real per-formation contexts, decided by KLT-0008 (docs/KILTIKONET_
# KLT0008_KLT06_08_CONTEXT_AND_SCOPE_DECISION.md) for KLT-06/07/08, and
# read from legacy catalog_cartography.py's own `contexts` field
# (KLT-0001 §3) for KLT-01/02/04/05 — KLT-03's canonical contexts were
# never resolved (KLT-0001 §3 leaves them `UNRESOLVED`, inherited
# pending confirmation), so it is intentionally absent here rather than
# guessed.
KLT_CONTEXTS: dict = {
    "KLT-01": ["EXTERNAL", "BRIDGE"],
    "KLT-02": ["EXTERNAL", "BRIDGE"],
    "KLT-04": ["EXTERNAL", "BRIDGE"],
    "KLT-05": ["INTERNAL", "BRIDGE"],
    "KLT-06": ["EXTERNAL"],
    "KLT-07": ["INTERNAL"],
    "KLT-08": ["INTERNAL"],
}

StructuralStatus = Literal["COMPLETE", "PARTIAL"]

# ---------------------------------------------------------------------
# Resource classification — mirrors fms_canonical/models.py's
# RESOURCE_AUDIENCE discipline: a learner must only ever receive
# genuinely learner-facing content by default.
# ---------------------------------------------------------------------

Audience = Literal["LEARNER", "TRAINER", "CORRECTOR", "JURY", "ADMIN", "INTERNAL"]

RESOURCE_AUDIENCE: dict = {
    "module": ["LEARNER"],
    "case_fil_rouge": ["LEARNER"],
    "case_angle": ["LEARNER"],
    "templates": ["LEARNER"],
    "candidate_guide": ["LEARNER"],
    "corrector_guide": ["CORRECTOR"],
    "jury_guide": ["JURY"],
    "n1_question_bank": ["CORRECTOR", "JURY"],
    "n2_evaluations": ["CORRECTOR", "JURY"],
    "certification_assessment": ["CORRECTOR", "JURY"],
    "rubric": ["CORRECTOR", "JURY", "ADMIN"],
    "referentiel_blueprints": ["TRAINER", "ADMIN", "INTERNAL"],
    "case_competency_matrix": ["TRAINER", "ADMIN", "INTERNAL"],
    "skill_id_registry": ["ADMIN", "INTERNAL"],
    "evidence_model": ["ADMIN", "INTERNAL"],
    "certification_model": ["ADMIN", "INTERNAL"],
    "integration_note": ["ADMIN", "INTERNAL"],
    "quality_gates": ["ADMIN", "INTERNAL"],
    "modules_status": ["ADMIN", "INTERNAL"],
}


def resource_audience(resource_type: str) -> List[Audience]:
    return RESOURCE_AUDIENCE.get(resource_type, ["ADMIN", "INTERNAL"])


def is_learner_facing(resource_type: str) -> bool:
    return "LEARNER" in resource_audience(resource_type)


LEARNER_FACING_TYPES: frozenset = frozenset(
    t for t, aud in RESOURCE_AUDIENCE.items() if "LEARNER" in aud
)


# ---------------------------------------------------------------------
# Skill / competency status — the derived-not-hardcoded FULLY_COMPLETE
# machinery.
# ---------------------------------------------------------------------

SkillStatus = Literal["BUILT", "BLOCKED"]


class CanonicalKltSkill(BaseModel):
    model_config = ConfigDict(extra="ignore")

    skill_id: str  # e.g. "KLT06.SKILL.C05"
    klt_formation_code: str
    label: str
    module_code: Optional[str] = None
    status: SkillStatus
    blocked_reason: Optional[str] = None  # real text after "BLOCKED —" when present


# ---------------------------------------------------------------------
# Module / Formation read model
# ---------------------------------------------------------------------


class CanonicalKltModule(BaseModel):
    model_config = ConfigDict(extra="ignore")

    klt_formation_code: str
    module_code: str  # e.g. "KLT06-M01"
    canonical_version: str = KLT_CANONICAL_VERSION_CURRENT

    order_index: int
    title: str
    competency_id: Optional[str] = None
    competency_label: Optional[str] = None
    prerequisites_raw: Optional[str] = None
    assessment_level: Optional[str] = None
    kiltikonet_dependency: Optional[str] = None
    role_boundaries: Optional[str] = None
    frek_proof_mapping: Optional[str] = None
    origin: Optional[str] = None

    # Learner-safe content only.
    content_markdown: Optional[str] = None
    content_source_file: Optional[str] = None


class CanonicalKltFormation(BaseModel):
    model_config = ConfigDict(extra="ignore")

    klt_formation_code: str  # "KLT-06"
    title: str
    canonical_version: str = KLT_CANONICAL_VERSION_CURRENT
    pedagogical_source: Literal["CANONICAL_KLT"] = "CANONICAL_KLT"

    structural_status: StructuralStatus
    # Derived, never hardcoded — see module docstring. False until the
    # underlying SKILL_ID_REGISTRY.md, on a future re-import, carries no
    # more BLOCKED rows.
    fully_complete: bool
    blocked_skill_ids: List[str] = Field(default_factory=list)

    contexts: List[str] = Field(default_factory=list)

    module_codes_in_order: List[str] = Field(default_factory=list)
    module_count: int = 0
    skill_count: int = 0
    built_skill_count: int = 0

    pedagogical_case_title: Optional[str] = None

    # Real, honest — never a real credential (see docs/klt/kltXX/
    # CERTIFICATION_MODEL.md). KLT-01→05 carry a legacy badge_name kept
    # DISPLAY_ONLY_LEGACY (not read here — that lives in seed_data.py,
    # untouched); KLT-06→08 have none at all.
    has_legacy_badge: bool = False
    certification_scope: Literal["FULL", "PARTIAL"] = "FULL"


# ---------------------------------------------------------------------
# Progress — separate collection, same rationale as fms_canonical/
# progress.py (a distinct namespace from db.progress's own
# (user_id, module_code) unique index).
# ---------------------------------------------------------------------


class CanonicalKltModuleProgress(BaseModel):
    model_config = ConfigDict(extra="ignore")

    user_id: str
    klt_formation_code: str
    module_code: str
    canonical_version: str = KLT_CANONICAL_VERSION_CURRENT

    content_viewed_at: Optional[str] = None
    updated_at: Optional[str] = None


# ---------------------------------------------------------------------
# File-level provenance — every real file under docs/klt/, parsed or
# not, individually accounted for. Same discipline as fms_canonical's
# FileProvenance (Founder's blocking correction on FMS, 2026-09-03),
# applied proactively here rather than after a similar correction.
# ---------------------------------------------------------------------

ParsingStatus = Literal["parsed", "unparsed_no_type_match", "unparsed_error"]


class KltFileProvenance(BaseModel):
    model_config = ConfigDict(extra="ignore")

    original_path: str  # relative to docs/klt/, e.g. "klt06/modules/M01_....md"
    original_filename: str
    sha256: str
    byte_size: int

    resource_type: Optional[str] = None
    formation_code: Optional[str] = None
    module_number: Optional[str] = None
    audience: List[Audience] = Field(default_factory=list)

    canonical_version: str = KLT_CANONICAL_VERSION_CURRENT
    parsing_status: ParsingStatus
    parsing_note: Optional[str] = None

    imported_at: Optional[str] = None


class KltCanonicalImportResult(BaseModel):
    model_config = ConfigDict(extra="ignore")

    import_id: str
    docs_dir: str
    total_files: int
    parsed_count: int
    unparsed_count: int
    formations_found: List[str] = Field(default_factory=list)
    all_files_accounted_for: bool
