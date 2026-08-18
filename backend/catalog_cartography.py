"""Catalogue cartography derived from the current CVLN Academy seed.

This file does not create new pedagogical content. It makes the existing catalogue
queryable for the August 2026 recalibration work: métiers, contexts, audiences,
activities, evidence, bridge entities, economics placeholders, and calibration gaps.
"""
from __future__ import annotations

from copy import deepcopy
from typing import Any

CALIBRATION_SOURCES = [
    "France Travail / ROME",
    "France compétences",
    "Marché réel",
    "Formation existante",
    "Financement",
    "Qualiopi",
]

DELIVERY_FORMATS = ["E_LEARNING", "PRESENTIEL", "HYBRIDE"]
DEFAULT_FORMAT = ["E_LEARNING"]
PRO_FORMAT = ["E_LEARNING", "PRESENTIEL", "HYBRIDE"]

_FORMATION_CARTOGRAPHY: dict[str, dict[str, Any]] = {
    "FMS-01": {"primary_job": "Artiste interprète / artiste entrepreneur", "secondary_jobs": ["Auteur-compositeur", "Performer", "Porteur de projet artistique"], "contexts": ["INTERNAL", "EXTERNAL", "BRIDGE"], "audience": ["DEBUTANT", "INTERMEDIAIRE", "AVANCE"], "level": "fondamentaux à professionnalisation", "meta_entities": ["FMS"], "bridges": ["showcase FMS", "développement catalogue", "signature ou résidence à qualifier"], "delivery_formats": PRO_FORMAT, "price_current_eur": None},
    "FMS-02": {"primary_job": "Chargé de production / label manager musique", "secondary_jobs": ["A&R", "Coordinateur distribution", "Responsable export musical"], "contexts": ["EXTERNAL", "BRIDGE"], "audience": ["INTERMEDIAIRE", "AVANCE", "PROFESSIONNEL"], "level": "professionnalisation", "meta_entities": ["LabelOS", "FMS", "KORA"], "bridges": ["audit catalogue LabelOS", "coordination sortie FMS", "production KORA"], "delivery_formats": PRO_FORMAT, "price_current_eur": 1400},
    "FMS-03": {"primary_job": "Beatmaker / producteur musical", "secondary_jobs": ["Sound designer", "Producteur catalogue", "Arrangeur home studio"], "contexts": ["EXTERNAL", "BRIDGE"], "audience": ["DEBUTANT", "INTERMEDIAIRE"], "level": "fondamentaux à opérationnel", "meta_entities": ["FMS", "KORA"], "bridges": ["placements catalogue", "production capsule sonore", "collaboration artiste"], "delivery_formats": PRO_FORMAT, "price_current_eur": None},
    "FMS-04": {"primary_job": "Brand manager artiste", "secondary_jobs": ["Directeur artistique", "Designer d'identité artistique", "Conseil image artiste"], "contexts": ["EXTERNAL", "BRIDGE"], "audience": ["INTERMEDIAIRE", "PROFESSIONNEL"], "level": "professionnalisation", "meta_entities": ["FMS", "LabelOS"], "bridges": ["kit presse", "branding sortie", "identité visuelle catalogue"], "delivery_formats": PRO_FORMAT, "price_current_eur": None},
    "FMS-05": {"primary_job": "Manager d'artiste", "secondary_jobs": ["Tour manager", "Coordinateur artistique", "Agent de développement"], "contexts": ["EXTERNAL", "BRIDGE"], "audience": ["INTERMEDIAIRE", "AVANCE", "PROFESSIONNEL"], "level": "professionnalisation", "meta_entities": ["FMS", "Good Mood", "LabelOS"], "bridges": ["management artiste FMS", "coordination live", "suivi budget artiste"], "delivery_formats": PRO_FORMAT, "price_current_eur": None},
    "FMS-06": {"primary_job": "Producteur exécutif culturel", "secondary_jobs": ["Senior A&R", "Directeur artistique", "Responsable investissement projet"], "contexts": ["INTERNAL", "EXTERNAL", "BRIDGE"], "audience": ["AVANCE", "PROFESSIONNEL"], "level": "avancé", "meta_entities": ["FMS", "CVL Group", "LabelOS"], "bridges": ["sélection projets", "développement roster", "pilotage investissement"], "delivery_formats": PRO_FORMAT, "price_current_eur": None},
    "KOR-01": {"primary_job": "Producteur podcast", "secondary_jobs": ["Animateur podcast", "Réalisateur audio", "Éditeur audio"], "contexts": ["EXTERNAL", "BRIDGE"], "audience": ["DEBUTANT", "INTERMEDIAIRE"], "level": "opérationnel", "meta_entities": ["KORA"], "bridges": ["production KORA", "capsules diaspora", "série éditoriale"], "delivery_formats": PRO_FORMAT, "price_current_eur": None},
    "KOR-02": {"primary_job": "Journaliste culturel / storyteller média", "secondary_jobs": ["Animateur culturel", "Rédacteur éditorial", "Producteur broadcast"], "contexts": ["EXTERNAL", "BRIDGE"], "audience": ["INTERMEDIAIRE", "PROFESSIONNEL"], "level": "professionnalisation", "meta_entities": ["KORA", "Kiltikonet"], "bridges": ["storytelling KORA", "reportage culturel", "chronique diaspora"], "delivery_formats": PRO_FORMAT, "price_current_eur": None},
    "GMD-01": {"primary_job": "Producteur événementiel / festival", "secondary_jobs": ["Coordinateur événement", "Régisseur production", "Responsable opérations festival"], "contexts": ["INTERNAL", "EXTERNAL", "BRIDGE"], "audience": ["DEBUTANT", "INTERMEDIAIRE", "PROFESSIONNEL"], "level": "opérationnel", "meta_entities": ["Good Mood", "DJ SAYD", "CVL Group"], "bridges": ["coordination CC2026/CC2027", "production événement CVLN", "missions opérations"], "delivery_formats": PRO_FORMAT, "price_current_eur": None},
    "SAY-01": {"primary_job": "Leader culturel / personal brand", "secondary_jobs": ["Ambassadeur diaspora", "Porte-parole culturel", "Responsable communauté"], "contexts": ["INTERNAL", "EXTERNAL", "BRIDGE"], "audience": ["INTERMEDIAIRE", "AVANCE", "PROFESSIONNEL"], "level": "leadership", "meta_entities": ["DJ SAYD", "CVL Group"], "bridges": ["ambassadeur CVLN", "leadership entité", "manifesto culturel"], "delivery_formats": PRO_FORMAT, "price_current_eur": None},
    "KLT-01": {"primary_job": "Médiateur culturel", "secondary_jobs": ["Animateur atelier", "Ambassadeur culturel", "Facilitateur patrimoine"], "contexts": ["EXTERNAL", "BRIDGE"], "audience": ["DEBUTANT", "INTERMEDIAIRE", "INSTITUTIONNEL"], "level": "fondamentaux", "meta_entities": ["Kiltikonet", "CIP Foundation"], "bridges": ["atelier médiation", "programme diaspora", "preuve terrain"], "delivery_formats": PRO_FORMAT, "price_current_eur": None},
    "KLT-02": {"primary_job": "Chef de projet culturel", "secondary_jobs": ["Coordinateur événement", "Chargé de production culturelle", "Responsable impact"], "contexts": ["EXTERNAL", "BRIDGE"], "audience": ["INTERMEDIAIRE", "PROFESSIONNEL", "INSTITUTIONNEL"], "level": "professionnalisation", "meta_entities": ["Kiltikonet", "Good Mood", "CVL Group"], "bridges": ["projet culturel CVLN", "coordination événement", "programme territorial"], "delivery_formats": PRO_FORMAT, "price_current_eur": None},
    "KLT-03": {"primary_job": "Responsable partenariats institutionnels culturels", "secondary_jobs": ["Stratège institutionnel", "Cultural diplomat", "Chargé de financement"], "contexts": ["INTERNAL", "EXTERNAL", "BRIDGE"], "audience": ["AVANCE", "PROFESSIONNEL", "INSTITUTIONNEL"], "level": "avancé", "meta_entities": ["Kiltikonet", "CVL Group", "CIP Foundation"], "bridges": ["partenariats institutionnels", "financement programme", "diplomatie culturelle"], "delivery_formats": PRO_FORMAT, "price_current_eur": None},
    "KLT-04": {"primary_job": "Responsable gouvernance associative culturelle", "secondary_jobs": ["Trésorier associatif", "Secrétaire général", "DAF association"], "contexts": ["EXTERNAL", "BRIDGE"], "audience": ["INTERMEDIAIRE", "PROFESSIONNEL", "INSTITUTIONNEL"], "level": "opérationnel", "meta_entities": ["Kiltikonet", "CIP Foundation", "CVL Group"], "bridges": ["conformité structure", "gouvernance association", "administration culturelle"], "delivery_formats": PRO_FORMAT, "price_current_eur": None},
    "KLT-05": {"primary_job": "Opérateur plateforme culturelle", "secondary_jobs": ["Community manager diaspora", "Administrateur contenu", "Chargé impact numérique"], "contexts": ["INTERNAL", "BRIDGE"], "audience": ["INTERMEDIAIRE", "PROFESSIONNEL"], "level": "opérationnel", "meta_entities": ["Kiltikonet", "FREK"], "bridges": ["opération Kiltikonet.fr", "animation communauté", "preuve d'impact diaspora"], "delivery_formats": DEFAULT_FORMAT, "price_current_eur": None},
    "FRK-01": {"primary_job": "Opérateur FREK / confiance numérique culturelle", "secondary_jobs": ["Assistant provenance", "Gestionnaire empreintes", "Référent traçabilité"], "contexts": ["INTERNAL", "EXTERNAL", "BRIDGE"], "audience": ["DEBUTANT", "INTERMEDIAIRE", "INSTITUTIONNEL"], "level": "fondamentaux", "meta_entities": ["FREK", "Kiltikonet", "CIP Foundation"], "bridges": ["FREK-ID", "empreintes œuvres", "missions traçabilité"], "delivery_formats": DEFAULT_FORMAT, "price_current_eur": None},
    "FRK-02": {"primary_job": "Spécialiste provenance numérique", "secondary_jobs": ["Consultant provenance", "Référent droits numériques", "Expert FREK"], "contexts": ["INTERNAL", "EXTERNAL", "BRIDGE"], "audience": ["AVANCE", "PROFESSIONNEL", "INSTITUTIONNEL"], "level": "avancé", "meta_entities": ["FREK", "CIP Foundation", "LabelOS"], "bridges": ["audit provenance", "expertise FREK", "consulting droits"], "delivery_formats": PRO_FORMAT, "price_current_eur": None},
    "FRK-03": {"primary_job": "Archiviste culturel numérique", "secondary_jobs": ["Gestionnaire patrimoine", "Documentaliste culturel", "Référent standards archive"], "contexts": ["EXTERNAL", "BRIDGE"], "audience": ["INTERMEDIAIRE", "PROFESSIONNEL", "INSTITUTIONNEL"], "level": "opérationnel", "meta_entities": ["FREK", "CIP Foundation", "Kiltikonet"], "bridges": ["archive patrimoine", "catalogue sécurisé", "programme mémoire"], "delivery_formats": PRO_FORMAT, "price_current_eur": None},
    "LOS-01": {"primary_job": "Label operations manager", "secondary_jobs": ["Catalog manager", "Ops manager label", "Coordinateur release"], "contexts": ["INTERNAL", "EXTERNAL", "BRIDGE"], "audience": ["INTERMEDIAIRE", "PROFESSIONNEL"], "level": "professionnalisation", "meta_entities": ["LabelOS", "FMS", "CVLN Brain"], "bridges": ["opérations LabelOS", "workflow label IA", "catalogue artiste"], "delivery_formats": PRO_FORMAT, "price_current_eur": None},
    "LOS-02": {"primary_job": "Metadata specialist musique", "secondary_jobs": ["Catalog manager", "Data steward musical", "Coordinateur royalties"], "contexts": ["EXTERNAL", "BRIDGE"], "audience": ["INTERMEDIAIRE", "PROFESSIONNEL"], "level": "opérationnel", "meta_entities": ["LabelOS", "FREK"], "bridges": ["audit metadata", "nettoyage catalogue", "preuve royalties"], "delivery_formats": PRO_FORMAT, "price_current_eur": None},
    "LOS-03": {"primary_job": "AI label workflow operator", "secondary_jobs": ["Workflow architect", "AI ops label", "Automatisation créative"], "contexts": ["INTERNAL", "EXTERNAL", "BRIDGE"], "audience": ["INTERMEDIAIRE", "AVANCE", "PROFESSIONNEL"], "level": "avancé", "meta_entities": ["LabelOS", "CVLN Brain", "FMS"], "bridges": ["automation LabelOS", "workflow Brain", "ops label augmentées"], "delivery_formats": DEFAULT_FORMAT, "price_current_eur": None},
    "BRN-01": {"primary_job": "Stratège écosystème culturel", "secondary_jobs": ["Directeur d'entité", "Architecte organisationnel", "Responsable modèle économique"], "contexts": ["INTERNAL", "BRIDGE"], "audience": ["AVANCE", "PROFESSIONNEL"], "level": "stratégique", "meta_entities": ["CVLN Brain", "CVL Group"], "bridges": ["direction entité", "architecture écosystème", "IPO readiness à qualifier"], "delivery_formats": DEFAULT_FORMAT, "price_current_eur": None},
    "BRN-02": {"primary_job": "Opérateur IA créative", "secondary_jobs": ["Prompt designer", "Creative technologist", "Assistant production augmentée"], "contexts": ["INTERNAL", "EXTERNAL", "BRIDGE"], "audience": ["DEBUTANT", "INTERMEDIAIRE", "PROFESSIONNEL"], "level": "opérationnel", "meta_entities": ["CVLN Brain", "Kiltikonet", "FMS"], "bridges": ["campagne IA CVLN", "production culturelle augmentée", "charte IA culturelle"], "delivery_formats": DEFAULT_FORMAT, "price_current_eur": None},
    "BRN-03": {"primary_job": "Architecte intelligence culturelle", "secondary_jobs": ["Data architect culturel", "Directeur observatoire", "Analyste système culturel"], "contexts": ["INTERNAL", "BRIDGE"], "audience": ["AVANCE", "PROFESSIONNEL", "INSTITUTIONNEL"], "level": "avancé", "meta_entities": ["CVLN Brain", "CIP Foundation", "CVL Group"], "bridges": ["observatoire culturel", "système intelligence", "data gouvernance"], "delivery_formats": DEFAULT_FORMAT, "price_current_eur": None},
    "AGR-01": {"primary_job": "Responsable transformation agroalimentaire premium", "secondary_jobs": ["Brand manager agroalimentaire", "Product manager alimentaire", "Coordinateur production locale"], "contexts": ["EXTERNAL", "BRIDGE"], "audience": ["INTERMEDIAIRE", "PROFESSIONNEL", "INSTITUTIONNEL"], "level": "professionnalisation", "meta_entities": ["CVL Agro", "CVL Group", "CVLN Hospitality"], "bridges": ["produit premium CVL Agro", "export produit caribéen", "hospitality/retail"], "delivery_formats": PRO_FORMAT, "price_current_eur": None},
    "BCH-01": {"primary_job": "Spécialiste blockchain culturelle", "secondary_jobs": ["Tokenomics architect", "Opérateur actifs numériques", "Conseil web3 culturel"], "contexts": ["INTERNAL", "EXTERNAL", "BRIDGE"], "audience": ["AVANCE", "PROFESSIONNEL"], "level": "spécialiste", "meta_entities": ["CVLN Blockchain", "FREK", "CVL Group"], "bridges": ["tokenisation actifs", "provenance blockchain", "économie numérique souveraine"], "delivery_formats": DEFAULT_FORMAT, "price_current_eur": None},
    "HOS-01": {"primary_job": "Manager de lieu hybride créatif", "secondary_jobs": ["Residence coordinator", "Hospitality experience designer", "Responsable tiers-lieu"], "contexts": ["EXTERNAL", "BRIDGE"], "audience": ["INTERMEDIAIRE", "PROFESSIONNEL", "INSTITUTIONNEL"], "level": "professionnalisation", "meta_entities": ["CVLN Hospitality", "FMS", "Good Mood"], "bridges": ["résidence créative", "lieu hybride", "expérience immersive"], "delivery_formats": PRO_FORMAT, "price_current_eur": None},
    "GRP-01": {"primary_job": "Entrepreneur d'écosystème culturel", "secondary_jobs": ["Co-entrepreneur CVLN", "Directeur d'entité", "Builder holding culturel"], "contexts": ["INTERNAL", "BRIDGE"], "audience": ["AVANCE", "PROFESSIONNEL"], "level": "stratégique", "meta_entities": ["CVL Group", "CVLN Brain"], "bridges": ["co-entrepreneuriat CVLN", "direction entité", "équity readiness à qualifier"], "delivery_formats": DEFAULT_FORMAT, "price_current_eur": None},
    "GRP-02": {"primary_job": "Stratège économie culturelle et partenariats", "secondary_jobs": ["Directeur partenariats", "Business developer culturel", "Conseil politiques culturelles"], "contexts": ["INTERNAL", "EXTERNAL", "BRIDGE"], "audience": ["AVANCE", "PROFESSIONNEL", "INSTITUTIONNEL"], "level": "stratégique", "meta_entities": ["CVL Group", "Kiltikonet", "CIP Foundation"], "bridges": ["partenariats stratégiques", "scaling international", "programmes institutionnels"], "delivery_formats": PRO_FORMAT, "price_current_eur": None},
    "CIP-01": {"primary_job": "Référent standardisation et gouvernance culturelle", "secondary_jobs": ["Architecte référentiel", "Responsable certification culturelle", "Archiviste gouvernance"], "contexts": ["INTERNAL", "BRIDGE"], "audience": ["AVANCE", "PROFESSIONNEL", "INSTITUTIONNEL"], "level": "spécialiste", "meta_entities": ["CIP Foundation", "FREK", "CVL Group"], "bridges": ["référentiel culturel", "standard certification", "gouvernance patrimoine"], "delivery_formats": DEFAULT_FORMAT, "price_current_eur": None},
}


