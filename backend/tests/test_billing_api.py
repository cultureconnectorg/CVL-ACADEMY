from types import SimpleNamespace

import pytest
from mongomock_motor import AsyncMongoMockClient

import api.billing as api_billing
from api.billing import BillingProfileInput


@pytest.fixture
async def billing_db(monkeypatch):
    client = AsyncMongoMockClient()
    mock_db = client["cvln_billing_test"]
    monkeypatch.setattr(api_billing, "db", mock_db)
    return mock_db


@pytest.fixture
def learner():
    return SimpleNamespace(
        id="user-billing-1",
        frek_id="FREK-BILLING-1",
        email="learner@example.invalid",
    )


@pytest.fixture(autouse=True)
def billing_env(monkeypatch):
    monkeypatch.setenv("ACADEMY_BILLING_LEGAL_NAME", "CVLN Academy Test")
    monkeypatch.setenv("ACADEMY_BILLING_COUNTRY", "FR")
    monkeypatch.setenv("ACADEMY_BILLING_REGISTRATION_ID", "999999998")
    monkeypatch.setenv("ACADEMY_BILLING_REGISTRATION_SCHEME", "0002")
    monkeypatch.setenv("ACADEMY_BILLING_ADDRESS_LINE1", "1 rue Test")
    monkeypatch.setenv("ACADEMY_BILLING_CITY", "Paris")
    monkeypatch.setenv("ACADEMY_BILLING_POSTAL_CODE", "75001")
    monkeypatch.setenv("ACADEMY_BILLING_INVOICE_SERIES", "ACA")
    monkeypatch.setenv("ACADEMY_BILLING_EINVOICE_PROFILE", "FACTUR-X_EN16931")
    monkeypatch.setenv("ACADEMY_BILLING_TAX_MODE", "STANDARD")
    monkeypatch.setenv("ACADEMY_BILLING_TAX_RATE_PERCENT", "20")
    monkeypatch.setenv("ACADEMY_BILLING_TAX_CATEGORY", "S")


def paid_order(user_id="user-billing-1"):
    return {
        "order_id": "ord_billing_api_1",
        "user_id": user_id,
        "user_frek_id": "FREK-BILLING-1",
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
        "payment_attempt_id": "pay_billing_api_1",
        "wallet_entity_id": "ent_cvln_academy",
        "wallet_response": {"transaction_id": "wallet_tx_api_1", "ok": True},
        "paid_at": "2026-09-11T13:00:00Z",
    }


async def test_profile_intent_issue_and_replay_keep_one_number(
    billing_db, learner
):
    await billing_db.commercial_orders.insert_one(paid_order())
    await api_billing.upsert_billing_profile(
        BillingProfileInput(
            legal_name="Learner Test",
            address_line1="2 rue Client",
            city="Lyon",
            postal_code="69001",
            country="FR",
        ),
        learner,
    )

    first_intent = await api_billing.ensure_invoice_intent(
        "ord_billing_api_1", learner
    )
    second_intent = await api_billing.ensure_invoice_intent(
        "ord_billing_api_1", learner
    )
    assert first_intent["billing_document_id"] == second_intent["billing_document_id"]
    assert await billing_db.billing_documents.count_documents({}) == 1

    issued = await api_billing.issue_order_invoice("ord_billing_api_1", learner)
    replay = await api_billing.issue_order_invoice("ord_billing_api_1", learner)

    assert issued["status"] == "ISSUED"
    assert issued["legal_invoice_number"].startswith("ACA-")
    assert replay["legal_invoice_number"] == issued["legal_invoice_number"]
    assert replay["artifact"]["xsd_validation"] == "PASS"
    assert await billing_db.billing_documents.count_documents({}) == 1
    sequence = await billing_db.billing_sequences.find_one({})
    assert sequence["value"] == 1


async def test_invoice_metadata_endpoint_does_not_expose_base64_artifact(
    billing_db, learner
):
    await billing_db.commercial_orders.insert_one(paid_order())
    await api_billing.upsert_billing_profile(
        BillingProfileInput(
            legal_name="Learner Test",
            address_line1="2 rue Client",
            city="Lyon",
            postal_code="69001",
            country="FR",
        ),
        learner,
    )
    await api_billing.ensure_invoice_intent("ord_billing_api_1", learner)
    await api_billing.issue_order_invoice("ord_billing_api_1", learner)
    metadata = await api_billing.get_order_invoice("ord_billing_api_1", learner)
    assert metadata["artifact"]["pdf_sha256"]
    assert "pdf_b64" not in metadata["artifact"]
    assert "xml_b64" not in metadata["artifact"]
