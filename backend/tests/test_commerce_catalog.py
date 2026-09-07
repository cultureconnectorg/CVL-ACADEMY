"""ACA-0025 — the real DECIDED_V1 commercial offer catalogue.

Real gap this closes: `ACA-0025` ("Define real commercial states by
delivery mode") was open — no code anywhere reflected the Founder's
actual, dated pricing/policy decisions
(`CVLN_Academy_Master_Economie_3D_DECIDE_V1.xlsx`, 2026-09-06). This
suite proves the transcription is faithful (spot-checked against the
source workbook's own figures) and that the gate this whole module is
built to satisfy — `NO_FAKE_PAID_STATE` (BIN-021/BIN-022) — actually
holds: the public catalogue never exposes internal cost/margin data,
and nothing in this module or its API creates/reads a paid/subscribed
flag on any user.
"""

from __future__ import annotations

import pytest

from commerce import OFFERS, POLICIES, get_offer
from models import STAFF_ROLES, User


def test_catalogue_has_all_twenty_source_offers():
    assert len(OFFERS) == 20
    assert {o.offer_id for o in OFFERS} == {
        "free-orientation",
        "academy-access",
        "academy-pro",
        "academy-career",
        "parcours-metier",
        "intensive-hybrid-week",
        "assessment-only",
        "certification-academy",
        "certification-renewal",
        "b2b-team",
        "b2b-growth",
        "b2b-enterprise",
        "b2g-pilot",
        "b2g-territory",
        "b2g-large",
        "learning-to-work-client",
        "methodology-ip-licence",
        "academy-spatial-licence",
        "white-label-enterprise",
        "internal-cvln-capability",
    }


def test_policies_registry_has_all_eighteen_source_rows():
    assert len(POLICIES) == 18
    assert all(p.decision_status == "DECIDED_V1" for p in POLICIES)


@pytest.mark.parametrize(
    "offer_id,expected_price,expected_annual",
    [
        ("academy-access", 24.90, 249.0),
        ("academy-pro", 69.0, 690.0),
        ("academy-career", 129.0, 1290.0),
        ("parcours-metier", 990.0, None),
        ("intensive-hybrid-week", 1400.0, None),
        ("assessment-only", 250.0, None),
        ("certification-academy", 390.0, None),
        ("certification-renewal", 190.0, None),
        ("b2b-team", 12000.0, None),
        ("b2b-growth", 39000.0, None),
        ("b2b-enterprise", 69000.0, None),
        ("b2g-pilot", 35000.0, None),
        ("b2g-territory", 120000.0, None),
        ("b2g-large", 250000.0, None),
        ("methodology-ip-licence", 25000.0, None),
        ("academy-spatial-licence", 60000.0, None),
        ("white-label-enterprise", 120000.0, None),
    ],
)
def test_prices_match_source_workbook_exactly(offer_id, expected_price, expected_annual):
    offer = get_offer(offer_id)
    assert offer is not None
    assert offer.price_eur == expected_price
    assert offer.price_eur_annual == expected_annual


def test_free_and_internal_offers_are_genuinely_zero_price():
    for offer_id in ("free-orientation", "internal-cvln-capability"):
        offer = get_offer(offer_id)
        assert offer.price_eur == 0
        assert offer.gross_margin_eur == 0


def test_internal_cvln_capability_is_engine_internal_value_never_public_pricing():
    offer = get_offer("internal-cvln-capability")
    assert offer.engine == "Internal Value"
    assert offer.pricing_unit == "Non commercial"


def test_unknown_offer_id_returns_none():
    assert get_offer("does-not-exist") is None


# --------------------------------------------------------------------
# NO_FAKE_PAID_STATE — the actual gate this module exists to satisfy.
# --------------------------------------------------------------------


def test_offer_model_has_no_paid_or_subscription_state_field():
    """A catalogue entry describes a product, never a user's relationship
    to it — no `paid`/`subscribed`/`active`/`user_id` field exists."""
    fields = set(type(OFFERS[0]).model_fields.keys())
    forbidden = {"paid", "subscribed", "active", "user_id", "purchased", "status"}
    assert not (fields & forbidden)


def test_offer_and_policy_models_carry_no_user_reference():
    for offer in OFFERS:
        assert not hasattr(offer, "user_id")
    for policy in POLICIES:
        assert not hasattr(policy, "user_id")


# --------------------------------------------------------------------
# API — public vs staff-only views
# --------------------------------------------------------------------


def _student() -> User:
    return User(
        frek_id="FREK-STUDENT",
        email="student@example.com",
        display_name="Student",
        password_hash="x",
        role="student",
    )


def _admin() -> User:
    return User(
        frek_id="FREK-ADMIN",
        email="admin@example.com",
        display_name="Admin",
        password_hash="x",
        role="admin",
    )


@pytest.mark.asyncio
async def test_public_offers_endpoint_needs_no_auth_and_hides_margin():
    from api.commerce import list_public_offers

    results = await list_public_offers()
    assert len(results) == 20
    academy_access = next(o for o in results if o.offer_id == "academy-access")
    assert academy_access.price_eur == 24.90
    # Only customer-facing fields exist on the response model at all —
    # cost/margin/floor/source_decision_id can't leak because the
    # PublicOffer schema itself has no such field.
    assert not hasattr(academy_access, "variable_cost_eur")
    assert not hasattr(academy_access, "gross_margin_eur")
    assert not hasattr(academy_access, "margin_floor_pct")


@pytest.mark.asyncio
async def test_internal_offers_endpoint_requires_staff():
    from api.commerce import list_internal_offers

    results = await list_internal_offers(current=_admin())
    assert len(results) == 20
    academy_access = next(o for o in results if o.offer_id == "academy-access")
    assert academy_access.gross_margin_eur == 20.4


def _allowed_roles(dependency_callable):
    """Same helper as test_fms_canonical.py — inspects a
    `require_role(...)`-closure's `__closure__`/`co_freevars` to
    extract the exact allowed-roles tuple."""
    freevars = dependency_callable.__code__.co_freevars
    if "allowed" not in freevars:
        return None
    idx = freevars.index("allowed")
    return dependency_callable.__closure__[idx].cell_contents


def test_internal_offers_route_declares_staff_auth():
    """Declarative check that the route itself is gated (mirrors
    test_fms_canonical.py's own convention) — a student calling the
    real FastAPI route (not the bare function) would 403."""
    from api.commerce import router

    for path in ("/commerce/offers/internal", "/commerce/policies"):
        route = next(r for r in router.routes if r.path == path)
        roles = next(
            (
                _allowed_roles(dep.call)
                for dep in route.dependant.dependencies
                if _allowed_roles(dep.call)
            ),
            None,
        )
        assert roles == STAFF_ROLES, path
