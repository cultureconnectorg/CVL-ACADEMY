"""External calibration layer for the CVLN Academy catalogue.

The goal is not to rewrite courses. It separates the current CVLN state from a
verifiable external market state and a recommended future state so each course can
later be reconstructed A→Z with evidence.
"""
from __future__ import annotations

from copy import deepcopy
from typing import Any

CALIBRATION_DATE = "2026-08-18"

SOURCES = {
    "rome_l1202": {"label": "France Travail MétierScope L1202 - Musicien / Musicienne", "url": "https://candidat.francetravail.fr/metierscope/fiche-metier/L1202/musicien-musicienne"},
    "rome_l1302": {"label": "France Travail MétierScope L1302 - Producteur / Productrice audiovisuel et cinéma", "url": "https://candidat.francetravail.fr/metierscope/fiche-metier/L1302/producteur-productrice-audiovisuel-et-cinema"},
    "rome_l1305": {"label": "France Travail MétierScope L1305 - Directeur / Directrice artistique spectacle", "url": "https://candidat.francetravail.fr/metierscope/fiche-metier/L1305/directeur-directrice-artistique-spectacle"},
    "rome_e1103": {"label": "France Travail MétierScope E1103 - Chargé / Chargée des relations publiques", "url": "https://candidat.francetravail.fr/metierscope/fiche-metier/E1103/charge-chargee-des-relations-publiques"},
    "rome_e1106": {"label": "France Travail MétierScope E1106 - Journaliste", "url": "https://candidat.francetravail.fr/metierscope/fiche-metier/E1106/journaliste"},
    "rome_e1107": {"label": "France Travail MétierScope E1107 - Chef / Cheffe de projet événementiel", "url": "https://candidat.francetravail.fr/metierscope/fiche-metier/E1107/chef-cheffe-de-projet-evenementiel"},
    "rome_e1124": {"label": "France Travail MétierScope E1124 - Social media manager", "url": "https://candidat.francetravail.fr/metierscope/fiche-metier/E1124/social-media-manager---responsable-des-medias-sociaux"},
    "rome_k1206": {"label": "France Travail MétierScope K1206 - Animateur coordinateur socioculturel", "url": "https://candidat.francetravail.fr/metierscope/fiche-metier/K1206/animateur-coordinateur-socioculturel-animatrice-coordinatrice-socioculturelle"},
    "rome_k1213": {"label": "France Travail MétierScope K1213 - Médiateur culturel / Médiatrice culturelle", "url": "https://candidat.francetravail.fr/metierscope/fiche-metier/K1213/mediateur-culturel-mediatrice-culturelle"},
    "rome_k1602": {"label": "France Travail MétierScope K1602 - Conservateur / Conservatrice du patrimoine", "url": "https://candidat.francetravail.fr/metierscope/fiche-metier/K1602/conservateur-conservatrice-du-patrimoine"},
    "rome_k1604": {"label": "France Travail MétierScope K1604 - Directeur / Directrice d'établissement culturel", "url": "https://candidat.francetravail.fr/metierscope/fiche-metier/K1604/directeur-directrice-etablissement-culturel"},
    "rome_k1605": {"label": "France Travail MétierScope K1605 - Commissaire d'exposition", "url": "https://candidat.francetravail.fr/metierscope/fiche-metier/K1605/commissaire-exposition"},
    "rome_k1802": {"label": "France Travail MétierScope K1802 - Chargé / Chargée de développement économique et local", "url": "https://candidat.francetravail.fr/metierscope/fiche-metier/K1802/charge-chargee-de-developpement-economique-et-local"},
    "rome_k1808": {"label": "France Travail MétierScope K1808 - Chargé / Chargée de développement culturel", "url": "https://candidat.francetravail.fr/metierscope/fiche-metier/K1808/charge-chargee-de-developpement-culturel"},
    "rome_m1419": {"label": "France Travail MétierScope M1419 - Data analyst", "url": "https://candidat.francetravail.fr/metierscope/fiche-metier/M1419/data-analyst"},
    "rome_m1805": {"label": "France Travail MétierScope M1805 - Développeur / Développeuse informatique", "url": "https://candidat.francetravail.fr/metierscope/fiche-metier/M1805/developpeur-developpeuse-informatique"},
    "rome_m1806": {"label": "France Travail MétierScope M1806 - Consultant fonctionnel / Consultante fonctionnelle SI", "url": "https://candidat.francetravail.fr/metierscope/fiche-metier/M1806/consultant-fonctionnel-consultante-fonctionnelle-des-systemes-information"},
    "rome_m1811": {"label": "France Travail MétierScope M1811 - Data engineer", "url": "https://candidat.francetravail.fr/metierscope/fiche-metier/M1811/data-engineer"},
    "rome_g1102": {"label": "France Travail MétierScope G1102 - Chargé / Chargée de promotion touristique", "url": "https://candidat.francetravail.fr/metierscope/fiche-metier/G1102/charge-chargee-de-promotion-touristique"},
    "rncp_40912": {"label": "France compétences RNCP40912 - Chef de projets culturels et évènementiels", "url": "https://www.francecompetences.fr/recherche/rncp/40912/"},
    "rncp_39865": {"label": "France compétences RNCP39865 - Chef de projet événementiel", "url": "https://www.francecompetences.fr/recherche/rncp/39865/"},
    "rncp_37827": {"label": "France compétences RNCP37827 - Développeur en intelligence artificielle", "url": "https://www.francecompetences.fr/recherche/rncp/37827/"},
    "rncp_38616": {"label": "France compétences RNCP38616 - Concepteur développeur en IA et analyse Big Data", "url": "https://www.francecompetences.fr/recherche/rncp/38616/"},
    "rncp_38829": {"label": "France compétences RNCP38829 - Artiste danseur chanteur comédien", "url": "https://www.francecompetences.fr/recherche/rncp/38829/"},
    "rncp_41321": {"label": "France compétences RNCP41321 - Artiste interprète de music-hall", "url": "https://www.francecompetences.fr/recherche/rncp/41321/"},
    "rncp_32052": {"label": "France compétences RNCP32052 - Chargé de projet culturel", "url": "https://www.francecompetences.fr/recherche/rncp/32052/"},
    "cpf_eligibility": {"label": "Mon Compte Formation - Formations éligibles CPF", "url": "https://of.moncompteformation.gouv.fr/espace-public/aide/quelles-sont-les-formations-eligibles-au-compte-personnel-de-formation"},
    "afdas": {"label": "Afdas - dispositifs et financement spectacle/audiovisuel", "url": "https://www.afdas.com/particulier/connaitre-les-dispositifs-et-les-modalites-dacces-a-la-formation/intermittents-du-spectacle-et-de-laudiovisuel.html"},
}

