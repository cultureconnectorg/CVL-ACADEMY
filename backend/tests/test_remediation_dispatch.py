from __future__ import annotations

import pytest

from services import remediation_dispatch


@pytest.fixture
def remediation():
    return {
        "id": "REMED-1",
        "title": "Patch authorization boundary",
        "proposed_change": "Enforce scoped authorization at request boundary",
        "target_system": "CVLN_AGENT_FACTORY",
        "rollback_plan": "Restore previous deployment artifact",
        "test_plan": ["test_cross_case_denied", "test_allowed_case"],
    }


@pytest.mark.asyncio
async def test_agent_factory_dispatch_uses_orchestrate_then_mission(
    monkeypatch, remediation
):
    monkeypatch.setenv("CVLN_AGENT_FACTORY_URL", "https://factory.example")
    monkeypatch.setenv("CVLN_AGENT_FACTORY_SERVICE_TOKEN", "svc_test_only")
    calls = []

    async def fake_post(url, *, token, payload, timeout=10.0):
        calls.append((url, token, payload))
        if url.endswith("/missions/orchestrate"):
            return {
                "recommended_agents": [{"agent_id": "AGT-SEC"}],
                "draft_mission": {"agent_ids": ["AGT-FALLBACK"]},
            }
        if url.endswith("/missions"):
            return {
                "id": "MISSION-1",
                "agent_ids": payload["agent_ids"],
                "workflow_stage": "specification",
            }
        raise AssertionError(url)

    monkeypatch.setattr(remediation_dispatch, "_post_json", fake_post)
    result = await remediation_dispatch.dispatch_to_agent_factory(remediation)

    assert [call[0] for call in calls] == [
        "https://factory.example/missions/orchestrate",
        "https://factory.example/missions",
    ]
    assert all(call[1] == "svc_test_only" for call in calls)
    assert calls[1][2]["agent_ids"] == ["AGT-SEC"]
    assert calls[1][2]["origin_request"] == "REMED-1"
    assert result["remote_task_id"] == "MISSION-1"
    assert result["status"] == "DISPATCHED_CONFIRMED"


@pytest.mark.asyncio
async def test_agent_factory_rejects_orchestration_without_agent(
    monkeypatch, remediation
):
    monkeypatch.setenv("CVLN_AGENT_FACTORY_URL", "https://factory.example")
    monkeypatch.setenv("CVLN_AGENT_FACTORY_SERVICE_TOKEN", "svc_test_only")

    async def fake_post(url, *, token, payload, timeout=10.0):
        return {"recommended_agents": [], "draft_mission": {"agent_ids": []}}

    monkeypatch.setattr(remediation_dispatch, "_post_json", fake_post)
    with pytest.raises(remediation_dispatch.DispatchRejected, match="no eligible"):
        await remediation_dispatch.dispatch_to_agent_factory(remediation)


@pytest.mark.asyncio
async def test_agent_factory_never_confirms_mission_without_real_id(
    monkeypatch, remediation
):
    monkeypatch.setenv("CVLN_AGENT_FACTORY_URL", "https://factory.example")
    monkeypatch.setenv("CVLN_AGENT_FACTORY_SERVICE_TOKEN", "svc_test_only")

    async def fake_post(url, *, token, payload, timeout=10.0):
        if url.endswith("/missions/orchestrate"):
            return {"recommended_agents": [{"agent_id": "AGT-SEC"}]}
        return {"agent_ids": ["AGT-SEC"], "workflow_stage": "specification"}

    monkeypatch.setattr(remediation_dispatch, "_post_json", fake_post)
    with pytest.raises(remediation_dispatch.DispatchRejected, match="missing id"):
        await remediation_dispatch.dispatch_to_agent_factory(remediation)


@pytest.mark.asyncio
async def test_command_center_mirror_uses_real_tasks_contract(
    monkeypatch, remediation
):
    monkeypatch.setenv("CVLN_COMMAND_CENTER_URL", "https://command.example")
    monkeypatch.setenv("CVLN_COMMAND_CENTER_ACCESS_TOKEN", "jwt_test_only")
    captured = {}

    async def fake_post(url, *, token, payload, timeout=10.0):
        captured.update({"url": url, "token": token, "payload": payload})
        return {"id": "TASK-1", **payload, "created_by": "manager-1", "created_at": "x"}

    monkeypatch.setattr(remediation_dispatch, "_post_json", fake_post)
    result = await remediation_dispatch.mirror_to_command_center(remediation)

    assert captured["url"] == "https://command.example/api/tasks"
    assert captured["token"] == "jwt_test_only"
    assert captured["payload"]["priority"] == "high"
    assert captured["payload"]["status"] == "todo"
    assert "REMED-1" in captured["payload"]["description"]
    assert result["remote_task_id"] == "TASK-1"


@pytest.mark.asyncio
async def test_command_center_never_confirms_task_without_real_id(
    monkeypatch, remediation
):
    monkeypatch.setenv("CVLN_COMMAND_CENTER_URL", "https://command.example")
    monkeypatch.setenv("CVLN_COMMAND_CENTER_ACCESS_TOKEN", "jwt_test_only")

    async def fake_post(url, *, token, payload, timeout=10.0):
        return {"title": payload["title"]}

    monkeypatch.setattr(remediation_dispatch, "_post_json", fake_post)
    with pytest.raises(remediation_dispatch.DispatchRejected, match="missing id"):
        await remediation_dispatch.mirror_to_command_center(remediation)


@pytest.mark.asyncio
async def test_aggregate_dispatch_reports_missing_integrations_without_fake_success(
    monkeypatch, remediation
):
    for name in (
        "CVLN_AGENT_FACTORY_URL",
        "CVLN_AGENT_FACTORY_SERVICE_TOKEN",
        "CVLN_AGENT_FACTORY_API_KEY",
        "CVLN_COMMAND_CENTER_URL",
        "CVLN_COMMAND_CENTER_ACCESS_TOKEN",
        "CVLN_COMMAND_CENTER_API_KEY",
    ):
        monkeypatch.delenv(name, raising=False)

    result = await remediation_dispatch.dispatch_remediation(remediation)
    assert result["status"] == "FAILED"
    assert result["execution_dispatch_confirmed"] is False
    assert result["operations_mirror_confirmed"] is False
    assert result["results"]["agent_factory"]["status"] == "NOT_CONFIGURED"
    assert result["results"]["command_center"]["status"] == "NOT_CONFIGURED"
