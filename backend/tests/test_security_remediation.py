from __future__ import annotations

import pytest
from mongomock_motor import AsyncMongoMockClient

from services import authority_policy, professional_governance, remediation_dispatch, security_remediation


@pytest.fixture
async def remediation_db(monkeypatch):
    client = AsyncMongoMockClient()
    test_db = client["cvln_security_remediation_test"]
    for module in (security_remediation, professional_governance, authority_policy):
        monkeypatch.setattr(module, "db", test_db)
    yield test_db
    client.close()


async def _remediation(remediation_db):
    await remediation_db.security_findings.insert_one(
        {"id": "FIND-1", "severity": "HIGH"}
    )
    return await security_remediation.create_remediation(
        actor_id="sec-1",
        finding_id="FIND-1",
        title="Close cross-case authorization gap",
        proposed_change="Enforce case scope at request boundary",
        target_system="CVLN_AGENT_FACTORY",
        rollback_plan="Revert change and restore previous deployment artifact",
        test_plan=["test_cross_case_denied", "test_assigned_case_allowed"],
        evidence_refs=["FIND-1", "THREAT-MODEL-1"],
    )


async def _authorize(
    remediation_db,
    remediation_id: str,
    *,
    decision="ALLOW",
    action="SECURITY_AUTONOMOUS_FIX",
    bound_id=None,
):
    decision_id = "AUTHDEC-1"
    await remediation_db.authority_decisions.insert_one(
        {
            "id": decision_id,
            "decision": decision,
            "action": action,
            "context": {
                "domain": "SECURITY",
                "remediation_id": bound_id or remediation_id,
                "target_system": "CVLN_AGENT_FACTORY",
            },
            "decision_hash": "AUTH-HASH-1",
            "policy_version_id": "POL-1",
        }
    )
    return await security_remediation.authorize_remediation(
        actor_id="founder-1",
        remediation_id=remediation_id,
        authority_decision_ref=decision_id,
    )


async def _authorize_and_confirm_dispatch(remediation_db, remediation_id: str):
    await _authorize(remediation_db, remediation_id)
    return await security_remediation.record_external_dispatch(
        actor_id="sec-1",
        remediation_id=remediation_id,
        target="CVLN_AGENT_FACTORY",
        remote_task_id="REMOTE-1",
        evidence_refs=["HTTP-202", "REMOTE-RESPONSE-HASH"],
    )


@pytest.mark.asyncio
async def test_remediation_requires_exactly_one_security_source(remediation_db):
    with pytest.raises(ValueError, match="exactly one"):
        await security_remediation.create_remediation(
            actor_id="sec-1",
            title="Invalid",
            proposed_change="x",
            target_system="LOCAL",
            rollback_plan="rollback",
            test_plan=["test"],
            evidence_refs=["E-1"],
        )


@pytest.mark.asyncio
async def test_remediation_rejects_fake_denied_or_cross_resource_authority(remediation_db):
    row = await _remediation(remediation_db)
    await remediation_db.authority_decisions.insert_one(
        {
            "id": "AUTH-DENY",
            "decision": "DENY",
            "action": "SECURITY_AUTONOMOUS_FIX",
            "context": {"domain": "SECURITY", "remediation_id": row["id"]},
        }
    )
    with pytest.raises(PermissionError, match="ALLOW authority decision"):
        await security_remediation.authorize_remediation(
            actor_id="founder-1",
            remediation_id=row["id"],
            authority_decision_ref="AUTH-DENY",
        )

    await remediation_db.authority_decisions.insert_one(
        {
            "id": "AUTH-OTHER",
            "decision": "ALLOW",
            "action": "SECURITY_AUTONOMOUS_FIX",
            "context": {"domain": "SECURITY", "remediation_id": "REMED-OTHER"},
        }
    )
    with pytest.raises(ValueError, match="not bound to this remediation"):
        await security_remediation.authorize_remediation(
            actor_id="founder-1",
            remediation_id=row["id"],
            authority_decision_ref="AUTH-OTHER",
        )