def _module_names(formation: dict[str, Any]) -> list[str]:
    return [m.get("name", "") for m in formation.get("modules", []) if m.get("name")]


def _module_deliverables(formation: dict[str, Any]) -> list[str]:
    return [m.get("deliverable", "") for m in formation.get("modules", []) if m.get("deliverable")]


def _infer_competencies(formation: dict[str, Any], mapping: dict[str, Any]) -> list[str]:
    competencies = list(dict.fromkeys(mapping.get("secondary_jobs", [])[:2] + _module_names(formation)[:6]))
    if not competencies:
        competencies = [formation.get("description", "À calibrer depuis le contenu existant")]
    return competencies


def _infer_activities(formation: dict[str, Any], mapping: dict[str, Any]) -> list[str]:
    activities = list(mapping.get("bridges", []))
    if formation.get("objective_strategic"):
        activities.append(formation["objective_strategic"])
    return list(dict.fromkeys(activities))


def _infer_tools(formation: dict[str, Any], mapping: dict[str, Any]) -> list[str]:
    tools = list(mapping.get("meta_entities", []))
    text = " ".join([formation.get("name", ""), formation.get("description", ""), *_module_names(formation)]).lower()
    candidates = {
        "FREK": "FREK / FREK-ID",
        "metadata": "ISRC / ISWC / DDEX à calibrer",
        "distribution": "DSP / agrégateurs à calibrer",
        "ia": "outils IA générative à calibrer",
        "daw": "DAW à calibrer",
        "podcast": "outils audio/podcast à calibrer",
        "blockchain": "outils blockchain à calibrer",
    }
    for key, value in candidates.items():
        if key in text:
            tools.append(value)
    return list(dict.fromkeys(tools))