CERT_PROJECT_CULTURE = [SOURCES["rncp_40912"], SOURCES["rncp_32052"]]
CERT_EVENT = [SOURCES["rncp_39865"], SOURCES["rncp_40912"]]
CERT_ARTIST = [SOURCES["rncp_38829"], SOURCES["rncp_41321"]]
CERT_AI = [SOURCES["rncp_37827"], SOURCES["rncp_38616"]]
FUNDING_DEFAULT = [SOURCES["cpf_eligibility"], SOURCES["afdas"]]

_MARKET_MAP: dict[str, dict[str, Any]] = {
    "FMS-01": {"market_job_title": "Artiste interprète / musicien", "refs": ["rome_l1202"], "certs": CERT_ARTIST, "skills": ["interprétation", "répétition", "préparation d'auditions", "communication du projet artistique"], "activities": ["préparer des interprétations", "répéter", "participer à des créations dirigées", "présenter un projet artistique"], "tools": ["voix/instrument", "dossier artistique", "captation", "outils de promotion"], "outcomes": ["artiste interprète", "musicien", "auteur-compositeur-interprète"], "confidence": "medium"},
    "FMS-02": {"market_job_title": "Chargé de production musicale / label manager", "refs": ["rome_l1302", "rome_k1808"], "certs": CERT_PROJECT_CULTURE, "skills": ["gestion de projet culturel", "partenariats", "budget", "droits et distribution à vérifier"], "activities": ["organiser un projet culturel", "rechercher des partenaires", "coordonner production et diffusion"], "tools": ["contrats", "tableaux budgétaires", "DSP/agrégateurs à benchmarker", "sociétés de droits à vérifier"], "outcomes": ["label manager", "chargé de production", "coordinateur de projet musical"], "confidence": "medium"},
    "FMS-03": {"market_job_title": "Producteur musical / musicien MAO", "refs": ["rome_l1202"], "certs": CERT_ARTIST, "skills": ["composition", "production audio", "arrangement", "mixage de base"], "activities": ["créer des œuvres musicales", "préparer des maquettes", "collaborer avec artistes"], "tools": ["DAW à benchmarker", "contrôleurs MIDI", "plugins audio", "bibliothèques sons"], "outcomes": ["beatmaker", "producteur musical", "compositeur"], "confidence": "low"},
    "FMS-04": {"market_job_title": "Directeur artistique / brand manager artiste", "refs": ["rome_l1305", "rome_e1103"], "certs": CERT_PROJECT_CULTURE, "skills": ["direction artistique", "image de marque", "relations publiques", "storytelling"], "activities": ["définir une identité", "valoriser l'image", "concevoir supports promotionnels"], "tools": ["brand book", "kit presse", "réseaux sociaux", "outils design à benchmarker"], "outcomes": ["directeur artistique", "brand manager", "chargé de communication culturelle"], "confidence": "medium"},
    "FMS-05": {"market_job_title": "Manager d'artiste / chargé de développement culturel", "refs": ["rome_k1808", "rome_e1103"], "certs": CERT_PROJECT_CULTURE, "skills": ["développement culturel", "partenariats", "coordination", "communication"], "activities": ["accompagner un projet artistique", "développer des partenariats", "coordonner production/promotion"], "tools": ["planning", "budget", "CRM à benchmarker", "contrats à vérifier"], "outcomes": ["manager d'artiste", "chargé de développement", "coordinateur artistique"], "confidence": "medium"},
    "FMS-06": {"market_job_title": "Producteur / directeur artistique", "refs": ["rome_l1302", "rome_l1305"], "certs": CERT_PROJECT_CULTURE, "skills": ["production", "direction artistique", "sélection de projets", "pilotage budget"], "activities": ["définir une orientation artistique", "piloter une production", "coordonner équipes et partenaires"], "tools": ["budget", "contrats", "planning production", "reporting"], "outcomes": ["producteur exécutif", "directeur artistique", "responsable production"], "confidence": "medium"},
    "KOR-01": {"market_job_title": "Producteur podcast / producteur audiovisuel", "refs": ["rome_l1302", "rome_e1106"], "certs": CERT_PROJECT_CULTURE, "skills": ["conception éditoriale", "production audio", "interview", "postproduction"], "activities": ["préparer une émission", "enregistrer", "monter", "diffuser"], "tools": ["microphones", "logiciels montage audio", "plateformes podcast à benchmarker"], "outcomes": ["producteur podcast", "réalisateur audio", "journaliste audio"], "confidence": "low"},
    "KOR-02": {"market_job_title": "Journaliste / storyteller culturel", "refs": ["rome_e1106", "rome_k1808"], "certs": CERT_PROJECT_CULTURE, "skills": ["enquête", "écriture journalistique", "interview", "médiation culturelle"], "activities": ["collecter information", "rédiger", "interviewer", "produire contenus"], "tools": ["outils rédaction", "enregistreur", "CMS", "réseaux sociaux"], "outcomes": ["journaliste culturel", "rédacteur", "producteur éditorial"], "confidence": "medium"},
    "GMD-01": {"market_job_title": "Chef de projet événementiel", "refs": ["rome_e1107"], "certs": CERT_EVENT, "skills": ["conception événement", "budget", "logistique", "sécurité", "coordination prestataires"], "activities": ["imaginer et organiser un événement", "analyser besoins", "coordonner production"], "tools": ["rétroplanning", "budget", "plan de site", "outils billetterie à benchmarker"], "outcomes": ["chef de projet événementiel", "coordinateur festival", "régisseur production"], "confidence": "high"},
    "SAY-01": {"market_job_title": "Chargé de relations publiques / responsable communauté", "refs": ["rome_e1103", "rome_e1124"], "certs": CERT_PROJECT_CULTURE, "skills": ["image publique", "prise de parole", "animation communauté", "stratégie média"], "activities": ["valoriser une image", "animer des communautés", "concevoir actions de communication"], "tools": ["réseaux sociaux", "kit média", "calendrier éditorial"], "outcomes": ["ambassadeur culturel", "responsable communauté", "chargé de relations publiques"], "confidence": "medium"},
    "KLT-01": {"market_job_title": "Médiateur culturel", "refs": ["rome_k1213", "rome_k1206"], "certs": CERT_PROJECT_CULTURE, "skills": ["médiation", "animation", "adaptation publics", "évaluation impact"], "activities": ["concevoir médiation", "animer ateliers", "mobiliser ressources locales"], "tools": ["supports pédagogiques", "grilles animation", "questionnaires impact"], "outcomes": ["médiateur culturel", "animateur socioculturel", "facilitateur patrimoine"], "confidence": "high"},
    "KLT-02": {"market_job_title": "Chef de projet culturel", "refs": ["rome_k1808", "rome_e1107"], "certs": CERT_PROJECT_CULTURE, "skills": ["conception projet", "partenariats", "financement", "coordination"], "activities": ["concevoir projet", "rechercher moyens", "mobiliser acteurs", "gérer mise en œuvre"], "tools": ["budget", "dossier financement", "rétroplanning", "CRM partenaires"], "outcomes": ["chef de projet culturel", "chargé de développement culturel", "coordinateur événement"], "confidence": "high"},
    "KLT-03": {"market_job_title": "Chargé de développement culturel / partenariats", "refs": ["rome_k1808", "rome_k1802"], "certs": CERT_PROJECT_CULTURE, "skills": ["partenariats", "financement", "développement territorial", "diplomatie culturelle à vérifier"], "activities": ["développer un projet culturel", "nouer partenariats", "rechercher financements"], "tools": ["dossier institutionnel", "veille appels à projets", "tableau partenaires"], "outcomes": ["responsable partenariats", "chargé développement", "coordinateur institutionnel"], "confidence": "medium"},
    "KLT-04": {"market_job_title": "Responsable administration culturelle / gouvernance associative", "refs": ["rome_k1808", "rome_k1604"], "certs": CERT_PROJECT_CULTURE, "skills": ["administration", "gouvernance", "budget", "conformité associative à vérifier"], "activities": ["administrer projets", "coordonner acteurs", "suivre budget"], "tools": ["statuts", "PV", "budget", "tableau obligations"], "outcomes": ["administrateur culturel", "secrétaire général", "responsable structure"], "confidence": "low"},
    "KLT-05": {"market_job_title": "Community manager / opérateur plateforme culturelle", "refs": ["rome_e1124", "rome_k1808"], "certs": CERT_PROJECT_CULTURE, "skills": ["animation communauté", "publication contenu", "modération", "suivi impact"], "activities": ["animer médias sociaux", "publier contenus", "mesurer engagement"], "tools": ["CMS", "réseaux sociaux", "analytics", "outils newsletter"], "outcomes": ["community manager", "opérateur plateforme", "chargé impact numérique"], "confidence": "medium"},
    "FRK-01": {"market_job_title": "Opérateur traçabilité / assistant gestion d'information", "refs": ["rome_m1806", "rome_k1602"], "certs": [], "skills": ["documentation", "traçabilité", "gestion de preuves", "sensibilisation droits"], "activities": ["créer dossiers de preuve", "documenter œuvres", "signaler anomalies"], "tools": ["FREK", "bases de données", "hash/provenance à vérifier"], "outcomes": ["opérateur provenance", "assistant documentation", "référent traçabilité"], "confidence": "low"},
    "FRK-02": {"market_job_title": "Consultant provenance numérique / consultant SI", "refs": ["rome_m1806", "rome_k1602"], "certs": [], "skills": ["audit", "provenance", "conformité", "conseil"], "activities": ["analyser processus", "recommander dispositifs", "documenter preuves"], "tools": ["outils audit", "bases documentaires", "FREK", "standards à vérifier"], "outcomes": ["consultant provenance", "expert traçabilité", "référent droits numériques"], "confidence": "low"},
    "FRK-03": {"market_job_title": "Archiviste / conservateur du patrimoine numérique", "refs": ["rome_k1602"], "certs": CERT_PROJECT_CULTURE, "skills": ["archivage", "classification", "conservation", "documentation"], "activities": ["collecter patrimoine", "classer", "documenter", "conserver"], "tools": ["système archivage", "métadonnées", "référentiels patrimoine"], "outcomes": ["archiviste", "gestionnaire patrimoine", "documentaliste culturel"], "confidence": "medium"},
    "LOS-01": {"market_job_title": "Label manager / chargé de production", "refs": ["rome_l1302", "rome_k1808"], "certs": CERT_PROJECT_CULTURE, "skills": ["release management", "catalogue", "budget", "coordination"], "activities": ["piloter sorties", "coordonner prestataires", "suivre catalogue"], "tools": ["LabelOS", "tableaux catalogue", "DSP/agrégateurs à benchmarker"], "outcomes": ["label manager", "operations manager", "catalog manager"], "confidence": "medium"},
    "LOS-02": {"market_job_title": "Gestionnaire metadata musicale / catalog manager", "refs": ["rome_l1302", "rome_m1806"], "certs": [], "skills": ["métadonnées", "contrôle qualité", "catalogue", "royalties à vérifier"], "activities": ["normaliser données", "auditer catalogue", "corriger erreurs"], "tools": ["ISRC/ISWC/DDEX à vérifier", "tableurs", "outils distributeurs"], "outcomes": ["metadata specialist", "catalog manager", "data steward musical"], "confidence": "low"},
    "LOS-03": {"market_job_title": "Consultant workflow IA / opérateur automatisation", "refs": ["rome_m1806", "rome_m1805"], "certs": CERT_AI, "skills": ["automatisation", "intégration IA", "workflow", "tests"], "activities": ["analyser processus", "intégrer services IA", "tester automatisations"], "tools": ["outils IA générative", "API", "no-code/automation à benchmarker"], "outcomes": ["AI ops", "workflow architect", "consultant automatisation"], "confidence": "medium"},
    "BRN-01": {"market_job_title": "Directeur d'établissement culturel / consultant stratégie", "refs": ["rome_k1604", "rome_m1806"], "certs": CERT_PROJECT_CULTURE, "skills": ["stratégie", "pilotage", "modèle économique", "gouvernance"], "activities": ["définir politique culturelle", "piloter développement", "orchestrer activités"], "tools": ["business model", "OKR/KPI", "cartographie parties prenantes"], "outcomes": ["directeur d'entité", "stratège écosystème", "consultant"], "confidence": "medium"},
    "BRN-02": {"market_job_title": "Opérateur IA créative / développeur IA adjacent", "refs": ["rome_m1805", "rome_e1124"], "certs": CERT_AI, "skills": ["prompting", "production assistée IA", "intégration services IA", "éthique culturelle"], "activities": ["produire assets", "intégrer services IA", "documenter prompts"], "tools": ["outils IA générative à benchmarker", "API", "outils multimédia"], "outcomes": ["creative AI operator", "prompt designer", "assistant production"], "confidence": "medium"},
    "BRN-03": {"market_job_title": "Data analyst / data engineer culturel", "refs": ["rome_m1419", "rome_m1811"], "certs": CERT_AI, "skills": ["analyse données", "collecte", "modélisation", "visualisation"], "activities": ["collecter données", "analyser volumes", "sécuriser données", "produire indicateurs"], "tools": ["SQL", "Python à benchmarker", "BI", "base de données"], "outcomes": ["data analyst", "data engineer", "architecte intelligence culturelle"], "confidence": "medium"},
    "AGR-01": {"market_job_title": "Chargé de développement économique local / produit agroalimentaire", "refs": ["rome_k1802"], "certs": [], "skills": ["développement local", "positionnement produit", "partenariats", "export à vérifier"], "activities": ["valoriser territoire", "stimuler activité économique", "structurer offre"], "tools": ["business plan", "packaging brief", "normes agroalimentaires à vérifier"], "outcomes": ["product manager", "chargé développement", "coordinateur production"], "confidence": "low"},
    "BCH-01": {"market_job_title": "Consultant blockchain / consultant SI", "refs": ["rome_m1806", "rome_m1805"], "certs": [], "skills": ["analyse SI", "tokenisation à vérifier", "smart contracts à vérifier", "provenance"], "activities": ["analyser besoin", "concevoir architecture", "documenter risques"], "tools": ["blockchain à benchmarker", "wallets", "smart contracts", "FREK"], "outcomes": ["consultant blockchain", "tokenomics architect", "opérateur actifs numériques"], "confidence": "low"},
    "HOS-01": {"market_job_title": "Directeur d'établissement culturel / promotion touristique", "refs": ["rome_k1604", "rome_g1102"], "certs": CERT_PROJECT_CULTURE, "skills": ["gestion lieu", "expérience client", "programmation", "partenariats tourisme"], "activities": ["définir activités", "promouvoir territoire", "coordonner expérience"], "tools": ["planning lieu", "CRM", "outils réservation à benchmarker"], "outcomes": ["manager tiers-lieu", "coordinateur résidence", "responsable expérience"], "confidence": "medium"},
    "GRP-01": {"market_job_title": "Entrepreneur / directeur d'établissement culturel", "refs": ["rome_k1604", "rome_k1802"], "certs": CERT_PROJECT_CULTURE, "skills": ["entrepreneuriat", "gouvernance", "développement économique", "pilotage"], "activities": ["définir stratégie", "développer activité", "piloter structure"], "tools": ["business model", "reporting", "gouvernance", "tableau de bord"], "outcomes": ["directeur d'entité", "entrepreneur culturel", "responsable développement"], "confidence": "medium"},
    "GRP-02": {"market_job_title": "Chargé de développement économique et culturel", "refs": ["rome_k1802", "rome_k1808"], "certs": CERT_PROJECT_CULTURE, "skills": ["partenariats", "développement économique", "politique culturelle", "négociation"], "activities": ["valoriser territoire", "développer partenariats", "financer projets"], "tools": ["CRM", "dossier partenaire", "veille appels à projets"], "outcomes": ["directeur partenariats", "business developer culturel", "stratège économie culturelle"], "confidence": "medium"},
    "CIP-01": {"market_job_title": "Conservateur / référent gouvernance patrimoine", "refs": ["rome_k1602", "rome_k1605"], "certs": CERT_PROJECT_CULTURE, "skills": ["référentiel", "gouvernance", "conservation", "médiation"], "activities": ["concevoir projet patrimonial", "documenter standards", "assurer médiation"], "tools": ["référentiel", "métadonnées", "grilles certification à construire"], "outcomes": ["référent gouvernance", "architecte référentiel", "responsable certification culturelle"], "confidence": "low"},
}


