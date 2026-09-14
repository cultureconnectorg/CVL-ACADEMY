"""Real, non-deployed CVLN runtime integration smoke.

Runs against three live FastAPI processes in CI:
Academy -> Agent Factory -> Command Center.
No HTTP mock and no fabricated remote ids are accepted.
"""

from __future__ import annotations

import os
import time
from typing import Any

import httpx
from pymongo import MongoClient

ACADEMY = os.environ.get("ACADEMY_URL", "http://127.0.0.1:8100")
FACTORY = os.environ.get("CVLN_AGENT_FACTORY_URL", "http://127.0.0.1:8101/api")
COMMAND = os.environ.get("CVLN_COMMAND_CENTER_URL", "http://127.0.0.1:8102")
FACTORY_TOKEN = os.environ["CVLN_AGENT_FACTORY_SERVICE_TOKEN"]
COMMAND_TOKEN = os.environ["CVLN_COMMAND_CENTER_ACCESS_TOKEN"]
MONGO_URL = os.environ.get("MONGO_URL", "mongodb://127.0.0.1:27017")
ACADEMY_DB = os.environ.get("DB_NAME", "cvln_academy_runtime_integration")


def request(method: str, url: str, *, token: str | None = None, json: dict[str, Any] | None = None):
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    response = httpx.request(method, url, headers=headers, json=json, timeout=15.0)
    if response.status_code >= 400:
        raise RuntimeError(f"{method} {url} -> {response.status_code}: {response.text[:1000]}")
    return response.json()


def wait(url: str, token: str | None = None, seconds: int = 60) -> None:
    deadline = time.time() + seconds
    last = None
    while time.time() < deadline:
        try:
            response = httpx.get(
                url,
                headers={"Authorization": f"Bearer {token}"} if token else {},
                timeout=2.0,
            )
            if response.status_code < 500:
                return
            last = f"HTTP {response.status_code}"
        except Exception as exc:  # CI readiness loop only
            last = repr(exc)
        time.sleep(1)
    raise RuntimeError(f"service not ready: {url}; last={last}")


