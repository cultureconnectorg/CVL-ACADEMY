"""Authenticated CVLN Academy MCP surface.

This module is additive: the existing public/read-only MCP remains unchanged.
Private tools operate only on the authenticated subject and require explicit
OAuth scopes. External funder submission is deliberately not simulated.
"""

from __future__ import annotations

import os
import uuid
from datetime import datetime, timezone
from typing import Any, Optional

from mcp.server import MCPServer
from mcp.server.auth.middleware.auth_context import get_access_token
from mcp.server.auth.settings import AuthSettings
from mcp.server.transport_security import TransportSecuritySettings
from pydantic import AnyHttpUrl

from db import db
from mcp_auth import MCP_OAUTH_ISSUER, MCP_PRIVATE_RESOURCE, AcademyMCPTokenVerifier
from services.institutional_bridge import registry as bridge_registry


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _uid() -> str:
    return str(uuid.uuid4())


def _principal(required_scopes: set[str]) -> tuple[str, set[str]]:
    token = get_access_token()
    if token is None or not token.subject:
        raise PermissionError("Authentication required")
    granted = set(token.scopes or [])
    missing = required_scopes - granted
    if missing:
        raise PermissionError(f"Missing OAuth scope(s): {', '.join(sorted(missing))}")
    return token.subject, granted


def _transport_security() -> Optional[TransportSecuritySettings]:
    """Reuse the production Host/Origin policy used by the public MCP."""
    raw_hosts = os.environ.get("MCP_ALLOWED_HOSTS", "")
    hosts = [item.strip() for item in raw_hosts.split(",") if item.strip()]
    if not hosts:
        render_host = os.environ.get("RENDER_EXTERNAL_HOSTNAME", "").strip()
        if render_host:
            hosts = [render_host, f"{render_host}:*"]
    if not hosts:
        return None

    raw_origins = os.environ.get("MCP_ALLOWED_ORIGINS", "")
    origins = [
        item.strip()
        for item in raw_origins.split(",")
        if item.strip() and item.strip() != "*"
    ]
    return TransportSecuritySettings(
        allowed_hosts=hosts,
        allowed_origins=origins,
    )


private_academy_mcp = MCPServer(
    "CVLN Academy Private",
    instructions=(
        "Authenticated CVLN Academy capability for the connected user. Never claim that "
        "a funding request was submitted to Afdas, France Travail or another institution "
        "unless a verified live connector explicitly reports that submission. Dossier "
        "preparation and enrollment requests are real Academy records, not external approvals."
    ),
    token_verifier=AcademyMCPTokenVerifier(),
    auth=AuthSettings(
        issuer_url=AnyHttpUrl(MCP_OAUTH_ISSUER),
        resource_server_url=AnyHttpUrl(MCP_PRIVATE_RESOURCE),
        required_scopes=["academy:profile.read"],
        validate_token_resource=True,
    ),
)


@private_academy_mcp.tool()
async def get_my_profile() -> dict[str, Any]:
    """Read the connected user's CVLN Academy profile."""
    user_id, _ = _principal({"academy:profile.read"})
    user = await db.users.find_one(
        {"id": user_id},
        {
            "_id": 0,
            "password_hash": 0,
            "totp_secret": 0,
            "oauth_accounts": 0,
        },
    )
    if not user:
        return {"found": False}
    return {"found": True, "user": user}


@private_academy_mcp.tool()
async def list_funding_connectors() -> dict[str, Any]:
    """List verified Academy funding/interoperability connector capabilities."""
    _principal({"academy:funding.read"})
    items = [item.model_dump() for item in bridge_registry.describe_connectors()]
    return {
        "count": len(items),
        "items": items,
        "policy": (
            "Connector capability is evidence-based; live_write_implemented=false "
            "means preparation only."
        ),
    }


@private_academy_mcp.tool()
async def create_funding_dossier(
    connector_code: str,
    formation_code: str,
    territory: str,
    funding_scheme: str,
    amount_requested_eur: Optional[float] = None,
) -> dict[str, Any]:
    """Create a real Academy funding dossier draft for the connected user.

    For Afdas/France Travail this prepares the Academy-side dossier; it does not
    claim to submit into an external portal.
    """
    user_id, _ = _principal({"academy:funding.write"})
    if amount_requested_eur is not None and amount_requested_eur < 0:
        raise ValueError("amount_requested_eur must be >= 0")
    try:
        connector = bridge_registry.require_capability(
            connector_code, "APPLICATION_PREPARE"
        )
    except (
        bridge_registry.UnknownConnector,
        bridge_registry.UnsupportedCapability,
    ) as exc:
        raise ValueError(str(exc)) from exc
    formation = await db.formations.find_one(
        {"code": formation_code, "content_status": "published"},
        {"_id": 0, "code": 1, "name": 1},
    )
    if not formation:
        raise ValueError("Published formation not found")
    dossier: dict[str, Any] = {
        "id": _uid(),
        "user_id": user_id,
        "connector_code": connector.code,
        "connector_name": connector.name,
        "formation_code": formation_code,
        "formation_name": formation.get("name"),
        "territory": territory.strip(),
        "funding_scheme": funding_scheme.strip(),
        "amount_requested_eur": amount_requested_eur,
        "documents": [],
        "status": "DRAFT",
        "external_submission_performed": False,
        "connection_mode": connector.connection_mode,
        "live_write_implemented": connector.live_write_implemented,
        "created_at": _now(),
        "updated_at": _now(),
    }
    await db.mcp_funding_dossiers.insert_one(dossier)
    dossier.pop("_id", None)
    return {"created": True, "dossier": dossier}


