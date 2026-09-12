"""End-to-end CVLN Academy journey tools registered on the private MCP surface."""

from __future__ import annotations

from typing import Any, Optional

from mcp.server.auth.middleware.auth_context import get_access_token

from mcp_private import private_academy_mcp
from services.academy_journey import (
    accept_terms,
    create_payment_order,
    finalize_enrollment,
    journey_status,
    open_support_request,
    pay_payment_order,
    start_certification,
    submit_certification,
)


def _principal(required_scopes: set[str]) -> str:
    token = get_access_token()
    if token is None or not token.subject:
        raise PermissionError("Authentication required")
    granted = set(token.scopes or [])
    missing = required_scopes - granted
    if missing:
        raise PermissionError(f"Missing OAuth scope(s): {', '.join(sorted(missing))}")
    return token.subject


@private_academy_mcp.tool()
async def get_my_journey(
    formation_code: str,
    economy_code: Optional[str] = None,
) -> dict[str, Any]:
    """Read the connected user's end-to-end Academy journey and blockers."""
    user_id = _principal(
        {
            "academy:profile.read",
            "academy:enrollment.read",
            "academy:funding.read",
            "academy:support.read",
            "academy:certification.read",
        }
    )
    return await journey_status(
        user_id=user_id,
        formation_code=formation_code,
        economy_code=economy_code,
    )


@private_academy_mcp.tool()
async def accept_current_academy_terms(
    signature_name: str,
    signature_method: str = "typed_name",
) -> dict[str, Any]:
    """Record the connected user's explicit acceptance of the current Academy terms."""
    user_id = _principal({"academy:legal.write"})
    return await accept_terms(
        user_id=user_id,
        signature_name=signature_name,
        method=signature_method,
    )


@private_academy_mcp.tool()
async def create_my_payment_order(
    economy_code: str,
    offer_kind: str = "path",
) -> dict[str, Any]:
    """Create a commercial order through the canonical Academy commercial runtime."""
    user_id = _principal({"academy:payment.write"})
    return await create_payment_order(
        user_id=user_id,
        economy_code=economy_code,
        offer_kind=offer_kind,
    )


@private_academy_mcp.tool()
async def pay_my_order_with_cvln_wallet(order_id: str) -> dict[str, Any]:
    """Pay an Academy order through the existing CVLN Wallet integration."""
    user_id = _principal({"academy:payment.write"})
    return await pay_payment_order(user_id=user_id, order_id=order_id)


@private_academy_mcp.tool()
async def finalize_my_enrollment(
    formation_code: str,
    economy_code: Optional[str] = None,
    funding_dossier_id: Optional[str] = None,
) -> dict[str, Any]:
    """Finalize enrolment when legal, payment and optional funding gates pass.

    A funded journey requires an APPROVED funding dossier. This tool never turns
    a prepared or READY Afdas/France Travail dossier into an approval by itself.
    """
    user_id = _principal({"academy:enrollment.write"})
    return await finalize_enrollment(
        user_id=user_id,
        formation_code=formation_code,
        economy_code=economy_code,
        funding_dossier_id=funding_dossier_id,
    )


@private_academy_mcp.tool()
async def open_my_support_or_claim(message: str) -> dict[str, Any]:
    """Open a CareOps support, payment, claim, access or incident ticket."""
    user_id = _principal({"academy:support.write"})
    return await open_support_request(user_id=user_id, message=message, channel="mcp")


@private_academy_mcp.tool()
async def start_my_certification(certification_code: str) -> dict[str, Any]:
    """Start a certification attempt through the canonical certification engine."""
    user_id = _principal({"academy:certification.write"})
    return await start_certification(
        user_id=user_id,
        certification_code=certification_code,
    )


@private_academy_mcp.tool()
async def submit_my_certification(attempt_id: str) -> dict[str, Any]:
    """Submit one of the connected user's certification attempts for grading."""
    user_id = _principal({"academy:certification.write"})
    return await submit_certification(user_id=user_id, attempt_id=attempt_id)
