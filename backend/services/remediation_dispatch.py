"""External dispatch adapters for Academy security remediation.

Contracts are grounded in the current CVLN repositories:

* Agent Factory (frekcore/CVLNAgentfactory, branch CVLN-AGENT-FACTORY):
  POST /missions/orchestrate then POST /missions. Mission creation is accepted only
  when the factory returns a real mission id. Its own service identity / gate model
  remains authoritative; Academy never bypasses it.
* Command Center (kimoune2025-a11y/Command-center, main):
  POST /api/tasks using an already-issued bearer token for an admin/manager account.
  Command Center is treated as the operations/visibility mirror, not as the code
  execution authority.

No adapter invents success. Missing configuration is reported explicitly, network or
contract errors are persisted by the caller as failed/partial dispatch evidence.
"""

from __future__ import annotations

import os
from typing import Any, Dict

import httpx


class DispatchNotConfigured(RuntimeError):
    pass


class DispatchRejected(RuntimeError):
    pass


def _url(name: str) -> str:
    value = (os.environ.get(name) or "").strip().rstrip("/")
    if not value:
        raise DispatchNotConfigured(f"{name} is not configured")
    return value


def _token(*names: str) -> str:
    for name in names:
        value = (os.environ.get(name) or "").strip()
        if value:
            return value
    raise DispatchNotConfigured(f"one of {', '.join(names)} is required")


async def _post_json(
    url: str,
    *,
    token: str,
    payload: Dict[str, Any],
    timeout: float = 10.0,
) -> Dict[str, Any]:
    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.post(
                url,
                json=payload,
                headers={"Authorization": f"Bearer {token}"},
            )
    except httpx.HTTPError as exc:
        raise DispatchRejected(
            f"network error calling {url}: {type(exc).__name__}"
        ) from exc
    if response.status_code >= 400:
        raise DispatchRejected(f"remote rejected request: HTTP {response.status_code}")
    try:
        data = response.json()
    except ValueError as exc:
        raise DispatchRejected("remote returned non-JSON response") from exc
    if not isinstance(data, dict):
        raise DispatchRejected("remote returned unexpected response shape")
    return data


async def dispatch_to_agent_factory(remediation: Dict[str, Any]) -> Dict[str, Any]:
    """Create a real Agent Factory mission for an already-authorized remediation."""
    base = _url("CVLN_AGENT_FACTORY_URL")
    token = _token("CVLN_AGENT_FACTORY_SERVICE_TOKEN", "CVLN_AGENT_FACTORY_API_KEY")

    request_text = (
        f"[CVLN Academy remediation {remediation['id']}] {remediation['title']}. "
        f"Implement: {remediation['proposed_change']}. "
        f"Rollback: {remediation['rollback_plan']}. "
        f"Tests required: {', '.join(remediation.get('test_plan', []))}."
    )
    orchestrated = await _post_json(
        f"{base}/missions/orchestrate",
        token=token,
        payload={"request_text": request_text, "entity": "CVLN Academy"},
    )
    agents = [
        row.get("agent_id")
        for row in orchestrated.get("recommended_agents", [])
        if isinstance(row, dict) and row.get("agent_id")
    ]
    if not agents:
        draft = orchestrated.get("draft_mission") or {}
        agents = [a for a in draft.get("agent_ids", []) if a]
    if not agents:
        raise DispatchRejected("Agent Factory returned no eligible remediation agent")

    mission = await _post_json(
        f"{base}/missions",
        token=token,
        payload={
            "title": f"[Academy remediation] {remediation['title']}",
            "objective": request_text,
            "entity": "CVLN Academy",
            "agent_ids": agents[:2],
            "autonomy_level": 2,
            "expected_results": [
                "implementation evidence",
                "tests executed",
                "security regression result",
                "rollback evidence if required",
            ],
            "mission_type": "application",
            "origin_request": remediation["id"],
        },
    )
    mission_id = str(mission.get("id") or "").strip()
    if not mission_id:
        raise DispatchRejected("Agent Factory mission response missing id")
    return {
        "target": "CVLN_AGENT_FACTORY",
        "status": "DISPATCHED_CONFIRMED",
        "remote_task_id": mission_id,
        "remote_kind": "mission",
        "agent_ids": mission.get("agent_ids", agents[:2]),
        "workflow_stage": mission.get("workflow_stage"),
    }


async def mirror_to_command_center(remediation: Dict[str, Any]) -> Dict[str, Any]:
    """Create a real Command Center tracking task."""
    base = _url("CVLN_COMMAND_CENTER_URL")
    token = _token("CVLN_COMMAND_CENTER_ACCESS_TOKEN", "CVLN_COMMAND_CENTER_API_KEY")
    task = await _post_json(
        f"{base}/api/tasks",
        token=token,
        payload={
            "title": f"[Academy remediation] {remediation['title']}",
            "description": (
                f"Academy remediation {remediation['id']}\n"
                f"Target system: {remediation['target_system']}\n"
                f"Change: {remediation['proposed_change']}\n"
                f"Rollback: {remediation['rollback_plan']}"
            ),
            "priority": "high",
            "status": "todo",
            "deadline": None,
            "assigned_to": None,
            "project_id": None,
        },
    )
    task_id = str(task.get("id") or "").strip()
    if not task_id:
        raise DispatchRejected("Command Center task response missing id")
    return {
        "target": "CVLN_COMMAND_CENTER",
        "status": "DISPATCHED_CONFIRMED",
        "remote_task_id": task_id,
        "remote_kind": "task",
    }


async def dispatch_remediation(remediation: Dict[str, Any]) -> Dict[str, Any]:
    """Dispatch execution to Agent Factory and mirror control to Command Center."""
    results: Dict[str, Any] = {}

    try:
        results["agent_factory"] = await dispatch_to_agent_factory(remediation)
    except DispatchNotConfigured as exc:
        results["agent_factory"] = {"status": "NOT_CONFIGURED", "error": str(exc)}
    except DispatchRejected as exc:
        results["agent_factory"] = {"status": "FAILED", "error": str(exc)}

    try:
        results["command_center"] = await mirror_to_command_center(remediation)
    except DispatchNotConfigured as exc:
        results["command_center"] = {"status": "NOT_CONFIGURED", "error": str(exc)}
    except DispatchRejected as exc:
        results["command_center"] = {"status": "FAILED", "error": str(exc)}

    execution_ok = results["agent_factory"].get("status") == "DISPATCHED_CONFIRMED"
    mirror_ok = results["command_center"].get("status") == "DISPATCHED_CONFIRMED"
    overall = (
        "CONFIRMED"
        if execution_ok and mirror_ok
        else "PARTIAL"
        if execution_ok
        else "FAILED"
    )
    return {
        "status": overall,
        "execution_dispatch_confirmed": execution_ok,
        "operations_mirror_confirmed": mirror_ok,
        "results": results,
    }
