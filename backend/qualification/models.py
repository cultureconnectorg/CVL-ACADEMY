"""Qualification Engine models — durable Academy qualification facts."""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import List, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field

QualificationValidityClass = Literal["standard", "sensitive"]


def _uid() -> str:
    return str(uuid.uuid4())


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


class QualificationDefinition(BaseModel):
    """Admin registry: which certification/skills issue a qualification."""

    model_config = ConfigDict(extra="ignore")

    code: str
    label: str
    formation_code: Optional[str] = None
    certification_codes: List[str] = Field(default_factory=list)
    required_skill_ids: List[str] = Field(default_factory=list)
    version: str = "1.0"
    # Economy 3D Policies: standard qualifications last 24 months;
    # sensitive (cyber/finance/privileged) qualifications last 12 months.
    # The class is explicit in the definition: runtime never infers sensitivity
    # from a label, code or formation name.
    validity_class: QualificationValidityClass = "standard"
    created_at: str = Field(default_factory=_now)


class QualificationDefinitionInput(BaseModel):
    label: str
    formation_code: Optional[str] = None
    certification_codes: List[str] = Field(default_factory=list)
    required_skill_ids: List[str] = Field(default_factory=list)
    version: str = "1.0"
    validity_class: QualificationValidityClass = "standard"


class Qualification(BaseModel):
    """One issued qualification; issuance facts are append-only."""

    model_config = ConfigDict(extra="ignore")

    id: str = Field(default_factory=_uid)
    user_id: str
    qualification_code: str
    formation_code: Optional[str] = None
    source_certification_code: str
    source_attempt_id: str
    sha256: str
    issued_at: str = Field(default_factory=_now)
    expires_at: Optional[str] = None
    validity_class: QualificationValidityClass = "standard"
    validity_months: int = 24
