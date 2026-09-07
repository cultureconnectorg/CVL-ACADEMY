"""RAIL 2 — Qualification Engine. See `models.py`'s module docstring for
the chain this closes: Learning -> Skill -> Evidence -> Assessment ->
Certification -> Qualification -> Opportunity -> Mission."""

from __future__ import annotations

from .models import (Qualification, QualificationDefinition,
                     QualificationDefinitionInput)
from .service import (get_definition, has_any_of, is_qualified,
                      list_definitions, list_user_qualifications,
                      maybe_issue_qualification, register_definition)

__all__ = [
    "Qualification",
    "QualificationDefinition",
    "QualificationDefinitionInput",
    "register_definition",
    "get_definition",
    "list_definitions",
    "maybe_issue_qualification",
    "list_user_qualifications",
    "is_qualified",
    "has_any_of",
]
