"""Runtime wiring for every Economy 3D Mapping_812 row.

The Excel row remains the authority for packaging/public/sale policy. Runtime
state only supplies evidence for activation gates; it never upgrades a source
row from CANDIDATE/HOLD to a stronger business status.
"""
from __future__ import annotations

from typing import Any, Iterable

from services.economy_importer import evaluate_sale_policy, load_economy_rows

PACKAGE_OFFERS: dict[str, set[str]] = {
    "INCLUDED_PRO + ELIGIBLE_PATH": {
        "academy-access", "academy-pro", "academy-career", "parcours-metier",
        "b2b-team", "b2b-growth", "b2b-enterprise", "b2g-pilot",
        "b2g-territory", "b2g-large",
    },
    "BUNDLED_BRIDGE": {
        "academy-career", "b2b-team", "b2b-growth", "b2b-enterprise",
        "b2g-pilot", "b2g-territory", "b2g-large",
    },
    "CROSS_CVLN_PROGRAM": {
        "b2b-team", "b2b-growth", "b2b-enterprise", "b2g-pilot",
        "b2g-territory", "b2g-large",
    },
    "INTERNAL_QUALIFICATION": set(),
    "RESTRICTED_INTERNAL": set(),
    "PRIVILEGED_INTERNAL": set(),
    "HOLD_FROM_SALE": set(),
}


def required_gates(row: dict[str, Any]) -> list[str]:
    return [part.strip() for part in str(row.get("activation_gate") or "").split("+") if part.strip()]


def public_discovery_allowed(row: dict[str, Any]) -> bool:
    return row.get("public") == "OUI" and row.get("economic_status") != "DECIDED_HOLD"


def allowed_offer_ids(row: dict[str, Any]) -> set[str]:
    return set(PACKAGE_OFFERS.get(str(row.get("packaging_v1") or ""), set()))


def evaluate_runtime_row(
    row: dict[str, Any],
    *,
    satisfied_gates: Iterable[str] = (),
    offer_id: str | None = None,
) -> dict[str, Any]:
    satisfied = set(satisfied_gates)
    sale = evaluate_sale_policy(row, satisfied)
    reasons: list[str] = []
    if row.get("economic_status") == "DECIDED_HOLD":
        sale = {"allowed": False, "reason": "DECIDED_HOLD", "required_gates": required_gates(row)}
    if not sale.get("allowed"):
        reasons.append(str(sale.get("reason")))
    compatible = allowed_offer_ids(row)
    if offer_id is not None and offer_id not in compatible:
        reasons.append("OFFER_NOT_ALLOWED_FOR_PACKAGE")
    return {
        "code": row["code"],
        "source_row": (row.get("source") or {}).get("row"),
        "public_discovery_allowed": public_discovery_allowed(row),
        "sale_allowed": bool(sale.get("allowed")) and not reasons,
        "sale_reason": sale.get("reason"),
        "required_gates": required_gates(row),
        "satisfied_gates": sorted(satisfied),
        "missing_gates": sale.get("missing_gates", []),
        "packaging_v1": row.get("packaging_v1"),
        "allowed_offer_ids": sorted(compatible),
        "offer_compatible": offer_id is None or offer_id in compatible,
        "public": row.get("public"),
        "channel": row.get("channel"),
        "revenue_recognition": row.get("revenue_recognition"),
        "economic_status": row.get("economic_status"),
        "reasons": reasons,
    }


async def _explicit_gate_state(db: Any, codes: list[str]) -> dict[str, set[str]]:
    if not codes:
        return {}
    docs = await db.academy_economy_gate_state.find(
        {"code": {"$in": codes}, "satisfied": True}, {"_id": 0}
    ).to_list(10000)
    result: dict[str, set[str]] = {code: set() for code in codes}
    for doc in docs:
        if doc.get("evidence_ref"):
            result.setdefault(doc["code"], set()).add(doc["gate"])
    return result


async def runtime_decisions(
    db: Any,
    codes: list[str],
    *,
    canonicalized_codes: set[str] | None = None,
) -> dict[str, dict[str, Any]]:
    rows = await db.academy_economy_master.find(
        {"code": {"$in": codes}}, {"_id": 0}
    ).to_list(max(len(codes), 1))
    gates = await _explicit_gate_state(db, codes)
    canonicalized = canonicalized_codes or set()
    result: dict[str, dict[str, Any]] = {}
    for row in rows:
        satisfied = set(gates.get(row["code"], set()))
        if row["code"] in canonicalized:
            satisfied.add("CANONICALIZED")
        result[row["code"]] = {**row, "runtime": evaluate_runtime_row(row, satisfied_gates=satisfied)}
    return result


async def set_gate_state(
    db: Any,
    *,
    code: str,
    gate: str,
    satisfied: bool,
    evidence_ref: str,
    actor_id: str,
) -> dict[str, Any]:
    row = await db.academy_economy_master.find_one({"code": code}, {"_id": 0})
    if not row:
        raise LookupError(f"economy row not found: {code}")
    if gate not in required_gates(row):
        raise ValueError(f"gate {gate} is not declared by Economy 3D row {code}")
    if satisfied and not evidence_ref.strip():
        raise ValueError("evidence_ref is required to satisfy an economy activation gate")
    doc = {
        "code": code,
        "gate": gate,
        "satisfied": satisfied,
        "evidence_ref": evidence_ref.strip(),
        "actor_id": actor_id,
        "source_hash": row["source_hash"],
    }
    await db.academy_economy_gate_state.update_one(
        {"code": code, "gate": gate}, {"$set": doc}, upsert=True
    )
    await db.academy_economy_gate_state.create_index([("code", 1), ("gate", 1)], unique=True)
    return doc


async def sync_economy_runtime_links(db: Any) -> dict[str, int]:
    """Attach an executable runtime handler/test to every one of the 812 rows."""
    rows = load_economy_rows()
    for row in rows:
        await db.academy_requirement_registry.update_one(
            {"requirement_id": f"ECONOMY_3D:{row['code']}"},
            {"$set": {
                "runtime_handler": "services.economy_runtime.evaluate_runtime_row",
                "runtime_surface": [
                    "api.formations.list_formations",
                    "api.formations.get_formation",
                    "payments.service.create_checkout",
                    "api.master_registry.economy_runtime",
                ],
                "runtime_test_ref": "backend/tests/test_economy_runtime_wiring.py",
            }},
            upsert=False,
        )
    return {"rows_linked": len(rows)}
