from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pytest
from mongomock_motor import AsyncMongoMockClient

from services import legal_deadlines, legal_ops, professional_governance as governance
from services import notifications as notifications_module


@pytest.fixture
async def deadline_db(monkeypatch):
    client = AsyncMongoMockClient()
    test_db = client["cvln_legal_deadline_test"]
    monkeypatch.setattr(legal_deadlines, "db", test_db)
    monkeypatch.setattr(legal_ops, "db", test_db)
    monkeypatch.setattr(governance, "db", test_db)
    monkeypatch.setattr(notifications_module, "db", test_db)
    yield test_db
    client.close()


@pytest.mark.asyncio
async def test_deadline_requires_explicit_future_due_and_thresholds(deadline_db):
    matter = await legal_ops.create_legal_matter(
        actor_id="legal-1", title="Renewal", matter_type="CONTRACT"
    )
    with pytest.raises(ValueError, match="future"):
        await legal_deadlines.create_deadline(
            actor_id="legal-1",
            matter_id=matter["id"],
            deadline_type="RENEWAL",
            title="Renew agreement",
            due_at=(datetime.now(timezone.utc) - timedelta(days=1)).isoformat(),
            owner_email="legal@example.test",
            reminder_days=[90, 60, 30],
            evidence_refs=["CONTRACT-1"],
        )


@pytest.mark.asyncio
async def test_due_reminder_is_idempotent_and_uses_notification_outbox(deadline_db):
    matter = await legal_ops.create_legal_matter(
        actor_id="legal-1", title="Renewal", matter_type="CONTRACT"
    )
    now = datetime.now(timezone.utc)
    row = await legal_deadlines.create_deadline(
        actor_id="legal-1",
        matter_id=matter["id"],
        deadline_type="RENEWAL",
        title="Renew agreement",
        due_at=(now + timedelta(days=29, hours=12)).isoformat(),
        owner_email="legal@example.test",
        reminder_days=[90, 60, 30],
        evidence_refs=["CONTRACT-2"],
    )
    first = await legal_deadlines.dispatch_due_reminders(actor_id="system", now=now)
    second = await legal_deadlines.dispatch_due_reminders(actor_id="system", now=now)
    assert {item["threshold_days"] for item in first["dispatched"]} == {90, 60, 30}
    assert second["dispatched"] == []
    stored = await deadline_db.legal_deadlines.find_one({"id": row["id"]}, {"_id": 0})
    assert set(stored["sent_thresholds"]) == {90, 60, 30}
    outbox = await deadline_db.notification_outbox.find({}, {"_id": 0}).to_list(10)
    assert len(outbox) == 3
    assert {item["status"] for item in outbox} == {"LOCAL_ONLY"}
    assert {item["kind"] for item in outbox} == {"legal_deadline"}


@pytest.mark.asyncio
async def test_deadline_close_requires_evidence(deadline_db):
    matter = await legal_ops.create_legal_matter(
        actor_id="legal-1", title="Notice", matter_type="CONTRACT"
    )
    row = await legal_deadlines.create_deadline(
        actor_id="legal-1",
        matter_id=matter["id"],
        deadline_type="NOTICE",
        title="Send notice",
        due_at=(datetime.now(timezone.utc) + timedelta(days=10)).isoformat(),
        owner_email="legal@example.test",
        reminder_days=[7, 1],
        evidence_refs=["NOTICE-1"],
    )
    with pytest.raises(ValueError, match="closure requires evidence"):
        await legal_deadlines.close_deadline(
            actor_id="legal-1",
            deadline_id=row["id"],
            status="COMPLETED",
            evidence_refs=[],
        )
    closed = await legal_deadlines.close_deadline(
        actor_id="legal-1",
        deadline_id=row["id"],
        status="COMPLETED",
        evidence_refs=["NOTICE-SENT-1"],
    )
    assert closed["status"] == "COMPLETED"
