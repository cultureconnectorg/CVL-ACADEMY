"""Executable Learning-to-Work economic rules from Economy 3D."""
from __future__ import annotations

from decimal import Decimal, ROUND_HALF_UP

CLIENT_FEE_RATE = Decimal("0.12")
CLIENT_FEE_MIN_EUR = Decimal("150.00")
CANDIDATE_FEE_EUR = Decimal("0.00")


def calculate_mission_fees(gmv_eur: Decimal | float | int | str) -> dict:
    """Apply the decided rule: candidate €0; client 12% GMV, min €150."""
    gmv = Decimal(str(gmv_eur)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    if gmv <= 0:
        raise ValueError("gmv_eur must be greater than zero")
    percentage_fee = (gmv * CLIENT_FEE_RATE).quantize(
        Decimal("0.01"),
        rounding=ROUND_HALF_UP,
    )
    client_fee = max(percentage_fee, CLIENT_FEE_MIN_EUR)
    return {
        "gmv_eur": float(gmv),
        "candidate_fee_eur": float(CANDIDATE_FEE_EUR),
        "client_fee_rate": float(CLIENT_FEE_RATE),
        "client_fee_min_eur": float(CLIENT_FEE_MIN_EUR),
        "client_fee_eur": float(client_fee),
        "rule": "12% GMV; min EUR 150",
        "candidate_rule": "NO_PAY_TO_WORK",
        "source": {
            "sheet": "Learning_to_Work",
            "step": "Mission",
        },
    }