def _source(ref_key: str) -> dict[str, str]:
    return deepcopy(SOURCES[ref_key])


def _price_range() -> dict[str, Any]:
    return {"status": "needs_benchmark", "observed_min_eur": None, "observed_max_eur": None, "note": "Prix comparable non retenu sans source directe formation par formation."}


def build_external_calibration(formation: dict[str, Any]) -> dict[str, Any]:
    code = formation["code"]
    market = deepcopy(_MARKET_MAP[code])
    current = formation.get("cartography", {})
    external_refs = [_source(key) | {"match_type": "direct_or_adjacent"} for key in market.pop("refs")]
    certs = market.pop("certs")
    gaps = []
    if formation.get("duration_h") != formation.get("cc"):
        gaps.append("Écart durée/CC à justifier ou corriger.")
    if current.get("current_price_eur") is None:
        gaps.append("Prix actuel absent du seed; benchmark concurrent à réaliser.")
    gaps.append("Correspondance ROME/RNCP à valider par revue humaine avant publication commerciale.")
    return {
        "calibration_date": CALIBRATION_DATE,
        "current_cvln_state": {
            "formation_code": code,
            "formation_name": formation.get("name"),
            "cvln_primary_job": current.get("primary_job"),
            "contexts": formation.get("contexts", []),
            "audience_levels": formation.get("audience_levels", []),
            "duration_h": formation.get("duration_h"),
            "cc": formation.get("cc"),
            "deliverables": current.get("deliverables", []),
            "meta_entities": current.get("meta_entities", []),
        },
        "external_market_state": {
            "market_job_title": market["market_job_title"],
            "external_job_references": external_refs,
            "market_skills": market["skills"],
            "market_activities": market["activities"],
            "market_tools": market["tools"],
            "market_outcomes": market["outcomes"],
            "certification_references": certs,
            "market_formats": ["e-learning", "présentiel", "hybride", "court", "long", "bootcamp à benchmarker"],
            "market_price_range": _price_range(),
            "funding_options": FUNDING_DEFAULT,
            "competitor_references": [{"status": "needs_benchmark", "note": "Offres concurrentes à lister avec prix/durée/syllabus vérifiés lors du benchmark dédié."}],
            "market_evidence": external_refs + certs + FUNDING_DEFAULT,
        },
        "recommended_future_state": {
            "gaps": gaps,
            "recommended_reconstruction": "KEEP seed content; CORRECT gaps; EXTEND with verified external skills/references; CONNECT to CVLN bridge evidence; do not rewrite pedagogy yet.",
        },
        "calibration_confidence": market["confidence"],
    }


def apply_external_calibration(formations: list[dict[str, Any]]) -> None:
    missing = sorted({f["code"] for f in formations} - set(_MARKET_MAP))
    if missing:
        raise ValueError(f"Missing external calibration for formations: {', '.join(missing)}")
    for formation in formations:
        calibration = build_external_calibration(formation)
        formation["external_calibration"] = calibration
        formation["market_job_title"] = calibration["external_market_state"]["market_job_title"]
        formation["calibration_confidence"] = calibration["calibration_confidence"]
        formation["calibration_date"] = calibration["calibration_date"]
        formation.setdefault("reconciliation_flags", [])
        for gap in calibration["recommended_future_state"]["gaps"]:
            if not any(flag.get("message") == gap for flag in formation["reconciliation_flags"]):
                formation["reconciliation_flags"].append({"type": "EXTERNAL_CALIBRATION_GAP", "message": gap})
