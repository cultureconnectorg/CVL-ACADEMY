"""CVLN Academy Model Context Protocol (MCP) server.

This module exposes the public Academy catalogue and expert-directory metadata
to LLM/MCP clients without creating a second business-logic stack. Tools read
the same MongoDB collections used by the FastAPI API and only return published
or explicitly public data.
"""

from __future__ import annotations

import json
import os
import re
from typing import Any, Dict, List, Optional

from mcp.server import MCPServer
from mcp.server.transport_security import TransportSecuritySettings

import fms_canonical
import frk_canonical
import klt_canonical
import kor_canonical
from db import db
from expert_directory import (
    get_expert as directory_get_expert,
    list_experts as directory_list_experts,
    route_experts as directory_route_experts,
)
from pricing_catalog import formation_commercialization
from services.canonical_convergence import (
    CANONICAL_ROUTE_PREFIX,
    get_canonical_authority_map,
)


academy_mcp = MCPServer(
    "CVLN Academy",
    instructions=(
        "CVLN Academy is an expert learning and career capability. Use the Expert "
        "Directory to identify the right domain, then use published Academy data to "
        "answer. Prefer search_formations before get_formation when the user has not "
        "supplied an exact formation code. Formations returned with "
        "pedagogical_source starting with CANONICAL are the current, authoritative "
        "curriculum (FMS/KLT/KOR/FRK); pedagogical_source LEGACY means no canonical "
        "build exists yet for that formation_code — present it as such, never as "
        "canonical-verified. Never infer unpublished programmes, funding "
        "eligibility, certifications or user state from missing results. Planned experts "
        "describe target capabilities only and must not be presented as implemented."
    ),
)


def _clean_limit(limit: int, maximum: int = 50) -> int:
    return max(1, min(int(limit), maximum))


def _public_summary(doc: Dict[str, Any]) -> Dict[str, Any]:
    """Return the same public catalogue shape exposed by the REST API."""
    return {
        "code": doc.get("code"),
        "name": doc.get("name"),
        "pole": doc.get("pole"),
        "pole_name": doc.get("pole_name"),
        "duration_h": doc.get("duration_h"),
        "stades": doc.get("stades", []),
        "cc": doc.get("cc"),
        "badge_name": doc.get("badge_name"),
        "description": doc.get("description", ""),
        "contexts": doc.get("contexts", []),
        "audience_levels": doc.get("audience_levels", []),
        "bridge_entities": doc.get("bridge_entities", []),
        "positioning_note": doc.get("positioning_note", ""),
        "primary_job": (doc.get("cartography") or {}).get("primary_job"),
        "delivery_formats": (doc.get("cartography") or {}).get(
            "delivery_formats", []
        ),
        "market_job_title": doc.get("market_job_title"),
        "calibration_confidence": doc.get("calibration_confidence"),
        "calibration_date": doc.get("calibration_date"),
        "modules_count": len(doc.get("modules", [])),
        "commercialization": formation_commercialization(doc),
    }


@academy_mcp.tool()
async def academy_capabilities() -> Dict[str, Any]:
    """Describe what the CVLN Academy MCP endpoint currently exposes."""
    active_experts = directory_list_experts(status="active")
    return {
        "name": "CVLN Academy",
        "mode": "public-read-only",
        "protocol": "MCP",
        "distribution": {
            "primary": "MCP-capable assistants",
            "compatible_targets": ["ChatGPT", "Claude", "Gemini", "other MCP clients"],
            "note": (
                "Client availability depends on each provider's connector/app review "
                "and configuration."
            ),
        },
        "domains": [
            "expert_directory",
            "formations",
            "poles",
            "pricing",
            "programme_details",
        ],
        "active_experts": [expert["id"] for expert in active_experts],
        "privacy": (
            "Only published catalogue data and public expert metadata are exposed. "
            "User progress, wallet, identity and admin data are not exposed by this MCP surface."
        ),
    }


@academy_mcp.tool()
async def list_experts(status: Optional[str] = None) -> Dict[str, Any]:
    """List CVLN Academy experts and whether each capability is active or planned."""
    items = directory_list_experts(status=status)
    return {"count": len(items), "items": items}


@academy_mcp.tool()
async def get_expert(expert_id: str) -> Dict[str, Any]:
    """Return one Expert Directory entry by stable expert id."""
    expert = directory_get_expert(expert_id)
    if not expert:
        return {"found": False, "expert_id": expert_id.strip().lower()}
    return {"found": True, "expert": expert}


@academy_mcp.tool()
async def route_expert(intent: str, limit: int = 3) -> Dict[str, Any]:
    """Route a user intent to the most relevant Academy experts transparently."""
    matches = directory_route_experts(intent, limit=limit)
    return {
        "intent": intent,
        "count": len(matches),
        "experts": matches,
        "routing": "deterministic-keyword-v1",
        "warning": (
            "A planned expert is not an implemented business capability. "
            "Use its status before invoking downstream actions."
        ),
    }


