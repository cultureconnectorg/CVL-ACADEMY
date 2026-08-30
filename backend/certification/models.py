"""Certification Engine — N1/N2/A01, rubrics, attempts, attestations.

Score chain: each rubric criterion maps to a bloc; a submitted attempt is
graded criterion-by-criterion, rolled up to score-per-bloc, then to one
global score. A jury signature (rule 6) is a hash over the graded attempt
+ grader identity — see attestation.py for the FREK-ready proof.
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
    id: str  # e.g. "C1"
    label: str
    bloc: str  # e.g. "B1" — rolls up into score_by_bloc
    skill_id: Optional[str] = None  # links back to the Skill Engine
    weight: float = 1.0
    max_score: float = 10.0


class Rubric(BaseModel):
    certification_code: str  # e.g. "FMS-N1"
    level: CertificationLevel
    formation_code: str
    version: str = "1.0"
    pass_threshold_pct: float = 80.0
    criteria: List[RubricCriterion] = Field(default_factory=list)
    created_at: str = Field(default_factory=_now)


class RubricInput(BaseModel):
    level: CertificationLevel
    formation_code: str
    version: str = "1.0"
    pass_threshold_pct: float = 80.0
    criteria: List[RubricCriterion]


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
    created_at: str
    graded_at: Optional[str] = None
