import copy

import pytest

from billing import (
    BillingNotReady,
    OrderNotPaid,
    assert_legal_issuance_ready,
    billing_idempotency_key,
    build_invoice_intent,
)


def paid_order():
    return {
        "order_id": "ord_test_001",
        "user_id": "usr_1",
        "user_frek_id": "FREK-TEST",
        "economy_code": "FMS-01",
        "economy_requirement_id": "ACA-ECO-0001",
        "amount_eur": 990.0,
        "currency": "EUR",
        "pricing_snapshot": {
            "economy_code": "FMS-01",
            "amount_eur": 990.0,
            "currency": "EUR",
            "source_sheet": "Mapping_812",
        },
        "status": "PAID",
        "payment_attempt_id": "pay_test_001",
        "wallet_entity_id": "entity_academy",
        "wallet_response": {"transaction_id": "wallet_tx_1"},
        "paid_at": "2026-09-11T13:00:00Z",
    }


def test_invoice_intent_requires_paid_order():
    order = paid_order()
    order["status"] = "PENDING_PAYMENT"
    with pytest.raises(OrderNotPaid):
        build_invoice_intent(order)


def test_invoice_intent_is_deterministic_per_order():
    first = build_invoice_intent(paid_order())
    second = build_invoice_intent(copy.deepcopy(paid_order()))
    assert first["billing_document_id"] == second["billing_document_id"]
    assert first["idempotency_key"] == second["idempotency_key"]
    assert first["legal_invoice_number"] is None
    assert first["status"] == "INVOICE_INTENT"


def test_idempotency_key_changes_for_different_document_type():
    assert billing_idempotency_key("ord_1", "INVOICE") != billing_idempotency_key(
        "ord_1", "CREDIT_NOTE"
    )


def test_invoice_intent_preserves_economy_and_wallet_evidence():
    document = build_invoice_intent(paid_order())
    assert document["economy_requirement_id"] == "ACA-ECO-0001"
    assert document["pricing_snapshot"]["amount_eur"] == 990.0
    assert document["payment_attempt_id"] == "pay_test_001"
    assert document["wallet_response"]["transaction_id"] == "wallet_tx_1"


def test_legal_issuance_fails_closed_without_tax_adapter(monkeypatch):
    monkeypatch.setenv("ACADEMY_BILLING_LEGAL_NAME", "CVLN Academy Test")
    monkeypatch.setenv("ACADEMY_BILLING_COUNTRY", "FR")
    monkeypatch.setenv("ACADEMY_BILLING_REGISTRATION_ID", "TEST-REG")
    monkeypatch.setenv("ACADEMY_BILLING_INVOICE_SERIES", "ACA")
    document = build_invoice_intent(paid_order())
    with pytest.raises(BillingNotReady, match="Tax/e-invoicing"):
        assert_legal_issuance_ready(document)