@academy_mcp.tool()
async def list_poles(limit: int = 50) -> Dict[str, Any]:
    """List Academy training poles available in the public catalogue."""
    safe_limit = _clean_limit(limit)
    poles = await db.poles.find({}, {"_id": 0}).limit(safe_limit).to_list(safe_limit)
    return {"count": len(poles), "items": poles}


def _text_matches(query: Optional[str], *fields: Optional[str]) -> bool:
    if not query:
        return True
    needle = query.strip().lower()
    return any(needle in (field or "").lower() for field in fields)


async def _canonical_fms_items(query: Optional[str]) -> List[Dict[str, Any]]:
    formations = await fms_canonical.list_canonical_formations()
    return [
        {
            "pedagogical_source": "CANONICAL",
            "domain": "FMS",
            "code": f.canonical_formation_code,
            "name": f.metier_name,
            "modules_count": f.module_count,
            "route": f"{CANONICAL_ROUTE_PREFIX['FMS']}/{f.canonical_formation_code}",
        }
        for f in formations
        if _text_matches(query, f.canonical_formation_code, f.metier_name)
    ]


async def _canonical_klt_items(query: Optional[str]) -> List[Dict[str, Any]]:
    formations = await klt_canonical.list_canonical_klt_formations()
    return [
        {
            "pedagogical_source": "CANONICAL_KLT",
            "domain": "KLT",
            "code": f.klt_formation_code,
            "name": f.title,
            "modules_count": f.module_count,
            "contexts": f.contexts,
            "route": f"{CANONICAL_ROUTE_PREFIX['KLT']}/{f.klt_formation_code}",
        }
        for f in formations
        if _text_matches(query, f.klt_formation_code, f.title, *f.contexts)
    ]


async def _canonical_kor_items(query: Optional[str]) -> List[Dict[str, Any]]:
    formations = await kor_canonical.list_canonical_kor_formations()
    return [
        {
            "pedagogical_source": "CANONICAL_KOR",
            "domain": "KOR",
            "code": f.kor_formation_code,
            "name": f.title,
            "modules_count": f.module_count,
            "contexts": f.contexts,
            "route": f"{CANONICAL_ROUTE_PREFIX['KOR']}/{f.kor_formation_code}",
        }
        for f in formations
        if _text_matches(query, f.kor_formation_code, f.title, *f.contexts)
    ]


async def _canonical_frk_items(query: Optional[str]) -> List[Dict[str, Any]]:
    formations = await frk_canonical.list_canonical_frk_formations()
    # FRK codes (FRK-01..75) never collide with legacy or the other three
    # canonical domains' codes — additive only, no authority-map dedup
    # needed for this domain (see services/canonical_convergence.py).
    return [
        {
            "pedagogical_source": "CANONICAL_FRK",
            "domain": "FRK",
            "code": f.frk_formation_code,
            "name": f.title,
            "modules_count": f.module_count,
            "route": f"{CANONICAL_ROUTE_PREFIX['FRK']}/{f.frk_formation_code}",
        }
        for f in formations
        if _text_matches(query, f.frk_formation_code, f.title, f.objectives)
    ]


async def _canonical_catalogue_items(query: Optional[str]) -> List[Dict[str, Any]]:
    """All real canonical formations (FMS/KLT/KOR/FRK) matching `query`.

    Reuses the exact same read functions and authority routing
    (`services.canonical_convergence`) the rest of the app already runs
    on — CANONICAL_CURRICULUM_RUNTIME=AUTHORITATIVE (Founder decision,
    ACA-0019) applies identically to the MCP surface, never a second,
    independently-invented ranking.
    """
    fms, klt, kor, frk = (
        await _canonical_fms_items(query),
        await _canonical_klt_items(query),
        await _canonical_kor_items(query),
        await _canonical_frk_items(query),
    )
    return fms + klt + kor + frk


@academy_mcp.tool()
async def search_formations(
    query: Optional[str] = None,
    pole: Optional[str] = None,
    limit: int = 20,
) -> Dict[str, Any]:
    """Search Academy formations by text and/or pole. Canonical FMS/KLT/KOR/FRK
    content (CANONICAL_CURRICULUM_RUNTIME=AUTHORITATIVE) is searched first;
    a legacy catalogue entry is only returned when no canonical formation
    has replaced it — never both for the same formation_code."""
    safe_limit = _clean_limit(limit)
    authority_map = await get_canonical_authority_map()

    canonical_items = await _canonical_catalogue_items(query)
    if pole:
        canonical_items = [
            item for item in canonical_items if item["domain"].lower() == pole.strip().lower()
        ]

    mongo_filter: Dict[str, Any] = {"content_status": "published"}

    if pole:
        mongo_filter["$or"] = [
            {"pole": {"$regex": f"^{re.escape(pole)}$", "$options": "i"}},
            {"pole_name": {"$regex": re.escape(pole), "$options": "i"}},
        ]

    if query:
        text_filter = {
            "$or": [
                {"code": {"$regex": re.escape(query), "$options": "i"}},
                {"name": {"$regex": re.escape(query), "$options": "i"}},
                {"description": {"$regex": re.escape(query), "$options": "i"}},
                {"market_job_title": {"$regex": re.escape(query), "$options": "i"}},
                {
                    "cartography.primary_job": {
                        "$regex": re.escape(query),
                        "$options": "i",
                    }
                },
            ]
        }
        if "$or" in mongo_filter:
            pole_filter = {"$or": mongo_filter.pop("$or")}
            mongo_filter["$and"] = [pole_filter, text_filter]
        else:
            mongo_filter.update(text_filter)

    legacy_docs = (
        await db.formations.find(mongo_filter, {"_id": 0})
        .limit(safe_limit)
        .to_list(safe_limit)
    )
    legacy_items = [
        {**_public_summary(doc), "pedagogical_source": "LEGACY"}
        for doc in legacy_docs
        if doc.get("code") not in authority_map
    ]

    items = (canonical_items + legacy_items)[:safe_limit]
    return {"count": len(items), "items": items}


