"""ACA-0025 — commercial offer catalogue API.

`GET /commerce/offers` is deliberately public (no auth) — pricing is
customer-facing content, same PUBLIC_DISCOVERY=TRUE logic already
applied to `/formations`/`/poles`, and returns ONLY customer-facing
fields (never cost/margin/floor). Staff can additionally read the full
internal figures (`/commerce/offers/internal`) and the policy registry
(`/commerce/policies`, a mix of customer and internal-financial rules
— kept staff-only rather than risk leaking one through the other).

See commerce/models.py's module docstring: nothing here creates or
reads a paid/subscribed state on any user (`NO_FAKE_PAID_STATE`) —
this is a read-only catalogue, never a transaction record.
"""

from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from auth import require_role
from commerce import OFFERS, POLICIES, CommercialOffer, EconomicPolicy
from models import STAFF_ROLES, User

router = APIRouter(prefix="/commerce", tags=["commerce"])


class PublicOffer(BaseModel):
    """Customer-facing view of a `CommercialOffer` — no cost, margin,
    floor, or internal source-decision id."""

    offer_id: str
    label: str
    engine: str
    buyer: str
    object_sold: str
    pricing_unit: str
    price_eur: float
    price_eur_annual: float | None = None
    notes: str


def _to_public(offer: CommercialOffer) -> PublicOffer:
    return PublicOffer(
        offer_id=offer.offer_id,
        label=offer.label,
        engine=offer.engine,
        buyer=offer.buyer,
        object_sold=offer.object_sold,
        pricing_unit=offer.pricing_unit,
        price_eur=offer.price_eur,
        price_eur_annual=offer.price_eur_annual,
        notes=offer.notes,
    )


@router.get("/offers", response_model=List[PublicOffer])
async def list_public_offers():
    return [_to_public(o) for o in OFFERS]


@router.get("/offers/internal", response_model=List[CommercialOffer])
async def list_internal_offers(current: User = Depends(require_role(*STAFF_ROLES))):
    return OFFERS


@router.get("/policies", response_model=List[EconomicPolicy])
async def list_policies(current: User = Depends(require_role(*STAFF_ROLES))):
    return POLICIES
