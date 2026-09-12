from __future__ import annotations

import json
from types import SimpleNamespace

import pytest
from mcp import Client

import mcp_server
from expert_directory import get_expert, list_experts, route_experts
from mcp_server import academy_mcp


class FakeCursor:
    def __init__(self, docs):
        self.docs = docs
        self._limit = len(docs)

    def limit(self, value):
        self._limit = value
        return self

    async def to_list(self, length):
        return self.docs[: min(length, self._limit)]


class FakeCollection:
    def __init__(self, docs):
        self.docs = docs
        self.last_filter = None

    def find(self, mongo_filter, projection):
        self.last_filter = mongo_filter
        return FakeCursor(self.docs)

    async def find_one(self, mongo_filter, projection):
        self.last_filter = mongo_filter
        for doc in self.docs:
            if doc.get("code") == mongo_filter.get("code") and doc.get("content_status") == "published":
                return dict(doc)
        return None


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
async def test_mcp_mongo_backed_tools_and_dynamic_resource(monkeypatch):
    formation = {
        "code": "MUS-101",
        "name": "Production musicale",
        "pole": "music",
        "pole_name": "Musique",
        "content_status": "published",
        "description": "Studio et production",
        "duration_h": 35,
        "modules": [{"name": "Session studio"}],
        "cartography": {"primary_job": "Producteur musical", "delivery_formats": ["presentiel"]},
    }
    fake_formations = FakeCollection([formation])
    fake_poles = FakeCollection([{"code": "music", "name": "Musique"}])
    monkeypatch.setattr(
        mcp_server,
        "db",
        SimpleNamespace(formations=fake_formations, poles=fake_poles),
    )

    async with Client(academy_mcp) as client:
        poles = await client.call_tool("list_poles", {"limit": 5})
        assert not poles.is_error
        poles_payload = json.dumps(poles.model_dump(mode="json"), ensure_ascii=False)
        assert "Musique" in poles_payload

        search = await client.call_tool(
            "search_formations",
            {"query": "production", "pole": "music", "limit": 10},
        )
        assert not search.is_error
        search_payload = json.dumps(search.model_dump(mode="json"), ensure_ascii=False)
        assert "MUS-101" in search_payload
        assert "Production musicale" in search_payload
        assert fake_formations.last_filter["content_status"] == "published"

        detail = await client.call_tool("get_formation", {"code": "MUS-101"})
        assert not detail.is_error
        detail_payload = json.dumps(detail.model_dump(mode="json"), ensure_ascii=False)
        assert "MUS-101" in detail_payload
        assert "commercialization" in detail_payload

        resource = await client.read_resource("academy://formations/MUS-101")
        resource_payload = json.dumps(resource.model_dump(mode="json"), ensure_ascii=False)
        assert "MUS-101" in resource_payload
        assert "Production musicale" in resource_payload


@pytest.mark.asyncio
async def test_mcp_never_exposes_unpublished_formation(monkeypatch):
    unpublished = {
        "code": "DRAFT-1",
        "name": "Draft programme",
        "content_status": "draft",
    }
    fake_formations = FakeCollection([unpublished])
    monkeypatch.setattr(
        mcp_server,
        "db",
        SimpleNamespace(formations=fake_formations, poles=FakeCollection([])),
    )

    async with Client(academy_mcp) as client:
        detail = await client.call_tool("get_formation", {"code": "DRAFT-1"})
        assert not detail.is_error
        payload = json.dumps(detail.model_dump(mode="json"), ensure_ascii=False)
        assert '"found": false' in payload.lower()


def test_expert_registry_has_stable_ids_and_statuses():
    experts = list_experts()
    ids = [expert["id"] for expert in experts]
    assert len(ids) == len(set(ids))
    assert {expert["status"] for expert in experts}.issubset({"active", "planned"})
    assert get_expert("formation")["status"] == "active"
    assert get_expert("funding")["status"] == "active"
    assert get_expert("funding")["access"] == "private_oauth"
    assert get_expert("does-not-exist") is None


def test_expert_router_is_deterministic_and_bounded():
    first = route_experts("Je cherche une formation en musique et studio", limit=3)
    second = route_experts("Je cherche une formation en musique et studio", limit=3)
    assert first == second
    assert 1 <= len(first) <= 3
    assert any(expert["id"] == "music" for expert in first)

    bounded = route_experts("formation musique cinema ia support certification", limit=999)
    assert len(bounded) <= 5
