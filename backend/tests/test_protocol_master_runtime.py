from copy import deepcopy
import importlib.util
from pathlib import Path

import pytest

from services.protocol_master_runtime import (
    EXPECTED_DOMAINS,
    EXPECTED_ROWS,
    EXPECTED_SHEET_ROWS,
    EXPECTED_WORKBOOK_ROWS,
    INTEGRATION_ADAPTERS,
    ROOT,
    evaluate_protocol_control,
    load_protocol_controls,
    load_protocol_workbook_rows,
)

CONTROLS = load_protocol_controls()
CONTROL_IDS = [control["control_id"] for control in CONTROLS]


def _valid_context(control):
    domain = control["domain"]
    context = {
        "actor_id": "test-actor",
        "evidence_ref": f"evidence:{control['control_id']}",
        "control_id": control["control_id"],
        "behavior_fingerprint": control["behavior_fingerprint"],
        "control_version_ref": f"version:{control['control_id']}:1",
        "integration_refs": {
            name: f"integration:{control['control_id']}:{index}"
            for index, name in enumerate(control["integrates_with"], start=1)
        },
        "frek_proof_ref": f"frek:{control['control_id']}",
        "production_gate_evidence_ref": f"gate:{control['control_id']}",
        "expert_review_ref": f"expert:{control['control_id']}",
        "systemic": False,
    }
    domain_context = {
        "GOVERNANCE": {"authority_context": "delegated"},
        "LEGAL": {"jurisdiction": "FR", "expert_review_state": "REVIEWED"},
        "PRIVACY": {
            "data_classification": "PERSONAL",
            "lawful_basis": "CONSENT",
        },
        "SECURITY": {"severity": "LOW"},
        "ACCOUNTING": {
            "entity_context": "ACADEMY",
            "accounting_state": "PREPARED",
        },
        "RISK": {"risk_level": "R2", "owner": "risk-owner"},
        "QUALITY": {"quality_scope": "academy"},
        "TRUST": {"proof_ref": "proof:1", "proof_verified": True},
        "DATA": {
            "provenance_ref": "provenance:1",
            "data_classification": "INTERNAL",
        },
        "REGULATORY": {
            "jurisdiction": "FR",
            "applicability_state": "REVIEWED",
            "expert_review_state": "REVIEWED",
        },
    }
    context.update(domain_context[domain])
    if control["cvln_ios"] == "YES":
        context["cvln_ios_ref"] = f"ios:{control['control_id']}"
    if control["control_id"] == "GOV-02":
        context["policy_version_id"] = "POLV-test"
    if control["control_id"] == "REG-04":
        context["legal_assurance_level"] = "REVIEWED_BY_LAWYER"
    return context


def test_entire_protocol_workbook_is_projected_line_by_line():
    rows = load_protocol_workbook_rows()
    assert len(rows) == EXPECTED_WORKBOOK_ROWS == 328
    assert len({row["row_id"] for row in rows}) == 328
    counts = {sheet: 0 for sheet in EXPECTED_SHEET_ROWS}
    for row in rows:
        counts[row["sheet"]] += 1
    assert counts == EXPECTED_SHEET_ROWS


def test_protocol_master_is_exactly_227_exact_excel_contracts():
    assert len(CONTROLS) == EXPECTED_ROWS == 227
    assert [control["excel_row"] for control in CONTROLS] == list(range(3, 230))
    assert len(set(CONTROL_IDS)) == 227
    assert len({control["row_hash"] for control in CONTROLS}) == 227
    assert len({control["behavior_fingerprint"] for control in CONTROLS}) == 227
    counts = {domain: 0 for domain in EXPECTED_DOMAINS}
    for control in CONTROLS:
        counts[control["domain"]] += 1
    assert counts == EXPECTED_DOMAINS


def test_every_excel_semantic_field_is_present_on_every_control():
    required = {
        "title",
        "type",
        "repo_status",
        "what_must_be_built",
        "verification_basis",
        "build_target",
        "integrates_with",
        "priority",
        "frek",
        "cvln_ios",
        "external_expert",
        "production_gate",
        "build_wave",
        "row_hash",
    }
    for control in CONTROLS:
        assert required <= control.keys(), control["control_id"]
        assert control["integrates_with"], control["control_id"]


