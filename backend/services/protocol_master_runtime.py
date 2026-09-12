"""Executable Protocol workbook runtime with 227 row-specific contracts."""

from __future__ import annotations

import base64
import hashlib
import json
import zlib
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = ROOT / "docs/cvln_academy_master/30_PROTOCOLS/raw"
MANIFEST_PATH = RAW_DIR / "protocol_master_runtime_snapshot.json"
CONTRACT_PARTS = tuple(
    RAW_DIR / f"contracts.zlib.b64.part{index:02d}" for index in range(1, 5)
)
EXPECTED_ROWS = 227
EXPECTED_WORKBOOK_ROWS = 328
EXPECTED_SHEET_ROWS = {
    "Dashboard": 24,
    "Protocol Master": 229,
    "Integration Map": 25,
    "Build Waves": 14,
    "Existing Repo Truth": 16,
    "External Regulatory Map": 10,
    "Lists": 10,
}
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
BEHAVIOR_SCHEMA_VERSION = "protocol-row-contract-v2"

INTEGRATION_ADAPTERS = {
    "Accounting": "services.accounting_core",
    "Agent Factory": "services.agent_factory",
    "Auth": "auth",
    "Auth/RBAC": "auth",
    "Authority Engine": "services.authority_policy",
    "CI": ".github/workflows/ci.yml",
    "CVLN iOS": "services.integrations",
    "CVLN iOS entity context": "services.integrations",
    "Certification": "api.certification",
    "Command Center": "services.integrations",
    "Commerce": "api.commerce",
    "Data Classification": "api.data_classification",
    "Document Registry": "services.document_registry",
    "Event Bus": "services.events",
    "Evidence Graph": "services.evidence_graph",
    "FREK": "services.frek_core",
    "Incident Core": "services.incident_core",
    "Learning": "api.learning",
    "Legal": "services.legal_core",
    "Legal/Regulatory": "api.regulatory_applicability",
    "Licensing": "api.license_entitlement",
    "Payments": "api.payments",
    "Physical Delivery": "api.physical_sessions",
    "Privacy": "services.privacy_core",
    "Professional Governance": "services.professional_governance",
    "Retention": "api.retention_executor",
    "Security": "services.security_core",
    "Trust/Signature": "api.trust_signature",
    "Wallet": "api.wallet",
    "domain-specific cores": "services.integrations",
}

DOMAIN_REQUIREMENTS = {
    "GOVERNANCE": ("authority_context",),
    "LEGAL": ("jurisdiction", "expert_review_state"),
    "PRIVACY": ("data_classification", "lawful_basis"),
    "SECURITY": ("severity",),
    "ACCOUNTING": ("entity_context", "accounting_state"),
    "RISK": ("risk_level", "owner"),
    "QUALITY": ("quality_scope",),
    "TRUST": ("proof_ref", "proof_verified"),
    "DATA": ("provenance_ref", "data_classification"),
    "REGULATORY": (
        "jurisdiction",
        "applicability_state",
        "expert_review_state",
    ),
}


def _canonical_hash(payload: Any) -> str:
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def _manifest() -> dict[str, Any]:
    with MANIFEST_PATH.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if data["control_count"] != EXPECTED_ROWS:
        raise ValueError("Protocol Master control manifest drift")
    if data["domain_counts"] != EXPECTED_DOMAINS:
        raise ValueError("Protocol Master domain manifest drift")
    if data["workbook_nonempty_rows"] != EXPECTED_WORKBOOK_ROWS:
        raise ValueError("Protocol workbook row manifest drift")
    if data["sheet_nonempty_rows"] != EXPECTED_SHEET_ROWS:
        raise ValueError("Protocol workbook sheet manifest drift")
    return data


def _load_contract_payload() -> dict[str, Any]:
    encoded = "".join(
        path.read_text(encoding="utf-8").strip() for path in CONTRACT_PARTS
    )
    try:
        raw = zlib.decompress(base64.b64decode(encoded)).decode("utf-8")
        payload = json.loads(raw)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        raise ValueError("Protocol Master contract archive is invalid") from exc
    return payload


def _behavior_fingerprint(control: dict[str, Any]) -> str:
    return _canonical_hash(
        {
            "schema": BEHAVIOR_SCHEMA_VERSION,
            "control_id": control["control_id"],
            "row_hash": control["row_hash"],
            "type": control["type"],
            "build_target": control["build_target"],
            "integrates_with": control["integrates_with"],
            "external_expert": control["external_expert"],
            "production_gate": control["production_gate"],
        }
    )


def _required_context(control: dict[str, Any]) -> list[str]:
    fields = [
        "actor_id",
        "evidence_ref",
        "control_id",
        "behavior_fingerprint",
        "control_version_ref",
        "integration_refs",
    ]
    fields.extend(DOMAIN_REQUIREMENTS[control["domain"]])
    if control["frek"] == "YES":
        fields.append("frek_proof_ref")
    if control["production_gate"] == "YES":
        fields.append("production_gate_evidence_ref")
    if control["external_expert"]:
        fields.append("expert_review_ref")
    if control["cvln_ios"] == "YES":
        fields.append("cvln_ios_ref")
    if control["control_id"] == "GOV-02":
        fields.append("policy_version_id")
    if control["control_id"] == "REG-04":
        fields.append("legal_assurance_level")
    return list(dict.fromkeys(fields))


