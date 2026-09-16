from __future__ import annotations

import json
from types import SimpleNamespace

import pytest
from mcp import Client

import mcp_server
from expert_directory import get_expert, list_experts, route_experts
from fms_canonical.models import CanonicalFormation
from frk_canonical.models import CanonicalFrkFormation
from klt_canonical.models import CanonicalKltFormation
from kor_canonical.models import CanonicalKorFormation
from mcp_server import academy_mcp


async def _empty_list(**_kwargs):
    return []


async def _empty_authority_map():
    return {}


@pytest.fixture(autouse=True)
def _stub_canonical_layer_by_default(monkeypatch):
    """Every canonical domain call defaults to "nothing imported" (empty
    list / empty authority map) unless a test explicitly overrides it.

    Without this, get_formation/search_formations's unconditional calls
    into fms_canonical/klt_canonical/kor_canonical/frk_canonical (via
    services.canonical_convergence) hit a real, unmocked Motor client in
    any test that only patches `mcp_server.db` for the legacy path (e.g.
    test_mcp_never_exposes_unpublished_formation) — CI's mcp-ci.yml job
    runs this file with no MOCK_DB and no real mongod, so that real call
    surfaces as `RuntimeError: Event loop is closed` deep in motor's
    asyncio executor rather than a clean, obviously-related failure.
    Stubbing the canonical layer here is itself a real, honest default —
    it matches the actual state of an environment where no canonical
    corpus has been imported yet, never fabricated data."""
    monkeypatch.setattr(mcp_server.fms_canonical, "list_canonical_formations", _empty_list)
    monkeypatch.setattr(mcp_server.klt_canonical, "list_canonical_klt_formations", _empty_list)
    monkeypatch.setattr(mcp_server.kor_canonical, "list_canonical_kor_formations", _empty_list)
    monkeypatch.setattr(mcp_server.frk_canonical, "list_canonical_frk_formations", _empty_list)
    monkeypatch.setattr(mcp_server, "get_canonical_authority_map", _empty_authority_map)


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


@pytest.mark.asyncio
async def test_search_formations_prefers_canonical_over_legacy_beatmaking(monkeypatch):
    """Regression for the reported bug: a query matching a legacy formation
    that HAS a real canonical replacement (FMS-03 "Beatmaking") must return
    the canonical formation, never the bare legacy db.formations doc —
    CANONICAL_CURRICULUM_RUNTIME=AUTHORITATIVE (ACA-0019) applies on the
    MCP surface exactly as it already does on the rest of the app."""
    legacy_beatmaking = {
        "code": "FMS-03",
        "name": "Beatmaking & Production musicale",
        "pole": "FMS",
        "content_status": "published",
        "description": "Ancienne fiche non calibrée",
        "calibration_confidence": "low",
    }
    fake_formations = FakeCollection([legacy_beatmaking])
    monkeypatch.setattr(
        mcp_server, "db", SimpleNamespace(formations=fake_formations, poles=FakeCollection([]))
    )

    canonical_fms03 = CanonicalFormation(
        canonical_formation_code="FMS-03",
        metier_number="03",
        metier_name="Beatmaking & Production Musicale",
        module_codes_in_order=["FMS03-M01", "FMS03-M02"],
        module_count=2,
    )

    async def fake_fms_list(**_kwargs):
        return [canonical_fms03]

    async def fake_authority_map():
        return {"FMS-03": {"domain": "FMS", "route": "/canonical/FMS-03"}}

    monkeypatch.setattr(mcp_server.fms_canonical, "list_canonical_formations", fake_fms_list)
    monkeypatch.setattr(mcp_server.klt_canonical, "list_canonical_klt_formations", _empty_list)
    monkeypatch.setattr(mcp_server.kor_canonical, "list_canonical_kor_formations", _empty_list)
    monkeypatch.setattr(mcp_server.frk_canonical, "list_canonical_frk_formations", _empty_list)
    monkeypatch.setattr(mcp_server, "get_canonical_authority_map", fake_authority_map)

    async with Client(academy_mcp) as client:
        result = await client.call_tool("search_formations", {"query": "beatmaking", "limit": 10})
        assert not result.is_error
        items = result.structured_content["result"]["items"]
        assert len(items) == 1, f"expected exactly one Beatmaking result, got {items}"
        assert items[0]["code"] == "FMS-03"
        assert items[0]["pedagogical_source"] == "CANONICAL"
        assert items[0]["name"] == "Beatmaking & Production Musicale"


