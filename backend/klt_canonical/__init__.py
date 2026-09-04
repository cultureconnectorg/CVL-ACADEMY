"""Canonical Kiltikonet runtime binding — "branchage complet de
Kiltikonet" (Founder, 2026-09-04). See `models.py`, `read_model.py`,
`import_pipeline.py`, `progress.py` module docstrings."""

from __future__ import annotations

from .import_pipeline import import_klt_docs
from .models import (KLT_CANONICAL_VERSION_CURRENT, KLT_CONTEXTS,
                     KLT_FORMATION_CODES, LEARNER_FACING_TYPES,
                     RESOURCE_AUDIENCE, CanonicalKltFormation,
                     CanonicalKltModule, CanonicalKltModuleProgress,
                     CanonicalKltSkill, KltCanonicalImportResult,
                     KltFileProvenance, is_learner_facing, resource_audience)
from .progress import get_user_klt_progress, record_klt_content_viewed
from .provenance import (build_klt_inventory, default_docs_dir,
                         list_klt_provenance)
from .read_model import (get_canonical_klt_formation, get_canonical_klt_module,
                         list_canonical_klt_formations,
                         list_canonical_klt_modules, list_canonical_klt_skills)

__all__ = [
    "KLT_CANONICAL_VERSION_CURRENT",
    "KLT_CONTEXTS",
    "KLT_FORMATION_CODES",
    "LEARNER_FACING_TYPES",
    "RESOURCE_AUDIENCE",
    "CanonicalKltFormation",
    "CanonicalKltModule",
    "CanonicalKltModuleProgress",
    "CanonicalKltSkill",
    "KltCanonicalImportResult",
    "KltFileProvenance",
    "is_learner_facing",
    "resource_audience",
    "get_user_klt_progress",
    "record_klt_content_viewed",
    "build_klt_inventory",
    "default_docs_dir",
    "list_klt_provenance",
    "get_canonical_klt_formation",
    "get_canonical_klt_module",
    "list_canonical_klt_formations",
    "list_canonical_klt_modules",
    "list_canonical_klt_skills",
    "import_klt_docs",
]
