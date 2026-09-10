from __future__ import annotations

import pytest
from mongomock_motor import AsyncMongoMockClient

from services import professional_governance, security_remediation


@pytest.fixture
async def remediation_db(monkeypatch):
    client = AsyncMongoMockClient()
    test_db = client["cvln_security_remediation_test"]
    for module in (security_remediation, professional_governance):
        monkeypatch.setattr(module, "db", test_db)
    yield test_db
    client.close()


async def _remediation(remediation_db):
    await remediation_db.security_findings.insert_one({"id": "FIND-1", "severity": "HIGH"})
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
async def test_external_dispatch_is_never_claimed_without_real_task_id_and_evidence(remediation_db):
    row = await _remediation(remediation_db)
    assert row["external_dispatch"]["status"] == "PENDING_EXTERNAL_CONTRACT"
    with pytest.raises(ValueError, match="real remote task id"):
        await security_remediation.record_external_dispatch(
            actor_id="sec-1",
            remediation_id=row["id"],
            target="CVLN_AGENT_FACTORY",
            remote_task_id="",
            evidence_refs=[],
        )
    stored = await remediation_db.security_remediations.find_one({"id": row["id"]}, {"_id": 0})
    assert stored["external_dispatch"]["status"] == "PENDING_EXTERNAL_CONTRACT"


@pytest.mark.asyncio
async def test_execution_requires_explicit_authority_decision(remediation_db):
    row = await _remediation(remediation_db)
    with pytest.raises(ValueError, match="invalid remediation transition"):
        await security_remediation.transition_remediation(
            actor_id="agent-1",
            remediation_id=row["id"],
            status="EXECUTING",
        )
    authorized = await security_remediation.authorize_remediation(
        actor_id="founder-1",
        remediation_id=row["id"],
        authority_decision_ref="AUTHDEC-1",
    )
    executing = await security_remediation.transition_remediation(
        actor_id="agent-1",
        remediation_id=authorized["id"],
        status="EXECUTING",
    )
    assert executing["status"] == "EXECUTING"


@pytest.mark.asyncio
async def test_verified_requires_execution_and_test_evidence(remediation_db):
    row = await _remediation(remediation_db)
    await security_remediation.authorize_remediation(
        actor_id="founder-1", remediation_id=row["id"], authority_decision_ref="AUTHDEC-1"
    )
    await security_remediation.transition_remediation(
        actor_id="agent-1", remediation_id=row["id"], status="EXECUTING"
    )
    with pytest.raises(ValueError, match="execution evidence"):
        await security_remediation.transition_remediation(
            actor_id="agent-1", remediation_id=row["id"], status="TESTING", evidence_refs=[]
        )
    testing = await security_remediation.transition_remediation(
        actor_id="agent-1",
        remediation_id=row["id"],
        status="TESTING",
        evidence_refs=["COMMIT-1", "DEPLOY-1"],
    )
    with pytest.raises(ValueError, match="test evidence"):
        await security_remediation.transition_remediation(
            actor_id="sec-1", remediation_id=testing["id"], status="VERIFIED", evidence_refs=[]
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
    await security_remediation.authorize_remediation(
        actor_id="founder-1", remediation_id=row["id"], authority_decision_ref="AUTHDEC-2"
    )
    await security_remediation.transition_remediation(
        actor_id="agent-1", remediation_id=row["id"], status="EXECUTING"
    )
    await security_remediation.transition_remediation(
        actor_id="agent-1", remediation_id=row["id"], status="ROLLBACK_REQUIRED"
    )
    with pytest.raises(ValueError, match="rollback completion requires evidence"):
        await security_remediation.transition_remediation(
            actor_id="ops-1", remediation_id=row["id"], status="ROLLED_BACK", evidence_refs=[]
        )
    rolled = await security_remediation.transition_remediation(
        actor_id="ops-1",
        remediation_id=row["id"],
        status="ROLLED_BACK",
        evidence_refs=["ROLLBACK-RUN-1", "POST-ROLLBACK-SMOKE-1"],
    )
    assert rolled["status"] == "ROLLED_BACK"
    assert (await security_remediation.remediation_gate())["pass"] is True
