from __future__ import annotations

from typing import Any

import pytest

import services.agent_factory as agent_factory_module
from services.agent_factory import AgentFactoryClient


class FakeResponse:
    def __init__(self, body: dict[str, Any]):
        self._body = body

    def raise_for_status(self) -> None:
        return None

    def json(self) -> dict[str, Any]:
        return self._body


class FakeAsyncClient:
    last_url: str | None = None
    last_json: dict[str, Any] | None = None
    last_headers: dict[str, str] | None = None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.timeout = kwargs.get("timeout")

    async def __aenter__(self) -> "FakeAsyncClient":
        return self

    async def __aexit__(self, *args: Any) -> None:
        return None

    async def post(
        self,
        url: str,
        *,
        json: dict[str, Any],
        headers: dict[str, str],
    ) -> FakeResponse:
        type(self).last_url = url
        type(self).last_json = json
        type(self).last_headers = headers
        return FakeResponse({"reply": "Réponse CVLN Agent Factory"})


@pytest.mark.asyncio
async def test_remote_factory_uses_real_cognitive_contract(monkeypatch):
    monkeypatch.setattr(
        agent_factory_module, "CVLN_AGENT_FACTORY_URL", "https://factory.cvln.test"
    )
    monkeypatch.setattr(agent_factory_module, "AGENT_FACTORY_API_KEY", "svc_test_token")
    monkeypatch.setattr(
        agent_factory_module, "AGENT_FACTORY_CHAT_PATH", "/api/cognitive/chat"
    )
    monkeypatch.setattr(agent_factory_module.httpx, "AsyncClient", FakeAsyncClient)

    client = AgentFactoryClient()
    reply = await client._agent_factory_chat_reply(
        system_prompt="Tu es le Mentor CVLN",
        session_ref="ai_opaque_session",
        message="Aide-moi à avancer",
        history=[{"role": "assistant", "content": "On continue."}],
    )

    assert reply == "Réponse CVLN Agent Factory"
    assert FakeAsyncClient.last_url == "https://factory.cvln.test/api/cognitive/chat"
    assert FakeAsyncClient.last_headers == {"Authorization": "Bearer svc_test_token"}
    assert FakeAsyncClient.last_json is not None
    assert FakeAsyncClient.last_json["conversation_id"] == "ai_opaque_session"
    assert FakeAsyncClient.last_json["disable_knowledge_search"] is False
    assert "Tu es le Mentor CVLN" in FakeAsyncClient.last_json["message"]
    assert "Aide-moi à avancer" in FakeAsyncClient.last_json["message"]


def test_remote_status_reports_contract_without_claiming_runtime_probe(monkeypatch):
    monkeypatch.setattr(
        agent_factory_module, "CVLN_AGENT_FACTORY_URL", "https://factory.cvln.test"
    )
    monkeypatch.setattr(agent_factory_module, "AGENT_FACTORY_API_KEY", "svc_test_token")
    monkeypatch.setattr(agent_factory_module, "AI_TRANSPORT", "agent_factory")

    status = AgentFactoryClient().remote_status()

    assert status["configured"] is True
    assert status["active"] is True
    assert status["contract_implemented"] is True
    assert status["endpoint"] == "/api/cognitive/chat"
    assert status["auth"] == "service-bearer-token"
    assert status["runtime_verified"] is False


@pytest.mark.asyncio
async def test_agent_factory_transport_receives_sanitised_payload(monkeypatch):
    monkeypatch.setattr(
        agent_factory_module, "CVLN_AGENT_FACTORY_URL", "https://factory.cvln.test"
    )
    monkeypatch.setattr(agent_factory_module, "AGENT_FACTORY_API_KEY", "svc_test_token")
    monkeypatch.setattr(agent_factory_module, "AI_TRANSPORT", "agent_factory")
    monkeypatch.setattr(agent_factory_module.httpx, "AsyncClient", FakeAsyncClient)

    client = AgentFactoryClient()
    reply = await client.chat_reply(
        "Utilisateur FREK-ABCD-1234",
        "raw-academy-session",
        "Contact user@example.com",
        [{"role": "user", "content": "Bearer abcdefghijklmnop"}],
    )

    assert reply == "Réponse CVLN Agent Factory"
    assert FakeAsyncClient.last_json is not None
    payload_text = FakeAsyncClient.last_json["message"]
    assert "FREK-ABCD-1234" not in payload_text
    assert "user@example.com" not in payload_text
    assert "abcdefghijklmnop" not in payload_text
    assert FakeAsyncClient.last_json["conversation_id"] != "raw-academy-session"
