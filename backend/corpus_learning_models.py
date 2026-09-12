"""Typed API models for corpus-to-learning reconciliation status."""

from enum import StrEnum

from pydantic import BaseModel, Field, computed_field


class CompletenessGate(StrEnum):
    CANONICAL_IDENTITY = "canonical_identity"
    PEDAGOGICAL_DESIGN = "pedagogical_design"
    LEARNING_CONTENT = "learning_content"
    ASSESSMENT = "assessment"
    COMMERCIALIZATION_ACCESS = "commercialization_access"
    RUNTIME = "runtime"
    VERIFICATION = "verification"


class LearningCoverageModel(BaseModel):
    canonical_identity: bool = False
    pedagogical_design: bool = False
    learning_content: bool = False
    assessment: bool = False
    commercialization_access: bool = False
    runtime: bool = False
    verification: bool = False

    @computed_field
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

    @computed_field
    @property
    def missing_gates(self) -> list[CompletenessGate]:
        return [
            gate
            for gate, value in (
                (CompletenessGate.CANONICAL_IDENTITY, self.canonical_identity),
                (CompletenessGate.PEDAGOGICAL_DESIGN, self.pedagogical_design),
                (CompletenessGate.LEARNING_CONTENT, self.learning_content),
                (CompletenessGate.ASSESSMENT, self.assessment),
                (
                    CompletenessGate.COMMERCIALIZATION_ACCESS,
                    self.commercialization_access,
                ),
                (CompletenessGate.RUNTIME, self.runtime),
                (CompletenessGate.VERIFICATION, self.verification),
            )
            if not value
        ]


class FormationLearningStatusModel(BaseModel):
    code: str
    module_count: int = Field(ge=0)
    coverage: LearningCoverageModel
    blockers: list[str] = []
