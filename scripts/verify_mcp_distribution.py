#!/usr/bin/env python3
"""Verify a deployed CVLN Academy MCP/OAuth surface without mutating data."""

from __future__ import annotations

import argparse
import sys

import requests


def check(base_url: str) -> int:
    base = base_url.rstrip("/")
    failures: list[str] = []

    def expect_json(path: str, expected: int = 200):
        response = requests.get(f"{base}{path}", timeout=15)
        if response.status_code != expected:
            failures.append(f"GET {path}: expected {expected}, got {response.status_code}")
            return None
        try:
            return response.json()
        except ValueError:
            failures.append(f"GET {path}: response is not JSON")
            return None

    auth = expect_json("/.well-known/oauth-authorization-server")
    prm = expect_json("/.well-known/oauth-protected-resource/mcp/private")

    if auth and auth.get("issuer", "").rstrip("/") != base:
        failures.append("OAuth issuer does not match the tested public base URL")
    if prm and prm.get("resource", "").rstrip("/") != f"{base}/mcp/private":
        failures.append("Protected resource metadata does not match /mcp/private")

    unauth = requests.post(
        f"{base}/mcp/private",
        headers={"accept": "application/json, text/event-stream"},
        json={"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}},
        timeout=15,
    )
    if unauth.status_code not in {401, 403}:
        failures.append(
            f"POST /mcp/private without token: expected 401/403, got {unauth.status_code}"
        )

    public = requests.post(
        f"{base}/mcp",
        headers={"accept": "application/json, text/event-stream"},
        json={
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2025-11-25",
                "capabilities": {},
                "clientInfo": {"name": "cvln-deploy-check", "version": "1.0"},
            },
        },
        timeout=15,
    )
    if public.status_code >= 500:
        failures.append(f"POST /mcp initialize returned {public.status_code}")

    if failures:
        for item in failures:
            print(f"FAIL: {item}")
        return 1

    print("OK: public MCP reachable, OAuth discovery valid, private MCP protected")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("base_url", help="Public Academy backend URL, e.g. https://api.example.com")
    args = parser.parse_args()
    return check(args.base_url)


if __name__ == "__main__":
    sys.exit(main())
