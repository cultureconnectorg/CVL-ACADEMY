"""ACA-0005 — Module Lineage service.

Non-negotiable rules this service enforces in code, not just in prose
(mirrors the Founder's ACA-0005 mission binary rules verbatim):

  LEGACY_PROGRESS_MUTATION      = FORBIDDEN  -> nothing in this file ever
                                                writes to `db.progress`.
  LEGACY_PROGRESS_DELETION      = FORBIDDEN  -> same; this file has no
                                                delete path for anything
                                                but a `module_lineage`
                                                record, and even that is
                                                a soft "revoked" status,
                                                never a real delete.
  LEGACY_CONTENT_DELETION       = FORBIDDEN  -> this file never touches
                                                `db.formations`.
  LEGACY_MODULE_CODE_REWRITE    = FORBIDDEN  -> legacy_formation_code/
                                                legacy_module_code are
                                                immutable after create
                                                (see LineageUpdateInput).
  CANONICAL_CODE_NORMALIZATION  = FORBIDDEN  -> codes are stored and
                                                compared as exact
                                                strings; nothing here
                                                strips/rewrites hyphens.
  CANONICAL_CREDIT_AUTO_TRANSFER = FORBIDDEN -> `resolve_canonical_target`
                                                always returns
                                                `credit_transfer=False`;
                                                no caller can flip that.
  POSITIONAL_EQUIVALENCE_INFERENCE   = FORBIDDEN
  PEDAGOGICAL_EQUIVALENCE_INFERENCE  = FORBIDDEN
                                    -> nothing in this file derives a
                                       relation from matching module
                                       numbers or titles; every relation
                                       is either the safe default
                                       (`NO_EQUIVALENCE`) or explicitly
                                       supplied by a caller, and
                                       `MANUAL_EQUIVALENCE` additionally
                                       requires real evidence + a human
                                       approver (enforced in
                                       `models.py`).

See `docs/ACADEMY_FMS_CANONICAL_LINEAGE_IMPLEMENTATION_REPORT.md` for the
full audit this service was built against.
"""

from __future__ import annotations

import logging
from typing import List, Literal, Optional

from db import db, utc_now_iso

from .models import (
    KNOWN_RELATIONS,
    LineageCreateInput,
    LineageUpdateInput,
    ModuleLineage,
    ResolvedTarget,
)

logger = logging.getLogger("cvln.fms_lineage")

COLLECTION = "module_lineage"

# Priority used only to pick *among a legacy module's own active records*
# which one `resolve_canonical_target` reports first when more than one
# exists (e.g. several RELATED entries plus one NO_EQUIVALENCE). It is
# never used to infer a relation that wasn't explicitly recorded.
_RELATION_PRIORITY = {
    "MANUAL_EQUIVALENCE": 3,
    "SUPERSEDED_BY": 2,
    "RELATED": 1,
    "NO_EQUIVALENCE": 0,
}


class LineageError(ValueError):
    """A governance or not-found error — callers (the API router) turn
    this into an HTTP 400/404, never a 500."""


def _coerce(doc: dict) -> Optional[ModuleLineage]:
    """Fail-safe parse: an unrecognized/corrupt `relation` value never
    crashes the service — it's logged and the record is dropped from
    results rather than raising. (Mission §13 test 15.)"""
    try:
        if doc.get("relation") not in KNOWN_RELATIONS:
            logger.warning(
                "module_lineage %s has unrecognized relation %r — ignored",
                doc.get("lineage_id"),
                doc.get("relation"),
            )
            return None
        return ModuleLineage(**doc)
    except Exception:  # noqa: BLE001 - deliberately broad: never raise from a read
        logger.warning(
            "module_lineage %s failed to parse — ignored", doc.get("lineage_id")
        )
        return None


async def create_lineage(
    payload: LineageCreateInput, *, created_by: str
) -> ModuleLineage:
    record = ModuleLineage(**payload.model_dump(), created_by=created_by)
    await db[COLLECTION].insert_one(record.model_dump())
    return record


async def update_lineage(lineage_id: str, payload: LineageUpdateInput) -> ModuleLineage:
    existing = await db[COLLECTION].find_one({"lineage_id": lineage_id}, {"_id": 0})
    if not existing:
        raise LineageError(f"No module_lineage record with id {lineage_id!r}")
    updates = {k: v for k, v in payload.model_dump().items() if v is not None}
    merged = {**existing, **updates, "updated_at": utc_now_iso()}
    # Re-validate the *whole* merged record (not just the patch) so an
    # update can never leave a MANUAL_EQUIVALENCE record without
    # evidence/approved_by, even if the update itself didn't touch those
    # fields.
    record = ModuleLineage(**merged)
    await db[COLLECTION].replace_one({"lineage_id": lineage_id}, record.model_dump())
    return record