@private_academy_mcp.tool()
async def get_my_funding_dossier(dossier_id: str) -> dict[str, Any]:
    """Read one funding dossier owned by the connected user."""
    user_id, _ = _principal({"academy:funding.read"})
    doc = await db.mcp_funding_dossiers.find_one(
        {"id": dossier_id, "user_id": user_id}, {"_id": 0}
    )
    return {"found": bool(doc), "dossier": doc}


@private_academy_mcp.tool()
async def add_funding_document_reference(
    dossier_id: str,
    document_type: str,
    document_reference: str,
) -> dict[str, Any]:
    """Attach a CVLN document reference to the user's funding dossier.

    This stores a reference/identifier, not secret file bytes inside the MCP log.
    """
    user_id, _ = _principal({"academy:funding.write"})
    item = {
        "id": _uid(),
        "type": document_type.strip(),
        "reference": document_reference.strip(),
        "added_at": _now(),
    }
    result = await db.mcp_funding_dossiers.update_one(
        {"id": dossier_id, "user_id": user_id, "status": "DRAFT"},
        {"$push": {"documents": item}, "$set": {"updated_at": _now()}},
    )
    if result.matched_count != 1:
        return {"updated": False, "reason": "dossier_not_found_or_not_editable"}
    return {"updated": True, "document": item}


@private_academy_mcp.tool()
async def mark_funding_dossier_ready(dossier_id: str) -> dict[str, Any]:
    """Mark an Academy dossier ready for review, without external submission."""
    user_id, _ = _principal({"academy:funding.write"})
    result = await db.mcp_funding_dossiers.update_one(
        {"id": dossier_id, "user_id": user_id, "status": "DRAFT"},
        {
            "$set": {
                "status": "READY",
                "external_submission_performed": False,
                "updated_at": _now(),
            }
        },
    )
    return {
        "updated": result.matched_count == 1,
        "status": "READY" if result.matched_count == 1 else None,
        "external_submission_performed": False,
    }


@private_academy_mcp.tool()
async def list_my_funding_dossiers(limit: int = 50) -> dict[str, Any]:
    """List funding dossiers belonging to the connected user."""
    user_id, _ = _principal({"academy:funding.read"})
    safe_limit = max(1, min(int(limit), 100))
    docs = (
        await db.mcp_funding_dossiers.find({"user_id": user_id}, {"_id": 0})
        .sort("created_at", -1)
        .limit(safe_limit)
        .to_list(safe_limit)
    )
    return {"count": len(docs), "items": docs}


@private_academy_mcp.tool()
async def create_enrollment_request(
    formation_code: str,
    preferred_session: Optional[str] = None,
    note: Optional[str] = None,
) -> dict[str, Any]:
    """Create an Academy enrollment request for a published formation.

    This is a real Academy request record. It does not bypass pricing, payment,
    legal acceptance, prerequisites or staff validation.
    """
    user_id, _ = _principal({"academy:enrollment.write"})
    formation = await db.formations.find_one(
        {"code": formation_code, "content_status": "published"},
        {"_id": 0, "code": 1, "name": 1},
    )
    if not formation:
        raise ValueError("Published formation not found")
    existing = await db.mcp_enrollment_requests.find_one(
        {
            "user_id": user_id,
            "formation_code": formation_code,
            "status": {"$in": ["PENDING_REVIEW", "APPROVED"]},
        },
        {"_id": 0},
    )
    if existing:
        return {
            "created": False,
            "reason": "active_request_exists",
            "request": existing,
        }
    request_doc = {
        "id": _uid(),
        "user_id": user_id,
        "formation_code": formation_code,
        "formation_name": formation.get("name"),
        "preferred_session": preferred_session,
        "note": (note or "")[:1000],
        "status": "PENDING_REVIEW",
        "creates_entitlement": False,
        "payment_bypassed": False,
        "created_at": _now(),
        "updated_at": _now(),
    }
    await db.mcp_enrollment_requests.insert_one(request_doc)
    request_doc.pop("_id", None)
    return {"created": True, "request": request_doc}


@private_academy_mcp.tool()
async def list_my_enrollment_requests(limit: int = 50) -> dict[str, Any]:
    """List enrollment requests belonging to the connected user."""
    user_id, _ = _principal({"academy:enrollment.read"})
    safe_limit = max(1, min(int(limit), 100))
    docs = (
        await db.mcp_enrollment_requests.find({"user_id": user_id}, {"_id": 0})
        .sort("created_at", -1)
        .limit(safe_limit)
        .to_list(safe_limit)
    )
    return {"count": len(docs), "items": docs}


private_mcp_http_app = private_academy_mcp.streamable_http_app(
    streamable_http_path="/",
    transport_security=_transport_security(),
)
