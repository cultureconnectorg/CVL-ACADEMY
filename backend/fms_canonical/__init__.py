"""ACA-0006 — Canonical FMS runtime binding. See `models.py`,
`read_model.py`, `progress.py`, `import_pipeline.py` module docstrings."""

from __future__ import annotations

from .import_pipeline import import_canonical_fms_zip
from .models import (
    CANONICAL_VERSION_CURRENT,
    LEARNER_FACING_TYPES,
    RESOURCE_AUDIENCE,
    STAFF_ONLY_TYPES,
    CanonicalFormation,
    CanonicalImportResult,
    CanonicalModule,
    CanonicalModuleProgress,
    CanonicalPrerequisites,
    CanonicalSkillDefinition,
    FileProvenance,
    is_learner_facing,
    resource_audience,
)
from .progress import get_user_canonical_progress, record_content_viewed
from .provenance import build_zip_inventory, count_zip_files, list_zip_provenance
from .read_model import (
    CANONICAL_FORMATION_CODES,
    get_canonical_formation,
    get_canonical_module,
    list_canonical_formations,
    list_canonical_modules,
    list_canonical_skill_definitions,
)

__all__ = [
    "CANONICAL_VERSION_CURRENT",
    "LEARNER_FACING_TYPES",
    "STAFF_ONLY_TYPES",
    "RESOURCE_AUDIENCE",
    "CanonicalFormation",
    "CanonicalImportResult",
    "CanonicalModule",
    "CanonicalModuleProgress",
    "CanonicalPrerequisites",
    "CanonicalSkillDefinition",
    "FileProvenance",
    "is_learner_facing",
    "resource_audience",
    "CANONICAL_FORMATION_CODES",
    "get_canonical_formation",
    "get_canonical_module",
    "list_canonical_formations",
    "list_canonical_modules",
    "list_canonical_skill_definitions",
    "get_user_canonical_progress",
    "record_content_viewed",
    "import_canonical_fms_zip",
    "build_zip_inventory",
    "count_zip_files",
    "list_zip_provenance",
]