async def _canonical_authority_detail(domain: str, code: str) -> Optional[Dict[str, Any]]:
    finders = {
        "FMS": _canonical_fms_items,
        "KLT": _canonical_klt_items,
        "KOR": _canonical_kor_items,
        "FRK": _canonical_frk_items,
    }
    finder = finders.get(domain)
    if not finder:
        return None
    items = await finder(None)
    return next((item for item in items if item["code"] == code), None)


@academy_mcp.tool()
async def get_formation(code: str) -> Dict[str, Any]:
    """Return one Academy formation, including modules and commercialisation.
    When `code` has real canonical content (FMS/KLT/KOR), the canonical
    formation is returned instead of the legacy catalogue entry at the same
    code — the legacy doc is never returned bare for a superseded code."""
    normalized = code.strip()

    authority_map = await get_canonical_authority_map()
    authority = authority_map.get(normalized)
    if authority:
        canonical = await _canonical_authority_detail(authority["domain"], normalized)
        if canonical:
            return {"found": True, "formation": canonical}

    for finder in (
        _canonical_fms_items,
        _canonical_klt_items,
        _canonical_kor_items,
        _canonical_frk_items,
    ):
        items = await finder(None)
        match = next((item for item in items if item["code"] == normalized), None)
        if match:
            return {"found": True, "formation": match}

    doc = await db.formations.find_one(
        {"code": normalized, "content_status": "published"}, {"_id": 0}
    )
    if not doc:
        return {"found": False, "code": normalized}

    doc["commercialization"] = formation_commercialization(doc)
    doc["pedagogical_source"] = "LEGACY"
    return {"found": True, "formation": doc}


@academy_mcp.resource("academy://about")
def academy_about() -> str:
    """Stable machine-readable description of the Academy MCP surface."""
    return json.dumps(
        {
            "name": "CVLN Academy",
            "resource": "academy://about",
            "access": "public-read-only",
            "endpoint": "/mcp",
            "purpose": (
                "Expose Academy expert discovery and published catalogue "
                "capabilities to MCP-capable assistants."
            ),
        },
        ensure_ascii=False,
    )


@academy_mcp.resource("academy://experts")
def experts_resource() -> str:
    """Read the complete public Expert Directory as JSON."""
    return json.dumps(
        {"count": len(directory_list_experts()), "items": directory_list_experts()},
        ensure_ascii=False,
    )


@academy_mcp.resource("academy://formations/{code}")
async def formation_resource(code: str) -> str:
    """Read one published formation as a JSON MCP resource."""
    result = await get_formation(code)
    return json.dumps(result, ensure_ascii=False, default=str)


@academy_mcp.prompt()
def recommend_training(goal: str, level: str = "non précisé") -> str:
    """Prompt template for selecting a CVLN Academy formation responsibly."""
    return (
        "Tu aides un utilisateur à choisir une formation CVLN Academy. "
        f"Objectif: {goal}. Niveau: {level}. "
        "Commence par appeler route_expert puis search_formations avec des mots-clés précis. "
        "Pour chaque résultat pertinent, appelle get_formation avant de recommander. "
        "N'invente jamais une formation absente du catalogue publié et distingue "
        "clairement les informations du catalogue de tes conseils."
    )


@academy_mcp.prompt()
def academy_expert_assist(request: str) -> str:
    """General Expert Directory orchestration prompt for LLM clients."""
    return (
        "Tu utilises CVLN Academy comme système expert. "
        f"Demande utilisateur: {request}. "
        "1) appelle route_expert; 2) vérifie le statut des experts proposés; "
        "3) n'utilise que les tools réellement déclarés pour les experts actifs; "
        "4) sépare les faits Academy vérifiés des conseils généraux; "
        "5) si une capacité est planned, explique qu'elle n'est pas encore disponible "
        "au lieu de simuler son résultat."
    )


def build_transport_security() -> Optional[TransportSecuritySettings]:
    """Build production-safe MCP Host/Origin allowlists from environment variables."""
    raw_hosts = os.environ.get("MCP_ALLOWED_HOSTS", "")
    hosts: List[str] = [item.strip() for item in raw_hosts.split(",") if item.strip()]

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


mcp_http_app = academy_mcp.streamable_http_app(
    streamable_http_path="/",
    transport_security=build_transport_security(),
)
