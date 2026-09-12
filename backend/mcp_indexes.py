"""Indexes for OAuth/MCP state kept separate from Academy core indexes."""

from __future__ import annotations

from db import db


async def ensure_mcp_indexes() -> None:
    await db.mcp_oauth_clients.create_index("client_id", unique=True)
    await db.mcp_auth_codes.create_index("code_hash", unique=True)
    await db.mcp_auth_codes.create_index("expires_at")
    await db.mcp_refresh_tokens.create_index("token_hash", unique=True)
    await db.mcp_refresh_tokens.create_index([("user_id", 1), ("client_id", 1)])
    await db.mcp_funding_dossiers.create_index("id", unique=True)
    await db.mcp_funding_dossiers.create_index([("user_id", 1), ("created_at", -1)])
    await db.mcp_funding_dossiers.create_index([("user_id", 1), ("status", 1)])
    await db.mcp_enrollment_requests.create_index("id", unique=True)
    await db.mcp_enrollment_requests.create_index([("user_id", 1), ("created_at", -1)])
    await db.mcp_enrollment_requests.create_index([("user_id", 1), ("formation_code", 1), ("status", 1)])
    await db.academy_terms_acceptances.create_index(
        [("user_id", 1), ("terms_version", 1)], unique=True
    )
    await db.academy_enrollments.create_index(
        [("user_id", 1), ("formation_code", 1)], unique=True
    )
    await db.academy_enrollments.create_index([("status", 1), ("updated_at", -1)])