@pytest.mark.asyncio
async def test_manual_external_dispatch_requires_authority_id_and_evidence(remediation_db):
    row = await _remediation(remediation_db)
    assert row["external_dispatch"]["status"] == "PENDING_EXTERNAL_CONTRACT"
    with pytest.raises(ValueError, match="authorized remediation"):
        await security_remediation.record_external_dispatch(
            actor_id="sec-1",
            remediation_id=row["id"],
            target="CVLN_AGENT_FACTORY",
            remote_task_id="REMOTE-1",
            evidence_refs=["HTTP-202"],
        )

    await _authorize(remediation_db, row["id"])
    with pytest.raises(ValueError, match="real remote task id"):
        await security_remediation.record_external_dispatch(
            actor_id="sec-1",
            remediation_id=row["id"],
            target="CVLN_AGENT_FACTORY",
            remote_task_id="",
            evidence_refs=[],
        )
    with pytest.raises(ValueError, match="target does not match"):
        await security_remediation.record_external_dispatch(
            actor_id="sec-1",
            remediation_id=row["id"],
            target="CVLN_COMMAND_CENTER",
            remote_task_id="REMOTE-1",
            evidence_refs=["HTTP-202"],
        )

    dispatched = await security_remediation.record_external_dispatch(
        actor_id="sec-1",
        remediation_id=row["id"],
        target="CVLN_AGENT_FACTORY",
        remote_task_id="REMOTE-1",
        evidence_refs=["HTTP-202", "REMOTE-RESPONSE-HASH"],
    )
    assert dispatched["external_dispatch"]["status"] == "CONFIRMED"
    assert dispatched["external_dispatch"]["execution_dispatch_confirmed"] is True
    assert dispatched["external_dispatch"]["results"]["manual_external"]["remote_task_id"] == "REMOTE-1"


@pytest.mark.asyncio
async def test_execution_requires_authority_and_confirmed_execution_dispatch(remediation_db):
    row = await _remediation(remediation_db)
    with pytest.raises(ValueError, match="invalid remediation transition"):
        await security_remediation.transition_remediation(
            actor_id="agent-1",
            remediation_id=row["id"],
            status="EXECUTING",
        )
    authorized = await _authorize(remediation_db, row["id"])
    with pytest.raises(ValueError, match="confirmed Agent Factory/external dispatch"):
        await security_remediation.transition_remediation(
            actor_id="agent-1",
            remediation_id=authorized["id"],
            status="EXECUTING",
        )

    await security_remediation.record_external_dispatch(
        actor_id="sec-1",
        remediation_id=authorized["id"],
        target="CVLN_AGENT_FACTORY",
        remote_task_id="REMOTE-1",
        evidence_refs=["HTTP-202"],
    )
    executing = await security_remediation.transition_remediation(
        actor_id="agent-1",
        remediation_id=authorized["id"],
        status="EXECUTING",
    )
    assert executing["status"] == "EXECUTING"


@pytest.mark.asyncio
async def test_authorized_auto_dispatch_persists_real_remote_ids_and_is_idempotent(remediation_db, monkeypatch):
    row = await _remediation(remediation_db)
    await _authorize(remediation_db, row["id"])
    calls = 0

    async def fake_dispatch(_row):
        nonlocal calls
        calls += 1
        return {
            "status": "CONFIRMED",
            "execution_dispatch_confirmed": True,
            "operations_mirror_confirmed": True,
            "results": {
                "agent_factory": {"status": "DISPATCHED_CONFIRMED", "remote_task_id": "MISSION-42"},
                "command_center": {"status": "DISPATCHED_CONFIRMED", "remote_task_id": "TASK-99"},
            },
        }

    monkeypatch.setattr(remediation_dispatch, "dispatch_remediation", fake_dispatch)
    first = await security_remediation.dispatch_authorized_remediation(
        actor_id="sec-1", remediation_id=row["id"]
    )
    second = await security_remediation.dispatch_authorized_remediation(
        actor_id="sec-1", remediation_id=row["id"]
    )
    assert first["external_dispatch"]["status"] == "CONFIRMED"
    assert first["external_dispatch"]["execution_dispatch_confirmed"] is True
    assert first["external_dispatch"]["results"]["agent_factory"]["remote_task_id"] == "MISSION-42"
    assert first["external_dispatch"]["results"]["command_center"]["remote_task_id"] == "TASK-99"
    assert second["external_dispatch"]["execution_dispatch_confirmed"] is True
    assert calls == 1


