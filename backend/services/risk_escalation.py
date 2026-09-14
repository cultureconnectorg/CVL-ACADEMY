"""Risk systemic escalation controls (RSK-03/RSK-20).

R5 is an explicit Academy risk condition. Escalation to CVLN iOS is a cross-system
contract and therefore fails closed when no real remote receipt is available. This
module never invents a CVLN iOS acknowledgement.
"""

from __future__ import annotations

import os
import uuid
from typing import Any, Dict, Iterable

import httpx

from db import db, utc_now_iso
from services import professional_governance as governance


def _id(prefix: str) -> str:
    return f"{prefix}-{uuid.uuid4()}"


def _refs(values: Iterable[str]) -> list[str]:
    return list(dict.fromkeys(str(v).strip() for v in values if str(v).strip()))


async def require_systemic_escalation(
    *, actor_id: str, risk_id: str, rationale: str, evidence_refs: Iterable[str]
) -> Dict[str, Any]:
    risk = await db.risks.find_one({"id": risk_id}, {"_id": 0})
    if not risk:
        raise LookupError("risk not found")
    if int(risk.get("level", 0)) != 5:
        raise ValueError("systemic escalation protocol applies only to R5 risk")
    refs = _refs(evidence_refs)
    if not rationale.strip() or not refs:
        raise ValueError("R5 escalation requires rationale and evidence")
    existing = await db.risk_systemic_escalations.find_one(
        {"risk_id": risk_id, "status": {"$in": ["REQUIRED", "PENDING_EXTERNAL", "ACKNOWLEDGED"]}},
        {"_id": 0},
    )
    if existing:
        return existing
    row = {
        "id": _id("R5ESC"),
        "risk_id": risk_id,
        "risk_level": 5,
        "rationale": rationale.strip(),
        "evidence_refs": refs,
        "status": "REQUIRED",
        "cvlnios_receipt": None,
        "created_by": actor_id,
        "created_at": utc_now_iso(),
        "updated_at": utc_now_iso(),
    }
    await db.risk_systemic_escalations.insert_one(dict(row))
    await governance.audit_event(
        event_type="risk.systemic_escalation.required",
        actor_id=actor_id,
        resource_type="risk",
        resource_id=risk_id,
        payload={"escalation_id": row["id"], "risk_level": 5, "evidence_refs": refs},
        reason=rationale.strip(),
        result="REQUIRED",
    )
    return row


def _config() -> tuple[str, str]:
    base = (os.environ.get("CVLN_IOS_URL") or "").strip().rstrip("/")
    token = (os.environ.get("CVLN_IOS_SERVICE_TOKEN") or "").strip()
    if not base or not token:
        raise RuntimeError("CVLN iOS escalation connector is not configured")
    return base, token


async def dispatch_to_cvlnios(
    *, actor_id: str, escalation_id: str
) -> Dict[str, Any]:
    row = await db.risk_systemic_escalations.find_one({"id": escalation_id}, {"_id": 0})
    if not row:
        raise LookupError("systemic escalation not found")
    if row["status"] == "ACKNOWLEDGED":
        return row
    if row["status"] not in {"REQUIRED", "PENDING_EXTERNAL"}:
        raise ValueError("systemic escalation is not dispatchable")

    try:
        base, token = _config()
    except RuntimeError as exc:
        now = utc_now_iso()
        update = {
            "status": "PENDING_EXTERNAL",
            "last_dispatch_status": "NOT_CONFIGURED",
            "last_dispatch_error": str(exc),
            "updated_at": now,
        }
        await db.risk_systemic_escalations.update_one({"id": escalation_id}, {"$set": update})
        return {**row, **update}

    risk = await db.risks.find_one({"id": row["risk_id"]}, {"_id": 0})
    if not risk:
        raise LookupError("risk not found")
    payload = {
        "source": "CVLN_ACADEMY",
        "source_escalation_id": row["id"],
        "risk_id": risk["id"],
        "risk_level": risk.get("level"),
        "domain": risk.get("domain"),
        "title": risk.get("title"),
        "rationale": row["rationale"],
        "evidence_refs": row["evidence_refs"],
    }
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(
                f"{base}/api/risk/escalations",
                json=payload,
                headers={"Authorization": f"Bearer {token}"},
            )
        if response.status_code >= 400:
            raise RuntimeError(f"CVLN iOS rejected escalation: HTTP {response.status_code}")
        data = response.json()
        receipt_id = str(data.get("id") or data.get("receipt_id") or "").strip()
        if not receipt_id:
            raise RuntimeError("CVLN iOS response missing receipt id")
    except (httpx.HTTPError, ValueError, RuntimeError) as exc:
        now = utc_now_iso()
        update = {
            "status": "PENDING_EXTERNAL",
            "last_dispatch_status": "FAILED",
            "last_dispatch_error": str(exc),
            "updated_at": now,
        }
        await db.risk_systemic_escalations.update_one({"id": escalation_id}, {"$set": update})
        return {**row, **update}

    now = utc_now_iso()
    receipt = {
        "receipt_id": receipt_id,
        "received_at": now,
        "remote_status": data.get("status"),
    }
    update = {
        "status": "ACKNOWLEDGED",
        "last_dispatch_status": "CONFIRMED",
        "last_dispatch_error": None,
        "cvlnios_receipt": receipt,
        "updated_at": now,
    }
    await db.risk_systemic_escalations.update_one({"id": escalation_id}, {"$set": update})
    await governance.audit_event(
        event_type="risk.systemic_escalation.acknowledged",
        actor_id=actor_id,
        resource_type="risk",
        resource_id=row["risk_id"],
        payload={"escalation_id": escalation_id, "cvlnios_receipt": receipt},
        result="ACKNOWLEDGED",
    )
    return {**row, **update}


async def systemic_escalation_gate() -> Dict[str, Any]:
    r5 = await db.risks.find({"level": 5}, {"_id": 0}).to_list(10000)
    blockers = []
    for risk in r5:
        escalation = await db.risk_systemic_escalations.find_one(
            {"risk_id": risk["id"], "status": "ACKNOWLEDGED"}, {"_id": 0}
        )
        if not escalation:
            blockers.append({"risk_id": risk["id"], "reason": "R5_CVLNIOS_ACK_MISSING"})
    return {
        "pass": not blockers,
        "blocking_count": len(blockers),
        "blocking_risks": blockers,
        "external_system": "CVLN_IOS",
    }