def load_protocol_workbook_rows() -> list[dict[str, Any]]:
    """Return a source identity for every non-empty row in all seven sheets."""
    manifest = _manifest()
    rows: list[dict[str, Any]] = []
    for sheet, count in EXPECTED_SHEET_ROWS.items():
        excel_rows = (
            [1] + list(range(3, 26)) if sheet == "Dashboard" else range(1, count + 1)
        )
        if len(list(excel_rows)) != count:
            raise ValueError(f"{sheet}: row identity count drift")
        for excel_row in excel_rows:
            rows.append(
                {
                    "row_id": f"{sheet}:{excel_row}",
                    "sheet": sheet,
                    "excel_row": excel_row,
                    "source": {
                        "kind": "PROTOCOL_WORKBOOK",
                        "workbook": manifest["source_workbook"],
                        "workbook_sha256": manifest["source_workbook_sha256"],
                        "sheet": sheet,
                        "excel_row": excel_row,
                    },
                }
            )
    if len(rows) != EXPECTED_WORKBOOK_ROWS:
        raise ValueError("Protocol workbook row count drift")
    if len({row["row_id"] for row in rows}) != EXPECTED_WORKBOOK_ROWS:
        raise ValueError("Protocol workbook row identities are not unique")
    return rows


def load_protocol_controls() -> list[dict[str, Any]]:
    """Load the exact 227 Excel contracts and attach executable metadata."""
    manifest = _manifest()
    payload = _load_contract_payload()
    raw_controls = payload.get("controls") or []
    controls: list[dict[str, Any]] = []
    for raw in raw_controls:
        control = dict(raw)
        control["behavior_fingerprint"] = _behavior_fingerprint(control)
        control["required_context"] = _required_context(control)
        control["integration_adapters"] = {
            name: INTEGRATION_ADAPTERS.get(name) for name in control["integrates_with"]
        }
        control["runtime_handler"] = f"protocol:{control['control_id'].lower()}"
        control["source"] = {
            "kind": "PROTOCOL_MASTER_WORKBOOK",
            "workbook": manifest["source_workbook"],
            "workbook_sha256": manifest["source_workbook_sha256"],
            "sheet": manifest["protocol_sheet"],
            "excel_row": control["excel_row"],
            "row_hash": control["row_hash"],
        }
        controls.append(control)

    if len(controls) != EXPECTED_ROWS:
        raise ValueError("Protocol Master is not exactly 227 contracts")
    if [row["excel_row"] for row in controls] != list(range(3, 230)):
        raise ValueError("Protocol Master Excel row mapping drift")
    if len({row["control_id"] for row in controls}) != EXPECTED_ROWS:
        raise ValueError("Protocol Master IDs are not unique")
    if len({row["row_hash"] for row in controls}) != EXPECTED_ROWS:
        raise ValueError("Protocol Master row hashes are not unique")
    if len({row["behavior_fingerprint"] for row in controls}) != EXPECTED_ROWS:
        raise ValueError("Protocol Master behaviors are not unique")
    if dict(Counter(row["domain"] for row in controls)) != EXPECTED_DOMAINS:
        raise ValueError("Protocol Master domain counts drift")
    unresolved = {
        name
        for row in controls
        for name, adapter in row["integration_adapters"].items()
        if not adapter
    }
    if unresolved:
        raise ValueError(f"Protocol integrations have no adapter: {sorted(unresolved)}")
    return controls


def _append_if_missing(context: dict[str, Any], key: str, reasons: list[str]) -> None:
    if not context.get(key):
        reasons.append(f"MISSING:{key}")