@pytest.mark.asyncio
async def test_command_center_failure_does_not_hide_confirmed_agent_factory_dispatch(remediation_db, monkeypatch):
    row = await _remediation(remediation_db)
    await _authorize(remediation_db, row["id"])

    async def fake_dispatch(_row):
        return {
            "status": "PARTIAL",
            "execution_dispatch_confirmed": True,
            "operations_mirror_confirmed": False,
            "results": {
                "agent_factory": {"status": "DISPATCHED_CONFIRMED", "remote_task_id": "MISSION-43"},
                "command_center": {"status": "NOT_CONFIGURED", "error": "CVLN_COMMAND_CENTER_URL is not configured"},
            },
        }

    monkeypatch.setattr(remediation_dispatch, "dispatch_remediation", fake_dispatch)
    dispatched = await security_remediation.dispatch_authorized_remediation(
        actor_id="sec-1", remediation_id=row["id"]
    )
    assert dispatched["external_dispatch"]["status"] == "PARTIAL"
    executing = await security_remediation.transition_remediation(
        actor_id="agent-1", remediation_id=row["id"], status="EXECUTING"
    )
    assert executing["status"] == "EXECUTING"


@pytest.mark.asyncio
async def test_agent_factory_dispatch_failure_blocks_execution(remediation_db, monkeypatch):
    row = await _remediation(remediation_db)
    await _authorize(remediation_db, row["id"])

    async def fake_dispatch(_row):
        return {
            "status": "FAILED",
            "execution_dispatch_confirmed": False,
            "operations_mirror_confirmed": True,
            "results": {
                "agent_factory": {"status": "FAILED", "error": "HTTP 403"},
                "command_center": {"status": "DISPATCHED_CONFIRMED", "remote_task_id": "TASK-100"},
            },
        }

    monkeypatch.setattr(remediation_dispatch, "dispatch_remediation", fake_dispatch)
    await security_remediation.dispatch_authorized_remediation(
        actor_id="sec-1", remediation_id=row["id"]
    )
    with pytest.raises(ValueError, match="confirmed Agent Factory/external dispatch"):
        await security_remediation.transition_remediation(
            actor_id="agent-1", remediation_id=row["id"], status="EXECUTING"
        )


@pytest.mark.asyncio
async def test_verified_requires_execution_and_test_evidence(remediation_db):
    row = await _remediation(remediation_db)
    await _authorize_and_confirm_dispatch(remediation_db, row["id"])
    await security_remediation.transition_remediation(
        actor_id="agent-1", remediation_id=row["id"], status="EXECUTING"
    )
    with pytest.raises(ValueError, match="execution evidence"):
        await security_remediation.transition_remediation(
            actor_id="agent-1",
            remediation_id=row["id"],
            status="TESTING",
            evidence_refs=[],
        )
    testing = await security_remediation.transition_remediation(
        actor_id="agent-1",
        remediation_id=row["id"],
        status="TESTING",
        evidence_refs=["COMMIT-1", "DEPLOY-1"],
    )
    with pytest.raises(ValueError, match="test evidence"):
        await security_remediation.transition_remediation(
            actor_id="sec-1",
            remediation_id=testing["id"],
            status="VERIFIED",
            evidence_refs=[],
        )
    verified = await security_remediation.transition_remediation(
        actor_id="sec-1",
        remediation_id=testing["id"],
        status="VERIFIED",
        evidence_refs=["CI-RUN-1", "ATTACK-RETEST-1"],
    )
    assert verified["status"] == "VERIFIED"
    assert verified["test_evidence_refs"] == ["CI-RUN-1", "ATTACK-RETEST-1"]
    assert (await security_remediation.remediation_gate())["pass"] is True


@pytest.mark.asyncio
async def test_rollback_requires_evidence_and_closes_gate(remediation_db):
    row = await _remediation(remediation_db)
    await _authorize_and_confirm_dispatch(remediation_db, row["id"])
    await security_remediation.transition_remediation(
        actor_id="agent-1", remediation_id=row["id"], status="EXECUTING"
    )
    await security_remediation.transition_remediation(
        actor_id="agent-1",
        remediation_id=row["id"],
        status="ROLLBACK_REQUIRED",
    )
    with pytest.raises(ValueError, match="rollback completion requires evidence"):
        await security_remediation.transition_remediation(
            actor_id="ops-1",
            remediation_id=row["id"],
            status="ROLLED_BACK",
            evidence_refs=[],
        )
    rolled = await security_remediation.transition_remediation(
        actor_id="ops-1",
        remediation_id=row["id"],
        status="ROLLED_BACK",
        evidence_refs=["ROLLBACK-RUN-1", "POST-ROLLBACK-SMOKE-1"],
    )
    assert rolled["status"] == "ROLLED_BACK"
    assert (await security_remediation.remediation_gate())["pass"] is True