def test_every_declared_integration_has_a_runtime_adapter():
    declared = {
        integration
        for control in CONTROLS
        for integration in control["integrates_with"]
    }
    assert declared <= INTEGRATION_ADAPTERS.keys()
    assert all(INTEGRATION_ADAPTERS[name] for name in declared)


def test_every_runtime_adapter_resolves_to_real_repo_boundary():
    for adapter in set(INTEGRATION_ADAPTERS.values()):
        if adapter.startswith(".github/"):
            assert (Path(ROOT) / adapter).is_file(), adapter
            continue
        assert importlib.util.find_spec(adapter) is not None, adapter


@pytest.mark.parametrize("control", CONTROLS, ids=CONTROL_IDS)
def test_each_of_227_behaviors_accepts_only_its_complete_contract(control):
    decision = evaluate_protocol_control(control, _valid_context(control))
    assert decision["allowed"] is True, decision
    assert decision["behavior_fingerprint"] == control["behavior_fingerprint"]
    assert decision["row_hash"] == control["row_hash"]


@pytest.mark.parametrize("control", CONTROLS, ids=CONTROL_IDS)
def test_each_of_227_behaviors_fails_if_one_declared_integration_is_unproven(
    control,
):
    context = _valid_context(control)
    missing_integration = control["integrates_with"][0]
    del context["integration_refs"][missing_integration]
    decision = evaluate_protocol_control(control, context)
    assert decision["allowed"] is False
    assert f"INTEGRATION_NOT_PROVEN:{missing_integration}" in decision["reasons"]


@pytest.mark.parametrize("index", range(EXPECTED_ROWS), ids=CONTROL_IDS)
def test_each_behavior_rejects_another_rows_fingerprint(index):
    control = CONTROLS[index]
    other = CONTROLS[(index + 1) % EXPECTED_ROWS]
    context = _valid_context(control)
    context["behavior_fingerprint"] = other["behavior_fingerprint"]
    decision = evaluate_protocol_control(control, context)
    assert decision["allowed"] is False
    assert "BEHAVIOR_FINGERPRINT_MISMATCH" in decision["reasons"]


def test_gov_02_is_the_authority_policy_engine_protocol():
    control = next(row for row in CONTROLS if row["control_id"] == "GOV-02")
    assert control["title"] == "Authority Policy Engine Protocol"
    assert "Auth/RBAC" in control["integrates_with"]
    assert "Event Bus" in control["integrates_with"]
    assert "FREK" in control["integrates_with"]
    assert "CVLN iOS" in control["integrates_with"]
    context = _valid_context(control)
    del context["policy_version_id"]
    decision = evaluate_protocol_control(control, context)
    assert decision["allowed"] is False
    assert "MISSING:policy_version_id" in decision["reasons"]


def test_acc_11_cannot_self_validate_tax():
    control = next(row for row in CONTROLS if row["control_id"] == "ACC-11")
    assert control["title"] == "TAX_PREPARED != TAX_VALIDATED"
    context = _valid_context(control)
    context["accounting_state"] = "TAX_VALIDATED"
    decision = evaluate_protocol_control(control, context)
    assert decision["allowed"] is False
    assert "MISSING:expert_validation_ref" in decision["reasons"]


def test_reg_04_requires_explicit_legal_assurance_level():
    control = next(row for row in CONTROLS if row["control_id"] == "REG-04")
    assert control["title"] == "Electronic Signature / Trust Applicability"
    context = _valid_context(control)
    del context["legal_assurance_level"]
    decision = evaluate_protocol_control(control, context)
    assert decision["allowed"] is False
    assert "MISSING:legal_assurance_level" in decision["reasons"]


def test_context_mode_cvln_ios_escalates_only_when_systemic():
    control = next(row for row in CONTROLS if row["cvln_ios"] == "CONTEXT")
    context = _valid_context(control)
    assert evaluate_protocol_control(control, context)["allowed"] is True
    context["systemic"] = True
    decision = evaluate_protocol_control(control, context)
    assert decision["allowed"] is False
    assert "MISSING:cvln_ios_ref" in decision["reasons"]


def test_control_contract_isolation_does_not_mutate_source():
    control = CONTROLS[0]
    context = _valid_context(control)
    snapshot = deepcopy(control)
    evaluate_protocol_control(control, context)
    assert control == snapshot
