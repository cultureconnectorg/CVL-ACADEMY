"""Canonical KORA (KOR) runtime models — RAIL 2, "MASTER -> RUNTIME
ACADEMY" (Founder instruction, 2026-09-06), same non-destructive pattern
already proven for FMS (`fms_canonical/`, ACA-0006) and Kiltikonet
(`klt_canonical/`, "branchage complet de Kiltikonet").

**Source of truth**: `docs/kor/kor01/` — already-unpacked Markdown, not a
ZIP upload (same situation as Kiltikonet). The import pipeline scans
that directory tree directly on the server filesystem; see
`import_pipeline.py`.

**Why this package is named `kor_canonical`, not the more generic
`master_canonical` the Rail 2 brief's own prose uses**: the brief's
"Master pédagogique" names the *docs corpus as a whole* (FMS + KLT + KOR
+ every other domain closed in Rail 1), but this pass only binds one
domain into the runtime — the existing precedent (`fms_canonical`,
`klt_canonical`) is domain-prefixed, one package per corpus, and this
package follows that precedent rather than claiming a scope it doesn't
cover. See `docs/cvln_academy_master/RAIL2_MASTER_RUNTIME_INTEGRATION.md`
for the full scoping decision.

**Real discrepancy found and deliberately not resolved by this ticket**:
`docs/kor/README.md` states `KOR-03`..`KOR-15` are `NEW_CANONICAL_TARGET`
/ `CURRICULUM_BUILT = FALSE` ("aucun module, aucun référentiel... écrit
pour elles"), yet real module/skill-registry files exist on disk under
`docs/kor/kor03/` (and others) at the time of this Rail 2 pass — content
that post-dates that README (consistent with the Founder's later "812
objects" closure instruction, which is out of scope for this file to
adjudicate). This package does not trust either claim silently: it
imports whatever real files exist per formation and derives
`fully_complete` from what the registry itself says (see
`read_model.py`), exactly the same discipline `klt_canonical` already
applies. Only `KOR-01` has been driven end-to-end through this runtime
binding this pass — see the architecture doc for the explicit
per-formation status this pass actually verified vs. left unverified.
"""

from __future__ import annotations

from typing import List, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field

from canonical_common.audience import Audience
from canonical_common.audience import is_learner_facing as _is_learner_facing
from canonical_common.audience import learner_facing_types
from canonical_common.audience import resource_audience as _resource_audience

KOR_CANONICAL_VERSION_CURRENT = "KOR_20260906_V1"

# The 15 formations frozen by KOR-0001 (`docs/KORA_KOR0001_CANONICAL_
# EDUCATION_MAP.md`) — never derived from a directory listing count,
# always this explicit, real list, exactly like FMS's
# CANONICAL_FORMATION_CODES and Kiltikonet's KLT_FORMATION_CODES.
KOR_FORMATION_CODES: List[str] = [
    "KOR-01",
    "KOR-02",
    "KOR-03",
    "KOR-04",
    "KOR-05",
    "KOR-06",
    "KOR-07",
    "KOR-08",
    "KOR-09",
    "KOR-10",
    "KOR-11",
    "KOR-12",
    "KOR-13",
    "KOR-14",
    "KOR-15",
]

# Per-formation INTERNAL/EXTERNAL/BRIDGE contexts — deliberately empty.
# Unlike Kiltikonet (whose KLT_CONTEXTS could be read off a real,
# already-decided source — legacy catalog_cartography.py for KLT-01/02/
# 04/05, KLT-0008 for KLT-06/07/08), no equivalent reconciliation ticket
# has ever fixed KOR's contexts: the legacy `seed_data.py` KOR-01/KOR-02
# entries carry no `contexts` field at all (grep-confirmed), and neither
# KOR-0001 nor KOR-0002 assigns one. Left UNRESOLVED here rather than
# guessed — same discipline KLT-03 already set precedent for.
KOR_CONTEXTS: dict = {}

# ---------------------------------------------------------------------
# Resource classification — mirrors klt_canonical/models.py's
# RESOURCE_AUDIENCE discipline.
# ---------------------------------------------------------------------

# `Audience` now lives in `canonical_common.audience` — reused, not
# redefined (see that module's docstring for why).

RESOURCE_AUDIENCE: dict = {
    "module": ["LEARNER"],
    "case_fil_rouge": ["LEARNER"],
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
}


def resource_audience(resource_type: str) -> List[Audience]:
    return _resource_audience(RESOURCE_AUDIENCE, resource_type)


def is_learner_facing(resource_type: str) -> bool:
    return _is_learner_facing(RESOURCE_AUDIENCE, resource_type)


LEARNER_FACING_TYPES: frozenset = learner_facing_types(RESOURCE_AUDIENCE)


# ---------------------------------------------------------------------
# Skill / competency
# ---------------------------------------------------------------------


