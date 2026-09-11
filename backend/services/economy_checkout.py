"""Economy workbook guard placed before the payment provider checkout."""
from __future__ import annotations

from commerce.catalog import get_offer
from payments.service import (
    EconomyPolicyBlockedError,
    create_checkout as create_payment_checkout,
)
from services.economy_workbook_runtime import (
    evaluate_offer_phase,
    evaluate_offer_unit_economics,
)


async def create_economy_guarded_checkout(
    *,
    db,
    user_id: str,
    offer_id: str,
    success_url: str,
    cancel_url: str,
    economy_code: str | None = None,
    formation_code: str | None = None,
):
    offer = get_offer(offer_id)
    if offer is not None:
        unit_decision = evaluate_offer_unit_economics(offer)
        if not unit_decision["allowed"]:
            raise EconomyPolicyBlockedError(
                f"Unit_Economics bloque {offer_id}: {unit_decision}"
            )

        phase_decision = await evaluate_offer_phase(db, offer_id)
        if not phase_decision["allowed"]:
            raise EconomyPolicyBlockedError(
                f"Roadmap_Monetisation bloque {offer_id}: "
                f"{phase_decision['reason']} ({phase_decision['phase']})"
            )

    return await create_payment_checkout(
        user_id=user_id,
        offer_id=offer_id,
        economy_code=economy_code,
        formation_code=formation_code,
        success_url=success_url,
        cancel_url=cancel_url,
    )
