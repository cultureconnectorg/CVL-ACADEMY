"""Machine-readable Excel/master -> runtime proof registry.

Evidence First invariants:
- ingesting a source row means ``INGESTED_RUNTIME``; it never means VERIFIED;
- a VERIFIED row stays verified across idempotent seeds while its source hash is
  unchanged;
- if the authoritative source hash changes, prior verification is invalidated
  and the row returns to ``INGESTED_RUNTIME`` until new evidence is supplied.
"""
from __future__ import annotations

from typing import Any

from services.catalogue_importer import load_catalogue_rows
from services.economy_importer import load_economy_rows


def _base_requirement(
    *,
    family: str,
    row: dict[str, Any],
    collection: str,
    importer: str,
    test_ref: str,
) -> dict[str, Any]:
    return {
        "requirement_id": f"{family}:{row['code']}",
        "family": family,
        "code": row["code"],
        "source": row["source"],
        "source_hash": row["source_hash"],
        "runtime_collection": collection,
        "runtime_key": {"code": row["code"]},
        "runtime_importer": importer,
        "test_ref": test_ref,
    }


def merge_ingested_requirement(
    base: dict[str, Any], existing: dict[str, Any] | None
) -> tuple[dict[str, Any], list[str]]:
    """Return the safe ``$set`` payload and fields that must be ``$unset``.

    Verification is evidence about one exact source version. Re-seeding the same
    hash is idempotent and must not destroy that evidence. A changed hash makes
    the old evidence stale, therefore verification is deliberately reset.
    """
    same_source = bool(existing) and existing.get("source_hash") == base["source_hash"]
    if same_source and existing.get("verified") is True:
        preserved = {
            "status": "VERIFIED",
            "verified": True,
            "verification_evidence": existing.get("verification_evidence"),
            "verified_by": existing.get("verified_by"),
        }
        if existing.get("verified_at"):
            preserved["verified_at"] = existing["verified_at"]
        return {**base, **preserved}, []

    unset = ["verification_evidence", "verified_by", "verified_at"]
    return {**base, "status": "INGESTED_RUNTIME", "verified": False}, unset


async def sync_master_requirements(db: Any) -> dict[str, int]:
    catalogue = load_catalogue_rows()
    economy = load_economy_rows()
    written = 0
    invalidated = 0
    preserved_verified = 0

    for family, rows, collection, importer, test_ref in (
        (
            "CATALOGUE_2D",
            catalogue,
            "academy_catalogue_master",
            "services.catalogue_importer.import_catalogue_master",
            "backend/tests/test_master_importers.py::test_catalogue_master_has_exact_812_unique_rows",
        ),
        (
            "ECONOMY_3D",
            economy,
            "academy_economy_master",
            "services.economy_importer.import_economy_master",
            "backend/tests/test_master_importers.py::test_economy_master_has_exact_812_unique_rows",
        ),
    ):
        for row in rows:
            base = _base_requirement(
                family=family,
                row=row,
                collection=collection,
                importer=importer,
                test_ref=test_ref,
            )
            requirement_id = base["requirement_id"]
            existing = await db.academy_requirement_registry.find_one(
                {"requirement_id": requirement_id}
            )
            doc, unset_fields = merge_ingested_requirement(base, existing)

            if existing and existing.get("verified") is True:
                if existing.get("source_hash") == base["source_hash"]:
                    preserved_verified += 1
                else:
                    invalidated += 1

            update: dict[str, Any] = {"$set": doc}
            if unset_fields:
                update["$unset"] = {field: "" for field in unset_fields}
            await db.academy_requirement_registry.update_one(
                {"requirement_id": requirement_id}, update, upsert=True
            )
            written += 1

    await db.academy_requirement_registry.create_index("requirement_id", unique=True)
    await db.academy_requirement_registry.create_index([("family", 1), ("code", 1)])
    return {
        "requirements": written,
        "catalogue": len(catalogue),
        "economy": len(economy),
        "preserved_verified": preserved_verified,
        "invalidated": invalidated,
    }


async def requirement_summary(db: Any) -> dict[str, int]:
    total = await db.academy_requirement_registry.count_documents({})
    verified = await db.academy_requirement_registry.count_documents({"verified": True})
    ingested = await db.academy_requirement_registry.count_documents(
        {"status": "INGESTED_RUNTIME"}
    )
    return {
        "total": total,
        "verified": verified,
        "ingested_runtime": ingested,
        "unverified": total - verified,
    }


async def promote_verified(
    db: Any,
    requirement_id: str,
    *,
    evidence_ref: str,
    actor_id: str,
) -> dict[str, Any]:
    """Promote only when a concrete evidence reference is supplied."""
    if not evidence_ref.strip():
        raise ValueError("evidence_ref is required to mark a requirement VERIFIED")
    result = await db.academy_requirement_registry.update_one(
        {"requirement_id": requirement_id, "status": "INGESTED_RUNTIME"},
        {
            "$set": {
                "status": "VERIFIED",
                "verified": True,
                "verification_evidence": evidence_ref.strip(),
                "verified_by": actor_id,
            }
        },
    )
    if not getattr(result, "matched_count", 0):
        raise LookupError(f"requirement not found or not eligible: {requirement_id}")
    return await db.academy_requirement_registry.find_one(
        {"requirement_id": requirement_id}, {"_id": 0}
    )
