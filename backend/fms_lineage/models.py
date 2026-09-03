"""ACA-0005 — Module Lineage models.

`module_lineage` is a new, additive collection: it never replaces, renames,
or deletes anything in `db.formations` or `db.progress`. Each record is one
explicit, human-auditable statement about how a **legacy** FMS module
(`FMS-01-M01`, served today from `seed_data.py`/`seed_modules.py`) relates
— or explicitly does *not* relate — to a **canonical** FMS module
(`FMS01-M01`, from the real `FMS_Chantier_Complet_20260822.zip` archive,
see `docs/ACADEMY_FMS_CANONICAL_DELTA_MATRIX.md`).

The one rule every other rule in this package serves: **a shared module
number (`M01` == `M01`) is never, by itself, evidence of equivalence.**
`docs/ACADEMY_FMS_CANONICAL_DELTA_MATRIX.md` §2 proved this concretely —
legacy `FMS-01-M01` ("Identité artistique et culturelle") and canonical
`FMS01-M01` ("Introduction au métier d'Artist Development") occupy the
same position and teach different things. `DEFAULT_RELATION` reflects
that: every record defaults to `NO_EQUIVALENCE` unless a human or a
documented process explicitly asserts otherwise.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field, model_validator

# The archive this session's Founder decision (DEC-002) confirmed as
# canonical-for-now. A future archive gets a new version string here —
# never a mutation of what "FMS_20260822_V1" already means.
CANONICAL_VERSION_CURRENT = "FMS_20260822_V1"

LineageRelation = Literal[
    "NO_EQUIVALENCE",
    "RELATED",
    "SUPERSEDED_BY",
    "MANUAL_EQUIVALENCE",
]

# Every relation the model will accept — used by service.py to fail safe
# (never crash) on any legacy/corrupt value it might read back.
KNOWN_RELATIONS: tuple[str, ...] = (
    "NO_EQUIVALENCE",
    "RELATED",
    "SUPERSEDED_BY",
    "MANUAL_EQUIVALENCE",
)

DEFAULT_RELATION: LineageRelation = "NO_EQUIVALENCE"

# A record's own governance lifecycle — distinct from `relation` (what it
# claims) and never destructive: "revoked" is the only way to retire a
# record, so the full history stays queryable (MAPPING_MUST_BE_AUDITABLE).
LineageStatus = Literal["active", "revoked"]


def _uid() -> str:
    return str(uuid.uuid4())


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


class ModuleLineage(BaseModel):
    """One lineage record. See module docstring for the governing rule."""

    model_config = ConfigDict(extra="ignore")

    lineage_id: str = Field(default_factory=_uid)

    # The legacy side — never mutated, never deleted, purely descriptive.
    legacy_formation_code: str
    legacy_module_code: str

    # The canonical side. `canonical_module_code` is optional: a record
    # can assert "this legacy module has no canonical counterpart at all"
    # without naming a specific (and therefore misleadingly precise)
    # canonical module.
    canonical_formation_code: str
    canonical_module_code: Optional[str] = None
    canonical_version: str = CANONICAL_VERSION_CURRENT

    relation: LineageRelation = DEFAULT_RELATION
    status: LineageStatus = "active"

    created_at: str = Field(default_factory=_now)
    updated_at: str = Field(default_factory=_now)
    created_by: str

    # Free-text, real evidence — required for MANUAL_EQUIVALENCE (below),
    # optional but strongly encouraged for RELATED.
    evidence: Optional[str] = None
    notes: Optional[str] = None

    # MANUAL_EQUIVALENCE-only governance fields (mission §4/§8): a human
    # pedagogical decision, never a system inference.
    approved_by: Optional[str] = None
    approved_at: Optional[str] = None
    scope: Optional[str] = None

    @model_validator(mode="after")
    def _manual_equivalence_requires_evidence_and_approval(self) -> "ModuleLineage":
        if self.relation == "MANUAL_EQUIVALENCE":
            if not (self.evidence and self.evidence.strip()):
                raise ValueError("MANUAL_EQUIVALENCE requires non-empty `evidence`")
            if not (self.approved_by and self.approved_by.strip()):
                raise ValueError("MANUAL_EQUIVALENCE requires non-empty `approved_by`")
        return self


class LineageCreateInput(BaseModel):
    """What a caller may set when creating a record — `lineage_id`,
    `created_at`/`updated_at`, and `created_by` are always server-assigned."""

    legacy_formation_code: str
    legacy_module_code: str
    canonical_formation_code: str
    canonical_module_code: Optional[str] = None
    canonical_version: str = CANONICAL_VERSION_CURRENT
    relation: LineageRelation = DEFAULT_RELATION
    evidence: Optional[str] = None
    notes: Optional[str] = None
    approved_by: Optional[str] = None
    approved_at: Optional[str] = None
    scope: Optional[str] = None


class LineageUpdateInput(BaseModel):
    """Partial update — every field optional; only provided fields change.
    `legacy_formation_code`/`legacy_module_code` are immutable once created
    (create a new record instead of repointing an existing one — keeps the
    audit trail honest about what a record has always meant)."""

    canonical_formation_code: Optional[str] = None
    canonical_module_code: Optional[str] = None
    canonical_version: Optional[str] = None
    relation: Optional[LineageRelation] = None
    status: Optional[LineageStatus] = None
    evidence: Optional[str] = None
    notes: Optional[str] = None
    approved_by: Optional[str] = None
    approved_at: Optional[str] = None
    scope: Optional[str] = None


class ResolvedTarget(BaseModel):
    """The conservative, read-only answer `resolve_canonical_target` gives.

    `credit_transfer` is hardcoded `False` on every branch that
    constructs this model — there is no code path in this package that
    can ever set it `True`. That is deliberate: crediting canonical
    progress from a resolved lineage is explicitly out of scope for
    ACA-0005 (mission §10) and belongs to a future, separately
    authorized wave."""

    model_config = ConfigDict(extra="ignore")

    legacy_formation_code: str
    legacy_module_code: str

    relation: Optional[LineageRelation] = None
    canonical_formation_code: Optional[str] = None
    canonical_module_code: Optional[str] = None
    canonical_version: Optional[str] = None

    credit_transfer: bool = False
    qualified: bool = False

    evidence: Optional[str] = None
    approved_by: Optional[str] = None
    source_lineage_id: Optional[str] = None

    note: Optional[str] = None
