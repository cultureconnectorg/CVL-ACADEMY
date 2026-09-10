from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pytest
from mongomock_motor import AsyncMongoMockClient

from services import accounting_core, accounting_workspace, expert_access
from services import professional_governance as governance


@pytest.fixture
async def workspace_db(monkeypatch):
    client = AsyncMongoMockClient()
    test_db = client["cvln_accounting_workspace_test"]
    for module in (accounting_core, accounting_workspace, expert_access, governance):
        monkeypatch.setattr(module, "db", test_db)
    yield test_db
    client.close()


def _future() -> str:
    return (datetime.now(timezone.utc) + timedelta(days=2)).isoformat()


async def _accounting_key(workspace_db, period_id: str, scope=None):
    case = await governance.create_case(
        actor_id="admin",
        title="September accounting review",
        domain="ACCOUNTING",
        description="External accountant workspace",
        metadata={"accounting_period_ids": [period_id]},
    )
    expert = await governance.create_expert(
        actor_id="admin",
        display_name="External Accountant",
        email="accountant@example.test",
        domains=["ACCOUNTING"],
    )
    assignment = await governance.assign_expert(
        actor_id="admin",
        case_id=case["id"],
        expert_id=expert["id"],
        scope=scope or ["accounting:read"],
    )
    raw, _public = await governance.issue_expert_api_key(
        actor_id="admin",
        assignment_id=assignment["id"],
        expires_at=_future(),
    )
    return case, raw


@pytest.mark.asyncio
async def test_workspace_exposes_only_periods_explicitly_bound_to_assigned_case(workspace_db):
    september = await accounting_core.create_period(
        actor_id="admin",
        code="2026-09",
        starts_at="2026-09-01T00:00:00+00:00",
        ends_at="2026-10-01T00:00:00+00:00",
    )
    october = await accounting_core.create_period(
        actor_id="admin",
        code="2026-10",
        starts_at="2026-10-01T00:00:00+00:00",
        ends_at="2026-11-01T00:00:00+00:00",
    )
    case, raw = await _accounting_key(workspace_db, september["id"])

    await workspace_db.payments.insert_many(
        [
            {
                "id": "PAY-SEP",
                "created_at": "2026-09-10T10:00:00+00:00",
                "status": "pending",
            },
            {
                "id": "PAY-OCT",
                "created_at": "2026-10-10T10:00:00+00:00",
                "status": "pending",
            },
        ]
    )

    workspace = await accounting_workspace.get_workspace(raw_key=raw, case_id=case["id"])
    assert workspace["workspace_type"] == "ACADEMY_ACCOUNTING_ONLY"
    assert [row["id"] for row in workspace["periods"]] == [september["id"]]
    assert [row["id"] for row in workspace["payments"]] == ["PAY-SEP"]
    assert "PAY-OCT" not in [row["id"] for row in workspace["payments"]]
    assert october["id"] not in workspace["case"]["accounting_period_ids"]
    assert workspace["external_system_data"] is None


@pytest.mark.asyncio
async def test_workspace_fails_closed_without_accounting_scope(workspace_db):
    period = await accounting_core.create_period(
        actor_id="admin",
        code="2026-09",
        starts_at="2026-09-01T00:00:00+00:00",
        ends_at="2026-10-01T00:00:00+00:00",
    )
    case, raw = await _accounting_key(workspace_db, period["id"], scope=["case:read"])
    with pytest.raises(PermissionError, match="scope denied"):
        await accounting_workspace.get_workspace(raw_key=raw, case_id=case["id"])


@pytest.mark.asyncio
async def test_workspace_rejects_nonaccounting_case_even_with_scope(workspace_db):
    period = await accounting_core.create_period(
        actor_id="admin",
        code="2026-09",
        starts_at="2026-09-01T00:00:00+00:00",
        ends_at="2026-10-01T00:00:00+00:00",
    )
    case = await governance.create_case(
        actor_id="admin",
        title="Legal case",
        domain="LEGAL",
        description="Not accounting",
        metadata={"accounting_period_ids": [period["id"]]},
    )
    expert = await governance.create_expert(
        actor_id="admin",
        display_name="Expert",
        email="expert@example.test",
        domains=["LEGAL"],
    )
    assignment = await governance.assign_expert(
        actor_id="admin",
        case_id=case["id"],
        expert_id=expert["id"],
        scope=["accounting:read"],
    )
    raw, _public = await governance.issue_expert_api_key(
        actor_id="admin", assignment_id=assignment["id"], expires_at=_future()
    )
    with pytest.raises(PermissionError, match="not an accounting workspace"):
        await accounting_workspace.get_workspace(raw_key=raw, case_id=case["id"])


@pytest.mark.asyncio
async def test_workspace_requires_explicit_period_scope(workspace_db):
    case = await governance.create_case(
        actor_id="admin",
        title="Accounting case",
        domain="ACCOUNTING",
        description="No periods yet",
        metadata={},
    )
    expert = await governance.create_expert(
        actor_id="admin",
        display_name="Accountant",
        email="accountant2@example.test",
        domains=["ACCOUNTING"],
    )
    assignment = await governance.assign_expert(
        actor_id="admin",
        case_id=case["id"],
        expert_id=expert["id"],
        scope=["accounting:read"],
    )
    raw, _public = await governance.issue_expert_api_key(
        actor_id="admin", assignment_id=assignment["id"], expires_at=_future()
    )
    with pytest.raises(PermissionError, match="no explicit period scope"):
        await accounting_workspace.get_workspace(raw_key=raw, case_id=case["id"])
