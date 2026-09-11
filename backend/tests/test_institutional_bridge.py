from __future__ import annotations

import pytest

from services.institutional_bridge import models as bridge_models
from services.institutional_bridge import registry as bridge_registry


def _case() -> bridge_models.FundingCase:
    return bridge_models.FundingCase(
        org_id="org-1",
        beneficiary_user_id="user-1",
        formation_code="FMS-01",
        territory="martinique",
        funding_scheme="test-scheme",
        amount_requested_eur=1400,
    )


def test_registry_never_claims_live_write_without_adapter():
    descriptors = list(bridge_registry.describe_connectors())
    assert descriptors
    assert all(item.live_write_implemented is False for item in descriptors)


def test_agora_is_explicitly_unavailable():
    agora = bridge_registry.connector_registry["agora"].describe()
    assert agora.connection_mode == "UNAVAILABLE"
    assert agora.capabilities == []
    assert agora.configured is False


def test_portal_and_manual_connectors_are_never_marked_configured():
    for code in ("france_travail", "afdas", "agefma", "ladom", "ctm_fse"):
        assert bridge_registry.connector_registry[code].describe().configured is False


def test_file_and_open_data_connectors_can_be_locally_available():
    assert bridge_registry.connector_registry["edof"].describe().configured is True
    assert (
        bridge_registry.connector_registry["france_competences"].describe().configured
        is True
    )


def test_prepare_case_keeps_canonical_format_and_never_submits():
    envelope = bridge_registry.prepare_case(
        _case(), "france_travail", "APPLICATION_PREPARE"
    )
    assert envelope.format == "CVLN_CANONICAL_V1"
    assert envelope.connector_code == "france_travail"
    assert envelope.payload["formation_code"] == "FMS-01"
    assert envelope.live_submission_performed is False


def test_prepare_rejects_unsupported_capability():
    with pytest.raises(bridge_registry.UnsupportedCapability):
        bridge_registry.prepare_case(_case(), "edof", "APPLICATION_PREPARE")


def test_unknown_connector_fails_closed():
    with pytest.raises(bridge_registry.UnknownConnector):
        bridge_registry.require_capability(
            "invented-financeur", "APPLICATION_PREPARE"
        )


def test_portal_connectors_do_not_advertise_application_submit():
    for code in ("france_travail", "afdas", "agefma", "ladom"):
        connector = bridge_registry.connector_registry[code]
        assert "APPLICATION_SUBMIT" not in connector.capabilities
        assert "INVOICE_SUBMIT" not in connector.capabilities
