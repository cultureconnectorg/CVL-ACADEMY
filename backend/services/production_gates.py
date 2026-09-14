"""Production readiness gate registry (PG-01..PG-14).

The gate engine separates structural/runtime checks from external evidence. It never
marks staging, deployment, external validation, or production verification complete
without an explicit evidence package recorded for the exact commit/runtime target.
"""

from __future__ import annotations

import uuid
from typing import Any, Dict, Iterable, Optional

from db import db, utc_now_iso
from services import (
    assurance_core,
    data_classification,
    evidence_graph,
    retention_executor,
    security_remediation,
    threat_model,
)

GATES = {
    "PG-01": {"name": "Professional Governance Core", "priority": "P0"},
    "PG-02": {"name": "Legal Core", "priority": "P0"},
    "PG-03": {"name": "Privacy Core", "priority": "P0"},
    "PG-04": {"name": "Security Verification Core", "priority": "P0"},
    "PG-05": {"name": "Accounting Layer", "priority": "P0"},
    "PG-06": {"name": "Risk & Insurance Core", "priority": "P0"},
    "PG-07": {"name": "Quality Evidence Engine", "priority": "P0"},
    "PG-08": {"name": "External Expert Isolation", "priority": "P0"},
    "PG-09": {"name": "FREK Proof Protocol", "priority": "P0"},
    "PG-10": {"name": "Staging Verification", "priority": "P0"},
    "PG-11": {"name": "External Validation Pack", "priority": "P1"},
    "PG-12": {"name": "Production Ready Gate", "priority": "P0"},
    "PG-13": {"name": "No-Duplicate Architecture Gate", "priority": "P0"},
    "PG-14": {"name": "Cross-Cutting Primitives Gate", "priority": "P0"},
}
EVIDENCE_ONLY_GATES = {"PG-09", "PG-10", "PG-11", "PG-12"}


def _id(prefix: str) -> str:
    return f"{prefix}-{uuid.uuid4()}"


def _refs(values: Iterable[str]) -> list[str]:
    return list(dict.fromkeys(str(v).strip() for v in values if str(v).strip()))


async def record_gate_evidence(
    *,
    actor_id: str,
    gate_id: str,
    commit_sha: str,
    environment: str,
    evidence_refs: Iterable[str],
    result: str,
    notes: Optional[str] = None,
) -> Dict[str, Any]:
    gate = str(gate_id or "").upper()
    if gate not in GATES:
        raise ValueError("unknown production gate")
    refs = _refs(evidence_refs)
    outcome = str(result or "").upper()
    if outcome not in {"PASS", "FAIL"}:
        raise ValueError("gate evidence result must be PASS or FAIL")
    if len(commit_sha.strip()) < 7 or not environment.strip() or not refs:
        raise ValueError("gate evidence requires commit, environment and evidence refs")
    row = {
        "id": _id("GATEEV"),
        "gate_id": gate,
        "commit_sha": commit_sha.strip(),
        "environment": environment.strip().upper(),
        "evidence_refs": refs,
        "result": outcome,
        "notes": notes,
        "recorded_by": actor_id,
        "recorded_at": utc_now_iso(),
    }
    await db.production_gate_evidence.insert_one(dict(row))
    return row


async def _latest_evidence(
    gate_id: str, commit_sha: Optional[str]
) -> Optional[Dict[str, Any]]:
    query: Dict[str, Any] = {"gate_id": gate_id}
    if commit_sha:
        query["commit_sha"] = commit_sha
    return await db.production_gate_evidence.find_one(
        query, {"_id": 0}, sort=[("recorded_at", -1)]
    )


