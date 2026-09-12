"""CVLN Academy expert directory.

Registry shared by MCP/LLM adapters. Keep expert definitions declarative so
ChatGPT, Claude, Gemini and future clients can discover the same capabilities
without duplicating business logic.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional


EXPERTS: List[Dict[str, Any]] = [
    {
        "id": "orientation",
        "name": "Orientation",
        "description": "Clarifie un objectif, un métier cible et un parcours de montée en compétences.",
        "domains": ["orientation", "reconversion", "competences", "metiers"],
        "tools": ["search_formations", "get_formation"],
        "status": "active",
    },
    {
        "id": "formation",
        "name": "Formation",
        "description": "Explore le catalogue publié, les programmes, prérequis, formats et durées.",
        "domains": ["formations", "programmes", "prerequis", "parcours"],
        "tools": ["list_poles", "search_formations", "get_formation"],
        "status": "active",
    },
    {
        "id": "funding",
        "name": "Financement",
        "description": (
            "Prépare et suit des dossiers de financement Academy avec capacités "
            "institutionnelles vérifiées, sans inventer d'éligibilité ni de soumission externe."
        ),
        "domains": ["financement", "afdas", "france-travail", "cpf", "aides"],
        "tools": [
            "list_funding_connectors",
            "create_funding_dossier",
            "get_my_funding_dossier",
            "add_funding_document_reference",
            "mark_funding_dossier_ready",
            "list_my_funding_dossiers",
        ],
        "status": "active",
        "access": "private_oauth",
        "guardrail": (
            "Une préparation de dossier n'est jamais présentée comme une approbation, "
            "une éligibilité certaine ou une soumission institutionnelle."
        ),
    },
    {
        "id": "career",
        "name": "Career",
        "description": "Relie compétences, métiers cibles, écarts de niveau et prochaines étapes professionnelles.",
        "domains": ["carriere", "emploi", "competences", "metiers"],
        "tools": ["search_formations", "get_formation"],
        "status": "active",
    },
    {
        "id": "music",
        "name": "Music",
        "description": "Expertise Academy autour de la production musicale, MAO, studio et music business.",
        "domains": ["musique", "mao", "studio", "music-business", "publishing"],
        "tools": ["search_formations", "get_formation"],
        "status": "active",
    },
    {
        "id": "cinema-av",
        "name": "Cinema & Audiovisuel",
        "description": "Expertise Academy autour de la réalisation, production, montage, image et son.",
        "domains": ["cinema", "audiovisuel", "realisation", "montage", "image", "son"],
        "tools": ["search_formations", "get_formation"],
        "status": "active",
    },
    {
        "id": "tech-ai",
        "name": "Tech & AI",
        "description": "Parcours numériques et IA appliqués aux industries créatives.",
        "domains": ["ia", "tech", "numerique", "automatisation"],
        "tools": ["search_formations", "get_formation"],
        "status": "active",
    },
    {
        "id": "caribbean-overseas",
        "name": "Caribbean / Overseas",
        "description": "Contexte Outre-mer/Caraïbes, opportunités et contraintes territoriales de formation.",
        "domains": ["outre-mer", "caraibes", "territoires", "mobilite"],
        "tools": ["search_formations", "get_formation"],
        "status": "active",
    },
    {
        "id": "tutor",
        "name": "Tutor",
        "description": "Accompagnement pédagogique, explications, exercices et progression.",
        "domains": ["cours", "tutorat", "exercices", "progression"],
        "tools": [],
        "status": "planned",
    },
    {
        "id": "assessment",
        "name": "Assessment",
        "description": "Évaluation de niveau, compétences acquises et lacunes.",
        "domains": ["evaluation", "niveau", "competences", "quiz"],
        "tools": [],
        "status": "planned",
    },
    {
        "id": "certification",
        "name": "Certification",
        "description": "Attestations, badges, preuves et statut de certification.",
        "domains": ["certification", "badge", "attestation", "preuve"],
        "tools": [],
        "status": "planned",
    },
    {
        "id": "institution",
        "name": "Institution",
        "description": "Interface de compréhension des parcours pour financeurs, organismes et entreprises.",
        "domains": ["institution", "financeur", "organisme", "entreprise"],
        "tools": [],
        "status": "planned",
    },
    {
        "id": "trainer",
        "name": "Trainer",
        "description": "Support aux formateurs pour le suivi et l'animation pédagogique.",
        "domains": ["formateur", "pedagogie", "suivi", "animation"],
        "tools": [],
        "status": "planned",
    },
    {
        "id": "support",
        "name": "Support",
        "description": "Aide, incidents, tickets et réclamations Academy.",
        "domains": ["support", "incident", "ticket", "reclamation"],
        "tools": [],
        "status": "planned",
    },
    {
        "id": "laurentia",
        "name": "Laurentia",
        "description": "Orchestration des experts Academy et escalade vers les capacités autorisées.",
        "domains": ["orchestration", "routing", "coordination"],
        "tools": ["academy_capabilities", "list_experts", "route_expert"],
        "status": "active",
    },
]


def list_experts(status: Optional[str] = None) -> List[Dict[str, Any]]:
    """Return a stable, optionally status-filtered expert registry."""
    if not status:
        return EXPERTS
    normalized = status.strip().lower()
    return [expert for expert in EXPERTS if expert["status"] == normalized]


def get_expert(expert_id: str) -> Optional[Dict[str, Any]]:
    """Find one expert by stable id."""
    normalized = expert_id.strip().lower()
    return next((expert for expert in EXPERTS if expert["id"] == normalized), None)


def route_experts(intent: str, limit: int = 3) -> List[Dict[str, Any]]:
    """Deterministically rank experts from intent text.

    This router is deliberately transparent and side-effect free. It does not
    pretend to be semantic AI routing; future embeddings/LLM routing can sit
    behind the same contract once tested.
    """
    tokens = {
        token
        for token in intent.lower().replace("/", " ").replace("-", " ").split()
        if token
    }
    scored = []
    for expert in EXPERTS:
        haystack = " ".join(
            [expert["id"], expert["name"], expert["description"], *expert["domains"]]
        ).lower().replace("-", " ")
        score = sum(1 for token in tokens if token in haystack)
        if score:
            scored.append((score, expert["id"], expert))

    scored.sort(key=lambda item: (-item[0], item[1]))
    return [expert for _, _, expert in scored[: max(1, min(int(limit), 5))]]
