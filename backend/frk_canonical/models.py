"""Canonical FREK (FRK) runtime models — Rail "MASTER -> RUNTIME
ACADEMY" continuation (Founder instruction, 2026-09-07: "raccorder ces
corpus au même runtime/funnel Academy"), same non-destructive,
domain-prefixed pattern already proven for FMS (`fms_canonical/`),
Kiltikonet (`klt_canonical/`) and KORA (`kor_canonical/`).

**Source of truth**: `docs/frk/frkNN/` — already-unpacked Markdown, not
a ZIP upload (same situation as Kiltikonet/KORA). The import pipeline
scans that directory tree directly on the server filesystem; see
`import_pipeline.py`.

**Why FRK's real file shape is genuinely different from KOR's, and why
this package does NOT force KOR's per-module-file convention onto it**:
every KOR-01 module is its own file under `korXX/modules/MNN_*.md`, with
a separate `skills/SKILL_ID_REGISTRY.md` cross-referencing them. FRK's
real, verified corpus (`docs/frk/frk01/` through `frk75/`, spot-checked
across frk01/frk10/frk16/frk58) carries no `modules/` subdirectory and
no skill registry at all — each formation is exactly 9 flat files
(`REFERENTIAL.md`, `BANQUE_N1.md`, `BANQUE_N2.md`,
`ASSESSMENT_AND_RUBRIC.md`, `EVIDENCE_MODEL.md`, `GUIDE_CANDIDAT.md`,
`GUIDE_CORRECTEUR.md`, `GUIDE_JURY.md`, `INTEGRATION_NOTE.md`), and
every formation's real "Modules" are a short numbered list *inside*
`REFERENTIAL.md`'s own "## Modules" section — real, authored content,
just not split into separate files. This package's `CanonicalFrkModule`
is therefore a computed decomposition of that one real file, not a
distinct provenance-tracked resource; `content_source_file` on every
module always points back to the real `REFERENTIAL.md` it came from —
never a fabricated per-module path.

**Corpus accounting (verified against the real `docs/frk/` tree this
pass, not merely cited from `docs/frk/README.md`)**: 67 of the 75 real
FRK-01..75 codes have a `docs/frk/frkNN/` directory at all; of those,
57 carry a real `REFERENTIAL.md` (54 `PACKAGE_COMPLETE` + 3
`MODULE_CONTENT_DRAFTED`/`NEEDS_EXPERT_REVIEW` — FRK-10/14/73) and 10
carry only a `GAP.md` (`BLOCKED_PRODUCT_DEPENDENCY` — FRK-19/21/22/24/
39/57/64/65/66/67, genuinely no learner content, never imported as a
formation). The remaining 8 codes (FRK-05/45/46/48/49/50/51/70) have no
directory at all (`EXTEND_EXISTING` — folded into a sibling formation
or an existing Master Package doc, per `docs/frk/README.md`'s own
verdict) and are simply absent from every read this package performs.

**`fully_complete` is read directly from the corpus's own `## Status`
section** (`` `STATUS = PACKAGE_COMPLETE` ``), unlike KOR (which has no
self-declared status line and needs a derived invariant instead) — FRK's
corpus already carries this fact explicitly and honestly, so this
package trusts it rather than re-deriving a weaker proxy.
"""

from __future__ import annotations

from typing import List, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field

from canonical_common.audience import Audience
from canonical_common.audience import is_learner_facing as _is_learner_facing
from canonical_common.audience import learner_facing_types
from canonical_common.audience import resource_audience as _resource_audience

FRK_CANONICAL_VERSION_CURRENT = "FRK_20260907_V1"

# The 75 real candidates named by FREK_01_75_RECONCILIATION.md — never
# derived from a directory listing, always this explicit, real list,
# exactly like FMS's/Kiltikonet's/KORA's own frozen code lists. Not
# every code has real importable content (see module docstring above);
# `import_pipeline.py` accounts for every one honestly either way.
FRK_FORMATION_CODES: List[str] = [f"FRK-{n:02d}" for n in range(1, 76)]

# ---------------------------------------------------------------------
# Resource classification — mirrors kor_canonical/klt_canonical's
# RESOURCE_AUDIENCE discipline. Domain-specific by design (see
# canonical_common/audience.py's own docstring): unlike KOR, where the
# référentiel/blueprints doc is TRAINER/ADMIN-only and only a separate
# `module` file is learner-facing, FRK's `REFERENTIAL.md` *is* the real
# syllabus a candidate needs (system map, objectives, module list) —
# there is no separate learner-facing module file to split it from.
# ---------------------------------------------------------------------