def _build_inconsistencies(formation: dict[str, Any], mapping: dict[str, Any]) -> list[dict[str, str]]:
    inconsistencies = list(formation.get("reconciliation_flags", []))
    if not formation.get("modules"):
        inconsistencies.append({"type": "MODULES_INJECTED_OR_EMPTY", "message": "Le détail pédagogique dépend de seed_modules.py ou reste à reconstruire depuis la fiche métier."})
    if mapping.get("price_current_eur") is None:
        inconsistencies.append({"type": "PRICE_MISSING", "message": "Aucun prix actuel explicite dans le seed; économie provisoire à calibrer."})
    return inconsistencies


def build_cartography(formation: dict[str, Any]) -> dict[str, Any]:
    mapping = deepcopy(_FORMATION_CARTOGRAPHY[formation["code"]])
    deliverables = _module_deliverables(formation)
    evidence = deliverables or ["preuve à définir lors de la reconstruction métier"]
    price_current = mapping.pop("price_current_eur")
    inconsistencies = _build_inconsistencies(formation, mapping | {"price_current_eur": price_current})
    return {
        **mapping,
        "duration_h": formation.get("duration_h"),
        "cc": formation.get("cc"),
        "competencies": _infer_competencies(formation, mapping),
        "professional_activities": _infer_activities(formation, mapping),
        "tools": _infer_tools(formation, mapping),
        "deliverables": deliverables,
        "evidence": evidence,
        "outcomes": [part.strip() for part in formation.get("debouches", "").split(",") if part.strip()],
        "current_price_eur": price_current,
        "provisional_economics": {
            "status": "needs_external_calibration" if price_current is None else "provisional_seed_value",
            "public_price_eur": price_current,
            "costs": "needs_external_calibration",
            "margin": "needs_external_calibration",
            "financing": "needs_external_calibration",
        },
        "calibration_sources": list(CALIBRATION_SOURCES),
        "needs_external_calibration": True,
        "inconsistencies": inconsistencies,
        "reconstruction_status": "NEEDS_RECONSTRUCTION" if inconsistencies else "MAPPED_FROM_SEED",
        "source": "seed_data + seed_modules; market values intentionally not invented",
    }