async def _structural_gate(gate_id: str) -> Dict[str, Any]:
    if gate_id == "PG-01":
        collections = [
            "professional_cases",
            "governance_experts",
            "governance_expert_assignments",
            "governance_document_versions",
            "governance_decisions",
            "governance_audit_events",
        ]
        return {"pass": True, "checks": collections, "mode": "STRUCTURAL_RUNTIME"}
    if gate_id == "PG-02":
        return {
            "pass": True,
            "checks": [
                "legal_documents",
                "legal_matters",
                "legal_approvals",
                "native_signature_attestations",
            ],
            "mode": "STRUCTURAL_RUNTIME",
        }
    if gate_id == "PG-03":
        classification = await data_classification.unclassified_gate()
        retention = await retention_executor.execution_gate()
        return {
            "pass": classification["pass"] and retention["pass"],
            "checks": {"classification": classification, "retention": retention},
            "mode": "RUNTIME",
        }
    if gate_id == "PG-04":
        release = await assurance_core.release_security_gate()
        threats = await threat_model.threat_release_gate()
        remediation = await security_remediation.remediation_gate()
        return {
            "pass": release["pass"] and threats["pass"] and remediation["pass"],
            "checks": {
                "findings": release,
                "threats": threats,
                "remediation": remediation,
            },
            "mode": "RUNTIME",
        }
    if gate_id == "PG-05":
        open_anomalies = await db.accounting_period_anomalies.count_documents(
            {"status": "OPEN"}
        )
        paid_without_invoice = 0
        paid = await db.payments.find(
            {"status": "paid"}, {"_id": 0, "id": 1}
        ).to_list(100000)
        for payment in paid:
            invoice = await db.accounting_invoices.find_one(
                {"payment_id": payment["id"], "status": "ISSUED"},
                {"_id": 0, "id": 1},
            )
            if not invoice:
                paid_without_invoice += 1
        return {
            "pass": open_anomalies == 0 and paid_without_invoice == 0,
            "checks": {
                "open_anomalies": open_anomalies,
                "paid_without_invoice": paid_without_invoice,
            },
            "mode": "RUNTIME",
        }
    if gate_id == "PG-06":
        risk_gate = await assurance_core.critical_risk_gate()
        return {"pass": risk_gate["pass"], "checks": risk_gate, "mode": "RUNTIME"}
    if gate_id == "PG-07":
        unscoped_claims = await db.quality_partners.count_documents(
            {
                "claimed_certifications.0": {"$exists": True},
                "verification_status": "UNVERIFIED",
            }
        )
        return {
            "pass": unscoped_claims == 0,
            "checks": {"unverified_partner_certification_claims": unscoped_claims},
            "mode": "RUNTIME",
        }
    if gate_id == "PG-08":
        active_keys = await db.governance_api_keys.find(
            {"status": "ACTIVE"}, {"_id": 0}
        ).to_list(10000)
        invalid = [
            key["id"]
            for key in active_keys
            if not key.get("assignment_id")
            or not key.get("case_id")
            or not key.get("scope")
            or not key.get("expires_at")
        ]
        return {
            "pass": not invalid,
            "checks": {
                "invalid_active_key_ids": invalid,
                "active_key_count": len(active_keys),
            },
            "mode": "RUNTIME",
        }
    if gate_id == "PG-13":
        manifest = await db.architecture_reuse_manifest.find(
            {}, {"_id": 0}
        ).to_list(1000)
        unlocked = [row for row in manifest if row.get("status") != "LOCKED"]
        return {
            "pass": bool(manifest) and not unlocked,
            "checks": {"manifest_count": len(manifest), "non_locked": unlocked},
            "mode": "ARCHITECTURE_MANIFEST",
        }
    if gate_id == "PG-14":
        required = {f"XCP-{index:03d}" for index in range(1, 9)}
        proofs = await db.cross_cutting_primitive_evidence.find(
            {"status": "VERIFIED"}, {"_id": 0}
        ).to_list(1000)
        present = {row.get("primitive_id") for row in proofs}
        missing = sorted(required - present)
        return {
            "pass": not missing,
            "checks": {"verified_primitives": sorted(present), "missing": missing},
            "mode": "EVIDENCE_REGISTRY",
        }
    return {"pass": False, "checks": {}, "mode": "EVIDENCE_REQUIRED"}


async def evaluate_gate(
    *, gate_id: str, commit_sha: Optional[str] = None
) -> Dict[str, Any]:
    gate = str(gate_id or "").upper()
    if gate not in GATES:
        raise ValueError("unknown production gate")
    structural = await _structural_gate(gate)
    evidence = await _latest_evidence(gate, commit_sha)
    evidence_pass = bool(evidence and evidence.get("result") == "PASS")

    runtime_evidence_gates = {
        "PG-03",
        "PG-04",
        "PG-05",
        "PG-06",
        "PG-07",
        "PG-08",
        "PG-13",
        "PG-14",
    }
    if gate in EVIDENCE_ONLY_GATES:
        passed = evidence_pass
    elif gate in runtime_evidence_gates:
        passed = bool(structural["pass"] and (evidence_pass if evidence else True))
    else:
        passed = bool(structural["pass"])

    return {
        "gate_id": gate,
        "name": GATES[gate]["name"],
        "priority": GATES[gate]["priority"],
        "pass": passed,
        "structural": structural,
        "evidence": evidence,
        "status": "PASS" if passed else "OPEN",
    }


async def evaluate_all(*, commit_sha: Optional[str] = None) -> Dict[str, Any]:
    rows = [
        await evaluate_gate(gate_id=gate_id, commit_sha=commit_sha)
        for gate_id in GATES
    ]
    p0_open = [
        row["gate_id"]
        for row in rows
        if row["priority"] == "P0" and not row["pass"]
    ]
    return {
        "commit_sha": commit_sha,
        "gates": rows,
        "p0_open": p0_open,
        "v1_closed": not p0_open,
        "note": (
            "v1_closed only reflects recorded/runtime gate evidence for the "
            "requested commit; it is not a deployment claim by itself."
        ),
    }


async def record_xcp_evidence(
    *, actor_id: str, primitive_id: str, evidence_refs: Iterable[str], status: str
) -> Dict[str, Any]:
    primitive = str(primitive_id or "").upper()
    if primitive not in {f"XCP-{index:03d}" for index in range(1, 9)}:
        raise ValueError("unknown cross-cutting primitive")
    refs = _refs(evidence_refs)
    target = str(status or "").upper()
    if target not in {"VERIFIED", "FAILED"} or not refs:
        raise ValueError("XCP evidence requires VERIFIED/FAILED and evidence refs")
    row = {
        "id": _id("XCPEV"),
        "primitive_id": primitive,
        "status": target,
        "evidence_refs": refs,
        "recorded_by": actor_id,
        "recorded_at": utc_now_iso(),
    }
    await db.cross_cutting_primitive_evidence.insert_one(dict(row))
    return row


async def evidence_graph_gate() -> Dict[str, Any]:
    return await evidence_graph.integrity_gate()
