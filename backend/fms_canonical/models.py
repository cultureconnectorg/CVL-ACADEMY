"""ACA-0006 — Canonical FMS runtime models.

**Real, audit-driven finding this package exists to correct**
(`docs/ACADEMY_FMS_CANONICAL_RUNTIME_BINDING_REPORT.md` §1): the existing
`fms_import` pipeline (built and validated before `ACA-0003`/`ACA-0005`
established the true canonical code convention) already normalizes a
canonical module's `db.fms_resources.code` to the **legacy-shaped**
`FMS-01-M01` (dashed) — `fms_import/models.py`'s own docstring says so
explicitly ("module code: FMS01_M07 -> FMS-01-M07 (dashed, gabarit
table)"). That field is therefore **not** this package's canonical
module identity — using it as one would silently reproduce the exact
collision `ACA-0005` was built to prevent. This package derives the true
canonical code (`FMS01-M01`, no dash — confirmed against
`fms_import/module_map.py`'s own `**ID**` regex and every real
`Master_Module_Map.md`) independently, and matches a `db.fms_resources`
document to it by `(formation_code, module_number)` extracted from the
resource's own `source_file`/body — never by trusting `.code`.

Nothing in this package renames, rewrites, or upserts over
`db.fms_resources.code` — that field, and the pipeline that produces it,
are read-only inputs here, untouched.
"""

from __future__ import annotations

from typing import Dict, List, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field

# The one archive this runtime binding was built and verified against
# (DEC-002). A future archive gets a new version string; nothing here
# assumes there will only ever be one.
CANONICAL_VERSION_CURRENT = "FMS_20260822_V1"

# ---------------------------------------------------------------------
# Resource classification — a student must never receive correction/jury
# material by accident (mission §3), refined per the Founder's blocking
# correction into the real 6-tier audience taxonomy (§ "audience" of
# docs/ACADEMY_FMS_CANONICAL_RUNTIME_BINDING_REPORT.md) rather than a
# learner/staff binary — a resource visible to correctors is not
# automatically visible to a learner just because both are "not staff
# generically", and some resources genuinely serve more than one role
# (e.g. a grading grille is used by both CORRECTOR and JURY).
# `is_learner_facing` below stays as a derived, backward-compatible
# helper — never leaked by default.
# ---------------------------------------------------------------------

Audience = Literal["LEARNER", "TRAINER", "CORRECTOR", "JURY", "ADMIN", "INTERNAL"]

# Every real type from `fms_import/models.py`'s own `FmsResourceType` —
# confirmed exhaustively against `docs/FMS_IMPORT_VALIDATION_REPORT.md`'s
# 26-type table and this session's own full-archive parse (0 unrecognized
# files, see the runtime binding report §"ZIP accounting"). A type not in
# this map (should never happen for a real archive, but a future one
# could add one) is treated as `["ADMIN", "INTERNAL"]` only — the
# conservative fail-safe default, never `LEARNER`.
RESOURCE_AUDIENCE: Dict[str, List[Audience]] = {
    # Real lesson content and materials a learner is meant to see directly.
    "module": ["LEARNER"],  # the actual lesson ("Contenu_Complet")
    "cas_fil_rouge": ["LEARNER"],  # the continuing case the learner works through
    "templates_etudiants": ["LEARNER"],  # blank templates the learner fills in
    "guide_candidat": ["LEARNER"],  # candidate-facing orientation guide
    # Trainer delivery material.
    "blueprint": ["TRAINER"],  # pedagogical *design* contract, not the lesson itself
    "guide_formateur": ["TRAINER"],
    # Correction material.
    "guide_correcteur": ["CORRECTOR"],
    "banque_n1": ["CORRECTOR", "JURY"],  # QCM bank — leaking it to learners defeats N1
    "banque_n2": ["CORRECTOR", "JURY"],
    # Certification/exam material — jury-administered, correctors grade too.
    "cas_inedit": ["CORRECTOR", "JURY"],  # exam case, must never leak before the exam
    "sujet_officiel": ["JURY"],  # exam subject, handed out exam-day only
    "grille_certificative": ["CORRECTOR", "JURY"],
    "guide_jury": ["JURY"],
    # Curriculum architecture / internal governance — trainers may
    # reasonably consult these for context; never learner-facing.
    "referentiel": ["TRAINER", "ADMIN", "INTERNAL"],
    "learning_map": ["TRAINER", "ADMIN", "INTERNAL"],
    "module_map": ["TRAINER", "ADMIN", "INTERNAL"],
    "competency_matrix": ["TRAINER", "ADMIN", "INTERNAL"],
    "matrice_tracabilite": ["ADMIN", "INTERNAL"],
    "infrastructure": ["ADMIN", "INTERNAL"],
    "evidence_registry": ["ADMIN", "INTERNAL"],
    "skill_ids_registry": ["ADMIN", "INTERNAL"],
    "rubric_master": ["CORRECTOR", "JURY", "ADMIN"],
    "note_harmonisation": ["CORRECTOR", "ADMIN"],
    # Archive governance — internal only.
    "index": ["ADMIN", "INTERNAL"],
    "gabarit": ["ADMIN", "INTERNAL"],
    "matrice_pedagogique": ["ADMIN", "INTERNAL"],
    "guide": ["ADMIN", "INTERNAL"],  # unclassified fallback — internal until reviewed
}

