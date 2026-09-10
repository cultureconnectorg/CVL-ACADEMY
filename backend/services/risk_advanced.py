"""Risk & Insurance advanced controls (RSK-001..013).

Reuses ``risks`` from Assurance Core and the existing incident/insurance projection
services. This module adds authority, coverage, renewal and evidence-pack controls
without pretending to purchase or validate insurance automatically.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Iterable, Optional

from db import db, utc_now_iso
from services import authority_policy, evidence_graph, expert_access, risk_ops
from services import professional_governance as governance


def _id(prefix: str) -> str:
    return f"{prefix}-{uuid.uuid4()}"


def _refs(values: Iterable[str]) -> list[str]:
    return list(dict.fromkeys(str(v).strip() for v in values if str(v).strip()))


def _parse(value: str) -> datetime:
    parsed = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ValueError("datetime must include timezone")
    return parsed.astimezone(timezone.utc)


async def set_critical_risk_treatment(
    *,
    actor_id: str,
    actor_role: str,
    authority_level: str,
    risk_id: str,
    treatment: str,
    policy_version_id: str,
    owner: str,
    mitigation: str,
    deadline: str,
    evidence_refs: Iterable[str],
) -> Dict[str, Any]:
    """RSK-003/004: critical risks need A5 authority and executable evidence."""
    risk = await db.risks.find_one({"id": risk_id}, {"_id": 0})
    if not risk:
        raise LookupError("risk not found")
    refs = _refs(evidence_refs)
    if int(risk.get("level", 0)) < 4:
        raise ValueError("critical treatment wrapper is only for R4/R5 risks")
    if not owner.strip() or not mitigation.strip() or not deadline.strip() or not refs:
        raise ValueError("critical risk requires owner, mitigation, deadline and evidence")
    decision = await authority_policy.evaluate_authority(
        actor_id=actor_id,
        actor_role=actor_role,
        action="CRITICAL_RISK_TREATMENT",
        context={
            "domain": "RISK",
            "authority_level": authority_level,
            "risk_id": risk_id,
            "risk_level": risk.get("level"),
            "treatment": treatment.strip().upper(),
        },
        policy_version_id=policy_version_id,
    )
    if decision["policy_key"] != "CRITICAL_RISK_TREATMENT":
        raise ValueError("critical risk requires CRITICAL_RISK_TREATMENT policy")
    if decision["decision"] != "ALLOW":
        raise PermissionError("authority policy did not allow critical risk treatment")
    normalized = treatment.strip().upper().replace("-", "_")
    if normalized not in {"ACCEPT", "MITIGATE", "TRANSFER_INSURE", "ESCALATE", "BLOCK"}:
        raise ValueError("invalid risk treatment")
    state_map = {
        "ACCEPT": "ACCEPTED",
        "MITIGATE": "TREATING",
        "TRANSFER_INSURE": "TRANSFERRED",
        "ESCALATE": "OPEN",
        "BLOCK": "BLOCKED",
    }
    update = {
        "treatment": normalized,
        "status": state_map[normalized],
        "owner": owner.strip(),
        "mitigation": mitigation.strip(),
        "deadline": deadline.strip(),
        "evidence_refs": refs,
        "authority_decision_id": decision["id"],
        "policy_version_id": decision["policy_version_id"],
        "updated_at": utc_now_iso(),
    }
    await db.risks.update_one({"id": risk_id}, {"$set": update})
    await governance.audit_event(
        event_type="risk.critical_treatment.authorized",
        actor_id=actor_id,
        resource_type="risk",
        resource_id=risk_id,
        payload={
            "treatment": normalized,
            "authority_decision_id": decision["id"],
            "evidence_refs": refs,
        },
    )
    return {**risk, **update, "authority": decision}


async def register_insurance_policy(
    *,
    actor_id: str,
    provider: str,
    policy_ref: str,
    coverage_types: Iterable[str],
    limits: Dict[str, int],
    starts_at: str,
    ends_at: str,
    evidence_refs: Iterable[str],
) -> Dict[str, Any]:
    refs = _refs(evidence_refs)
    start = _parse(starts_at)
    end = _parse(ends_at)
    if start >= end:
        raise ValueError("insurance policy start must precede end")
    if not provider.strip() or not policy_ref.strip() or not refs:
        raise ValueError("insurance policy requires provider, policy_ref and evidence")
    if not coverage_types or not limits or any(int(v) < 0 for v in limits.values()):
        raise ValueError("insurance policy requires coverage types and non-negative limits")
    row = {
        "id": _id("INSPOL"),
        "provider": provider.strip(),
        "policy_ref": policy_ref.strip(),
        "coverage_types": sorted({str(v).strip().upper() for v in coverage_types if str(v).strip()}),
        "limits": {str(k).upper(): int(v) for k, v in limits.items()},
        "starts_at": start.isoformat(),
        "ends_at": end.isoformat(),
        "evidence_refs": refs,
        "status": "REGISTERED_NOT_LEGALLY_VALIDATED",
        "created_by": actor_id,
        "created_at": utc_now_iso(),
    }
    await db.insurance_policies.insert_one(dict(row))
    return row


async def link_risk_coverage(
    *,
    actor_id: str,
    risk_id: str,
    insurance_policy_id: str,
    coverage_type: str,
    evidence_refs: Iterable[str],
) -> Dict[str, Any]:
    refs = _refs(evidence_refs)
    risk = await db.risks.find_one({"id": risk_id}, {"_id": 0})
    policy = await db.insurance_policies.find_one({"id": insurance_policy_id}, {"_id": 0})
    if not risk or not policy:
        raise LookupError("risk or insurance policy not found")
    target = coverage_type.strip().upper()
    if target not in policy.get("coverage_types", []):
        raise ValueError("coverage type is not listed on insurance policy")
    if not refs:
        raise ValueError("risk coverage link requires evidence")
    row = {
        "id": _id("COV"),
        "risk_id": risk_id,
        "insurance_policy_id": insurance_policy_id,
        "coverage_type": target,
        "evidence_refs": refs,
        "coverage_confirmed": False,
        "status": "REVIEW_REQUIRED",
        "created_by": actor_id,
        "created_at": utc_now_iso(),
    }
    await db.risk_insurance_links.insert_one(dict(row))
    return row


async def review_coverage_link(
    *,
    actor_id: str,
    link_id: str,
    coverage_confirmed: bool,
    rationale: str,
    evidence_refs: Iterable[str],
) -> Dict[str, Any]:
    refs = _refs(evidence_refs)
    link = await db.risk_insurance_links.find_one({"id": link_id}, {"_id": 0})
    if not link:
        raise LookupError("risk coverage link not found")
    if not rationale.strip() or not refs:
        raise ValueError("coverage review requires rationale and evidence")
    update = {
        "coverage_confirmed": bool(coverage_confirmed),
        "status": "CONFIRMED" if coverage_confirmed else "NOT_COVERED",
        "rationale": rationale.strip(),
        "review_evidence_refs": refs,
        "reviewed_by": actor_id,
        "reviewed_at": utc_now_iso(),
    }
    await db.risk_insurance_links.update_one({"id": link_id}, {"$set": update})
    return {**link, **update}


async def uncovered_asset_gate() -> Dict[str, Any]:
    """RSK-006/007: critical risks without confirmed active coverage are explicit."""
    critical = await db.risks.find({"level": {"$gte": 4}}, {"_id": 0}).to_list(10000)
    now = datetime.now(timezone.utc)
    uncovered = []
    for risk in critical:
        links = await db.risk_insurance_links.find(
            {"risk_id": risk["id"], "coverage_confirmed": True}, {"_id": 0}
        ).to_list(1000)
        active = False
        for link in links:
            policy = await db.insurance_policies.find_one(
                {"id": link["insurance_policy_id"]}, {"_id": 0}
            )
            if policy and _parse(policy["starts_at"]) <= now < _parse(policy["ends_at"]):
                active = True
                break
        if not active:
            uncovered.append({"risk_id": risk["id"], "level": risk["level"], "domain": risk.get("domain")})
    return {"pass": not uncovered, "uncovered_count": len(uncovered), "uncovered_risks": uncovered}


async def renewal_alerts(*, as_of: Optional[datetime] = None) -> list[Dict[str, Any]]:
    moment = as_of or datetime.now(timezone.utc)
    policies = await db.insurance_policies.find({}, {"_id": 0}).to_list(10000)
    alerts = []
    for policy in policies:
        end = _parse(policy["ends_at"])
        days = (end - moment).days
        threshold = next((value for value in (30, 60, 90) if days <= value), None)
        if threshold is not None and days >= 0:
            alerts.append(
                {
                    "insurance_policy_id": policy["id"],
                    "days_remaining": days,
                    "threshold_days": threshold,
                    "ends_at": policy["ends_at"],
                }
            )
    return sorted(alerts, key=lambda row: row["days_remaining"])


async def create_claim_package(
    *, actor_id: str, risk_id: str, evidence_node_ids: Iterable[str], evidence_refs: Iterable[str]
) -> Dict[str, Any]:
    return await evidence_graph.create_pack(
        actor_id=actor_id,
        title=f"Insurance claim evidence — {risk_id}",
        consumer="RISK",
        node_ids=evidence_node_ids,
        purpose="Claim-support evidence package; coverage/legal acceptance remains external",
        evidence_refs=evidence_refs,
    )


async def create_renewal_package(
    *,
    actor_id: str,
    insurance_policy_id: str,
    evidence_node_ids: Iterable[str],
    evidence_refs: Iterable[str],
) -> Dict[str, Any]:
    if not await db.insurance_policies.find_one({"id": insurance_policy_id}):
        raise LookupError("insurance policy not found")
    return await evidence_graph.create_pack(
        actor_id=actor_id,
        title=f"Insurance renewal evidence — {insurance_policy_id}",
        consumer="RISK",
        node_ids=evidence_node_ids,
        purpose="Renewal evidence package for external broker/insurer review",
        evidence_refs=evidence_refs,
    )


async def get_broker_workspace(*, raw_key: str, case_id: str) -> Dict[str, Any]:
    context = await expert_access.authorize_case_scope(raw_key, case_id, "risk:insurance:read")
    case = await db.professional_cases.find_one({"id": case_id}, {"_id": 0})
    if not case:
        raise LookupError("professional case not found")
    if str(case.get("domain", "")).upper() != "RISK":
        raise PermissionError("broker workspace only exposes RISK cases")
    risk_ids = list((case.get("metadata") or {}).get("risk_ids", []))
    policy_ids = list((case.get("metadata") or {}).get("insurance_policy_ids", []))
    risks = await db.risks.find({"id": {"$in": risk_ids}}, {"_id": 0}).to_list(500)
    policies = await db.insurance_policies.find({"id": {"$in": policy_ids}}, {"_id": 0}).to_list(500)
    return {
        "case": case,
        "expert": {"id": context["expert"]["id"], "display_name": context["expert"]["display_name"]},
        "granted_scope": context["assignment"].get("scope", []),
        "risks": risks,
        "insurance_policies": policies,
        "external_cvl_data": None,
    }
