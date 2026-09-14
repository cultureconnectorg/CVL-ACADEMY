from __future__ import annotations

import pytest
from mongomock_motor import AsyncMongoMockClient

from services import expert_access
from services import expert_cost_ledger
from services import governance_notifications
from services import professional_governance
from services import professional_workspace


@pytest.fixture
async def governance_db(monkeypatch):
    client = AsyncMongoMockClient()
    test_db = client["cvln_governance_advanced_test"]
    for module in (
        expert_access,
        expert_cost_ledger,
        governance_notifications,
        professional_governance,
        professional_workspace,
    ):
        monkeypatch.setattr(module, "db", test_db)
    yield test_db
    client.close()


async def _assigned_case():
    case = await professional_governance.create_case(
        actor_id="admin",
        title="Legal review",
        domain="LEGAL",
        description="Scoped case",
    )
    expert = await professional_governance.create_expert(
        actor_id="admin",
        display_name="Counsel",
        email="counsel@example.test",
        domains=["LEGAL"],
    )
    assignment = await professional_governance.assign_expert(
        actor_id="admin",
        case_id=case["id"],
        expert_id=expert["id"],
        scope=["case:read", "legal:matter:write"],
    )
    raw, _ = await professional_governance.issue_expert_api_key(
        actor_id="admin",
        assignment_id=assignment["id"],
        expires_at="2099-09-10T00:00:00+00:00",
    )
    return case, expert, raw


@pytest.mark.asyncio
async def test_workspace_is_case_scoped(governance_db):
    case, _, raw = await _assigned_case()
    other = await professional_governance.create_case(
        actor_id="admin",
        title="Other",
        domain="LEGAL",
        description="Not assigned",
    )
    workspace = await professional_workspace.get_workspace(raw_key=raw, case_id=case["id"])
    assert workspace["case"]["id"] == case["id"]
    assert workspace["global_browse"] is False
    with pytest.raises(PermissionError, match="not assigned"):
        await professional_workspace.get_workspace(raw_key=raw, case_id=other["id"])


@pytest.mark.asyncio
async def test_cost_ledger_requires_assignment_and_real_baseline(governance_db):
    case, expert, _ = await _assigned_case()
    entry = await expert_cost_ledger.record_cost(
        actor_id="admin",
        case_id=case["id"],
        expert_id=expert["id"],
        intervention_type="review",
        hours=2,
        amount_cents=20000,
        currency="EUR",
        evidence_refs=["INV-EXT-1"],
        baseline_without_core_hours=5,
        baseline_hourly_rate_cents=10000,
    )
    assert entry["baseline_external_cost_cents"] == 50000
    assert entry["estimated_cost_avoided_cents"] == 30000
    summary = await expert_cost_ledger.case_cost_summary(case["id"])
    assert summary["totals"]["external_cost_cents"] == 20000
    assert summary["totals"]["estimated_cost_avoided_cents"] == 30000


@pytest.mark.asyncio
async def test_cost_ledger_does_not_invent_missing_baseline(governance_db):
    case, expert, _ = await _assigned_case()
    entry = await expert_cost_ledger.record_cost(
        actor_id="admin",
        case_id=case["id"],
        expert_id=expert["id"],
        intervention_type="review",
        hours=1,
        amount_cents=10000,
        currency="EUR",
        evidence_refs=["INV-EXT-2"],
    )
    assert entry["baseline_external_cost_cents"] is None
    assert entry["estimated_cost_avoided_cents"] is None


@pytest.mark.asyncio
async def test_platform_notification_has_real_local_receipt(governance_db):
    result = await governance_notifications.route_notification(
        actor_id="admin",
        subject_id="CASE-1",
        kind="deadline",
        payload={"message": "review due"},
        criticality="INFO",
        channels=["PLATFORM"],
    )
    assert result["results"][0]["status"] == "DELIVERED_LOCAL"
    receipt = await governance_db.platform_notifications.find_one(
        {"id": result["results"][0]["receipt_id"]}
    )
    assert receipt is not None


@pytest.mark.asyncio
async def test_whatsapp_without_provider_never_claims_sent(governance_db, monkeypatch):
    monkeypatch.delenv("WHATSAPP_PROVIDER_URL", raising=False)
    result = await governance_notifications.route_notification(
        actor_id="admin",
        subject_id="CASE-1",
        kind="critical",
        payload={"message": "action"},
        criticality="CRITICAL",
        phone="+0000000000",
        channels=["WHATSAPP"],
    )
    assert result["results"][0]["status"] == "NOT_CONFIGURED"
    assert result["results"][0]["receipt_id"] is None