def main() -> None:
    wait(f"{FACTORY}/")
    wait(f"{ACADEMY}/api/")

    # Create a real Academy user through the public API, then promote only the CI
    # fixture row directly in the ephemeral Mongo database. The integration under
    # test starts after this fixture setup; no production bootstrap is bypassed.
    registered = request(
        "POST",
        f"{ACADEMY}/api/auth/register",
        json={
            "email": "runtime-smoke@academy.invalid",
            "password": "RuntimeSmoke-Only-2026",
            "display_name": "Runtime Smoke",
            "lang": "fr",
        },
    )
    academy_token = registered["token"]
    academy_user_id = registered["user"]["id"]
    mongo = MongoClient(MONGO_URL)
    result = mongo[ACADEMY_DB].users.update_one(
        {"id": academy_user_id}, {"$set": {"role": "founder"}}
    )
    if result.modified_count != 1:
        raise RuntimeError("failed to promote ephemeral Academy smoke user")

    # Create a real immutable authority policy and evaluate a real ALLOW decision.
    policy = request(
        "POST",
        f"{ACADEMY}/api/authority/policies/versions",
        token=academy_token,
        json={
            "policy_key": "CI_SECURITY_REMEDIATION_AUTHORITY",
            "version": "1.0.0",
            "title": "CI runtime remediation authority",
            "rules": [
                {
                    "id": "ALLOW-FOUNDER-REMEDIATION",
                    "priority": 1,
                    "effect": "ALLOW",
                    "reason": "Ephemeral CI founder may authorize one remediation smoke.",
                    "conditions": {
                        "actor_roles": ["founder"],
                        "actions": ["SECURITY_REMEDIATION_AUTHORIZE"],
                        "domains": ["SECURITY"],
                        "minimum_authority_level": "A4_CVL_AUTHORITY",
                    },
                }
            ],
            "effective_at": "2026-01-01T00:00:00+00:00",
            "doctrine_ref": "CI-RUNTIME-INTEGRATION-ONLY",
            "evidence_refs": ["CI-WORKFLOW-RUNTIME-SMOKE"],
        },
    )
    decision = request(
        "POST",
        f"{ACADEMY}/api/authority/evaluate",
        token=academy_token,
        json={
            "action": "SECURITY_REMEDIATION_AUTHORIZE",
            "context": {
                "domain": "SECURITY",
                "authority_level": "A4_CVL_AUTHORITY",
                "sensitivity": "HIGH",
            },
            "policy_version_id": policy["id"],
            "request_id": "CI-REMEDIATION-AUTHORITY-REQUEST",
        },
    )
    if decision["decision"] != "ALLOW":
        raise RuntimeError(f"authority decision is not ALLOW: {decision}")

    finding = request(
        "POST",
        f"{ACADEMY}/api/assurance/security/findings",
        token=academy_token,
        json={
            "title": "CI runtime cross-system authorization finding",
            "severity": "HIGH",
            "asset_id": None,
            "evidence_refs": ["CI-RUNTIME-EVIDENCE"],
            "remediation": "Route an authorized remediation through CVLN Agent Factory.",
        },
    )
    remediation = request(
        "POST",
        f"{ACADEMY}/api/security/remediations",
        token=academy_token,
        json={
            "finding_id": finding["id"],
            "title": "Sécurité autorisation Academy runtime",
            "proposed_change": "Vérifier la sécurité et l'autorisation du flux Academy.",
            "target_system": "CVLN_AGENT_FACTORY",
            "rollback_plan": "Annuler la mission CI et supprimer les données éphémères.",
            "test_plan": ["runtime_http_roundtrip", "remote_id_persistence"],
            "evidence_refs": [finding["id"], decision["id"]],
        },
    )
    request(
        "POST",
        f"{ACADEMY}/api/security/remediations/{remediation['id']}/authorize",
        token=academy_token,
        json={"authority_decision_ref": decision["id"]},
    )
    dispatched = request(
        "POST",
        f"{ACADEMY}/api/security/remediations/{remediation['id']}/dispatch",
        token=academy_token,
    )

    external = dispatched["external_dispatch"]
    if external["status"] != "CONFIRMED":
        raise RuntimeError(f"dispatch not fully confirmed: {external}")
    if not external["execution_dispatch_confirmed"]:
        raise RuntimeError("Agent Factory execution dispatch was not confirmed")
    if not external["operations_mirror_confirmed"]:
        raise RuntimeError("Command Center operations mirror was not confirmed")

    mission_id = external["results"]["agent_factory"]["remote_task_id"]
    task_id = external["results"]["command_center"]["remote_task_id"]
    if not mission_id or not task_id:
        raise RuntimeError("remote ids missing after confirmed dispatch")

    # Verify the exact objects through each remote system's own real API.
    missions = request("GET", f"{FACTORY}/missions", token=FACTORY_TOKEN)
    mission = next((m for m in missions if m.get("id") == mission_id), None)
    if not mission:
        raise RuntimeError(f"Agent Factory mission {mission_id} not found")
    if mission.get("origin_request") != remediation["id"]:
        raise RuntimeError("Agent Factory mission is not bound to the Academy remediation")

    task = request("GET", f"{COMMAND}/api/tasks/{task_id}", token=COMMAND_TOKEN)
    if task.get("id") != task_id:
        raise RuntimeError("Command Center task id mismatch")
    if remediation["id"] not in task.get("description", ""):
        raise RuntimeError("Command Center task is not bound to the Academy remediation")

    # Only after a real Agent Factory mission exists may Academy enter EXECUTING.
    executing = request(
        "PATCH",
        f"{ACADEMY}/api/security/remediations/{remediation['id']}",
        token=academy_token,
        json={"status": "EXECUTING", "evidence_refs": []},
    )
    if executing["status"] != "EXECUTING":
        raise RuntimeError("Academy remediation did not enter EXECUTING")

    print(
        "INTEGRATION_RUNTIME_VERIFIED "
        f"remediation={remediation['id']} mission={mission_id} command_task={task_id}"
    )


if __name__ == "__main__":
    main()