def apply_catalog_cartography(formations: list[dict[str, Any]]) -> None:
    missing = sorted({f["code"] for f in formations} - set(_FORMATION_CARTOGRAPHY))
    if missing:
        raise ValueError(f"Missing catalogue cartography for formations: {', '.join(missing)}")
    for formation in formations:
        cartography = build_cartography(formation)
        formation["cartography"] = cartography
        formation["contexts"] = cartography["contexts"]
        formation["audience_levels"] = cartography["audience"]
        formation["bridge_entities"] = cartography["meta_entities"]
        formation["positioning_note"] = f"Métier principal: {cartography['primary_job']} · reconstruction: {cartography['reconstruction_status']}"
        formation["needs_external_calibration"] = cartography["needs_external_calibration"]
        formation["reconstruction_status"] = cartography["reconstruction_status"]
        formation["reconciliation_flags"] = list(cartography["inconsistencies"])
        formation["economics"] = {
            **formation.get("economics", {}),
            "public_price_eur": cartography["current_price_eur"],
            "funding_options": ["needs_external_calibration"],
        }
        formation["job_truth"] = {
            **formation.get("job_truth", {}),
            "market_name": cartography["primary_job"],
            "cvln_name": formation.get("debouches"),
            "technical_skills": cartography["competencies"],
            "tools": cartography["tools"],
            "deliverables": cartography["deliverables"],
            "evidence": cartography["evidence"],
            "outcomes": cartography["outcomes"],
            "bridge": {
                "cvln_entities": cartography["meta_entities"],
                "missions": cartography["bridges"],
                "opportunities": cartography["outcomes"],
                "contribution": "Passerelle à valider par missions, preuves FREK et calibration externe.",
            },
        }
