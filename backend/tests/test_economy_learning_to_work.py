from __future__ import annotations

import pytest

from services.economy_learning_to_work import calculate_mission_fees


def test_candidate_never_pays_and_client_fee_has_150_eur_floor():
    result = calculate_mission_fees(500)
    assert result["candidate_fee_eur"] == 0.0
    assert result["client_fee_eur"] == 150.0
    assert result["candidate_rule"] == "NO_PAY_TO_WORK"


def test_client_fee_is_12_percent_above_floor_threshold():
    result = calculate_mission_fees(2000)
    assert result["candidate_fee_eur"] == 0.0
    assert result["client_fee_rate"] == 0.12
    assert result["client_fee_eur"] == 240.0


@pytest.mark.parametrize("gmv", [0, -1, -100.0])
def test_mission_fee_refuses_missing_or_non_positive_gmv(gmv):
    with pytest.raises(ValueError):
        calculate_mission_fees(gmv)
