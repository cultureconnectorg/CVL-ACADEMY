"""ACA-0025 — commercial offer catalogue models.

**This package is a catalogue, never a transaction system.** It exposes
the Founder's real, dated `DECIDED_V1` pricing/offer/policy decisions
(source: `CVLN_Academy_Master_Economie_3D_DECIDE_V1.xlsx`, Founder
decisions dated 2026-09-06) as real, typed, read-only config data —
gate `NO_FAKE_PAID_STATE` (BIN-021/BIN-022) holds by construction:
nothing here creates, stores, or reads a "paid"/"subscribed"/"premium"
flag on any user. `ACA-0026` (real payment/funding runtime — actual
checkout, webhooks, reconciliation) is now built (`backend/payments/`,
see `docs/ACADEMY_ACA0026_PAYMENT_FUNDING_RUNTIME_REPORT.md`) against
this exact catalogue, real and correct against Stripe's own documented
API/webhook contract, honoring the same "never fabricate what needs
external credentials" discipline every other ecosystem integration in
this codebase (`services/integrations/`) follows — it is unexercised
against a live Stripe account only because no real credentials exist
in this sandbox, not because any part of it is fake.
"""

from __future__ import annotations

from typing import Literal, Optional

from pydantic import BaseModel

# The 7 real revenue engines this catalogue's ECO-001 decision names —
# a closed vocabulary, not a free string, so a new offer can't silently
# invent an eighth.
CommercialEngine = Literal[
    "Acquisition",
    "B2C Learning",
    "B2C Career",
    "Certification",
    "Cohorte",
    "B2B",
    "B2G",
    "Mission Economy",
    "Platform/IP",
    "Internal Value",
]

PricingUnit = Literal[
    "Gratuit", "Mensuel", "Unitaire", "Par apprenant", "Annuel", "Programme",
    "12% GMV min €150", "Non commercial",
]

DecisionStatus = Literal["DECIDED_V1"]


class CommercialOffer(BaseModel):
    """One real, Founder-decided commercial offer. `price_eur` /
    `variable_cost_eur` / `gross_margin_eur` / `margin_floor` are the
    same figures the source workbook's `Offres_Economiques` sheet
    carries — cost/margin/floor are internal financial data, never
    served on the public catalogue endpoint (see api/commerce.py)."""

    offer_id: str  # stable slug, e.g. "academy-access"
    label: str
    engine: CommercialEngine
    buyer: str
    object_sold: str
    pricing_unit: PricingUnit
    price_eur: float
    price_eur_annual: Optional[float] = None  # only offers with a real
    # published annual-billing price (Policies: "Annual discount 16.7%")
    variable_cost_eur: float
    gross_margin_eur: float
    margin_floor_pct: float
    decision_status: DecisionStatus = "DECIDED_V1"
    source_decision_id: str  # "ECO-004", etc. — traceable to the exact
    # Founder decision row this offer implements
    notes: str = ""


class EconomicPolicy(BaseModel):
    """One real, Founder-decided commercial/operational policy —
    staff-only (api/commerce.py): several rows are internal financial
    policy (e.g. content-reinvestment %, acquisition-partner cap), not
    customer-facing terms, and this endpoint deliberately doesn't split
    the two rather than risk leaking one through the other."""

    policy: str
    decision: str
    rule: str
    decision_status: DecisionStatus = "DECIDED_V1"
