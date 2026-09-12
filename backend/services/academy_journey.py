"""Canonical CVLN Academy journey orchestration used by MCP and future clients.

This module deliberately reuses existing Academy business services instead of
creating a second payment/support/certification stack. External funder approval
remains an explicit gate: CVLN may prepare and track dossiers, but a funded
enrolment is finalized only after an approved dossier exists.
"""

from __future__ import annotations

import os
from types import SimpleNamespace
from typing import Any, Optional

from api.commercial import OrderCreate, create_order, pay_order_with_wallet
from certification import list_user_attempts, start_attempt, submit_attempt
from db import db, utc_now_iso
from services.careops import create_ticket, list_user_tickets

CURRENT_TERMS_VERSION = os.environ.get("ACADEMY_TERMS_VERSION", "2026-09")


class JourneyPolicyError(ValueError):
    """Raised when a guarded journey transition is not allowed."""


async def _actor(user_id: str) -> SimpleNamespace:
    user = await db.users.find_one(
        {"id": user_id}, {"_id": 0, "id": 1, "frek_id": 1, "email": 1}
    )
    if not user:
        raise JourneyPolicyError("USER_NOT_FOUND")
    return SimpleNamespace(**user)


async def accept_terms(
    *,
    user_id: str,
    signature_name: str,
    version: str = CURRENT_TERMS_VERSION,
    method: str = "typed_name",
) -> dict[str, Any]:
    name = signature_name.strip()
    if len(name) < 2:
        raise JourneyPolicyError("SIGNATURE_NAME_REQUIRED")
    if method not in {"typed_name", "pointer", "touch"}:
        raise JourneyPolicyError("UNSUPPORTED_SIGNATURE_METHOD")
    now = utc_now_iso()
    acceptance = {
        "user_id": user_id,
        "terms_version": version.strip() or CURRENT_TERMS_VERSION,
        "signature_name": name,
        "signature_method": method,
        "accepted": True,
        "accepted_at": now,
        "source": "mcp",
    }
    await db.academy_terms_acceptances.update_one(
        {"user_id": user_id, "terms_version": acceptance["terms_version"]},
        {"$setOnInsert": acceptance},
        upsert=True,
    )
    stored = await db.academy_terms_acceptances.find_one(
        {"user_id": user_id, "terms_version": acceptance["terms_version"]},
        {"_id": 0},
    )
    return stored or acceptance


async def create_payment_order(
    *, user_id: str, economy_code: str, offer_kind: str = "path"
) -> dict[str, Any]:
    """Create an Academy commercial order through the existing commercial runtime."""
    actor = await _actor(user_id)
    return await create_order(
        OrderCreate(economy_code=economy_code, offer_kind=offer_kind), current=actor
    )


async def pay_payment_order(*, user_id: str, order_id: str) -> dict[str, Any]:
    """Charge the existing CVLN Wallet path and let it grant the entitlement."""
    actor = await _actor(user_id)
    return await pay_order_with_wallet(order_id, current=actor)


