"""Governance notification router (GOV-009 / FD-009).

Extends the existing NotificationService boundary instead of creating a parallel mail
engine. Platform notifications are persisted locally. Email delegates to the existing
tracked outbox. WhatsApp uses one explicit provider boundary and never reports SENT
without a real HTTP success response.
"""

from __future__ import annotations

import os
import uuid
from typing import Any, Dict, Iterable, Optional

import httpx

from db import db, utc_now_iso
from services.notifications import notifications
from services import professional_governance as governance

CHANNELS = {"PLATFORM", "EMAIL", "WHATSAPP"}
CRITICALITY_DEFAULTS = {
    "INFO": ["PLATFORM"],
    "NORMAL": ["PLATFORM", "EMAIL"],
    "HIGH": ["PLATFORM", "EMAIL", "WHATSAPP"],
    "CRITICAL": ["PLATFORM", "EMAIL", "WHATSAPP"],
}


def _id(prefix: str) -> str:
    return f"{prefix}-{uuid.uuid4()}"


def _wa_config() -> tuple[str, str]:
    return (
        (os.environ.get("WHATSAPP_PROVIDER_URL") or "").rstrip("/"),
        (os.environ.get("WHATSAPP_PROVIDER_TOKEN") or "").strip(),
    )


async def set_channel_preference(
    *, actor_id: str, subject_id: str, channels: Iterable[str]
) -> Dict[str, Any]:
    normalized = sorted({str(c).strip().upper() for c in channels if str(c).strip()})
    if not normalized or any(channel not in CHANNELS for channel in normalized):
        raise ValueError("channels must contain PLATFORM, EMAIL and/or WHATSAPP")
    row = {
        "subject_id": subject_id,
        "channels": normalized,
        "updated_by": actor_id,
        "updated_at": utc_now_iso(),
    }
    await db.governance_notification_preferences.update_one(
        {"subject_id": subject_id}, {"$set": row}, upsert=True
    )
    return row


async def _platform_dispatch(
    *, subject_id: str, kind: str, payload: Dict[str, Any]
) -> Dict[str, Any]:
    row = {
        "id": _id("PNOTIF"),
        "subject_id": subject_id,
        "kind": kind,
        "payload": payload,
        "status": "DELIVERED_LOCAL",
        "created_at": utc_now_iso(),
    }
    await db.platform_notifications.insert_one(dict(row))
    return {"channel": "PLATFORM", "status": row["status"], "receipt_id": row["id"]}


async def _email_dispatch(
    *, email: str, kind: str, payload: Dict[str, Any]
) -> Dict[str, Any]:
    result = await notifications._dispatch(kind, email, payload)
    return {
        "channel": "EMAIL",
        "status": result["status"],
        "receipt_id": result["id"],
    }


async def _whatsapp_dispatch(
    *, phone: str, kind: str, payload: Dict[str, Any]
) -> Dict[str, Any]:
    base, token = _wa_config()
    if not base:
        return {"channel": "WHATSAPP", "status": "NOT_CONFIGURED", "receipt_id": None}
    try:
        headers = {"Authorization": f"Bearer {token}"} if token else {}
        async with httpx.AsyncClient(timeout=8.0) as client:
            response = await client.post(
                f"{base}/send",
                json={"to": phone, "kind": kind, "payload": payload},
                headers=headers,
            )
    except httpx.HTTPError:
        return {"channel": "WHATSAPP", "status": "FAILED", "receipt_id": None}
    if response.status_code >= 400:
        return {"channel": "WHATSAPP", "status": "FAILED", "receipt_id": None}
    receipt_id = None
    try:
        body = response.json()
        receipt_id = str(body.get("id") or body.get("message_id") or "").strip() or None
    except ValueError:
        pass
    if not receipt_id:
        return {"channel": "WHATSAPP", "status": "FAILED_NO_RECEIPT", "receipt_id": None}
    return {"channel": "WHATSAPP", "status": "SENT", "receipt_id": receipt_id}


async def route_notification(
    *,
    actor_id: str,
    subject_id: str,
    kind: str,
    payload: Dict[str, Any],
    criticality: str,
    email: Optional[str] = None,
    phone: Optional[str] = None,
    channels: Optional[Iterable[str]] = None,
) -> Dict[str, Any]:
    level = str(criticality or "").upper()
    if level not in CRITICALITY_DEFAULTS:
        raise ValueError("invalid notification criticality")
    if channels is None:
        pref = await db.governance_notification_preferences.find_one(
            {"subject_id": subject_id}, {"_id": 0}
        )
        selected = pref.get("channels") if pref else CRITICALITY_DEFAULTS[level]
    else:
        selected = sorted({str(c).strip().upper() for c in channels if str(c).strip()})
    if any(channel not in CHANNELS for channel in selected):
        raise ValueError("invalid notification channel")

    results = []
    for channel in selected:
        if channel == "PLATFORM":
            results.append(await _platform_dispatch(subject_id=subject_id, kind=kind, payload=payload))
        elif channel == "EMAIL":
            if not email:
                results.append({"channel": "EMAIL", "status": "MISSING_DESTINATION", "receipt_id": None})
            else:
                results.append(await _email_dispatch(email=email, kind=kind, payload=payload))
        elif channel == "WHATSAPP":
            if not phone:
                results.append({"channel": "WHATSAPP", "status": "MISSING_DESTINATION", "receipt_id": None})
            else:
                results.append(await _whatsapp_dispatch(phone=phone, kind=kind, payload=payload))

    row = {
        "id": _id("GNOTIF"),
        "subject_id": subject_id,
        "kind": kind,
        "criticality": level,
        "channels": selected,
        "results": results,
        "created_by": actor_id,
        "created_at": utc_now_iso(),
    }
    await db.governance_notification_dispatches.insert_one(dict(row))
    await governance.audit_event(
        event_type="governance.notification.dispatched",
        actor_id=actor_id,
        resource_type="notification_dispatch",
        resource_id=row["id"],
        payload={"subject_id": subject_id, "criticality": level, "results": results},
    )
    return row
