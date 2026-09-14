"""Expert cost ledger (GOV-011 / FD-011 / FD-012).

Records real external expert cost/time per professional case and optional baseline
assumptions used to calculate cost avoided. It never invents market rates: baselines
must be supplied with evidence and can be revised through additional immutable entries.
"""

from __future__ import annotations

import uuid
from typing import Any, Dict, Iterable, Optional

from db import db, utc_now_iso
from services import professional_governance as governance


def _id(prefix: str) -> str:
    return f"{prefix}-{uuid.uuid4()}"


def _refs(values: Iterable[str]) -> list[str]:
    return list(dict.fromkeys(str(v).strip() for v in values if str(v).strip()))


async def record_cost(
    *,
    actor_id: str,
    case_id: str,
    expert_id: str,
    intervention_type: str,
    hours: float,
    amount_cents: int,
    currency: str,
    evidence_refs: Iterable[str],
    baseline_without_core_hours: Optional[float] = None,
    baseline_hourly_rate_cents: Optional[int] = None,
    note: Optional[str] = None,
) -> Dict[str, Any]:
    refs = _refs(evidence_refs)
    if not refs:
        raise ValueError("expert cost entry requires evidence")
    if hours < 0 or amount_cents < 0:
        raise ValueError("hours and amount_cents must be non-negative")
    if (baseline_without_core_hours is None) != (baseline_hourly_rate_cents is None):
        raise ValueError("baseline hours and hourly rate must be supplied together")
    if baseline_without_core_hours is not None and baseline_without_core_hours < 0:
        raise ValueError("baseline_without_core_hours must be non-negative")
    if baseline_hourly_rate_cents is not None and baseline_hourly_rate_cents < 0:
        raise ValueError("baseline_hourly_rate_cents must be non-negative")

    case = await db.professional_cases.find_one({"id": case_id}, {"_id": 0})
    expert = await db.governance_experts.find_one({"id": expert_id}, {"_id": 0})
    if not case or not expert:
        raise LookupError("case or expert not found")
    assigned = await db.governance_expert_assignments.find_one(
        {"case_id": case_id, "expert_id": expert_id, "status": "ACTIVE"}, {"_id": 0}
    )
    if not assigned:
        raise PermissionError("expert is not actively assigned to case")

    baseline_cents = None
    avoided_cents = None
    if baseline_without_core_hours is not None and baseline_hourly_rate_cents is not None:
        baseline_cents = round(float(baseline_without_core_hours) * int(baseline_hourly_rate_cents))
        avoided_cents = baseline_cents - amount_cents

    row = {
        "id": _id("EXPCOST"),
        "case_id": case_id,
        "expert_id": expert_id,
        "assignment_id": assigned["id"],
        "domain": case.get("domain"),
        "intervention_type": intervention_type.strip().upper(),
        "hours": float(hours),
        "amount_cents": int(amount_cents),
        "currency": currency.strip().upper(),
        "baseline_without_core_hours": baseline_without_core_hours,
        "baseline_hourly_rate_cents": baseline_hourly_rate_cents,
        "baseline_external_cost_cents": baseline_cents,
        "estimated_cost_avoided_cents": avoided_cents,
        "evidence_refs": refs,
        "note": note,
        "recorded_by": actor_id,
        "recorded_at": utc_now_iso(),
    }
    await db.governance_expert_costs.insert_one(dict(row))
    await governance.audit_event(
        event_type="governance.expert_cost.recorded",
        actor_id=actor_id,
        resource_type="professional_case",
        resource_id=case_id,
        payload={
            "cost_entry_id": row["id"],
            "expert_id": expert_id,
            "amount_cents": amount_cents,
            "estimated_cost_avoided_cents": avoided_cents,
            "evidence_refs": refs,
        },
    )
    return row


async def case_cost_summary(case_id: str) -> Dict[str, Any]:
    if not await db.professional_cases.find_one({"id": case_id}):
        raise LookupError("professional case not found")
    rows = await db.governance_expert_costs.find(
        {"case_id": case_id}, {"_id": 0}
    ).sort("recorded_at", 1).to_list(5000)
    currencies = sorted({row.get("currency") for row in rows if row.get("currency")})
    if len(currencies) > 1:
        totals = None
    else:
        total_cost = sum(int(row.get("amount_cents", 0)) for row in rows)
        known_baselines = [
            int(row["baseline_external_cost_cents"])
            for row in rows
            if row.get("baseline_external_cost_cents") is not None
        ]
        total_baseline = sum(known_baselines) if known_baselines else None
        total_avoided = (
            total_baseline - total_cost if total_baseline is not None else None
        )
        totals = {
            "currency": currencies[0] if currencies else None,
            "external_cost_cents": total_cost,
            "baseline_external_cost_cents": total_baseline,
            "estimated_cost_avoided_cents": total_avoided,
            "reduction_pct": (
                round((total_avoided / total_baseline) * 100, 2)
                if total_baseline and total_avoided is not None
                else None
            ),
        }
    return {
        "case_id": case_id,
        "entries": rows,
        "totals": totals,
        "mixed_currency": len(currencies) > 1,
    }


async def global_cost_reduction_summary() -> Dict[str, Any]:
    rows = await db.governance_expert_costs.find({}, {"_id": 0}).to_list(100000)
    by_currency: Dict[str, Dict[str, Any]] = {}
    for row in rows:
        currency = row.get("currency") or "UNKNOWN"
        bucket = by_currency.setdefault(
            currency,
            {"external_cost_cents": 0, "baseline_external_cost_cents": 0, "baseline_entry_count": 0},
        )
        bucket["external_cost_cents"] += int(row.get("amount_cents", 0))
        if row.get("baseline_external_cost_cents") is not None:
            bucket["baseline_external_cost_cents"] += int(row["baseline_external_cost_cents"])
            bucket["baseline_entry_count"] += 1
    for bucket in by_currency.values():
        baseline = bucket["baseline_external_cost_cents"]
        avoided = baseline - bucket["external_cost_cents"] if bucket["baseline_entry_count"] else None
        bucket["estimated_cost_avoided_cents"] = avoided
        bucket["reduction_pct"] = (
            round((avoided / baseline) * 100, 2) if baseline and avoided is not None else None
        )
    return {"currencies": by_currency, "entry_count": len(rows)}