class CanonicalKorSkill(BaseModel):
    model_config = ConfigDict(extra="ignore")

    skill_id: str  # e.g. "KOR01.SKILL.C04"
    kor_formation_code: str
    label: str
    module_code_raw: Optional[str] = None  # bare, as the registry writes it: "M04"
    canonical_module_code: Optional[str] = None  # derived: "KOR01-M04"
    assessment_ref_raw: Optional[str] = None  # e.g. "N2 (`E-N2-02`)"
    evidence_expected: Optional[str] = None
    # KOR's registry format carries no per-skill BUILT/BLOCKED status
    # column (unlike KLT-06/07/08) — every parsed row is structurally
    # "BUILT" by the corpus's own vocabulary. Kept as a real Literal
    # (not just a display string) so a future formation that does add
    # such a column needs no model change, only a parser change.
    status: Literal["BUILT", "BLOCKED"] = "BUILT"


# ---------------------------------------------------------------------
# Module / Formation read model
# ---------------------------------------------------------------------


class CanonicalKorModule(BaseModel):
    model_config = ConfigDict(extra="ignore")

    kor_formation_code: str
    module_code: str  # e.g. "KOR01-M04"
    canonical_version: str = KOR_CANONICAL_VERSION_CURRENT

    order_index: int
    title: str
    competency_id: Optional[str] = None
    competency_label: Optional[str] = None
    prerequisites_raw: Optional[str] = None  # "Aucun" | "M03" — real corpus text
    # Derived from prerequisites_raw + this module's own formation code —
    # None both for "Aucun" and for free text this parser doesn't
    # recognize (never guessed, see parser.py::resolve_prerequisite_
    # module_code).
    prerequisite_module_code: Optional[str] = None
    assessment_level: Optional[str] = None
    kora_dependency: Optional[str] = None
    role_boundaries: Optional[str] = None
    frek_proof_mapping: Optional[str] = None
    origin: Optional[str] = None

    # Learner-safe content only.
    content_markdown: Optional[str] = None
    content_source_file: Optional[str] = None


class CanonicalKorFormation(BaseModel):
    model_config = ConfigDict(extra="ignore")

    kor_formation_code: str  # "KOR-01"
    title: str
    canonical_version: str = KOR_CANONICAL_VERSION_CURRENT
    pedagogical_source: Literal["CANONICAL_KOR"] = "CANONICAL_KOR"

    # Derived, never hardcoded — see read_model.py. True only when this
    # formation's own SKILL_ID_REGISTRY.md has been imported AND every
    # skill row's module reference resolves to a real imported module
    # (the one real invariant KOR's corpus lets this package check,
    # since it carries no BUILT/BLOCKED column to read instead).
    fully_complete: bool
    unresolved_skill_ids: List[str] = Field(default_factory=list)

    contexts: List[str] = Field(default_factory=list)

    module_codes_in_order: List[str] = Field(default_factory=list)
    module_count: int = 0
    skill_count: int = 0

    pedagogical_case_title: Optional[str] = None
    certification_scope: Literal["FULL", "PARTIAL"] = "FULL"


# ---------------------------------------------------------------------
# Progress — separate collection, same rationale as fms_canonical's and
# klt_canonical's progress.py (a distinct namespace from db.progress's
# own (user_id, module_code) unique index).
# ---------------------------------------------------------------------


class CanonicalKorModuleProgress(BaseModel):
    model_config = ConfigDict(extra="ignore")

    user_id: str
    kor_formation_code: str
    module_code: str
    canonical_version: str = KOR_CANONICAL_VERSION_CURRENT

    content_viewed_at: Optional[str] = None
    updated_at: Optional[str] = None


# ---------------------------------------------------------------------
# File-level provenance — every real file under docs/kor/, parsed or
# not, individually accounted for. Same discipline as fms_canonical's
# FileProvenance / klt_canonical's KltFileProvenance.
# ---------------------------------------------------------------------

ParsingStatus = Literal["parsed", "unparsed_no_type_match", "unparsed_error"]


class KorFileProvenance(BaseModel):
    model_config = ConfigDict(extra="ignore")

    original_path: str  # relative to docs/kor/, e.g. "kor01/modules/M01_....md"
    original_filename: str
    sha256: str
    byte_size: int

    resource_type: Optional[str] = None
    formation_code: Optional[str] = None
    module_number: Optional[str] = None
    audience: List[Audience] = Field(default_factory=list)

    canonical_version: str = KOR_CANONICAL_VERSION_CURRENT
    parsing_status: ParsingStatus
    parsing_note: Optional[str] = None

    imported_at: Optional[str] = None


class KorCanonicalImportResult(BaseModel):
    model_config = ConfigDict(extra="ignore")

    import_id: str
    docs_dir: str
    total_files: int
    parsed_count: int
    unparsed_count: int
    formations_found: List[str] = Field(default_factory=list)
    all_files_accounted_for: bool
