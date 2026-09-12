from __future__ import annotations

import pytest

from services import agent_factory as agent_factory_module
from services import nvidia_runtime
from services.nvidia_runtime import (
    DynamoClient,
    DynamoConfigurationError,
    NvidiaAccelerationError,
    accelerated_group_count,
)


def test_small_workload_stays_on_cpu():
    counts, engine, reason = accelerated_group_count(
        [{"segment": "A"}, {"segment": "A"}, {"segment": "B"}],
        "segment",
    )

    assert counts == {"A": 2, "B": 1}
    assert engine == "python"
    assert reason == "below-gpu-threshold"


def test_required_gpu_fails_closed_when_runtime_is_unavailable(monkeypatch):
    monkeypatch.setattr(
        nvidia_runtime,
        "_nvidia_smi_status",
        lambda: {
            "detected": False,
            "driver_version": None,
            "gpus": [],
            "reason": "test-no-gpu",
        },
    )
    monkeypatch.setattr(
        nvidia_runtime,
        "_cudf_status",
        lambda: {
            "installed": False,
            "version": None,
            "importable": False,
            "reason": "test-no-cudf",
        },
    )

    with pytest.raises(NvidiaAccelerationError):
        accelerated_group_count(
            [{"segment": "A"}],
            "segment",
            min_rows=0,
            require_gpu=True,
        )


def test_gpu_unavailable_falls_back_without_false_gpu_claim(monkeypatch):
    monkeypatch.setattr(
        nvidia_runtime,
        "_nvidia_smi_status",
        lambda: {
            "detected": False,
            "driver_version": None,
            "gpus": [],
            "reason": "test-no-gpu",
        },
    )
    monkeypatch.setattr(
        nvidia_runtime,
        "_cudf_status",
        lambda: {
            "installed": False,
            "version": None,
            "importable": False,
            "reason": "test-no-cudf",
        },
    )

    counts, engine, reason = accelerated_group_count(
        [{"segment": "A"}, {"segment": "B"}],
        "segment",
        min_rows=0,
    )

    assert counts == {"A": 1, "B": 1}
    assert engine == "python"
    assert reason == "test-no-cudf"


def test_jetson_flag_never_fakes_device_detection(monkeypatch):
    monkeypatch.setenv("JETSON_EDGE_MODE", "true")
    monkeypatch.setattr(nvidia_runtime, "_read_text", lambda path: "")

    status = nvidia_runtime._jetson_status()

    assert status["requested"] is True
    assert status["detected"] is False
    assert status["active"] is False
    assert status["reason"] == "edge-mode-requested-but-jetson-not-detected"


def test_dynamo_status_redacts_url_credentials(monkeypatch):
    monkeypatch.setenv(
        "NVIDIA_DYNAMO_BASE_URL",
        "https://academy-user:secret@dynamo.internal:8443/private",
    )
    monkeypatch.setenv("NVIDIA_DYNAMO_MODEL", "academy-model")
    client = DynamoClient()

    status = client.status()

    assert status["configured"] is True
    assert status["base_url"] == "https://dynamo.internal:8443"
    assert "secret" not in str(status)
    assert "academy-user" not in str(status)


def test_dynamo_endpoint_is_openai_compatible(monkeypatch):
    monkeypatch.setenv("NVIDIA_DYNAMO_BASE_URL", "http://dynamo:8000/")
    monkeypatch.setenv("NVIDIA_DYNAMO_MODEL", "academy-model")
    monkeypatch.delenv("NVIDIA_DYNAMO_CHAT_PATH", raising=False)
    client = DynamoClient()

    assert client._endpoint() == "http://dynamo:8000/v1/chat/completions"


def test_dynamo_rejects_non_http_endpoint(monkeypatch):
    monkeypatch.setenv("NVIDIA_DYNAMO_BASE_URL", "ftp://dynamo.internal")
    monkeypatch.setenv("NVIDIA_DYNAMO_MODEL", "academy-model")
    client = DynamoClient()

    assert client.is_configured() is False
    assert client.status()["base_url"] is None
    with pytest.raises(DynamoConfigurationError):
        client._endpoint()


@pytest.mark.asyncio
async def test_dynamo_reuses_and_closes_http_connection_pool(monkeypatch):
    monkeypatch.setenv("NVIDIA_DYNAMO_BASE_URL", "http://dynamo:8000")
    monkeypatch.setenv("NVIDIA_DYNAMO_MODEL", "academy-model")
    client = DynamoClient()

    first = client._http_client()
    second = client._http_client()

    assert first is second
    assert client.status()["connection_pool_initialized"] is True

    await client.aclose()

    assert client.status()["connection_pool_initialized"] is False


@pytest.mark.asyncio
async def test_assistant_transport_reaches_dynamo(monkeypatch):
    calls = []

    async def fake_dynamo_reply(**kwargs):
        calls.append(kwargs)
        return "dynamo-ok"

    monkeypatch.setattr(agent_factory_module, "AI_TRANSPORT", "dynamo")
    monkeypatch.setattr(agent_factory_module, "AI_STRICT", True)
    monkeypatch.setattr(
        agent_factory_module.nvidia_dynamo, "chat_reply", fake_dynamo_reply
    )

    client = agent_factory_module.AgentFactoryClient()
    result = await client.chat_reply(
        "system",
        "session-1",
        "message",
        [{"role": "user", "content": "before"}],
    )

    assert result == "dynamo-ok"
    assert len(calls) == 1
    assert calls[0]["session_id"] == "session-1"
    assert calls[0]["message"] == "message"


def test_remote_agent_factory_configuration_is_not_reported_active(monkeypatch):
    monkeypatch.setattr(
        agent_factory_module, "CVLN_AGENT_FACTORY_URL", "https://factory.example"
    )
    client = agent_factory_module.AgentFactoryClient()

    status = client.remote_status()

    assert status["configured"] is True
    assert status["active"] is False
    assert status["contract_implemented"] is False
