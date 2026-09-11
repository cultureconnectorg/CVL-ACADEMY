import os

from backend.services.integrations.cvln_wallet import CVLNWalletIntegration


def test_cvln_wallet_requires_url_and_api_key(monkeypatch):
    monkeypatch.delenv("CVLN_WALLET_URL", raising=False)
    monkeypatch.delenv("CVLN_WALLET_API_KEY", raising=False)
    integration = CVLNWalletIntegration()
    assert integration.is_remote_enabled() is False


def test_cvln_wallet_describes_group_financial_role(monkeypatch):
    monkeypatch.setenv("CVLN_WALLET_URL", "https://wallet.example.test")
    monkeypatch.setenv("CVLN_WALLET_API_KEY", "test-key")
    integration = CVLNWalletIntegration()
    desc = integration.describe()
    assert desc["configured"] is True
    assert desc["role"] == "group_financial_core"
    assert "CVLN_WALLET_API_KEY" in desc["env_vars"]
