"""Machine-readable Excel/master -> runtime proof registry.

The registry never equates documentation with implementation. Import into a
runtime collection is recorded as INGESTED_RUNTIME; VERIFIED requires an
explicit test/evidence promotion performed by CI or an authorised operator.
"""
from __future__ import annotations

from typing import Any

from services.catalogue_importer import load_catalogue_rows
from services.economy_importer import load_economy_rows


async def sync_master_requirements(db: Any) -> dict[str, int]:
    catalogue = load_catalogue_rows()
    economy = load_economy_rows()
    written = 0

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
            requirement_id = f"{family}:{row['code']}"
            doc = {
                "requirement_id": requirement_id,
                "family": family,
                "code": row["code"],
                "source": row["source"],
                "source_hash": row["source_hash"],
                "runtime_collection": collection,
                "runtime_key": {"code": row["code"]},
                "runtime_importer": importer,
                "test_ref": test_ref,
                "status": "INGESTED_RUNTIME",
                "verified": False,
            }
            await db.academy_requirement_registry.update_one(
                {"requirement_id": requirement_id}, {"$set": doc}, upsert=True
            )
            written += 1

    await db.academy_requirement_registry.create_index("requirement_id", unique=True)
    await db.academy_requirement_registry.create_index([("family", 1), ("code", 1)])
    return {"requirements": written, "catalogue": len(catalogue), "economy": len(economy)}


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
