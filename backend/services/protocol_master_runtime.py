"""Executable CVLN Academy Protocol Master control plane — 227/227 Excel rows.

The workbook is authority for the control catalogue. This module makes every
Protocol Master row addressable and executable at runtime without inventing
legal/business approvals. Shared engines are reused: one control plane, one
proof registry, one incident/authority boundary.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
MANIFEST_PATH = ROOT / "docs/cvln_academy_master/30_PROTOCOLS/raw/protocol_master_runtime_snapshot.json"
EXPECTED_ROWS = 227
EXPECTED_DOMAINS = {
    "GOVERNANCE": 18,
    "LEGAL": 24,
    "PRIVACY": 35,
    "SECURITY": 40,
    "ACCOUNTING": 27,
    "RISK": 20,
    "QUALITY": 27,
    "TRUST": 14,
    "DATA": 14,
    "REGULATORY": 8,
}
DOMAIN_PREFIXES = {
    "GOVERNANCE": ("GOV", 18),
    "LEGAL": ("LEG", 24),
    "PRIVACY": ("PRI", 35),
    "SECURITY": ("SEC", 40),
    "ACCOUNTING": ("ACC", 27),
    "RISK": ("RSK", 20),
    "QUALITY": ("QLT", 27),
    "TRUST": ("TRU", 14),
    "DATA": ("DAT", 14),
    "REGULATORY": ("REG", 8),
}

# Fail-closed runtime requirements shared by every control in a domain. These
# are execution prerequisites, not claims that an external expert approved a
# doctrine. Human Authority remains explicit.
DOMAIN_REQUIREMENTS = {
    "GOVERNANCE": ("actor_id", "authority_context", "evidence_ref"),
    "LEGAL": ("actor_id", "jurisdiction", "expert_review_state", "evidence_ref"),
    "PRIVACY": ("actor_id", "data_classification", "lawful_basis", "evidence_ref"),
    "SECURITY": ("actor_id", "severity", "evidence_ref"),
    "ACCOUNTING": ("actor_id", "entity_context", "accounting_state", "evidence_ref"),
    "RISK": ("actor_id", "risk_level", "owner", "evidence_ref"),
    "QUALITY": ("actor_id", "quality_scope", "evidence_ref"),
    "TRUST": ("actor_id", "proof_ref", "evidence_ref"),
    "DATA": ("actor_id", "provenance_ref", "data_classification", "evidence_ref"),
    "REGULATORY": ("actor_id", "jurisdiction", "applicability_state", "expert_review_state", "evidence_ref"),
}


def _manifest() -> dict[str, Any]:
    with MANIFEST_PATH.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if data["row_count"] != EXPECTED_ROWS or data["domain_counts"] != EXPECTED_DOMAINS:
        raise ValueError("Protocol Master manifest drift")
    return data


def load_protocol_controls() -> list[dict[str, Any]]:
    manifest = _manifest()
    controls: list[dict[str, Any]] = []
    excel_row = int(manifest["first_excel_row"])
    for domain, (prefix, count) in DOMAIN_PREFIXES.items():
        for number in range(1, count + 1):
            control_id = f"{prefix}-{number:02d}"
            controls.append({
                "control_id": control_id,
                "domain": domain,
                "excel_row": excel_row,
                "runtime_handler": f"protocol:{domain.lower()}",
                "required_context": list(DOMAIN_REQUIREMENTS[domain]),
                "source": {
                    "kind": "PROTOCOL_MASTER_WORKBOOK",
                    "workbook": manifest["source_workbook"],
                    "workbook_sha256": manifest["source_workbook_sha256"],
                    "sheet": manifest["sheet"],
                    "excel_row": excel_row,
                },
            })
            excel_row += 1
    if len(controls) != EXPECTED_ROWS or excel_row - 1 != manifest["last_excel_row"]:
        raise ValueError("Protocol Master row mapping is not 3..229 / 227 rows")
    ids = [item["control_id"] for item in controls]
    if len(ids) != len(set(ids)):
        raise ValueError("Protocol Master contains duplicate runtime IDs")
    return controls


def evaluate_protocol_control(control: dict[str, Any], context: dict[str, Any]) -> dict[str, Any]:
    """Execute one row's fail-closed protocol gate.

    Every row has an executable handler. Missing authority/evidence never
    silently passes. Domain-specific invariants protect the dangerous edges.
    """
    missing = [key for key in control["required_context"] if not context.get(key)]
    reasons = [f"MISSING:{key}" for key in missing]
    domain = control["domain"]

    if domain in {"LEGAL", "REGULATORY"} and context.get("expert_review_state") == "REJECTED":
        reasons.append("EXPERT_REJECTED")
    if domain == "PRIVACY" and context.get("lawful_basis") in {"", None, "UNKNOWN"}:
        reasons.append("LAWFUL_BASIS_UNRESOLVED")
    if domain == "SECURITY" and context.get("severity") in {"HIGH", "CRITICAL", "SEV-1", "SEV-2"} and not context.get("incident_ref"):
        reasons.append("INCIDENT_REFERENCE_REQUIRED")
    if domain == "ACCOUNTING" and context.get("accounting_state") == "TAX_VALIDATED" and not context.get("expert_validation_ref"):
        reasons.append("TAX_PREPARED_NOT_VALIDATED_BY_EXPERT")
    if domain == "RISK" and context.get("risk_level") in {"R4", "R5", "HIGH", "CRITICAL"}:
        for key in ("mitigation", "deadline"):
            if not context.get(key):
                reasons.append(f"CRITICAL_RISK_MISSING:{key}")
    if domain == "TRUST" and context.get("proof_ref") and not context.get("proof_verified", False):
        reasons.append("PROOF_NOT_VERIFIED")
    if domain == "DATA" and context.get("mutation") and not context.get("mutation_evidence_ref"):
        reasons.append("SILENT_DATA_MUTATION_BLOCKED")
    if domain == "REGULATORY" and context.get("applicability_state") not in {"APPLIES", "DOES_NOT_APPLY", "REVIEWED"}:
        reasons.append("APPLICABILITY_UNRESOLVED")

    return {
        "control_id": control["control_id"],
        "excel_row": control["excel_row"],
        "domain": domain,
        "handler": control["runtime_handler"],
        "allowed": not reasons,
        "reasons": reasons,
        "evidence_ref": context.get("evidence_ref"),
    }


async def import_protocol_master_runtime(db: Any) -> dict[str, Any]:
    controls = load_protocol_controls()
    manifest = _manifest()
    for control in controls:
        await db.academy_protocol_controls.update_one(
            {"control_id": control["control_id"]}, {"$set": control}, upsert=True
        )
        requirement_id = f"PROTOCOL_MASTER:{control['control_id']}"
        await db.academy_requirement_registry.update_one(
            {"requirement_id": requirement_id},
            {"$set": {
                "requirement_id": requirement_id,
                "family": "PROTOCOL_MASTER",
                "control_id": control["control_id"],
                "domain": control["domain"],
                "excel_row": control["excel_row"],
                "source": control["source"],
                "runtime_collection": "academy_protocol_controls",
                "runtime_key": {"control_id": control["control_id"]},
                "runtime_importer": "services.protocol_master_runtime.import_protocol_master_runtime",
                "runtime_handler": control["runtime_handler"],
                "test_ref": "backend/tests/test_protocol_master_runtime.py",
            }, "$setOnInsert": {"status": "INGESTED_RUNTIME", "verified": False}},
            upsert=True,
        )
    await db.academy_protocol_controls.create_index("control_id", unique=True)
    await db.academy_protocol_controls.create_index([("domain", 1), ("excel_row", 1)])
    await db.academy_requirement_registry.create_index("requirement_id", unique=True)
    await db.academy_protocol_manifest.update_one(
        {"kind": "PROTOCOL_MASTER_WORKBOOK"},
        {"$set": {
            "kind": "PROTOCOL_MASTER_WORKBOOK",
            "source_workbook": manifest["source_workbook"],
            "source_workbook_sha256": manifest["source_workbook_sha256"],
            "runtime_rows": len(controls),
            "first_excel_row": 3,
            "last_excel_row": 229,
            "domain_counts": EXPECTED_DOMAINS,
        }}, upsert=True,
    )
    return {"rows": len(controls), "domain_counts": EXPECTED_DOMAINS, "source_workbook_sha256": manifest["source_workbook_sha256"]}
