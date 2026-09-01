"""Certification Engine — N1/N2/A01, rubrics, attempts, attestations.

Score chain: each rubric criterion maps to a bloc; a submitted attempt is
graded criterion-by-criterion, rolled up to score-per-bloc, then to one
global score. A jury signature (rule 6) is a hash over the graded attempt
+ grader identity — see attestation.py for the FREK-ready proof.

**Reconciled against the real FMS ZIP's grading doctrine**
(`28_FMS01_Rubric_Master.md`, `49_FMS01_A01_Grille_Certificative_V1.md`):
FMS certifies with a universal 0-4 "Rubric Master" scale, one score per
official Skill ID, that already fits this model unmodified — a criterion
with `max_score=4` *is* a Rubric Master criterion, and a rubric with N
equal-weight criteria naturally reproduces the real grille's "bloc weight
derived from its Skill ID count, not an arbitrary number" rule (§2 of that
grille). Two behaviours the original weighted-average model didn't have,
both real (not hypothetical) per that grille, are added below:

- **Critères éliminatoires** — a Skill ID tied to a "verrou doctrinal": a
  raw score of 0 on it auto-fails the attempt regardless of the total
  score (§3 of the grille).
- **Plafonnement de mention** — a low score on one specific criterion (in
  FMS-01, the "cohérence globale" Skill ID) caps the attainable mention
  regardless of the numeric total (§3-4 of the grille) — modeled as
  mention thresholds (numeric bands, e.g. Ajourné/Passable/Bien/Très
  bien/Excellence) plus a cap rule that can only ever lower the mention a
  numeric band would otherwise give.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Dict, List, Literal, Optional

from pydantic import BaseModel, Field

CertificationLevel = Literal["N1", "N2", "A01"]
AttemptStatus = Literal["in_progress", "submitted", "graded", "passed", "failed"]


def _uid() -> str:
    return str(uuid.uuid4())


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


class RubricCriterion(BaseModel):
    id: str  # e.g. "C1" — or a real Skill ID, e.g. "FMS01-B2"
    label: str
    bloc: str  # e.g. "B1" — rolls up into score_by_bloc
    skill_id: Optional[str] = None  # links back to the Skill Engine
    weight: float = 1.0
    max_score: float = 10.0
    # Real doctrine: "un niveau 0 sur un Skill ID rattaché à un verrou
    # bloque la validation, quel que soit le score total" — a raw score of
    # exactly 0 on an eliminatory criterion fails the attempt outright.
    is_eliminatory: bool = False


class RubricCapRule(BaseModel):
    """A low score on one criterion caps the mention the attempt can reach,
    independently of the numeric total — e.g. FMS-01's rule F1: "un niveau
    0 ou 1 sur FMS01-F1 plafonne automatiquement le résultat à la mention
    Passable, quel que soit le score obtenu par ailleurs"."""

    criterion_id: str
    max_raw_score_to_trigger: float  # cap applies when raw score <= this
    capped_mention: str  # e.g. "Passable"


class MentionThreshold(BaseModel):
    """One band of the mention scale, e.g. {min_pct: 90, mention: "Excellence"}.
    Evaluated highest-first — the first band whose min_pct the score meets
    or exceeds wins."""

    min_pct: float
    mention: str


class Rubric(BaseModel):
    certification_code: str  # e.g. "FMS-N1"
    level: CertificationLevel
    formation_code: str
    version: str = "1.0"
    pass_threshold_pct: float = 80.0
    criteria: List[RubricCriterion] = Field(default_factory=list)
    cap_rules: List[RubricCapRule] = Field(default_factory=list)
    mention_thresholds: List[MentionThreshold] = Field(default_factory=list)
    created_at: str = Field(default_factory=_now)


class RubricInput(BaseModel):
    level: CertificationLevel
    formation_code: str
    version: str = "1.0"
    pass_threshold_pct: float = 80.0
    criteria: List[RubricCriterion]
    cap_rules: List[RubricCapRule] = Field(default_factory=list)
    mention_thresholds: List[MentionThreshold] = Field(default_factory=list)


class GradeInput(BaseModel):
    """Jury/corrector submits one raw score per criterion id."""

    scores: Dict[str, float]  # criterion_id -> raw score (0..max_score)
    comments: Optional[str] = None


class JurySignature(BaseModel):
    jury_id: str
    signed_at: str = Field(default_factory=_now)
    sha256: str  # hash over {attempt_id, jury_id, scores, signed_at}


class CertificationAttempt(BaseModel):
    id: str = Field(default_factory=_uid)
    user_id: str
    certification_code: str
    formation_code: str
    level: CertificationLevel
    rubric_version: str
    attempt_number: int = 1
    status: AttemptStatus = "in_progress"
    raw_scores: Dict[str, float] = Field(default_factory=dict)  # criterion_id -> score
    score_by_competency: Dict[str, float] = Field(
        default_factory=dict
    )  # criterion_id -> pct
    score_by_bloc: Dict[str, float] = Field(default_factory=dict)  # bloc -> pct
    score_global: float = 0.0
    passed: bool = False
    eliminated: bool = False
    eliminated_reason: Optional[str] = None
    mention: Optional[str] = None
    jury_signature: Optional[JurySignature] = None
    comments: Optional[str] = None
    created_at: str = Field(default_factory=_now)
    submitted_at: Optional[str] = None
    graded_at: Optional[str] = None


class AttemptSummary(BaseModel):
    id: str
    certification_code: str
    level: CertificationLevel
    status: AttemptStatus
    attempt_number: int
    score_global: float
    passed: bool
    eliminated: bool = False
    mention: Optional[str] = None
    created_at: str
    graded_at: Optional[str] = None
