import asyncio

import pytest

import mcp_journey
from mcp_auth import SCOPES, normalize_scopes
from services.academy_journey import JourneyPolicyError, accept_terms


REQUIRED_JOURNEY_SCOPES = {
    "academy:legal.write",
    "academy:payment.write",
    "academy:support.read",
    "academy:support.write",
    "academy:certification.read",
    "academy:certification.write",
}


def test_journey_scopes_are_allowlisted():
    assert REQUIRED_JOURNEY_SCOPES.issubset(SCOPES)
    assert set(normalize_scopes(REQUIRED_JOURNEY_SCOPES)) == REQUIRED_JOURNEY_SCOPES


def test_journey_tools_are_registered_as_callables():
    expected = [
        "get_my_journey",
        "accept_current_academy_terms",
        "create_my_payment_order",
        "pay_my_order_with_cvln_wallet",
        "finalize_my_enrollment",
        "open_my_support_or_claim",
        "start_my_certification",
        "submit_my_certification",
    ]
    for name in expected:
        assert callable(getattr(mcp_journey, name))


def test_terms_reject_unsupported_signature_method_before_persistence():
    with pytest.raises(JourneyPolicyError, match="UNSUPPORTED_SIGNATURE_METHOD"):
        asyncio.run(
            accept_terms(
                user_id="usr_test",
                signature_name="Test User",
                method="voice_guess",
            )
        )


def test_terms_reject_empty_signature_before_persistence():
    with pytest.raises(JourneyPolicyError, match="SIGNATURE_NAME_REQUIRED"):
        asyncio.run(
            accept_terms(
                user_id="usr_test",
                signature_name=" ",
            )
        )
