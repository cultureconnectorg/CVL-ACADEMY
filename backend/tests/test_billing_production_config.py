import pytest

from billing_config import assert_billing_production_ready, billing_production_status

ISSUER_ENV = {
    "ACADEMY_BILLING_LEGAL_NAME": "CVLN Academy Test Entity",
    "ACADEMY_BILLING_COUNTRY": "FR",
    "ACADEMY_BILLING_REGISTRATION_ID": "999999998",
    "ACADEMY_BILLING_REGISTRATION_SCHEME": "0002",
    "ACADEMY_BILLING_ADDRESS_LINE1": "1 rue Test",
    "ACADEMY_BILLING_CITY": "Paris",
    "ACADEMY_BILLING_POSTAL_CODE": "75001",
    "ACADEMY_BILLING_INVOICE_SERIES": "ACA",
    "ACADEMY_BILLING_EINVOICE_PROFILE": "FACTUR-X_EN16931",
}

TAX_ENV = {
    "ACADEMY_BILLING_TAX_MODE": "STANDARD",
    "ACADEMY_BILLING_TAX_RATE_PERCENT": "20",
    "ACADEMY_BILLING_TAX_CATEGORY": "S",
}


def clear_billing_env(monkeypatch):
    for name in (*ISSUER_ENV.keys(), *TAX_ENV.keys()):
        monkeypatch.delenv(name, raising=False)


def test_development_reports_missing_config_without_blocking(monkeypatch):
    clear_billing_env(monkeypatch)
    monkeypatch.setenv("ACADEMY_ENV", "development")

    status = assert_billing_production_ready()

    assert status["required"] is False
    assert status["ready"] is False
    assert "ACADEMY_BILLING_LEGAL_NAME" in status["missing_env"]


def test_production_fails_closed_with_exact_missing_env(monkeypatch):
    clear_billing_env(monkeypatch)
    monkeypatch.setenv("ACADEMY_ENV", "production")

    with pytest.raises(RuntimeError, match="BILLING_PRODUCTION_NOT_READY") as exc:
        assert_billing_production_ready()

    message = str(exc.value)
    assert "ACADEMY_BILLING_LEGAL_NAME" in message
    assert "ACADEMY_BILLING_REGISTRATION_ID" in message
    assert "ACADEMY_BILLING_TAX_MODE" in message


def test_production_accepts_explicit_complete_config(monkeypatch):
    clear_billing_env(monkeypatch)
    monkeypatch.setenv("ACADEMY_ENV", "production")
    for name, value in {**ISSUER_ENV, **TAX_ENV}.items():
        monkeypatch.setenv(name, value)

    status = assert_billing_production_ready()

    assert status["required"] is True
    assert status["ready"] is True
    assert status["missing_env"] == []
    assert status["tax_ready"] is True
    assert status["einvoice_profile_ready"] is True


def test_production_rejects_invalid_tax_policy(monkeypatch):
    clear_billing_env(monkeypatch)
    monkeypatch.setenv("ACADEMY_ENV", "production")
    for name, value in {**ISSUER_ENV, **TAX_ENV}.items():
        monkeypatch.setenv(name, value)
    monkeypatch.setenv("ACADEMY_BILLING_TAX_RATE_PERCENT", "0")

    status = billing_production_status()
    assert status["ready"] is False
    assert status["tax_ready"] is False
    assert "positive tax rate" in status["tax_error"]

    with pytest.raises(RuntimeError, match="BILLING_PRODUCTION_NOT_READY"):
        assert_billing_production_ready()
