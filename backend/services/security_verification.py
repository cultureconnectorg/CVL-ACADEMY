"""Security Verification Core (SEC-001..010, SEC-013/014).

This service composes existing security truth instead of creating parallel engines:
- ``security_assets`` and ``security_findings`` remain the Assurance Core stores;
- ``security_threats`` remains the Threat Model registry;
- remediation state remains in security_remediation;
- XCP-001 governs risk acceptance authority;
- XCP-004 composes evidence packs by reference only;
- XCP-006 scopes external pentest access.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, Optional

from db import db, utc_now_iso
from services import assurance_core, authority_policy, evidence_graph, expert_access
from services import professional_governance as governance
from services import security_remediation, threat_model


CI_GATES = {"SAST", "DEPENDENCY_AUDIT", "SECRET_DETECTION"}
REQUIRED_ATTACK_AREAS = {
    "AUTH",
    "RBAC",
    "IDOR",
    "JWT",
    "INJECTION",
    "XSS",
    "SSRF",
    "CSRF",
    "CORS",
    "RATE_LIMIT",
}
PAYMENT_ATTACK_AREAS = {
    "WEBHOOK_REPLAY",
    "AMOUNT_TAMPER",
    "DUPLICATE_PAYMENT",
    "IDEMPOTENCY",
}


def _id(prefix: str) -> str:
    return f"{prefix}-{uuid.uuid4()}"


def _refs(values: Iterable[str]) -> list[str]:
    return list(dict.fromkeys(str(v).strip() for v in values if str(v).strip()))


def _parse_future(value: str) -> str:
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError("expires_at must be ISO-8601") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ValueError("expires_at must include timezone")
    parsed = parsed.astimezone(timezone.utc)
    if parsed <= datetime.now(timezone.utc):
        raise ValueError("expires_at must be in the future")
    return parsed.isoformat()


async def register_asset(
    *,
    actor_id: str,
    name: str,
    asset_type: str,
    owner: str,
    exposure: str,
    criticality: str,
    endpoints: Iterable[str] = (),
    services: Iterable[str] = (),
    data_stores: Iterable[str] = (),
    attack_surfaces: Iterable[str] = (),
    evidence_refs: Iterable[str] = (),
) -> Dict[str, Any]:
    """SEC-001: inventory one asset plus its concrete runtime surfaces."""
    refs = _refs(evidence_refs)
    asset = await assurance_core.create_security_asset(
        actor_id=actor_id,
        name=name,
        asset_type=asset_type,
        owner=owner,
        exposure=exposure,
        criticality=criticality,
    )
    extension = {
        "endpoints": sorted({str(v).strip() for v in endpoints if str(v).strip()}),
        "services": sorted({str(v).strip() for v in services if str(v).strip()}),
        "data_stores": sorted({str(v).strip() for v in data_stores if str(v).strip()}),
        "attack_surfaces": sorted(
            {str(v).strip().upper() for v in attack_surfaces if str(v).strip()}
        ),
        "evidence_refs": refs,
        "inventory_complete": bool(refs),
        "updated_at": utc_now_iso(),
    }
    await db.security_assets.update_one({"id": asset["id"]}, {"$set": extension})
    await governance.audit_event(
        event_type="security.asset.inventory_registered",
        actor_id=actor_id,
        resource_type="security_asset",
        resource_id=asset["id"],
        payload={
            "endpoints": extension["endpoints"],
            "services": extension["services"],
            "data_stores": extension["data_stores"],
            "evidence_refs": refs,
        },
    )
    return {**asset, **extension}


async def record_ci_gate(
    *,
    actor_id: str,
    gate: str,
    run_ref: str,
    passed: bool,
    findings: Iterable[str] = (),
    evidence_refs: Iterable[str] = (),
) -> Dict[str, Any]:
    """SEC-003/004/005: persist real CI outcome; no assumed green state."""
    target = gate.strip().upper()
    refs = _refs(evidence_refs)
    if target not in CI_GATES:
        raise ValueError("invalid security CI gate")
    if not run_ref.strip() or not refs:
        raise ValueError("security CI gate requires run_ref and evidence")
    row = {
        "id": _id("SCIG"),
        "gate": target,
        "run_ref": run_ref.strip(),
        "passed": bool(passed),
        "findings": _refs(findings),
        "evidence_refs": refs,
        "recorded_by": actor_id,
        "recorded_at": utc_now_iso(),
    }
    await db.security_ci_gate_runs.insert_one(dict(row))
    return row


async def record_attack_suite_run(
    *,
    actor_id: str,
    suite: str,
    run_ref: str,
    covered_areas: Iterable[str],
    failed_cases: Iterable[str] = (),
    evidence_refs: Iterable[str],
) -> Dict[str, Any]:
    """SEC-006/007: record coverage and negative test outcome from a real test run."""
    target = suite.strip().upper()
    if target not in {"APPLICATION", "PAYMENT"}:
        raise ValueError("attack suite must be APPLICATION or PAYMENT")
    refs = _refs(evidence_refs)
    covered = {str(v).strip().upper() for v in covered_areas if str(v).strip()}
    required = REQUIRED_ATTACK_AREAS if target == "APPLICATION" else PAYMENT_ATTACK_AREAS
    missing = sorted(required - covered)
    failures = _refs(failed_cases)
    if not run_ref.strip() or not refs:
        raise ValueError("attack suite run requires run_ref and evidence")
    row = {
        "id": _id("ATKRUN"),
        "suite": target,
        "run_ref": run_ref.strip(),
        "covered_areas": sorted(covered),
        "required_areas": sorted(required),
        "missing_areas": missing,
        "failed_cases": failures,
        "passed": not missing and not failures,
        "evidence_refs": refs,
        "recorded_by": actor_id,
        "recorded_at": utc_now_iso(),
    }
    await db.security_attack_runs.insert_one(dict(row))
    return row


async def record_finding_retest(
    *,
    actor_id: str,
    finding_id: str,
    passed: bool,
    test_refs: Iterable[str],
    evidence_refs: Iterable[str],
) -> Dict[str, Any]:
    """SEC-008: finding remediation must have concrete retest evidence."""
    tests = _refs(test_refs)
    refs = _refs(evidence_refs)
    finding = await db.security_findings.find_one({"id": finding_id}, {"_id": 0})
    if not finding:
        raise LookupError("security finding not found")
    if not tests or not refs:
        raise ValueError("finding retest requires test_refs and evidence_refs")
    row = {
        "id": _id("RETEST"),
        "finding_id": finding_id,
        "passed": bool(passed),
        "test_refs": tests,
        "evidence_refs": refs,
        "recorded_by": actor_id,
        "recorded_at": utc_now_iso(),
    }
    await db.security_finding_retests.insert_one(dict(row))
    status = "RESOLVED" if passed else "REMEDIATING"
    await db.security_findings.update_one(
        {"id": finding_id},
        {
            "$set": {
                "status": status,
                "last_retest_id": row["id"],
                "updated_at": utc_now_iso(),
            }
        },
    )
    await governance.audit_event(
        event_type="security.finding.retested",
        actor_id=actor_id,
        resource_type="security_finding",
        resource_id=finding_id,
        payload={"retest_id": row["id"], "passed": bool(passed), "evidence_refs": refs},
    )
    return {**row, "finding_status": status}


async def accept_finding_risk(
    *,
    actor_id: str,
    actor_role: str,
    authority_level: str,
    finding_id: str,
    rationale: str,
    expires_at: str,
    policy_version_id: str,
    evidence_refs: Iterable[str],
) -> Dict[str, Any]:
    """SEC-010: A5 evidence-backed, expiring risk acceptance."""
    finding = await db.security_findings.find_one({"id": finding_id}, {"_id": 0})
    if not finding:
        raise LookupError("security finding not found")
    refs = _refs(evidence_refs)
    expiry = _parse_future(expires_at)
    if not rationale.strip() or not refs:
        raise ValueError("risk acceptance requires rationale and evidence")
    decision = await authority_policy.evaluate_authority(
        actor_id=actor_id,
        actor_role=actor_role,
        action="SECURITY_RISK_ACCEPT",
        context={
            "domain": "SECURITY",
            "authority_level": authority_level,
            "finding_id": finding_id,
            "severity": finding.get("severity"),
            "expires_at": expiry,
        },
        policy_version_id=policy_version_id,
    )
    if decision["policy_key"] != "SECURITY_RISK_ACCEPTANCE":
        raise ValueError("risk acceptance requires SECURITY_RISK_ACCEPTANCE policy")
    if decision["decision"] != "ALLOW":
        raise PermissionError("authority policy did not allow security risk acceptance")
    row = {
        "id": _id("RACC"),
        "finding_id": finding_id,
        "rationale": rationale.strip(),
        "accepted_by": actor_id,
        "authority_decision_id": decision["id"],
        "policy_version_id": decision["policy_version_id"],
        "policy_hash": decision["policy_content_hash"],
        "evidence_refs": refs,
        "expires_at": expiry,
        "status": "ACTIVE",
        "created_at": utc_now_iso(),
    }
    await db.security_risk_acceptances.insert_one(dict(row))
    await db.security_findings.update_one(
        {"id": finding_id},
        {
            "$set": {
                "status": "ACCEPTED",
                "risk_acceptance_id": row["id"],
                "updated_at": utc_now_iso(),
            }
        },
    )
    return {**row, "authority": decision}


async def expire_risk_acceptances(*, actor_id: str) -> list[str]:
    now = datetime.now(timezone.utc).isoformat()
    rows = await db.security_risk_acceptances.find(
        {"status": "ACTIVE", "expires_at": {"$lte": now}}, {"_id": 0}
    ).to_list(1000)
    expired_ids = []
    for row in rows:
        await db.security_risk_acceptances.update_one(
            {"id": row["id"], "status": "ACTIVE"},
            {"$set": {"status": "EXPIRED", "expired_at": utc_now_iso()}},
        )
        await db.security_findings.update_one(
            {"id": row["finding_id"], "status": "ACCEPTED", "risk_acceptance_id": row["id"]},
            {"$set": {"status": "OPEN", "updated_at": utc_now_iso()}},
        )
        expired_ids.append(row["id"])
        await governance.audit_event(
            event_type="security.risk_acceptance.expired",
            actor_id=actor_id,
            resource_type="security_finding",
            resource_id=row["finding_id"],
            payload={"risk_acceptance_id": row["id"]},
        )
    return expired_ids


async def security_release_gate() -> Dict[str, Any]:
    """SEC-009: aggregate all concrete security blockers before release."""
    await expire_risk_acceptances(actor_id="SYSTEM:SECURITY_GATE")
    finding_gate = await assurance_core.release_security_gate()
    threat_gate = await threat_model.threat_release_gate()
    remediation = await security_remediation.remediation_gate()

    ci_latest: Dict[str, Optional[Dict[str, Any]]] = {}
    for gate in sorted(CI_GATES):
        ci_latest[gate] = await db.security_ci_gate_runs.find_one(
            {"gate": gate}, {"_id": 0}, sort=[("recorded_at", -1)]
        )
    ci_missing_or_failed = [
        gate for gate, row in ci_latest.items() if not row or not row.get("passed")
    ]

    attack_latest: Dict[str, Optional[Dict[str, Any]]] = {}
    for suite in ("APPLICATION", "PAYMENT"):
        attack_latest[suite] = await db.security_attack_runs.find_one(
            {"suite": suite}, {"_id": 0}, sort=[("recorded_at", -1)]
        )
    attack_missing_or_failed = [
        suite for suite, row in attack_latest.items() if not row or not row.get("passed")
    ]

    pass_gate = (
        finding_gate["pass"]
        and threat_gate["pass"]
        and remediation["pass"]
        and not ci_missing_or_failed
        and not attack_missing_or_failed
    )
    return {
        "pass": pass_gate,
        "finding_gate": finding_gate,
        "threat_gate": threat_gate,
        "remediation_gate": remediation,
        "ci_latest": ci_latest,
        "ci_missing_or_failed": ci_missing_or_failed,
        "attack_latest": attack_latest,
        "attack_missing_or_failed": attack_missing_or_failed,
    }


async def create_security_evidence_pack(
    *,
    actor_id: str,
    title: str,
    evidence_node_ids: Iterable[str],
    evidence_refs: Iterable[str],
) -> Dict[str, Any]:
    """SEC-014: reference-only external audit pack via XCP-004."""
    return await evidence_graph.create_pack(
        actor_id=actor_id,
        title=title,
        consumer="SECURITY",
        node_ids=evidence_node_ids,
        purpose="Security controls, tests, findings, retests and accepted-risk evidence",
        evidence_refs=evidence_refs,
    )


async def get_pentest_workspace(*, raw_key: str, case_id: str) -> Dict[str, Any]:
    """SEC-013: isolated black-box scope; never exposes internal code/findings globally."""
    context = await expert_access.authorize_case_scope(raw_key, case_id, "security:pentest:read")
    case = await db.professional_cases.find_one({"id": case_id}, {"_id": 0})
    if not case:
        raise LookupError("professional case not found")
    if str(case.get("domain", "")).upper() != "SECURITY":
        raise PermissionError("pentest workspace only exposes SECURITY cases")
    expert = context["expert"]
    if "SECURITY" not in {str(v).upper() for v in expert.get("domains", [])}:
        raise PermissionError("expert identity is not authorised for SECURITY domain")
    scope = case.get("metadata", {}).get("black_box_scope", {})
    return {
        "case": {
            "id": case["id"],
            "title": case["title"],
            "status": case["status"],
            "sensitivity": case.get("sensitivity"),
        },
        "black_box_scope": scope,
        "expert": {"id": expert["id"], "display_name": expert["display_name"]},
        "granted_scope": context["assignment"].get("scope", []),
        "internal_code_exposed": False,
        "unassigned_findings_exposed": False,
    }
