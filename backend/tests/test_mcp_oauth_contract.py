from __future__ import annotations

import jwt
import pytest

import mcp_auth
from api import mcp_oauth
from server import app


def test_private_mcp_mounts_are_additive():
    paths = {
        path
        for route in app.routes
        if (path := getattr(route, "path", None)) is not None
    }
    assert "/mcp" in paths
    assert "/mcp/private" in paths
    assert "/.well-known/oauth-authorization-server" in paths
    assert "/.well-known/oauth-protected-resource/mcp/private" in paths
    assert "/oauth/authorize" in paths
    assert "/oauth/token" in paths


def test_oauth_scope_contract_is_allowlisted():
    scopes = mcp_auth.normalize_scopes(
        ["academy:profile.read", "not-a-scope", "academy:funding.write"]
    )
    assert scopes == ["academy:profile.read", "academy:funding.write"]
    assert "academy:enrollment.write" in mcp_auth.SCOPES


def test_access_token_is_resource_bound_and_scoped():
    raw, _ = mcp_auth.issue_access_token(
        "user-1",
        "client-1",
        ["academy:profile.read", "academy:funding.read"],
    )
    payload = jwt.decode(
        raw,
        mcp_auth.JWT_SECRET,
        algorithms=[mcp_auth.JWT_ALGO],
        audience=mcp_auth.MCP_PRIVATE_RESOURCE,
        issuer=mcp_auth.MCP_OAUTH_ISSUER,
    )
    assert payload["sub"] == "user-1"
    assert payload["client_id"] == "client-1"
    assert payload["type"] == "mcp_access"
    assert set(payload["scope"].split()) == {
        "academy:profile.read",
        "academy:funding.read",
    }


def test_pkce_s256_and_redirect_policy():
    verifier = "test-verifier-with-enough-entropy-1234567890"
    assert mcp_oauth._b64url_sha256(verifier) == mcp_oauth._b64url_sha256(verifier)
    assert mcp_oauth._safe_redirect_uri("https://chatgpt.com/example/callback")
    assert mcp_oauth._safe_redirect_uri("http://localhost:8787/callback")
    assert not mcp_oauth._safe_redirect_uri("http://example.com/callback")
    assert not mcp_oauth._safe_redirect_uri("javascript:alert(1)")


@pytest.mark.asyncio
async def test_discovery_metadata_declares_pkce_and_resource():
    auth = await mcp_oauth.oauth_metadata()
    prm = await mcp_oauth.protected_resource_metadata()
    assert auth["code_challenge_methods_supported"] == ["S256"]
    assert auth["token_endpoint_auth_methods_supported"] == ["none"]
    assert prm["resource"] == mcp_auth.MCP_PRIVATE_RESOURCE
    assert mcp_auth.MCP_OAUTH_ISSUER in prm["authorization_servers"]
