from services.catalogue_importer import EXPECTED_MASTER_ROWS as CATALOGUE_EXPECTED
from services.catalogue_importer import load_catalogue_rows
from services.economy_importer import EXPECTED_MASTER_ROWS as ECONOMY_EXPECTED
from services.economy_importer import evaluate_sale_policy, load_economy_rows


def test_catalogue_master_has_exact_812_unique_rows():
    rows = load_catalogue_rows()
    assert CATALOGUE_EXPECTED == 812
    assert len(rows) == 812
    assert len({row["code"] for row in rows}) == 812
    assert all(row["source_hash"] for row in rows)
    assert all(row["source"]["row"] >= 2 for row in rows)


def test_economy_master_has_exact_812_unique_rows():
    rows = load_economy_rows()
    assert ECONOMY_EXPECTED == 812
    assert len(rows) == 812
    assert len({row["code"] for row in rows}) == 812
    assert all(row["economic_status"] for row in rows)
    assert all(row["source_hash"] for row in rows)


def test_catalogue_and_economy_are_one_to_one_by_code():
    catalogue_codes = {row["code"] for row in load_catalogue_rows()}
    economy_codes = {row["code"] for row in load_economy_rows()}
    assert catalogue_codes == economy_codes


def test_not_for_sale_policy_is_hard_denied():
    row = next(row for row in load_economy_rows() if row["public_price_v1"] == "NOT_FOR_SALE")
    decision = evaluate_sale_policy(row, {"PRODUCT_VERIFIED", "ROLE_DEFINED"})
    assert decision["allowed"] is False
    assert decision["reason"] == "NOT_FOR_SALE"


def test_activation_gate_requires_every_declared_gate():
    record = {
        "sale_policy": "GATED",
        "activation_gate": "CANONICALIZED + HANDOFF_VERIFIED",
    }
    denied = evaluate_sale_policy(record, {"CANONICALIZED"})
    assert denied["allowed"] is False
    assert denied["missing_gates"] == ["HANDOFF_VERIFIED"]

    allowed = evaluate_sale_policy(record, {"CANONICALIZED", "HANDOFF_VERIFIED"})
    assert allowed["allowed"] is True
