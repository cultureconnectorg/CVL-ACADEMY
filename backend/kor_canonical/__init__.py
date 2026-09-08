"""RAIL 2 — Canonical KORA (KOR) runtime binding. See `models.py`,
`read_model.py`, `progress.py`, `import_pipeline.py` module docstrings."""

from __future__ import annotations

from .import_pipeline import import_kor_docs
from .models import (
    KOR_CANONICAL_VERSION_CURRENT,
    KOR_CONTEXTS,
    KOR_FORMATION_CODES,
    LEARNER_FACING_TYPES,
    RESOURCE_AUDIENCE,
    CanonicalKorFormation,
    CanonicalKorModule,
    CanonicalKorModuleProgress,
    CanonicalKorSkill,
    KorCanonicalImportResult,
    KorFileProvenance,
    is_learner_facing,
    resource_audience,
)
from .progress import get_user_kor_progress, record_content_viewed
from .provenance import list_kor_provenance
from .read_model import (
    get_canonical_kor_formation,
    get_canonical_kor_module,
    list_canonical_kor_formations,
    list_canonical_kor_modules,
    list_canonical_kor_skills,
)
from .rubric_import import certification_code_for, import_rubric_for_formation

__all__ = [
    "KOR_CANONICAL_VERSION_CURRENT",
    "KOR_CONTEXTS",
    "KOR_FORMATION_CODES",
    "LEARNER_FACING_TYPES",
    "RESOURCE_AUDIENCE",
    "CanonicalKorFormation",
    "CanonicalKorModule",
    "CanonicalKorModuleProgress",
    "CanonicalKorSkill",
    "KorCanonicalImportResult",
    "KorFileProvenance",
    "is_learner_facing",
    "resource_audience",
    "get_canonical_kor_formation",
    "get_canonical_kor_module",
    "list_canonical_kor_formations",
    "list_canonical_kor_modules",
    "list_canonical_kor_skills",
    "get_user_kor_progress",
    "record_content_viewed",
    "import_kor_docs",
    "list_kor_provenance",
    "certification_code_for",
    "import_rubric_for_formation",
]
