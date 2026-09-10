"""License Entitlement / Tenant Policy boundary (XCP-007 / GOV-012).

A licensee receives only an explicit capability surface. Internal CVL doctrine,
policy implementation, evidence internals and other tenant state are never returned
through the entitlement view. Entitlements are versioned through XCP-008.
"""

from __future__ import annotations

import uuid
from typing import Any, Dict, Iterable, Optional

from db import db, utc_now_iso
from services import policy_registry
from services import professional_governance as governance


def _id(prefix: str) -> str:
    return f"{prefix}-{uuid.uuid4()}"


def _refs(values: Iterable[str]) -> list[str]:
    return list(dict.fromkeys(str(v).strip() for v in values if str(v).strip()))


async def register_tenant(
    *,
    actor_id: str,
    tenant_key: str,
    display_name: str,
    owner_ref: str,
    evidence_refs: Iterable[str],
) -> Dict[str, Any]:
    refs = _refs(evidence_refs)
    key = tenant_key.strip().upper()
    if not key or not display_name.strip() or not owner_ref.strip() or not refs:
        raise ValueError("tenant requires key, display_name, owner_ref and evidence")
    existing = await db.license_tenants.find_one({"tenant_key": key}, {"_id": 0})
    if existing:
        return existing
    row = {
        "id": _id("TENANT"),
        "tenant_key": key,
        "display_name": display_name.strip(),
        "owner_ref": owner_ref.strip(),
        "evidence_refs": refs,
        "status": "ACTIVE",
        "created_by": actor_id,
        "created_at": utc_now_iso(),
    }
    await db.license_tenants.insert_one(dict(row))
    await governance.audit_event(
        event_type="license.tenant.registered",
        actor_id=actor_id,
        resource_type="license_tenant",
        resource_id=row["id"],
        payload={"tenant_key": key, "evidence_refs": refs},
    )
    return row


async def register_entitlement_version(
    *,
    actor_id: str,
    tenant_id: str,
    version: str,
    effective_at: str,
    capabilities: Iterable[str],
    public_constraints: Optional[Dict[str, Any]],
    evidence_refs: Iterable[str],
    supersedes_version_id: Optional[str] = None,
) -> Dict[str, Any]:
    tenant = await db.license_tenants.find_one({"id": tenant_id, "status": "ACTIVE"}, {"_id": 0})
    if not tenant:
        raise LookupError("active license tenant not found")
    refs = _refs(evidence_refs)
    caps = sorted({str(v).strip().upper() for v in capabilities if str(v).strip()})
    if not caps or not refs:
        raise ValueError("entitlement requires capabilities and evidence")
    policy = await policy_registry.register_version(
        actor_id=actor_id,
        policy_key=f"LICENSE_ENTITLEMENT::{tenant['tenant_key']}",
        version=version,
        kind="POLICY",
        title=f"License entitlement — {tenant['display_name']}",
        content={
            "tenant_id": tenant_id,
            "capabilities": caps,
            "public_constraints": public_constraints or {},
            "internal_doctrine_exposed": False,
        },
        effective_at=effective_at,
        evidence_refs=refs,
        supersedes_version_id=supersedes_version_id,
    )
    projection = {
        "id": f"ENT::{tenant_id}",
        "tenant_id": tenant_id,
        "tenant_key": tenant["tenant_key"],
        "capabilities": caps,
        "public_constraints": public_constraints or {},
        "policy_version_id": policy["id"],
        "policy_hash": policy["content_hash"],
        "effective_at": policy["effective_at"],
        "status": "ACTIVE",
        "updated_by": actor_id,
        "updated_at": utc_now_iso(),
    }
    await db.license_entitlements.update_one(
        {"tenant_id": tenant_id}, {"$set": projection}, upsert=True
    )
    return {**projection, "governance_policy": policy}


async def entitlement_view(tenant_id: str) -> Dict[str, Any]:
    tenant = await db.license_tenants.find_one({"id": tenant_id, "status": "ACTIVE"}, {"_id": 0})
    entitlement = await db.license_entitlements.find_one(
        {"tenant_id": tenant_id, "status": "ACTIVE"}, {"_id": 0}
    )
    if not tenant or not entitlement:
        raise LookupError("active tenant entitlement not found")
    policy = await policy_registry.require_effective_version(entitlement["policy_version_id"])
    if policy["content_hash"] != entitlement.get("policy_hash"):
        raise ValueError("license entitlement projection integrity check failed")
    return {
        "tenant_id": tenant_id,
        "tenant_key": tenant["tenant_key"],
        "display_name": tenant["display_name"],
        "capabilities": list(entitlement["capabilities"]),
        "constraints": dict(entitlement.get("public_constraints") or {}),
        "effective_at": entitlement["effective_at"],
        "entitlement_version": policy["version"],
        "internal_doctrine": None,
        "internal_policy_content": None,
        "evidence_refs": None,
    }


async def require_capability(tenant_id: str, capability: str) -> Dict[str, Any]:
    view = await entitlement_view(tenant_id)
    target = capability.strip().upper()
    if target not in view["capabilities"]:
        raise PermissionError("tenant is not entitled to capability")
    return {"tenant_id": tenant_id, "capability": target, "entitled": True}