async def get_lineage_for_legacy_module(
    legacy_formation_code: str, legacy_module_code: str, *, active_only: bool = True
) -> List[ModuleLineage]:
    query = {
        "legacy_formation_code": legacy_formation_code,
        "legacy_module_code": legacy_module_code,
    }
    if active_only:
        query["status"] = "active"
    docs = await db[COLLECTION].find(query, {"_id": 0}).to_list(1000)
    return [r for r in (_coerce(d) for d in docs) if r is not None]


async def get_lineage_for_canonical_module(
    canonical_formation_code: str,
    canonical_module_code: str,
    *,
    active_only: bool = True,
) -> List[ModuleLineage]:
    query = {
        "canonical_formation_code": canonical_formation_code,
        "canonical_module_code": canonical_module_code,
    }
    if active_only:
        query["status"] = "active"
    docs = await db[COLLECTION].find(query, {"_id": 0}).to_list(1000)
    return [r for r in (_coerce(d) for d in docs) if r is not None]


async def list_lineage_for_formation(
    formation_code: str,
    *,
    side: Literal["legacy", "canonical", "both"] = "both",
    active_only: bool = True,
) -> List[ModuleLineage]:
    or_clauses = []
    if side in ("legacy", "both"):
        or_clauses.append({"legacy_formation_code": formation_code})
    if side in ("canonical", "both"):
        or_clauses.append({"canonical_formation_code": formation_code})
    query: dict = {"$or": or_clauses} if len(or_clauses) > 1 else or_clauses[0]
    if active_only:
        query["status"] = "active"
    docs = await db[COLLECTION].find(query, {"_id": 0}).to_list(5000)
    return [r for r in (_coerce(d) for d in docs) if r is not None]


async def resolve_canonical_target(
    legacy_formation_code: str, legacy_module_code: str
) -> ResolvedTarget:
    """Conservative, read-only. Never writes anything. Never returns
    `credit_transfer=True`. See module docstring for the full rule set."""
    records = await get_lineage_for_legacy_module(
        legacy_formation_code, legacy_module_code
    )
    valid = [r for r in records if r.relation in _RELATION_PRIORITY]

    if not valid:
        return ResolvedTarget(
            legacy_formation_code=legacy_formation_code,
            legacy_module_code=legacy_module_code,
            note="No lineage record exists for this legacy module — unmapped.",
        )

    best = max(valid, key=lambda r: _RELATION_PRIORITY[r.relation])

    if best.relation == "NO_EQUIVALENCE":
        return ResolvedTarget(
            legacy_formation_code=legacy_formation_code,
            legacy_module_code=legacy_module_code,
            relation="NO_EQUIVALENCE",
            source_lineage_id=best.lineage_id,
            note="Explicitly recorded as having no canonical equivalent.",
        )

    if best.relation == "RELATED":
        return ResolvedTarget(
            legacy_formation_code=legacy_formation_code,
            legacy_module_code=legacy_module_code,
            relation="RELATED",
            canonical_formation_code=best.canonical_formation_code,
            canonical_module_code=best.canonical_module_code,
            canonical_version=best.canonical_version,
            evidence=best.evidence,
            source_lineage_id=best.lineage_id,
            note="Thematically related only — never treat as equivalence or credit.",
        )

    if best.relation == "SUPERSEDED_BY":
        return ResolvedTarget(
            legacy_formation_code=legacy_formation_code,
            legacy_module_code=legacy_module_code,
            relation="SUPERSEDED_BY",
            canonical_formation_code=best.canonical_formation_code,
            canonical_module_code=best.canonical_module_code,
            canonical_version=best.canonical_version,
            evidence=best.evidence,
            source_lineage_id=best.lineage_id,
            note=(
                "Canonical module is the active replacement for new learners; "
                "historical legacy completion is not automatically validated "
                "against it."
            ),
        )

    # MANUAL_EQUIVALENCE — the only branch that can ever set qualified=True.
    # credit_transfer is still, deliberately, always False (mission §7/§10:
    # "Même dans ce cas, ne migre aucun ModuleProgress dans ACA-0005").
    return ResolvedTarget(
        legacy_formation_code=legacy_formation_code,
        legacy_module_code=legacy_module_code,
        relation="MANUAL_EQUIVALENCE",
        canonical_formation_code=best.canonical_formation_code,
        canonical_module_code=best.canonical_module_code,
        canonical_version=best.canonical_version,
        qualified=True,
        evidence=best.evidence,
        approved_by=best.approved_by,
        source_lineage_id=best.lineage_id,
        note="Human-approved equivalence — still no automatic credit transfer.",
    )
