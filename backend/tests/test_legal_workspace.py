from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pytest
from mongomock_motor import AsyncMongoMockClient

from services import expert_access, legal_ops, legal_workspace
from services import professional_governance as governance


@pytest.fixture
async def workspace_db(monkeypatch):
    client = AsyncMongoMockClient()
    test_db = client["cvln_legal_workspace_test"]
    for module in (expert_access, legal_ops, legal_workspace, governance):
        monkeypatch.setattr(module, "db", test_db)
    yield test_db
    client.close()


async def _assignment(workspace_db, case_id: str, scope: list[str]):
    expert = await governance.create_expert(
        actor_id="admin-1",
        display_name="External Counsel",
        email="counsel@example.test",
        domains=["LEGAL"],
    )
    assignment = await governance.assign_expert(
        actor_id="admin-1",
        case_id=case_id,
        expert_id=expert["id"],
        scope=scope,
        authority_level="A3_EXTERNAL_EXPERT",
    )
    raw, _public = await governance.issue_expert_api_key(
        actor_id="admin-1",
        assignment_id=assignment["id"],
        expires_at=(datetime.now(timezone.utc) + timedelta(days=1)).isoformat(),
    )
    return expert, assignment, raw


@pytest.mark.asyncio
async def test_workspace_only_returns_assigned_case_records(workspace_db):
    case = await governance.create_case(
        actor_id="admin-1", title="Assigned", domain="LEGAL", description="Assigned case"
    )
    other = await governance.create_case(
        actor_id="admin-1", title="Other", domain="LEGAL", description="Other case"
    )
    _expert, assignment_row, raw = await _assignment(
        workspace_db, case["id"], ["legal:workspace:read"]
    )
    assert assignment_row["case_id"] == case["id"]
    own_matter = await legal_ops.create_legal_matter(
        actor_id="admin-1", title="Own", matter_type="CONTRACT", case_id=case["id"]
    )
    other_matter = await legal_ops.create_legal_matter(
        actor_id="admin-1", title="Other", matter_type="CONTRACT", case_id=other["id"]
    )
    await workspace_db.risks.insert_many(
        [
            {"id": "R1", "source_type": "LEGAL_MATTER", "source_id": own_matter["id"]},
            {"id": "R2", "source_type": "LEGAL_MATTER", "source_id": other_matter["id"]},
        ]
    )
    view = await legal_workspace.get_workspace(raw_key=raw, case_id=case["id"])
    assert [row["id"] for row in view["matters"]] == [own_matter["id"]]
    assert [row["id"] for row in view["risks"]] == ["R1"]
    assert view["case"]["id"] == case["id"]


@pytest.mark.asyncio
async def test_workspace_fails_closed_without_scope_or_assignment(workspace_db):
    case = await governance.create_case(
        actor_id="admin-1", title="Assigned", domain="LEGAL", description="Assigned case"
    )
    other = await governance.create_case(
        actor_id="admin-1", title="Other", domain="LEGAL", description="Other case"
    )
    _expert, assignment_row, raw = await _assignment(
        workspace_db, case["id"], ["case:read"]
    )
    assert assignment_row["case_id"] == case["id"]
    with pytest.raises(PermissionError, match="scope denied"):
        await legal_workspace.get_workspace(raw_key=raw, case_id=case["id"])
    with pytest.raises(PermissionError, match="not assigned"):
        await legal_workspace.get_workspace(raw_key=raw, case_id=other["id"])
