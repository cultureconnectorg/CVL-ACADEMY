"""Commercial policy derived from the canonical Economy 3D projection.

No client-supplied price is accepted. A concrete charge is produced only when
Economy 3D expresses an exact sellable amount that Academy can interpret
without inventing a financing or subscription rule.
"""

from __future__ import annotations

import re
from typing import Any, Dict

from economy_3d import commercial_class, record_by_code


class CommercialPolicyError(ValueError):
    pass


class QuoteRequired(CommercialPolicyError):
    pass


class NotForSale(CommercialPolicyError):
    pass


class EligibilityRequired(CommercialPolicyError):
    pass


def resolve_offer(economy_code: str, offer_kind: str = "path") -> Dict[str, Any]:
    record = record_by_code(economy_code)
    classification = commercial_class(record)

    if classification == "INTERNAL_NOT_FOR_SALE" or classification == "HOLD_FROM_SALE":
        raise NotForSale(f"{economy_code} is not commercially sellable")
    if classification == "CROSS_ECOSYSTEM_PROGRAM":
        raise QuoteRequired(f"{economy_code} requires B2B/B2G/enterprise quoting")
    if classification == "BUNDLED_BRIDGE":
        raise EligibilityRequired(f"{economy_code} requires bridge eligibility")
    if classification != "PUBLIC_MARKET":
        raise CommercialPolicyError(f"Unsupported Economy 3D commercial class: {classification}")

    if offer_kind != "path":
        # The canonical phrase is "€990 path / subscription". The workbook
        # proves the path price but does not, in this projection, encode which
        # subscription plan/rate applies to this item. Human Authority: refuse
        # to invent a subscription amount.
        raise QuoteRequired("Subscription offer requires a concrete canonical plan mapping")

    price_label = str(record["prix_public_v1"])
    match = re.match(r"^€([0-9]+(?:\.[0-9]+)?)\s+path\b", price_label)
    if not match:
        raise CommercialPolicyError(f"No exact path amount in Economy 3D: {price_label}")
    amount_eur = float(match.group(1))
    return {
        "economy_code": record["code"],
        "requirement_id": record["requirement_id"],
        "offer_kind": "path",
        "amount_eur": amount_eur,
        "currency": "EUR",
        "price_label": price_label,
        "commercial_class": classification,
        "source_workbook": "CVLN_Academy_Master_Economie_3D_DECIDE_V1.xlsx",
        "source_sheet": "Mapping_812",
        "source_row": record["source_row"],
        "economic_status": record["economic_status"],
    }


def amount_eur_to_jcc(amount_eur: float, rate_eur_per_jcc: float) -> float:
    if amount_eur <= 0 or rate_eur_per_jcc <= 0:
        raise CommercialPolicyError("Invalid EUR/JCC conversion inputs")
    return round(amount_eur / rate_eur_per_jcc, 2)


def entitlement_filter(user_id: str, economy_code: str) -> Dict[str, Any]:
    return {
        "user_id": user_id,
        "economy_code": economy_code,
        "status": "ACTIVE",
    }