# Backward-compatible derived sets (used by read_model.py's learner-safe
# content lookup) — computed from RESOURCE_AUDIENCE, never maintained
# separately, so the two can't drift apart.
LEARNER_FACING_TYPES: frozenset = frozenset(
    t for t, aud in RESOURCE_AUDIENCE.items() if "LEARNER" in aud
)
STAFF_ONLY_TYPES: frozenset = frozenset(
    t for t, aud in RESOURCE_AUDIENCE.items() if "LEARNER" not in aud
)


def resource_audience(resource_type: str) -> List[Audience]:
    """Fail-safe: an unrecognized type gets the most restrictive default
    (`ADMIN`+`INTERNAL`), never `LEARNER`."""
    return RESOURCE_AUDIENCE.get(resource_type, ["ADMIN", "INTERNAL"])


def is_learner_facing(resource_type: str) -> bool:
    """Fail-safe: an unrecognized type is treated as staff-only, never
    leaked by default."""
    return "LEARNER" in resource_audience(resource_type)


# ---------------------------------------------------------------------
# Prerequisites — mission §8: never invent a lock where the source is
# silent.
# ---------------------------------------------------------------------

PrerequisiteStatus = Literal["DEFINED", "NONE", "UNSPECIFIED"]


class CanonicalPrerequisites(BaseModel):
    model_config = ConfigDict(extra="ignore")

    status: PrerequisiteStatus
    # Full canonical module codes (e.g. "FMS01-M03"), only populated when
    # status == DEFINED.
    required_module_codes: List[str] = Field(default_factory=list)


# ---------------------------------------------------------------------
# Module / Formation read model
# ---------------------------------------------------------------------


class CanonicalAssessmentRefs(BaseModel):
    """What kind of assessment this module textually references — real,
    extracted metadata (mission §10's N1/N2/N3 distinction), not an
    interactive quiz engine. See the runtime binding report §4 for why
    this stays metadata-only in this pass."""

    model_config = ConfigDict(extra="ignore")

    n1_reference: Optional[str] = None  # e.g. "QCM de 10 questions sur..."
    n2_reference: Optional[str] = None
    n3_reference: Optional[str] = None  # "Préparation N3" / certification prep note


class CanonicalModule(BaseModel):
    model_config = ConfigDict(extra="ignore")

    canonical_formation_code: (
        str  # "FMS-01" (métier family — see §7 of the report re: FMS-01 collision)
    )
    canonical_module_code: str  # "FMS01-M01" — no dash, the true canonical identity
    canonical_version: str = CANONICAL_VERSION_CURRENT

    order_index: int  # 0-based position in the Master Module Map
    title: str
    bloc_competence: Optional[str] = None
    niveau_progression: Optional[str] = None

    prerequisites: CanonicalPrerequisites

    skill_ids: List[str] = Field(default_factory=list)
    assessment: CanonicalAssessmentRefs = Field(default_factory=CanonicalAssessmentRefs)

    # Learner-safe content only — never a staff-only resource's body.
    content_markdown: Optional[str] = None
    content_source_file: Optional[str] = None


class CanonicalFormation(BaseModel):
    model_config = ConfigDict(extra="ignore")

    canonical_formation_code: str  # "FMS-01"
    metier_number: str  # "01".."06"
    metier_name: str  # from the référentiel title, e.g. "Artist Development"
    canonical_version: str = CANONICAL_VERSION_CURRENT
    pedagogical_source: Literal["CANONICAL"] = "CANONICAL"

    module_codes_in_order: List[str] = Field(
        default_factory=list
    )  # canonical codes, ordered
    module_count: int = 0

    # Real, when the formation's own cas_fil_rouge resource names one
    # (e.g. "Anaïs Solaine") — from that resource's own title, never
    # invented. None if no cas_fil_rouge resource is present.
    pedagogical_case_title: Optional[str] = None

    # Real, honest reporting of what's actually available for this métier
    # — not every métier's archive carries the same 21 file types
    # (docs/ACADEMY_FMS_CANONICAL_DELTA_MATRIX.md §3).
    has_dedicated_skill_registry: bool = False
    has_infrastructure_doc: bool = False


