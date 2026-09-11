from collections import Counter

from services.protocol_master_runtime import (
    EXPECTED_DOMAINS, EXPECTED_ROWS, EXPECTED_SHEET_ROWS, EXPECTED_WORKBOOK_ROWS,
    evaluate_protocol_control, load_protocol_controls, load_protocol_workbook_rows,
)


def _valid_context(domain):
    base = {"actor_id": "test-actor", "evidence_ref": "evidence:test"}
    extra = {
        "GOVERNANCE": {"authority_context": "delegated"},
        "LEGAL": {"jurisdiction": "FR", "expert_review_state": "REVIEWED"},
        "PRIVACY": {"data_classification": "PERSONAL", "lawful_basis": "CONSENT"},
        "SECURITY": {"severity": "LOW"},
        "ACCOUNTING": {"entity_context": "ACADEMY", "accounting_state": "PREPARED"},
        "RISK": {"risk_level": "R2", "owner": "risk-owner"},
        "QUALITY": {"quality_scope": "academy"},
        "TRUST": {"proof_ref": "proof:1", "proof_verified": True},
        "DATA": {"provenance_ref": "prov:1", "data_classification": "INTERNAL"},
        "REGULATORY": {"jurisdiction": "FR", "applicability_state": "REVIEWED", "expert_review_state": "REVIEWED"},
    }
    return {**base, **extra[domain]}


def test_entire_protocol_workbook_is_projected_line_by_line():
    rows = load_protocol_workbook_rows()
    assert len(rows) == EXPECTED_WORKBOOK_ROWS == 328
    assert len({row["row_id"] for row in rows}) == 328
    assert Counter(row["sheet"] for row in rows) == Counter(EXPECTED_SHEET_ROWS)
    assert all(len(row["source"]["workbook_sha256"]) == 64 for row in rows)
    assert {row["excel_row"] for row in rows if row["sheet"] == "Dashboard"} == {1, *range(3, 26)}


def test_protocol_master_is_exactly_227_controls_rows_3_through_229():
    controls = load_protocol_controls()
    assert len(controls) == EXPECTED_ROWS == 227
    assert [c["excel_row"] for c in controls] == list(range(3, 230))
    assert len({c["control_id"] for c in controls}) == 227
    assert Counter(c["domain"] for c in controls) == Counter(EXPECTED_DOMAINS)


def test_every_control_line_has_runtime_handler_and_source_identity():
    for control in load_protocol_controls():
        assert control["runtime_handler"].startswith("protocol:")
        assert control["required_context"]
        assert control["source"]["sheet"] == "Protocol Master"
        assert control["source"]["excel_row"] == control["excel_row"]


def test_all_227_controls_fail_closed_without_required_context():
    for control in load_protocol_controls():
        decision = evaluate_protocol_control(control, {})
        assert decision["allowed"] is False, control["control_id"]
        assert decision["reasons"], control["control_id"]


def test_all_227_controls_are_executable_with_domain_contract():
    for control in load_protocol_controls():
        decision = evaluate_protocol_control(control, _valid_context(control["domain"]))
        assert decision["control_id"] == control["control_id"]
        assert decision["excel_row"] == control["excel_row"]
        assert decision["handler"] == control["runtime_handler"]
        assert decision["allowed"] is True, (control["control_id"], decision["reasons"])


def test_high_security_requires_incident_reference():
    control = next(c for c in load_protocol_controls() if c["control_id"] == "SEC-01")
    context = _valid_context("SECURITY"); context["severity"] = "CRITICAL"
    decision = evaluate_protocol_control(control, context)
    assert decision["allowed"] is False
    assert "INCIDENT_REFERENCE_REQUIRED" in decision["reasons"]


def test_critical_risk_requires_mitigation_and_deadline():
    control = next(c for c in load_protocol_controls() if c["control_id"] == "RSK-01")
    context = _valid_context("RISK"); context["risk_level"] = "R5"
    decision = evaluate_protocol_control(control, context)
    assert decision["allowed"] is False
    assert "CRITICAL_RISK_MISSING:mitigation" in decision["reasons"]
    assert "CRITICAL_RISK_MISSING:deadline" in decision["reasons"]


def test_accounting_cannot_self_validate_tax():
    control = next(c for c in load_protocol_controls() if c["control_id"] == "ACC-01")
    context = _valid_context("ACCOUNTING"); context["accounting_state"] = "TAX_VALIDATED"
    decision = evaluate_protocol_control(control, context)
    assert decision["allowed"] is False
    assert "TAX_PREPARED_NOT_VALIDATED_BY_EXPERT" in decision["reasons"]


def test_data_mutation_requires_explicit_evidence():
    control = next(c for c in load_protocol_controls() if c["control_id"] == "DAT-01")
    context = _valid_context("DATA"); context["mutation"] = True
    decision = evaluate_protocol_control(control, context)
    assert decision["allowed"] is False
    assert "SILENT_DATA_MUTATION_BLOCKED" in decision["reasons"]