def evaluate_protocol_control(
    control: dict[str, Any], context: dict[str, Any]
) -> dict[str, Any]:
    """Evaluate one exact Excel row contract, fail-closed."""
    reasons: list[str] = []
    for key in control["required_context"]:
        _append_if_missing(context, key, reasons)

    if context.get("control_id") != control["control_id"]:
        reasons.append("CONTROL_ID_MISMATCH")
    if context.get("behavior_fingerprint") != control["behavior_fingerprint"]:
        reasons.append("BEHAVIOR_FINGERPRINT_MISMATCH")

    integration_refs = context.get("integration_refs") or {}
    for name in control["integrates_with"]:
        if not integration_refs.get(name):
            reasons.append(f"INTEGRATION_NOT_PROVEN:{name}")

    domain = control["domain"]
    if domain in {"LEGAL", "REGULATORY"}:
        if context.get("expert_review_state") == "REJECTED":
            reasons.append("EXPERT_REJECTED")
    if domain == "PRIVACY" and context.get("lawful_basis") in {
        "",
        None,
        "UNKNOWN",
    }:
        reasons.append("LAWFUL_BASIS_UNRESOLVED")
    if domain == "SECURITY" and context.get("severity") in {
        "HIGH",
        "CRITICAL",
        "SEV-1",
        "SEV-2",
    }:
        _append_if_missing(context, "incident_ref", reasons)
    if control["control_id"] == "ACC-11":
        if context.get("accounting_state") == "TAX_VALIDATED":
            _append_if_missing(context, "expert_validation_ref", reasons)
    if domain == "RISK" and context.get("risk_level") in {
        "R4",
        "R5",
        "HIGH",
        "CRITICAL",
    }:
        _append_if_missing(context, "mitigation", reasons)
        _append_if_missing(context, "deadline", reasons)
    if domain == "TRUST" and context.get("proof_ref"):
        if context.get("proof_verified") is not True:
            reasons.append("PROOF_NOT_VERIFIED")
    if domain == "DATA" and context.get("mutation"):
        _append_if_missing(context, "mutation_evidence_ref", reasons)
    if domain == "REGULATORY" and context.get("applicability_state") not in {
        "APPLIES",
        "DOES_NOT_APPLY",
        "REVIEWED",
    }:
        reasons.append("APPLICABILITY_UNRESOLVED")
    if control["cvln_ios"] == "CONTEXT" and context.get("systemic"):
        _append_if_missing(context, "cvln_ios_ref", reasons)

    return {
        "control_id": control["control_id"],
        "excel_row": control["excel_row"],
        "domain": domain,
        "title": control["title"],
        "behavior_fingerprint": control["behavior_fingerprint"],
        "handler": control["runtime_handler"],
        "allowed": not reasons,
        "reasons": reasons,
        "evidence_ref": context.get("evidence_ref"),
        "row_hash": control["row_hash"],
    }


async def import_protocol_master_runtime(db: Any) -> dict[str, Any]:
    controls = load_protocol_controls()
    workbook_rows = load_protocol_workbook_rows()
    manifest = _manifest()

    for row in workbook_rows:
        await db.academy_protocol_workbook_rows.update_one(
            {"row_id": row["row_id"]}, {"$set": row}, upsert=True
        )
    for control in controls:
        await db.academy_protocol_controls.update_one(
            {"control_id": control["control_id"]}, {"$set": control}, upsert=True
        )
        requirement_id = f"PROTOCOL_MASTER:{control['control_id']}"
        await db.academy_requirement_registry.update_one(
            {"requirement_id": requirement_id},
            {
                "$set": {
                    "requirement_id": requirement_id,
                    "family": "PROTOCOL_MASTER",
                    "control_id": control["control_id"],
                    "domain": control["domain"],
                    "excel_row": control["excel_row"],
                    "row_hash": control["row_hash"],
                    "behavior_fingerprint": control["behavior_fingerprint"],
                    "source": control["source"],
                    "runtime_collection": "academy_protocol_controls",
                    "runtime_key": {"control_id": control["control_id"]},
                    "runtime_importer": (
                        "services.protocol_master_runtime."
                        "import_protocol_master_runtime"
                    ),
                    "runtime_handler": control["runtime_handler"],
                    "test_ref": "backend/tests/test_protocol_master_runtime.py",
                },
                "$setOnInsert": {"status": "INGESTED_RUNTIME", "verified": False},
            },
            upsert=True,
        )

    await db.academy_protocol_workbook_rows.create_index("row_id", unique=True)
    await db.academy_protocol_workbook_rows.create_index(
        [("sheet", 1), ("excel_row", 1)], unique=True
    )
    await db.academy_protocol_controls.create_index("control_id", unique=True)
    await db.academy_protocol_controls.create_index([("domain", 1), ("excel_row", 1)])
    await db.academy_requirement_registry.create_index("requirement_id", unique=True)
    await db.academy_protocol_manifest.update_one(
        {"kind": "PROTOCOL_MASTER_WORKBOOK"},
        {
            "$set": {
                "kind": "PROTOCOL_MASTER_WORKBOOK",
                "source_workbook": manifest["source_workbook"],
                "source_workbook_sha256": manifest["source_workbook_sha256"],
                "workbook_runtime_rows": len(workbook_rows),
                "runtime_controls": len(controls),
                "unique_behaviors": len(
                    {row["behavior_fingerprint"] for row in controls}
                ),
                "sheet_nonempty_rows": EXPECTED_SHEET_ROWS,
                "domain_counts": EXPECTED_DOMAINS,
            }
        },
        upsert=True,
    )
    return {
        "workbook_rows": len(workbook_rows),
        "controls": len(controls),
        "unique_behaviors": len({row["behavior_fingerprint"] for row in controls}),
        "sheet_nonempty_rows": EXPECTED_SHEET_ROWS,
        "domain_counts": EXPECTED_DOMAINS,
        "source_workbook_sha256": manifest["source_workbook_sha256"],
    }
