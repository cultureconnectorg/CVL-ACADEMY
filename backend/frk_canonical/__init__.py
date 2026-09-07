"""Canonical FREK (FRK) runtime binding — "raccorder ces corpus au même
runtime/funnel Academy" (Founder instruction, 2026-09-07), same
domain-prefixed pattern as `fms_canonical/`, `klt_canonical/`,
`kor_canonical/`. See `models.py`, `read_model.py`, `progress.py`,
`import_pipeline.py` module docstrings."""

from __future__ import annotations

from .import_pipeline import import_frk_docs
from .models import (FRK_CANONICAL_VERSION_CURRENT, FRK_FORMATION_CODES,
                     LEARNER_FACING_TYPES, RESOURCE_AUDIENCE,
                     CanonicalFrkFormation, CanonicalFrkModule,
                     CanonicalFrkModuleProgress, FrkCanonicalImportResult,
                     FrkFileProvenance, is_learner_facing, resource_audience)
from .progress import get_user_frk_progress, record_content_viewed
from .provenance import list_frk_provenance
from .read_model import (get_canonical_frk_formation, get_canonical_frk_module,
                         list_canonical_frk_formations,
                         list_canonical_frk_modules)

__all__ = [
    "FRK_CANONICAL_VERSION_CURRENT",
    "FRK_FORMATION_CODES",
    "LEARNER_FACING_TYPES",
    "RESOURCE_AUDIENCE",
    "CanonicalFrkFormation",
    "CanonicalFrkModule",
    "CanonicalFrkModuleProgress",
    "FrkCanonicalImportResult",
    "FrkFileProvenance",
    "is_learner_facing",
    "resource_audience",
    "get_canonical_frk_formation",
    "get_canonical_frk_module",
    "list_canonical_frk_formations",
    "list_canonical_frk_modules",
    "get_user_frk_progress",
    "record_content_viewed",
    "import_frk_docs",
    "list_frk_provenance",
]
