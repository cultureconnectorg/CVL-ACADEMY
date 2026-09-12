"""Canonical corpus-to-learning reconciliation contract for CVLN Academy.

This module defines evidence-first statuses and completeness gates used to reconcile
canonical workbook rows with runtime learning objects. It intentionally does not
invent missing pedagogical content.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any


class CorpusObjectType(StrEnum):
    FORMATION = "FORMATION"
    INTERNAL_SKILL_OPERATOR = "INTERNAL_SKILL_OPERATOR"
    CROSS_ECOSYSTEM_COMPETENCY = "CROSS_ECOSYSTEM_COMPETENCY"
    TRANSVERSAL = "TRANSVERSAL"
    CASE_LAB = "CASE_LAB"
    GAP_TO_RECONCILE = "GAP_TO_RECONCILE"


class ReconciliationStatus(StrEnum):
    CANDIDATE = "CANDIDATE"
    MAPPED = "MAPPED"
    DESIGNED = "DESIGNED"
    IMPLEMENTED = "IMPLEMENTED"
    VERIFIED = "VERIFIED"
    PUBLISHED = "PUBLISHED"
    BLOCKED = "BLOCKED"
    DEPRECATED = "DEPRECATED"


@dataclass(frozen=True)
class LearningCompleteness:
    canonical_identity: bool = False
    pedagogical_design: bool = False
    learning_content: bool = False
    assessment: bool = False
    commercialization_access: bool = False
    runtime: bool = False
    verification: bool = False

    @property
    def complete(self) -> bool:
        return all(
            (
                self.canonical_identity,
                self.pedagogical_design,
                self.learning_content,
                self.assessment,
                self.commercialization_access,
                self.runtime,
                self.verification,
            )
        )

    def missing_gates(self) -> list[str]:
        return [
            name
            for name, value in (
                ("canonical_identity", self.canonical_identity),
                ("pedagogical_design", self.pedagogical_design),
                ("learning_content", self.learning_content),
                ("assessment", self.assessment),
                ("commercialization_access", self.commercialization_access),
                ("runtime", self.runtime),
                ("verification", self.verification),
            )
            if not value
        ]


@dataclass
class ReconciliationRecord:
    canonical_code: str
    canonical_title: str
    source_workbook: str
    source_sheet: str
    source_row: int
    classification: CorpusObjectType
    context: str | None = None
    status: ReconciliationStatus = ReconciliationStatus.CANDIDATE
    legacy_runtime_code: str | None = None
    mapping_relation: str | None = None
    module_count_expected: int | None = None
    module_count_implemented: int = 0
    completeness: LearningCompleteness = field(default_factory=LearningCompleteness)
    blocking_gaps: list[str] = field(default_factory=list)
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def publishable(self) -> bool:
        return (
            self.status
            in {
                ReconciliationStatus.VERIFIED,
                ReconciliationStatus.PUBLISHED,
            }
            and self.completeness.complete
        )

    def validate(self) -> list[str]:
        errors: list[str] = []
        if self.classification == CorpusObjectType.FORMATION:
            if self.module_count_implemented < 1 and self.status in {
                ReconciliationStatus.IMPLEMENTED,
                ReconciliationStatus.VERIFIED,
                ReconciliationStatus.PUBLISHED,
            }:
                errors.append("implemented formation has no real module")
            if self.status == ReconciliationStatus.PUBLISHED and not self.publishable:
                errors.append("published formation does not pass every completeness gate")
        return errors


def classify_corpus_type(raw_type: str | None) -> CorpusObjectType:
    value = (raw_type or "").strip().lower()
    if value == "formation":
        return CorpusObjectType.FORMATION
    if "internal skill" in value or "operator" in value:
        return CorpusObjectType.INTERNAL_SKILL_OPERATOR
    if "cross-ecosystem" in value:
        return CorpusObjectType.CROSS_ECOSYSTEM_COMPETENCY
    if "transversal" in value:
        return CorpusObjectType.TRANSVERSAL
    if "case lab" in value:
        return CorpusObjectType.CASE_LAB
    return CorpusObjectType.GAP_TO_RECONCILE
