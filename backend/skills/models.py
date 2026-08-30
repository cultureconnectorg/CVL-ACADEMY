"""Skill Engine — Skill IDs, evidence, progression.

A Skill ID looks like `FMS.N1.B1.S1` — <métier>.<niveau>.<bloc>.<compétence>.
Skills are registered either by an FMS import (a module's `skill_ids:`
frontmatter) or directly by the Admin CMS; a user's progress on each skill
is derived from the evidence attached to it (deliverables, quiz passes,
mini-missions, certification attempts).
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import List, Literal, Optional

from pydantic import BaseModel, Field

SkillState = Literal["not_started", "in_progress", "acquired"]
EvidenceType = Literal["quiz", "deliverable", "mini_mission", "certification"]


def _uid() -> str:
    return str(uuid.uuid4())


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


class Skill(BaseModel):
    """A skill definition — the registry entry, not a user's progress."""

    id: str  # the Skill ID itself, e.g. "FMS.N1.B1.S1" — used as the Mongo key
    metier: str  # pole code, e.g. "FMS"
    niveau: str  # "N1" | "N2" | "A01" | ...
    bloc: str  # e.g. "B1"
    label: str
    version: str = "1.0"
    source: Literal["fms_import", "admin"] = "admin"
    created_at: str = Field(default_factory=_now)


class EvidenceEntry(BaseModel):
    """One piece of proof that a user progressed on a skill — durable,
    never mutated after creation (append-only registry)."""

    id: str = Field(default_factory=_uid)
    user_id: str
    skill_id: str
    evidence_type: EvidenceType
    ref: str  # module_code / mission_code / certification_attempt_id
    detail: Optional[str] = None
    sha256: str  # content hash of the evidence payload — FREK-ready (rule 11)
    created_at: str = Field(default_factory=_now)


class UserSkill(BaseModel):
    """One user's live progression on one skill — derived/recomputed from
    EvidenceEntry rows, cached here for fast reads."""

    user_id: str
    skill_id: str
    state: SkillState = "not_started"
    progression_pct: int = 0
    evidence_count: int = 0
    updated_at: str = Field(default_factory=_now)


class SkillProgressSummary(BaseModel):
    skill: Skill
    state: SkillState
    progression_pct: int
    evidence_count: int


class SkillsByBloc(BaseModel):
    bloc: str
    skills: List[SkillProgressSummary]
