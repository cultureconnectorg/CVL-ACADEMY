from __future__ import annotations

import pytest

from services.agent_factory import AgentFactoryClient
from services.ai_data_policy import (
    OUTBOUND_HISTORY_LIMIT,
    policy_status,
    prepare_outbound_conversation,
    pseudonymise_session,
    redact_text,
    sanitise_history,
)


def test_redact_text_removes_provider_unnecessary_identifiers():
    source = (
        "contact maya@example.com FREK-ABCD-1234 "
        "Bearer abcdefghijklmnop sk-abcdefghijklmnop1234"
    )

    redacted = redact_text(source)

    assert "maya@example.com" not in redacted
    assert "FREK-ABCD-1234" not in redacted
    assert "abcdefghijklmnop" not in redacted
    assert "sk-abcdefghijklmnop1234" not in redacted
    assert "[redacted-email]" in redacted
    assert "[redacted-frek-id]" in redacted


def test_generic_frek_id_label_is_not_destroyed():
    assert redact_text("Le FREK-ID reste dans CVLN") == "Le FREK-ID reste dans CVLN"


def test_history_is_minimized_redacted_and_metadata_is_dropped():
    history = [
        {
            "role": "user",
            "content": f"message-{index} person{index}@example.com",
            "ts": "private-timestamp",
            "user_id": f"user-{index}",
        }
        for index in range(OUTBOUND_HISTORY_LIMIT + 5)
    ]

    clean = sanitise_history(history)

    assert len(clean) == OUTBOUND_HISTORY_LIMIT
    assert clean[0]["content"].startswith("message-5")
    assert all(set(item) == {"role", "content"} for item in clean)
    assert all("@example.com" not in item["content"] for item in clean)


def test_prepare_outbound_conversation_applies_same_policy_everywhere():
    system, message, history = prepare_outbound_conversation(
        "Utilisateur FREK-AAAA-9999",
        "Mon email est user@example.com",
        [{"role": "assistant", "content": "Bearer abcdefghijklmnop"}],
    )

    assert "FREK-AAAA-9999" not in system
    assert "user@example.com" not in message
    assert "abcdefghijklmnop" not in history[0]["content"]


def test_session_pseudonym_is_stable_and_not_raw(monkeypatch):
    monkeypatch.setenv("AI_PSEUDONYMIZATION_KEY", "test-key-that-never-leaves-cvln")

    first = pseudonymise_session("student-session-123")
    second = pseudonymise_session("student-session-123")
    other = pseudonymise_session("student-session-456")

    assert first == second
    assert first != other
    assert "student-session-123" not in first
    assert first.startswith("ai_")


def test_policy_status_exposes_no_secret(monkeypatch):
    monkeypatch.setenv("ACADEMY_ENV", "production")
    monkeypatch.setenv("AI_PSEUDONYMIZATION_KEY", "super-secret-pseudonym-key")

    status = policy_status()

    assert status["enabled"] is True
    assert status["canonical_identity_exported"] is False
    assert status["session_ids_pseudonymised"] is True
    assert status["production_key_ready"] is True
    assert "super-secret-pseudonym-key" not in str(status)


@pytest.mark.asyncio
async def test_mentor_does_not_inject_name_or_frek_id(monkeypatch):
    client = AgentFactoryClient()
    captured = {}

    async def fake_chat_reply(system_prompt, session_id, message, history):
        captured.update(
            {
                "system_prompt": system_prompt,
                "session_id": session_id,
                "message": message,
                "history": history,
            }
        )
        return "ok"

    monkeypatch.setattr(client, "chat_reply", fake_chat_reply)

    result = await client.mentor_reply(
        user_frek_id="FREK-AAAA-9999",
        display_name="Maya Example",
        session_id="mentor-session",
        message="Aide-moi",
        history=[],
        lang="fr",
    )

    assert result == "ok"
    assert "Maya Example" not in captured["system_prompt"]
    assert "FREK-AAAA-9999" not in captured["system_prompt"]
    assert "Langue préférée: fr" in captured["system_prompt"]
