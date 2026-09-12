"""Commercial runtime policy tests: Economy 3D -> concrete Wallet charge inputs."""

from __future__ import annotations

import pytest
from commercial import (
    EligibilityRequired,
    NotForSale,
    QuoteRequired,
    amount_eur_to_jcc,
    resolve_offer,
)


def test_public_market_path_is_server_priced_from_economy_3d():
    offer = resolve_offer("FMS-07", "path")
    assert offer["economy_code"] == "FMS-07"
    assert offer["requirement_id"] == "ACA-ECO-0013"
    assert offer["commercial_class"] == "PUBLIC_MARKET"
    assert offer["amount_eur"] == 990.0
    assert offer["currency"] == "EUR"
    assert offer["price_label"] == "€990 path / subscription"
    assert offer["source_sheet"] == "Mapping_812"


def test_wallet_amount_uses_wallet_runtime_rate_not_client_price():
    assert amount_eur_to_jcc(990.0, 1.5) == 660.0


def test_subscription_is_fail_closed_until_plan_mapping_is_canonical():
    with pytest.raises(QuoteRequired):
        resolve_offer("FMS-07", "subscription")


def test_internal_row_can_never_be_sold():
    with pytest.raises(NotForSale):
        resolve_offer("KLT-09", "path")


def test_cross_ecosystem_requires_quote_instead_of_direct_wallet_charge():
    with pytest.raises(QuoteRequired):
        resolve_offer("FMS-18", "path")


def test_bridge_requires_eligibility_instead_of_fake_zero_euro_purchase():
    with pytest.raises(EligibilityRequired):
        resolve_offer("SAY-LAB", "path")


def test_hold_row_can_never_be_sold():
    with pytest.raises(NotForSale):
        resolve_offer("HOS-GAP", "path")


@pytest.mark.parametrize(
    "amount_eur,rate",
    [(0, 1.5), (-1, 1.5), (990, 0), (990, -1)],
)
def test_invalid_conversion_inputs_fail_closed(amount_eur, rate):
    with pytest.raises(ValueError):
        amount_eur_to_jcc(amount_eur, rate)