async def finalize_enrollment(
    *,
    user_id: str,
    formation_code: str,
    economy_code: Optional[str] = None,
    funding_dossier_id: Optional[str] = None,
) -> dict[str, Any]:
    """Finalize an Academy enrolment after deterministic legal/payment/funding gates."""
    formation = await db.formations.find_one(
        {"code": formation_code, "content_status": "published"},
        {"_id": 0, "code": 1, "name": 1},
    )
    if not formation:
        raise JourneyPolicyError("PUBLISHED_FORMATION_NOT_FOUND")

    acceptance = await db.academy_terms_acceptances.find_one(
        {
            "user_id": user_id,
            "terms_version": CURRENT_TERMS_VERSION,
            "accepted": True,
        },
        {"_id": 0},
    )
    if not acceptance:
        raise JourneyPolicyError("CURRENT_TERMS_NOT_ACCEPTED")

    entitlement = None
    if economy_code:
        entitlement = await db.academy_entitlements.find_one(
            {
                "user_id": user_id,
                "economy_code": economy_code,
                "status": "ACTIVE",
            },
            {"_id": 0},
        )
        if not entitlement:
            raise JourneyPolicyError("ACTIVE_ENTITLEMENT_REQUIRED")

    funding = None
    if funding_dossier_id:
        funding = await db.mcp_funding_dossiers.find_one(
            {"id": funding_dossier_id, "user_id": user_id}, {"_id": 0}
        )
        if not funding:
            raise JourneyPolicyError("FUNDING_DOSSIER_NOT_FOUND")
        if funding.get("status") != "APPROVED":
            raise JourneyPolicyError("FUNDING_APPROVAL_REQUIRED")

    now = utc_now_iso()
    insert_fields = {
        "user_id": user_id,
        "formation_code": formation_code,
        "formation_name": formation.get("name"),
        "terms_version": CURRENT_TERMS_VERSION,
        "economy_code": economy_code,
        "source_entitlement_id": (entitlement or {}).get("entitlement_id"),
        "funding_dossier_id": funding_dossier_id,
        "funding_connector": (funding or {}).get("connector_code"),
        "enrolled_at": now,
        "source": "mcp_journey",
    }
    await db.academy_enrollments.update_one(
        {"user_id": user_id, "formation_code": formation_code},
        {
            "$setOnInsert": insert_fields,
            "$set": {"status": "ENROLLED", "updated_at": now},
        },
        upsert=True,
    )
    await db.mcp_enrollment_requests.update_many(
        {
            "user_id": user_id,
            "formation_code": formation_code,
            "status": "PENDING_REVIEW",
        },
        {"$set": {"status": "APPROVED", "updated_at": now}},
    )
    stored = await db.academy_enrollments.find_one(
        {"user_id": user_id, "formation_code": formation_code}, {"_id": 0}
    )
    return stored or {**insert_fields, "status": "ENROLLED", "updated_at": now}


async def journey_status(
    *, user_id: str, formation_code: str, economy_code: Optional[str] = None
) -> dict[str, Any]:
    formation = await db.formations.find_one(
        {"code": formation_code, "content_status": "published"}, {"_id": 0}
    )
    acceptance = await db.academy_terms_acceptances.find_one(
        {"user_id": user_id, "terms_version": CURRENT_TERMS_VERSION, "accepted": True},
        {"_id": 0},
    )
    entitlement = None
    if economy_code:
        entitlement = await db.academy_entitlements.find_one(
            {"user_id": user_id, "economy_code": economy_code, "status": "ACTIVE"},
            {"_id": 0},
        )
    funding = await db.mcp_funding_dossiers.find_one(
        {"user_id": user_id, "formation_code": formation_code},
        {"_id": 0},
        sort=[("created_at", -1)],
    )
    enrollment = await db.academy_enrollments.find_one(
        {"user_id": user_id, "formation_code": formation_code}, {"_id": 0}
    )
    attempts = [a.model_dump() for a in await list_user_attempts(user_id)]
    tickets = await list_user_tickets(user_id, limit=10)
    blockers = []
    if not formation:
        blockers.append("formation_not_published")
    if not acceptance:
        blockers.append("terms_not_accepted")
    if economy_code and not entitlement:
        blockers.append("payment_or_entitlement_missing")
    if funding and funding.get("status") != "APPROVED":
        blockers.append("funding_approval_required")
    return {
        "formation": formation,
        "terms": acceptance,
        "entitlement": entitlement,
        "funding": funding,
        "enrollment": enrollment,
        "certification_attempts": attempts,
        "recent_support_tickets": tickets,
        "blockers": blockers,
        "can_finalize_enrollment": bool(
            formation
            and acceptance
            and (not economy_code or entitlement)
            and (not funding or funding.get("status") == "APPROVED")
        ),
    }


async def open_support_request(
    *, user_id: str, message: str, channel: str = "mcp"
) -> dict[str, Any]:
    return await create_ticket(
        user_id=user_id,
        message=message,
        product="academy",
        channel=channel,
    )


async def start_certification(
    *, user_id: str, certification_code: str
) -> dict[str, Any]:
    attempt = await start_attempt(user_id, certification_code)
    return attempt.model_dump()


async def submit_certification(
    *, user_id: str, attempt_id: str
) -> dict[str, Any]:
    attempt = await submit_attempt(attempt_id, user_id)
    return attempt.model_dump()
