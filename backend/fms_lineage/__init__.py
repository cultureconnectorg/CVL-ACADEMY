"""ACA-0005 — Module Lineage: the safe legacy<->canonical FMS mapping
infrastructure. See `models.py` and `service.py` docstrings for the rules;
`initial_matrix.py` for the additive, review-only seed."""

from __future__ import annotations

from .initial_matrix import build_initial_records, seed_initial_matrix
from .models import (
    CANONICAL_VERSION_CURRENT,
    DEFAULT_RELATION,
    KNOWN_RELATIONS,
    LineageCreateInput,
    LineageRelation,
    LineageStatus,
    LineageUpdateInput,
    ModuleLineage,
    ResolvedTarget,
)
from .service import (
    COLLECTION,
    LineageError,
    create_lineage,
    get_lineage_for_canonical_module,
    get_lineage_for_legacy_module,
    list_lineage_for_formation,
    resolve_canonical_target,
    update_lineage,
)

__all__ = [
    "CANONICAL_VERSION_CURRENT",
    "DEFAULT_RELATION",
    "KNOWN_RELATIONS",
    "LineageCreateInput",
    "LineageRelation",
    "LineageStatus",
    "LineageUpdateInput",
    "ModuleLineage",
    "ResolvedTarget",
    "COLLECTION",
    "LineageError",
    "create_lineage",
    "get_lineage_for_canonical_module",
    "get_lineage_for_legacy_module",
    "list_lineage_for_formation",
    "resolve_canonical_target",
    "update_lineage",
    "build_initial_records",
    "seed_initial_matrix",
]