@pytest.mark.asyncio
async def test_get_formation_returns_canonical_not_legacy_for_superseded_code(monkeypatch):
    legacy_beatmaking = {
        "code": "FMS-03",
        "name": "Beatmaking & Production musicale",
        "content_status": "published",
    }
    fake_formations = FakeCollection([legacy_beatmaking])
    monkeypatch.setattr(
        mcp_server, "db", SimpleNamespace(formations=fake_formations, poles=FakeCollection([]))
    )

    canonical_fms03 = CanonicalFormation(
        canonical_formation_code="FMS-03",
        metier_number="03",
        metier_name="Beatmaking & Production Musicale",
        module_codes_in_order=["FMS03-M01"],
        module_count=1,
    )

    async def fake_fms_list(**_kwargs):
        return [canonical_fms03]

    async def fake_authority_map():
        return {"FMS-03": {"domain": "FMS", "route": "/canonical/FMS-03"}}

    monkeypatch.setattr(mcp_server.fms_canonical, "list_canonical_formations", fake_fms_list)
    monkeypatch.setattr(mcp_server.klt_canonical, "list_canonical_klt_formations", _empty_list)
    monkeypatch.setattr(mcp_server.kor_canonical, "list_canonical_kor_formations", _empty_list)
    monkeypatch.setattr(mcp_server.frk_canonical, "list_canonical_frk_formations", _empty_list)
    monkeypatch.setattr(mcp_server, "get_canonical_authority_map", fake_authority_map)

    async with Client(academy_mcp) as client:
        detail = await client.call_tool("get_formation", {"code": "FMS-03"})
        assert not detail.is_error
        formation = detail.structured_content["result"]["formation"]
        assert formation["pedagogical_source"] == "CANONICAL"
        assert formation["name"] == "Beatmaking & Production Musicale"


@pytest.mark.asyncio
async def test_search_formations_covers_fms_klt_kor_frk_canonical_domains(monkeypatch):
    monkeypatch.setattr(
        mcp_server, "db", SimpleNamespace(formations=FakeCollection([]), poles=FakeCollection([]))
    )

    async def fake_authority_map():
        return {}

    fms_item = CanonicalFormation(
        canonical_formation_code="FMS-01",
        metier_number="01",
        metier_name="Artist Development",
        module_count=3,
    )
    klt_item = CanonicalKltFormation(
        klt_formation_code="KLT-06",
        title="Analyste Observatory",
        structural_status="PARTIAL",
        fully_complete=False,
        contexts=["observatoire"],
        module_count=5,
    )
    kor_item = CanonicalKorFormation(
        kor_formation_code="KOR-01",
        title="Podcast & Audio Production",
        fully_complete=True,
        contexts=["podcast"],
        module_count=4,
    )
    frk_item = CanonicalFrkFormation(
        frk_formation_code="FRK-01",
        title="Culture Connect Operator",
        status="PACKAGE_COMPLETE",
        fully_complete=True,
        module_count=6,
    )

    monkeypatch.setattr(mcp_server.fms_canonical, "list_canonical_formations", lambda **_k: _one(fms_item))
    monkeypatch.setattr(mcp_server.klt_canonical, "list_canonical_klt_formations", lambda **_k: _one(klt_item))
    monkeypatch.setattr(mcp_server.kor_canonical, "list_canonical_kor_formations", lambda **_k: _one(kor_item))
    monkeypatch.setattr(mcp_server.frk_canonical, "list_canonical_frk_formations", lambda **_k: _one(frk_item))
    monkeypatch.setattr(mcp_server, "get_canonical_authority_map", fake_authority_map)

    async with Client(academy_mcp) as client:
        result = await client.call_tool("search_formations", {"limit": 20})
        assert not result.is_error
        items = result.structured_content["result"]["items"]
        codes = {item["code"] for item in items}
        assert {"FMS-01", "KLT-06", "KOR-01", "FRK-01"}.issubset(codes)
        sources = {item["code"]: item["pedagogical_source"] for item in items}
        assert sources["FMS-01"] == "CANONICAL"
        assert sources["KLT-06"] == "CANONICAL_KLT"
        assert sources["KOR-01"] == "CANONICAL_KOR"
        assert sources["FRK-01"] == "CANONICAL_FRK"


async def _one(item):
    return [item]


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
