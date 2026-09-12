import copy
from datetime import datetime, timezone

import pytest
from billing import (
    BillingNotReady,
    OrderNotPaid,
    assert_legal_issuance_ready,
    billing_idempotency_key,
    build_invoice_intent,
)
from billing_einvoice import (
    build_en16931_data,
    generate_invoice_artifacts,
    invoice_breakdown,
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


def configure_issuer(monkeypatch):
    monkeypatch.setenv("ACADEMY_BILLING_LEGAL_NAME", "CVLN Academy Test")
    monkeypatch.setenv("ACADEMY_BILLING_COUNTRY", "FR")
    monkeypatch.setenv("ACADEMY_BILLING_REGISTRATION_ID", "999999998")
    monkeypatch.setenv("ACADEMY_BILLING_REGISTRATION_SCHEME", "0002")
    monkeypatch.setenv("ACADEMY_BILLING_ADDRESS_LINE1", "1 rue Test")
    monkeypatch.setenv("ACADEMY_BILLING_CITY", "Paris")
    monkeypatch.setenv("ACADEMY_BILLING_POSTAL_CODE", "75001")
    monkeypatch.setenv("ACADEMY_BILLING_INVOICE_SERIES", "ACA")
    monkeypatch.setenv("ACADEMY_BILLING_EINVOICE_PROFILE", "FACTUR-X_EN16931")


def configure_standard_tax(monkeypatch):
    monkeypatch.setenv("ACADEMY_BILLING_TAX_MODE", "STANDARD")
    monkeypatch.setenv("ACADEMY_BILLING_TAX_RATE_PERCENT", "20")
    monkeypatch.setenv("ACADEMY_BILLING_TAX_CATEGORY", "S")


def buyer_profile():
    return {
        "user_id": "usr_1",
        "frek_id": "FREK-TEST",
        "email": "buyer@example.invalid",
        "legal_name": "Buyer Test",
        "address_line1": "2 rue Client",
        "city": "Lyon",
        "postal_code": "69001",
        "country": "FR",
        "vat_id": None,
        "registration_id": None,
        "registration_scheme": "0002",
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


def test_legal_issuance_fails_closed_without_full_issuer(monkeypatch):
    monkeypatch.setenv("ACADEMY_BILLING_LEGAL_NAME", "CVLN Academy Test")
    monkeypatch.setenv("ACADEMY_BILLING_COUNTRY", "FR")
    monkeypatch.setenv("ACADEMY_BILLING_REGISTRATION_ID", "TEST-REG")
    monkeypatch.setenv("ACADEMY_BILLING_INVOICE_SERIES", "ACA")
    document = build_invoice_intent(paid_order())
    with pytest.raises(BillingNotReady, match="issuer profile"):
        assert_legal_issuance_ready(document)


def test_standard_tax_breakdown_is_exact(monkeypatch):
    configure_standard_tax(monkeypatch)
    breakdown = invoice_breakdown(990)
    assert str(breakdown["gross"]) == "990.00"
    assert str(breakdown["net"]) == "825.00"
    assert str(breakdown["tax"]) == "165.00"


def test_en16931_data_never_reprices_order(monkeypatch):
    configure_issuer(monkeypatch)
    configure_standard_tax(monkeypatch)
    document = build_invoice_intent(paid_order())
    document["legal_invoice_number"] = "ACA-2026-000001"
    data = build_en16931_data(
        document, buyer_profile(), datetime(2026, 9, 11, tzinfo=timezone.utc)
    )
    assert data["BT-1"] == "ACA-2026-000001"
    assert data["BT-112"] == "990.00"
    assert data["BT-109"] == "825.00"
    assert data["BT-110"] == "165.00"
    assert data["BG-25"][0]["BT-131"] == "825.00"


def test_facturx_en16931_pdf_and_xml_are_generated(monkeypatch):
    configure_issuer(monkeypatch)
    configure_standard_tax(monkeypatch)
    document = build_invoice_intent(paid_order())
    document["legal_invoice_number"] = "ACA-2026-000001"
    artifact = generate_invoice_artifacts(
        document,
        buyer_profile(),
        datetime(2026, 9, 11, 13, 0, tzinfo=timezone.utc),
    )
    assert artifact["format"] == "FACTUR-X_EN16931"
    assert artifact["xsd_validation"] == "PASS"
    assert artifact["xml_size"] > 500
    assert artifact["pdf_size"] > 1000
    assert len(artifact["xml_sha256"]) == 64
    assert len(artifact["pdf_sha256"]) == 64
