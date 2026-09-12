"""Autonomous incident correlation and maintenance orchestration for CVLN CareOps.

This layer never deploys arbitrary code by itself. It creates auditable incident and
operational recovery records, links affected tickets, and advances only through explicit
states backed by verification evidence.
"""

from __future__ import annotations

import secrets
from typing import Any, Dict, Optional

from db import db, utc_now_iso

INCIDENT_THRESHOLD = 3
OPEN_TICKET_STATES = ("triaged", "in_progress", "waiting", "incident")


def incident_action_type(kind: str) -> str:
    return {
        "security": "security_response",
        "claim": "claims_review",
        "payment": "billing_investigation",
        "access": "service_recovery",
        "maintenance": "technical_maintenance",
        "support": "service_recovery",
    }.get(kind, "service_recovery")


def _incident_id() -> str:
    return f"INC-{secrets.token_hex(4).upper()}"


def _maintenance_id() -> str:
    return f"MNT-{secrets.token_hex(4).upper()}"


async def correlate_ticket(ticket: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Attach recurring tickets to one incident once the threshold is reached."""
    query = {
        "product": ticket["product"],
        "fingerprint": ticket["fingerprint"],
        "status": {"$in": list(OPEN_TICKET_STATES)},
    }
    related = (
        await db.careops_tickets.find(query, {"_id": 0})
        .sort("created_at", 1)
        .to_list(100)
    )
    if len(related) < INCIDENT_THRESHOLD:
        return None

    existing = await db.careops_incidents.find_one(
        {
            "product": ticket["product"],
            "fingerprint": ticket["fingerprint"],
            "status": {"$ne": "resolved"},
        },
        {"_id": 0},
    )
    now = utc_now_iso()
    if existing:
        incident_id = existing["incident_id"]
        await db.careops_incidents.update_one(
            {"incident_id": incident_id},
            {"$set": {"ticket_count": len(related), "updated_at": now}},
        )
    else:
        incident_id = _incident_id()
        incident = {
            "incident_id": incident_id,
            "product": ticket["product"],
            "fingerprint": ticket["fingerprint"],
            "kind": ticket["kind"],
            "action_type": incident_action_type(ticket["kind"]),
            "priority": (
                "P1" if ticket["priority"] in ("P2", "P3") else ticket["priority"]
            ),
            "status": "detected",
            "ticket_count": len(related),
            "created_by": "careops-correlation",
            "created_at": now,
            "updated_at": now,
            "events": [
                {"type": "incident.detected", "actor": "careops", "ts": now}
            ],
        }
        await db.careops_incidents.insert_one(incident.copy())
        await _create_maintenance_task(incident)

    await db.careops_tickets.update_many(
        {"ticket_id": {"$in": [item["ticket_id"] for item in related]}},
        {
            "$set": {
                "incident_id": incident_id,
                "status": "incident",
                "updated_at": now,
            },
            "$push": {
                "events": {
                    "type": "ticket.correlated",
                    "actor": "careops",
                    "ts": now,
                    "incident_id": incident_id,
                }
            },
        },
    )
    return await db.careops_incidents.find_one(
        {"incident_id": incident_id}, {"_id": 0}
    )


async def _create_maintenance_task(incident: Dict[str, Any]) -> Dict[str, Any]:
    now = utc_now_iso()
    task = {
        "maintenance_id": _maintenance_id(),
        "incident_id": incident["incident_id"],
        "product": incident["product"],
        "action_type": incident.get(
            "action_type", incident_action_type(incident["kind"])
        ),
        "status": "queued",
        "automation_mode": "guarded",
        "diagnostics": [
            "health",
            "logs",
            "recent_release",
            "dependencies",
            "database",
            "permissions",
        ],
        "verification_required": True,
        "created_at": now,
        "updated_at": now,
        "events": [{"type": "maintenance.queued", "actor": "careops", "ts": now}],
    }
    await db.careops_maintenance.insert_one(task.copy())
    await db.careops_incidents.update_one(
        {"incident_id": incident["incident_id"]},
        {
            "$set": {
                "maintenance_id": task["maintenance_id"],
                "status": "maintenance_queued",
                "updated_at": now,
            }
        },
    )
    return task


async def record_maintenance_result(
    *, maintenance_id: str, success: bool, evidence: Dict[str, Any]
) -> Dict[str, Any]:
    """Record machine-verifiable evidence and close the loop only on success."""
    task = await db.careops_maintenance.find_one(
        {"maintenance_id": maintenance_id}, {"_id": 0}
    )
    if not task:
        raise KeyError("maintenance task not found")

    now = utc_now_iso()
    status = "verified" if success else "failed"
    await db.careops_maintenance.update_one(
        {"maintenance_id": maintenance_id},
        {
            "$set": {"status": status, "evidence": evidence, "updated_at": now},
            "$push": {
                "events": {
                    "type": f"maintenance.{status}",
                    "actor": "careops",
                    "ts": now,
                }
            },
        },
    )

    incident_id = task["incident_id"]
    if success:
        await db.careops_incidents.update_one(
            {"incident_id": incident_id},
            {
                "$set": {
                    "status": "resolved",
                    "resolved_at": now,
                    "updated_at": now,
                    "verification_evidence": evidence,
                },
                "$push": {
                    "events": {
                        "type": "incident.resolved",
                        "actor": "careops",
                        "ts": now,
                    }
                },
            },
        )
        await db.careops_tickets.update_many(
            {"incident_id": incident_id},
            {
                "$set": {
                    "status": "resolved",
                    "resolved_at": now,
                    "updated_at": now,
                },
                "$push": {
                    "events": {
                        "type": "ticket.resolved_from_incident",
                        "actor": "careops",
                        "ts": now,
                    }
                },
            },
        )
        await db.careops_learnings.insert_one(
            {
                "incident_id": incident_id,
                "product": task["product"],
                "maintenance_id": maintenance_id,
                "action_type": task.get("action_type"),
                "evidence": evidence,
                "created_at": now,
                "kind": "verified_resolution",
            }
        )
    else:
        await db.careops_incidents.update_one(
            {"incident_id": incident_id},
            {"$set": {"status": "needs_attention", "updated_at": now}},
        )

    return (
        await db.careops_maintenance.find_one(
            {"maintenance_id": maintenance_id}, {"_id": 0}
        )
        or task
    )