class CanonicalSkillDefinition(BaseModel):
    """A registered skill definition — mission §9:
    `REGISTER_SKILL_DEFINITION = ALLOWED`, but nothing in this model or
    anywhere in this package ever credits a skill to a user."""

    model_config = ConfigDict(extra="ignore")

    skill_id: (
        str  # e.g. "FMS01-A1" — matches skills/models.py's existing Skill.id format
    )
    canonical_formation_code: str
    canonical_version: str = CANONICAL_VERSION_CURRENT

    # Rich metadata only where the source genuinely provides it
    # (skill_ids_registry exists for FMS-01/02/03 only — see the delta
    # matrix §3). FMS-04/05/06 skills are registered with just the ID,
    # sourced from real inline mentions across their own resources
    # (`fms_resources.skill_ids`, already extracted by `fms_import`'s own
    # `extract_skill_ids` — reused, not reinvented).
    label: Optional[str] = None
    bloc: Optional[str] = None
    is_eliminatory: Optional[bool] = None
    source: Literal["skill_ids_registry", "inline_extraction"] = "inline_extraction"


# ---------------------------------------------------------------------
# Canonical progress — mission §6: a separate collection so legacy
# db.progress's own (user_id, module_code) unique index is never at risk
# of a cross-namespace collision, by construction, not by convention.
# ---------------------------------------------------------------------


class CanonicalModuleProgress(BaseModel):
    """A learner's real progress on one canonical module. Deliberately
    minimal this pass (mission §4: don't force the canonical corpus into
    the legacy 7-phase shape) — `content_viewed_at` is the one honest
    signal this pass records; see the runtime binding report for what's
    REPRESENTABLE vs NOT_REPRESENTABLE and left for a future pass."""

    model_config = ConfigDict(extra="ignore")

    user_id: str
    canonical_formation_code: str
    canonical_module_code: str
    canonical_version: str = CANONICAL_VERSION_CURRENT

    content_viewed_at: Optional[str] = None
    updated_at: Optional[str] = None


# ---------------------------------------------------------------------
# Source-file provenance — Founder correction: every entry the ZIP
# contains must be individually accounted for, including one this
# session's classifier cannot yet interpret. A file the parser doesn't
# recognize still gets a provenance record (`parsing_status =
# "unparsed_no_type_match"`) — it is never silently dropped. See
# `provenance.py` for the exhaustive, read-only inventory this backs.
# ---------------------------------------------------------------------

ParsingStatus = Literal["parsed", "unparsed_no_type_match", "unparsed_error"]


class FileProvenance(BaseModel):
    """One real ZIP entry, independent of whether the classifier could
    interpret it. `sha256`/`byte_size` are computed directly off the raw
    bytes inside the archive — this is how "which source file produced
    which Academy data" stays provable without re-opening the ZIP."""

    model_config = ConfigDict(extra="ignore")

    original_path: str  # full path inside the archive, e.g. "FMS_Chantier_Complet/14_FMS01_M01_Contenu_Complet.md"
    original_filename: str  # basename only
    sha256: str
    byte_size: int

    resource_type: Optional[str] = None  # None only when parsing_status != "parsed"
    formation_code: Optional[str] = None
    module_number: Optional[str] = None  # "M01" when applicable, else None
    audience: List[Audience] = Field(default_factory=list)

    canonical_version: str = CANONICAL_VERSION_CURRENT
    parsing_status: ParsingStatus
    parsing_note: Optional[str] = None

    imported_at: Optional[str] = None


class CanonicalImportResult(BaseModel):
    """`POST /canonical/import`'s response — pairs the existing
    `fms_import.ImportReport` (resource-level: what got persisted to
    `db.fms_resources`) with the full, independent file-level accounting
    (`ALL_ZIP_FILES_ACCOUNTED_FOR`) so a caller never has to infer one
    from the other."""

    model_config = ConfigDict(extra="ignore")

    import_id: str
    zip_total_files: int
    parsed_count: int
    unparsed_count: int
    provenance_inserted: int
    provenance_updated: int
    all_zip_files_accounted_for: bool
