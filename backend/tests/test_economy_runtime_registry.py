from __future__ import annotations

import pytest
from mongomock_motor import AsyncMongoMockClient

from services.economy_importer import load_economy_rows
from services.economy_runtime import runtime_decisions, set_gate_state, sync_economy_runtime_links
from services.requirement_registry import sync_master_requirements


@pytest.mark.asyncio
async def test_all_812_economy_requirements_are_runtime_linked():
    client = AsyncMongoMockClient()
    db = client["economy_registry_test"]
    await sync_master_requirements(db)
    result = await sync_economy_runtime_links(db)
    assert result == {"rows_linked": 812}

    docs = await db.academy_requirement_registry.find(
        {"family": "ECONOMY_3D"}, {"_id": 0}
    ).to_list(812)
    assert len(docs) == 812
    assert all(doc["runtime_handler"] == "services.economy_runtime.evaluate_runtime_row" for doc in docs)
    assert all("payments.service.create_checkout" in doc["runtime_surface"] for doc in docs)
    assert all(doc["runtime_test_ref"] == "backend/tests/test_economy_runtime_wiring.py" for doc in docs)


@pytest.mark.asyncio
async def test_gate_evidence_is_invalid_when_excel_source_hash_changes():
    client = AsyncMongoMockClient()
    db = client["economy_gate_hash_test"]
    row = next(row for row in load_economy_rows() if row["code"] == "KLT-09")
    await db.academy_economy_master.insert_one(dict(row))
    await set_gate_state(
        db,
        code="KLT-09",
        gate="ROLE_DEFINED",
        satisfied=True,
        evidence_ref="evidence:role-v1",
        actor_id="founder",
    )

    first = await runtime_decisions(db, ["KLT-09"])
    assert "ROLE_DEFINED" in first["KLT-09"]["runtime"]["satisfied_gates"]

    await db.academy_economy_master.update_one(
        {"code": "KLT-09"}, {"$set": {"source_hash": "changed-excel-row-hash"}}
    )
    second = await runtime_decisions(db, ["KLT-09"])
    assert "ROLE_DEFINED" not in second["KLT-09"]["runtime"]["satisfied_gates"]
    assert "ROLE_DEFINED" in second["KLT-09"]["runtime"]["missing_gates"]
