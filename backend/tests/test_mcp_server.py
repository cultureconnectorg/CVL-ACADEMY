from __future__ import annotations

import json

import pytest
from mcp import Client

from mcp_server import academy_mcp


@pytest.mark.asyncio
async def test_mcp_discovers_expected_surface():
    async with Client(academy_mcp) as client:
        tools = await client.list_tools()
        tool_names = {tool.name for tool in tools.tools}
        assert {
            "academy_capabilities",
            "list_poles",
            "search_formations",
            "get_formation",
        }.issubset(tool_names)

        resources = await client.list_resources()
        resource_uris = {str(resource.uri) for resource in resources.resources}
        assert "academy://about" in resource_uris

        prompts = await client.list_prompts()
        prompt_names = {prompt.name for prompt in prompts.prompts}
        assert "recommend_training" in prompt_names


@pytest.mark.asyncio
async def test_mcp_static_tool_and_resource_are_callable():
    async with Client(academy_mcp) as client:
        result = await client.call_tool("academy_capabilities", {})
        assert not result.is_error
        payload = json.dumps(result.model_dump(mode="json"), ensure_ascii=False)
        assert "CVLN Academy" in payload
        assert "public-read-only" in payload

        resource = await client.read_resource("academy://about")
        resource_payload = json.dumps(resource.model_dump(mode="json"), ensure_ascii=False)
        assert "CVLN Academy" in resource_payload
        assert "/mcp" in resource_payload