RESOURCE_AUDIENCE: dict = {
    "referential": ["LEARNER"],
    "candidate_guide": ["LEARNER"],
    "corrector_guide": ["CORRECTOR"],
    "jury_guide": ["JURY"],
    "n1_question_bank": ["CORRECTOR", "JURY"],
    "n2_evaluations": ["CORRECTOR", "JURY"],
    "assessment_and_rubric": ["CORRECTOR", "JURY", "ADMIN"],
    "evidence_model": ["ADMIN", "INTERNAL"],
    "integration_note": ["ADMIN", "INTERNAL"],
    "gap": ["ADMIN", "INTERNAL"],
}


def resource_audience(resource_type: str) -> List[Audience]:
    return _resource_audience(RESOURCE_AUDIENCE, resource_type)


def is_learner_facing(resource_type: str) -> bool:
    return _is_learner_facing(RESOURCE_AUDIENCE, resource_type)


LEARNER_FACING_TYPES: frozenset = learner_facing_types(RESOURCE_AUDIENCE)


# ---------------------------------------------------------------------
# Module (computed decomposition of REFERENTIAL.md's own "## Modules"
# section) / Formation read model
# ---------------------------------------------------------------------


class CanonicalFrkModule(BaseModel):
    model_config = ConfigDict(extra="ignore")

    frk_formation_code: str
    module_code: str  # e.g. "FRK01-M02" — same "no dash after the
    # number" convention as FMS/KLT/KOR canonical module codes.
    canonical_version: str = FRK_CANONICAL_VERSION_CURRENT

    order_index: int
    title: str
    # The item's real text beyond the bold title, when the corpus's own
    # "**Title** — description" shape is present; None when a formation's
    # module line carries no such split (e.g. FRK-10's plain-sentence
    # items) — never fabricated to fill the gap.
    description: Optional[str] = None

    # Learner-safe: always the real, verbatim module-list item text.
    content_markdown: str
    content_source_file: str  # always "frkNN/REFERENTIAL.md" — real file


class CanonicalFrkFormation(BaseModel):
    model_config = ConfigDict(extra="ignore")

    frk_formation_code: str  # "FRK-01"
    title: str
    canonical_version: str = FRK_CANONICAL_VERSION_CURRENT
    pedagogical_source: Literal["CANONICAL_FRK"] = "CANONICAL_FRK"

    # Read directly from the corpus's own "## Status" section — see
    # module docstring above for why FRK doesn't need a derived proxy.
    status: str  # e.g. "PACKAGE_COMPLETE", "MODULE_CONTENT_DRAFTED"
    needs_expert_review: bool = False
    fully_complete: bool  # status == "PACKAGE_COMPLETE"

    prerequisites: Optional[str] = None
    objectives: Optional[str] = None
    assessment_summary: Optional[str] = None

    module_codes_in_order: List[str] = Field(default_factory=list)
    module_count: int = 0

    certification_scope: Literal["FULL", "PARTIAL"] = "FULL"


# ---------------------------------------------------------------------
# Progress — separate collection, same rationale as fms_canonical's,
# klt_canonical's and kor_canonical's own progress.py.
# ---------------------------------------------------------------------


class CanonicalFrkModuleProgress(BaseModel):
    model_config = ConfigDict(extra="ignore")

    user_id: str
    frk_formation_code: str
    module_code: str
    canonical_version: str = FRK_CANONICAL_VERSION_CURRENT

    content_viewed_at: Optional[str] = None
    updated_at: Optional[str] = None


# ---------------------------------------------------------------------
# File-level provenance — every real file under docs/frk/, parsed or
# not, individually accounted for. Same discipline as the other three
# canonical packages' own provenance models.
# ---------------------------------------------------------------------

ParsingStatus = Literal["parsed", "unparsed_no_type_match", "unparsed_error"]


class FrkFileProvenance(BaseModel):
    model_config = ConfigDict(extra="ignore")

    original_path: str  # relative to docs/frk/, e.g. "frk01/REFERENTIAL.md"
    original_filename: str
    sha256: str
    byte_size: int

    resource_type: Optional[str] = None
    formation_code: Optional[str] = None
    audience: List[Audience] = Field(default_factory=list)

    canonical_version: str = FRK_CANONICAL_VERSION_CURRENT
    parsing_status: ParsingStatus
    parsing_note: Optional[str] = None

    imported_at: Optional[str] = None


class FrkCanonicalImportResult(BaseModel):
    model_config = ConfigDict(extra="ignore")

    import_id: str
    docs_dir: str
    total_files: int
    parsed_count: int
    unparsed_count: int
    formations_found: List[str] = Field(default_factory=list)
    all_files_accounted_for: bool
