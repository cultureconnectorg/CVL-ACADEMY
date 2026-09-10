"""Legal deadline engine (LEG-010 / FD-L13).

Tracks contractual/legal due dates and sends due reminders only through the single
Academy notifications boundary. Reminder thresholds are explicit per deadline; the
engine does not invent jurisdictional notice periods.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, Optional

from db import db, utc_now_iso
from services.notifications import notifications
from services import professional_governance as governance

DEADLINE_TYPES = {
    "RENEWAL",
    "TERMINATION_NOTICE",
    "NOTICE",
    "EXPIRATION",
    "FILING",
    "REVIEW",
    "OTHER",
}
DEADLINE_STATES = {"ACTIVE", "COMPLETED", "CANCELLED"}


def _id(prefix: str) -> str:
    return f"{prefix}-{uuid.uuid4()}"


def _instant(value: str) -> datetime:
    try:
        parsed = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except (TypeError, ValueError) as exc:
        raise ValueError("due_at must be ISO-8601") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ValueError("due_at must include timezone")
    return parsed.astimezone(timezone.utc)


async def create_deadline(
    *,
    actor_id: str,
    matter_id: str,
    deadline_type: str,
    title: str,
    due_at: str,
    owner_email: str,
    reminder_days: Iterable[int],
    contract_id: Optional[str] = None,
    document_id: Optional[str] = None,
    evidence_refs: Iterable[str],
) -> Dict[str, Any]:
    kind = str(deadline_type or "").upper()
    if kind not in DEADLINE_TYPES:
        raise ValueError("invalid legal deadline type")
    due = _instant(due_at)
    refs = list(
        dict.fromkeys(
            str(ref).strip() for ref in evidence_refs if str(ref).strip()
        )
    )
    thresholds = sorted(
        {int(value) for value in reminder_days if int(value) >= 0}, reverse=True
    )
    if not refs:
        raise ValueError("legal deadline requires evidence")
    if not thresholds:
        raise ValueError("legal deadline requires explicit reminder thresholds")
    if not owner_email.strip():
        raise ValueError("deadline owner_email is required")
    if due <= datetime.now(timezone.utc):
        raise ValueError("new legal deadline must be in the future")
    matter = await db.legal_matters.find_one({"id": matter_id}, {"_id": 0})
    if not matter:
        raise LookupError("legal matter not found")
    if contract_id and not await db.legal_contracts.find_one({"id": contract_id}):
        raise LookupError("contract not found")
    if document_id and not await db.legal_documents.find_one({"id": document_id}):
        raise LookupError("legal document not found")

    row = {
        "id": _id("LDDL"),
        "matter_id": matter_id,
        "contract_id": contract_id,
        "document_id": document_id,
        "deadline_type": kind,
        "title": str(title).strip(),
        "due_at": due.isoformat(),
        "owner_email": owner_email.strip(),
        "reminder_days": thresholds,
        "sent_thresholds": [],
        "evidence_refs": refs,
        "status": "ACTIVE",
        "created_by": actor_id,
        "created_at": utc_now_iso(),
        "updated_at": utc_now_iso(),
    }
    if not row["title"]:
        raise ValueError("deadline title is required")
    await db.legal_deadlines.insert_one(dict(row))
    await governance.audit_event(
        event_type="legal.deadline.created",
        actor_id=actor_id,
        resource_type="legal_deadline",
        resource_id=row["id"],
        payload={"matter_id": matter_id, "due_at": row["due_at"], "evidence_refs": refs},
    )
    return row


async def dispatch_due_reminders(
    *, actor_id: str, now: Optional[datetime] = None
) -> Dict[str, Any]:
    moment = (now or datetime.now(timezone.utc)).astimezone(timezone.utc)
    rows = await db.legal_deadlines.find(
        {"status": "ACTIVE"}, {"_id": 0}
    ).to_list(5000)
    dispatched: list[Dict[str, Any]] = []
    overdue: list[str] = []
    for row in rows:
        due = _instant(row["due_at"])
        seconds = (due - moment).total_seconds()
        if seconds < 0:
            overdue.append(row["id"])
        days_remaining = max(0, int(seconds // 86400))
        sent = {int(value) for value in row.get("sent_thresholds", [])}
        eligible = [
            int(threshold)
            for threshold in row.get("reminder_days", [])
            if int(threshold) not in sent and seconds <= int(threshold) * 86400
        ]
        for threshold in sorted(eligible, reverse=True):
            result = await notifications.send_operational_event(
                kind="legal_deadline",
                email=row["owner_email"],
                subject=f"Legal deadline: {row['title']}",
                data={
                    "deadline_id": row["id"],
                    "matter_id": row["matter_id"],
                    "deadline_type": row["deadline_type"],
                    "due_at": row["due_at"],
                    "threshold_days": threshold,
                    "days_remaining": days_remaining,
                    "overdue": seconds < 0,
                },
            )
            await db.legal_deadlines.update_one(
                {"id": row["id"], "sent_thresholds": {"$ne": threshold}},
                {
                    "$addToSet": {"sent_thresholds": threshold},
                    "$set": {"updated_at": utc_now_iso()},
                },
            )
            receipt = {
                "deadline_id": row["id"],
                "threshold_days": threshold,
                "notification_id": result["id"],
                "notification_status": result["status"],
            }
            dispatched.append(receipt)
            await governance.audit_event(
                event_type="legal.deadline.reminder_dispatched",
                actor_id=actor_id,
                resource_type="legal_deadline",
                resource_id=row["id"],
                payload=receipt,
            )
    return {"dispatched": dispatched, "overdue_deadline_ids": sorted(overdue)}


async def close_deadline(
    *, actor_id: str, deadline_id: str, status: str, evidence_refs: Iterable[str]
) -> Dict[str, Any]:
    target = str(status or "").upper()
    if target not in {"COMPLETED", "CANCELLED"}:
        raise ValueError("deadline can only close as COMPLETED or CANCELLED")
    refs = list(
        dict.fromkeys(
            str(ref).strip() for ref in evidence_refs if str(ref).strip()
        )
    )
    if not refs:
        raise ValueError("deadline closure requires evidence")
    row = await db.legal_deadlines.find_one({"id": deadline_id}, {"_id": 0})
    if not row:
        raise LookupError("legal deadline not found")
    if row["status"] != "ACTIVE":
        raise ValueError("legal deadline is not active")
    now = utc_now_iso()
    update = {
        "status": target,
        "closed_at": now,
        "closed_by": actor_id,
        "closure_evidence_refs": refs,
        "updated_at": now,
    }
    result = await db.legal_deadlines.update_one(
        {"id": deadline_id, "status": "ACTIVE"}, {"$set": update}
    )
    if result.modified_count != 1:
        raise ValueError("deadline closure lost race")
    return {**row, **update}
