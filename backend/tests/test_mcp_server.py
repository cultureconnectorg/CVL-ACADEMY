from __future__ import annotations

import json
from types import SimpleNamespace

import pytest
from mcp import Client

import mcp_server
from expert_directory import get_expert, list_experts, route_experts
from mcp_server import academy_mcp


@pytest.mark.asyncio
async def test_mcp_discovers_expected_surface():
    async with Client(academy_mcp) as client:
        tools = await client.list_tools()
        tool_names = {tool.name for tool in tools.tools}
        assert {
            "academy_capabilities",
            "list_experts",
            "get_expert",
            "route_expert",
            "list_poles",
            "search_formations",
            "get_formation",
        }.issubset(tool_names)

        for tool in tools.tools:
            if tool.name in tool_names:
                assert tool.annotations is not None
                assert tool.annotations.read_only_hint is True
                assert tool.annotations.destructive_hint is False
                assert tool.annotations.open_world_hint is False

        resources = await client.list_resources()
        resource_uris = {str(resource.uri) for resource in resources.resources}
        assert "academy://about" in resource_uris
        assert "academy://experts" in resource_uris

        prompts = await client.list_prompts()
        prompt_names = {prompt.name for prompt in prompts.prompts}
        assert {"recommend_training", "academy_expert_assist"}.issubset(prompt_names)


@pytest.mark.asyncio
async def test_mcp_static_tool_and_resource_are_callable():
    async with Client(academy_mcp) as client:
        result = await client.call_tool("academy_capabilities", {})
        assert not result.is_error
        payload = json.dumps(result.model_dump(mode="json"), ensure_ascii=False)
        assert "CVLN Academy" in payload
        assert "public-read-only" in payload
        assert "expert_directory" in payload

        experts = await client.call_tool("list_experts", {"status": "active"})
        assert not experts.is_error
        experts_payload = json.dumps(experts.model_dump(mode="json"), ensure_ascii=False)
        assert "orientation" in experts_payload
        assert "laurentia" in experts_payload

        resource = await client.read_resource("academy://about")
        resource_payload = json.dumps(resource.model_dump(mode="json"), ensure_ascii=False)
        assert "CVLN Academy" in resource_payload
        assert "/mcp" in resource_payload

        expert_resource = await client.read_resource("academy://experts")
        expert_payload = json.dumps(expert_resource.model_dump(mode="json"), ensure_ascii=False)
        assert "Financement" in expert_payload
        assert "planned" in expert_payload


@pytest.mark.asyncio
async def test_dynamic_formation_tool_and_resource_share_published_lookup(monkeypatch):
    formation = {
        "code": "FMS-A",
        "name": "Artist Development",
        "content_status": "published",
        "modules": [{"name": "Direction artistique"}],
    }

    class FakeFormations:
        async def find_one(self, query, projection):
            assert query == {"code": "FMS-A", "content_status": "published"}
            assert projection == {"_id": 0}
            return dict(formation)

    monkeypatch.setattr(mcp_server, "db", SimpleNamespace(formations=FakeFormations()))
    monkeypatch.setattr(
        mcp_server,
        "formation_commercialization",
        lambda doc: {"available": True, "code": doc["code"]},
    )

    async with Client(academy_mcp) as client:
        tool_result = await client.call_tool("get_formation", {"code": " FMS-A "})
        assert not tool_result.is_error
        tool_payload = json.dumps(tool_result.model_dump(mode="json"), ensure_ascii=False)
        assert "Artist Development" in tool_payload
        assert '"available": true' in tool_payload.lower()

        resource = await client.read_resource("academy://formations/FMS-A")
        resource_payload = json.dumps(resource.model_dump(mode="json"), ensure_ascii=False)
        assert "Artist Development" in resource_payload
        assert "published" in resource_payload


def test_expert_registry_has_stable_ids_and_statuses():
    experts = list_experts()
    ids = [expert["id"] for expert in experts]
    assert len(ids) == len(set(ids))
    assert {expert["status"] for expert in experts}.issubset({"active", "planned"})
    assert get_expert("formation")["status"] == "active"
    assert get_expert("funding")["status"] == "planned"
    assert get_expert("does-not-exist") is None


def test_expert_router_is_deterministic_and_bounded():
    first = route_experts("Je cherche une formation en musique et studio", limit=3)
    second = route_experts("Je cherche une formation en musique et studio", limit=3)
    assert first == second
    assert 1 <= len(first) <= 3
    assert any(expert["id"] == "music" for expert in first)

    bounded = route_experts("formation musique cinema ia support certification", limit=999)
    assert len(bounded) <= 5
