from __future__ import annotations

import pytest
from mongomock_motor import AsyncMongoMockClient

from services import professional_governance, risk_escalation


@pytest.fixture
async def risk_escalation_db(monkeypatch):
    client = AsyncMongoMockClient()
    test_db = client["cvln_risk_escalation_test"]
    for module in (risk_escalation, professional_governance):
        monkeypatch.setattr(module, "db", test_db)
    monkeypatch.delenv("CVLN_IOS_URL", raising=False)
    monkeypatch.delenv("CVLN_IOS_SERVICE_TOKEN", raising=False)
    yield test_db
    client.close()


@pytest.mark.asyncio
async def test_only_r5_requires_systemic_escalation(risk_escalation_db):
    await risk_escalation_db.risks.insert_one({"id": "RISK-4", "level": 4})
    with pytest.raises(ValueError, match="only to R5"):
        await risk_escalation.require_systemic_escalation(
            actor_id="risk", risk_id="RISK-4", rationale="not systemic", evidence_refs=["E-1"]
        )


@pytest.mark.asyncio
async def test_unconfigured_cvlnios_stays_pending_and_gate_blocks(risk_escalation_db):
    await risk_escalation_db.risks.insert_one(
        {"id": "RISK-5", "level": 5, "domain": "SECURITY", "title": "Systemic outage"}
    )
    escalation = await risk_escalation.require_systemic_escalation(
        actor_id="risk", risk_id="RISK-5", rationale="Systemic impact", evidence_refs=["E-5"]
    )
    dispatched = await risk_escalation.dispatch_to_cvlnios(
        actor_id="risk", escalation_id=escalation["id"]
    )
    assert dispatched["status"] == "PENDING_EXTERNAL"
    assert dispatched["last_dispatch_status"] == "NOT_CONFIGURED"
    gate = await risk_escalation.systemic_escalation_gate()
    assert gate["pass"] is False
    assert gate["blocking_risks"] == [{"risk_id": "RISK-5", "reason": "R5_CVLNIOS_ACK_MISSING"}]


@pytest.mark.asyncio
async def test_real_remote_receipt_is_required_for_acknowledgement(
    risk_escalation_db, monkeypatch
):
    await risk_escalation_db.risks.insert_one(
        {"id": "RISK-5", "level": 5, "domain": "RISK", "title": "Systemic risk"}
    )
    escalation = await risk_escalation.require_systemic_escalation(
        actor_id="risk", risk_id="RISK-5", rationale="R5", evidence_refs=["E-5"]
    )
    monkeypatch.setenv("CVLN_IOS_URL", "https://ios.example")
    monkeypatch.setenv("CVLN_IOS_SERVICE_TOKEN", "secret")

    class Response:
        status_code = 200
        def json(self):
            return {"status": "received"}

    class Client:
        async def __aenter__(self): return self
        async def __aexit__(self, *args): return None
        async def post(self, *args, **kwargs): return Response()

    monkeypatch.setattr(risk_escalation.httpx, "AsyncClient", lambda **kwargs: Client())
    result = await risk_escalation.dispatch_to_cvlnios(
        actor_id="risk", escalation_id=escalation["id"]
    )
    assert result["status"] == "PENDING_EXTERNAL"
    assert result["last_dispatch_status"] == "FAILED"


@pytest.mark.asyncio
async def test_confirmed_remote_receipt_closes_r5_gate(risk_escalation_db, monkeypatch):
    await risk_escalation_db.risks.insert_one(
        {"id": "RISK-5", "level": 5, "domain": "RISK", "title": "Systemic risk"}
    )
    escalation = await risk_escalation.require_systemic_escalation(
        actor_id="risk", risk_id="RISK-5", rationale="R5", evidence_refs=["E-5"]
    )
    monkeypatch.setenv("CVLN_IOS_URL", "https://ios.example")
    monkeypatch.setenv("CVLN_IOS_SERVICE_TOKEN", "secret")

    class Response:
        status_code = 202
        def json(self):
            return {"id": "IOS-REC-1", "status": "accepted"}

    class Client:
        async def __aenter__(self): return self
        async def __aexit__(self, *args): return None
        async def post(self, *args, **kwargs): return Response()

    monkeypatch.setattr(risk_escalation.httpx, "AsyncClient", lambda **kwargs: Client())
    result = await risk_escalation.dispatch_to_cvlnios(
        actor_id="risk", escalation_id=escalation["id"]
    )
    assert result["status"] == "ACKNOWLEDGED"
    assert result["cvlnios_receipt"]["receipt_id"] == "IOS-REC-1"
    assert (await risk_escalation.systemic_escalation_gate())["pass"] is True
