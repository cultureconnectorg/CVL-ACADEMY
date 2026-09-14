"""Qualification Engine — RAIL 2, "MASTER -> RUNTIME ACADEMY" (Founder
instruction, 2026-09-06).

The Rail 2 target chain is:

    Learning -> Skill -> Evidence -> Assessment -> Certification ->
    Qualification -> Opportunity -> Mission

Before this pass, the runtime already covered Learning through
Certification (`lx.py`/`db.progress`, `skills/`, `certification/` —
all real, already-reconciled code) — the chain simply stopped there.
This package is the one genuinely missing link: **Qualification**, an
admin-configured registry entry (`QualificationDefinition`) plus a real,
issued instance (`Qualification`) a learner earns by passing a
certification that a definition names.

**Opportunity is deliberately not a new stored entity here** — see
`docs/cvln_academy_master/RAIL2_MASTER_RUNTIME_INTEGRATION.md` for the
full reasoning: it is modeled as a computed eligibility view over the
existing `Mission` model (its new, additive
`required_qualification_codes` field), never a duplicated third
representation of "what a qualified learner can now do."

Purely additive: no existing collection, model, or route is modified by
this package's own code. The one integration point — `certification/
service.py::grade_attempt`'s `if passed:` block calling
`maybe_issue_qualification` — is a no-op whenever no
`QualificationDefinition` names the certification just passed, so every
certification flow that predates this ticket (FMS, GMD, WAL, ...)
behaves identically to before.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


def _uid() -> str:
    return str(uuid.uuid4())


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


class QualificationDefinition(BaseModel):
    """Admin-configured registry entry — "passing certification X (and
    optionally holding skills Y) earns qualification Z". Never issued to
    anyone by itself; see `Qualification` for the issued instance."""

    model_config = ConfigDict(extra="ignore")

    code: str  # e.g. "QUAL-KOR01-PRODUCTEUR-PODCAST" — the Mongo key
    label: str
    formation_code: Optional[str] = None  # e.g. "KOR-01" — informational link
    # Any one of these certification codes passing issues this
    # qualification (usually exactly one — a list only so a
    # qualification can later be reachable via more than one
    # certification path without a model change).
    certification_codes: List[str] = Field(default_factory=list)
    # Optional additional gate: every skill_id here must already be
    # "acquired" (skills.progression.UserSkill) for the qualification to
    # issue — empty means "the certification pass alone is sufficient",
    # the common case.
    required_skill_ids: List[str] = Field(default_factory=list)
    version: str = "1.0"
    created_at: str = Field(default_factory=_now)


class QualificationDefinitionInput(BaseModel):
    label: str
    formation_code: Optional[str] = None
    certification_codes: List[str] = Field(default_factory=list)
    required_skill_ids: List[str] = Field(default_factory=list)
    version: str = "1.0"


class Qualification(BaseModel):
    """One real, issued qualification — a durable fact, never mutated
    after creation (append-only, same discipline as
    `skills.models.EvidenceEntry`)."""

    model_config = ConfigDict(extra="ignore")

    id: str = Field(default_factory=_uid)
    user_id: str
    qualification_code: str
    formation_code: Optional[str] = None
    source_certification_code: str
    source_attempt_id: str
    sha256: str  # content hash of the issuance payload — FREK-ready
    issued_at: str = Field(default_factory=_now)
