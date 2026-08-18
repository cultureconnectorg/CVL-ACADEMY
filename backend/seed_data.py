"""Seed data extracted from CVLN Academy Master OS v3.0 (30 formations, 13 poles).

Each formation has code, pole, hours, stages, cc credits, badge name.
A subset of formations includes detailed modules; others are marked "coming_soon"
with module count only. Missions and badges are also defined here.
"""
from copy import deepcopy

# 13 poles with their canonical colors (aligned with Caribbean Futurism palette)
POLES = [
    {"code": "FMS", "name": "Factory Maker Studio",  "color": "#E05A33"},
    {"code": "KOR", "name": "KORA",                  "color": "#F59E0B"},
    {"code": "GMD", "name": "Good Mood by DJ Sayd",  "color": "#C2410C"},
    {"code": "SAY", "name": "DJ SAYD",               "color": "#7C2D12"},
    {"code": "KLT", "name": "Kiltikonet",            "color": "#15803D"},
    {"code": "FRK", "name": "FREK",                  "color": "#0EA5E9"},
    {"code": "LOS", "name": "LabelOS",               "color": "#EA580C"},
    {"code": "BRN", "name": "CVLN Brain",            "color": "#8B5CF6"},
    {"code": "AGR", "name": "CVL Agro",              "color": "#65A30D"},
    {"code": "BCH", "name": "CVLN Blockchain",       "color": "#DB2777"},
    {"code": "HOS", "name": "CVLN Hospitality",      "color": "#0891B2"},
    {"code": "GRP", "name": "CVL Group",             "color": "#B45309"},
    {"code": "CIP", "name": "CIP Foundation",        "color": "#059669"},
]

STADES = ["graine", "pousse", "racine", "branches", "arbre", "foret"]


# Academy OS cartography contexts and audience levels.
# These metadata make the legacy catalogue explicit without deleting or flattening
# the CVLN vision: a formation can be market-facing, internal, and/or a bridge
# toward missions in the META-CVLN ecosystem.
CONTEXTS = ["INTERNAL", "EXTERNAL", "BRIDGE"]
AUDIENCE_LEVELS = ["DEBUTANT", "INTERMEDIAIRE", "AVANCE", "PROFESSIONNEL", "INSTITUTIONNEL"]

DEFAULT_ECONOMICS = {
    "public_price_eur": None,
    "company_price_eur": None,
    "funding_options": [],
    "pedagogical_cost_eur": None,
    "instructors_cost_eur": None,
    "production_cost_eur": None,
    "studio_or_venue_cost_eur": None,
    "tech_cost_eur": None,
    "acquisition_cost_eur": None,
    "administration_cost_eur": None,
    "reinvestment_rate": None,
    "margin_target": None,
}

DEFAULT_CALIBRATION_SOURCES = [
    "France Travail / ROME",
    "France compétences",
    "Marché réel",
    "Formation existante",
    "Financement",
    "Qualiopi",
]

JOB_TRUTH_TEMPLATE = {
    "market_name": None,
    "cvln_name": None,
    "rome_refs": [],
    "external_certification_refs": [],
    "level": None,
    "sectors": [],
    "real_missions": [],
    "technical_skills": [],
    "behavioral_skills": [],
    "tools": [],
    "deliverables": [],
    "evidence": [],
    "prerequisites": [],
    "outcomes": [],
    "market_salary_or_economics": None,
    "market_need": None,
    "job_evolution": None,
    "internal_version": {"context": None, "tools": [], "methods": [], "missions": []},
    "external_version": {"transferable_skills": [], "market_tools": [], "market_practices": [], "outcomes": []},
    "bridge": {"cvln_entities": [], "missions": [], "opportunities": [], "contribution": None},
}


# 30 formations — condensed
FORMATIONS = [
    # POLE 1 — FMS (Factory Maker Studio)
    {
        "code": "FMS-01", "name": "Artist Development", "pole": "FMS",
        "duration_h": 70, "stades": ["graine", "foret"], "cc": 70,
        "badge_name": "Artist Development",
        "prerequisites": "Aucun",
        "debouches": "Artiste FMS, signing potentiel, développement long terme",
        "description": "Former tout être humain avec envie de créer. Identifier leadership artistique, identité forte, régularité.",
        "objective_strategic": "Détecter les talents et leur donner une identité artistique caribéenne solide.",
        "contexts": ["INTERNAL", "EXTERNAL", "BRIDGE"],
        "audience_levels": ["DEBUTANT", "INTERMEDIAIRE", "AVANCE"],
        "positioning_note": "Couche professionnelle universelle de développement artistique, avec couche écosystème vers FMS pour les talents qui veulent contribuer.",
        "bridge_entities": ["FMS"],
        "job_truth": {
            **JOB_TRUTH_TEMPLATE,
            "market_name": "Artiste interprète / artiste entrepreneur",
            "cvln_name": "Artiste FMS",
            "sectors": ["musique", "spectacle vivant", "contenu culturel"],
            "evidence": ["kit presse", "bio trilingue", "showcase", "plan de sortie"],
            "bridge": {"cvln_entities": ["FMS"], "missions": ["showcase", "développement catalogue"], "opportunities": ["signature", "résidence", "collaboration"], "contribution": "Produire une identité artistique prouvable et activable dans FMS."},
        },
        "economics": {**deepcopy(DEFAULT_ECONOMICS)},
        "calibration_sources": DEFAULT_CALIBRATION_SOURCES,
        "modules": [
            {"code": "FMS-01-M01", "name": "Identité artistique et culturelle", "duration_h": 6, "stade": "graine", "hook": "Extrait artiste martiniquais inconnu", "deliverable": "Carte identité artistique trilingue + photo", "frek_signal": "FREK-WORK"},
            {"code": "FMS-01-M02", "name": "Mon univers sonore — références et influences", "duration_h": 5, "stade": "graine", "hook": "Blind test 5 sons caribéens", "deliverable": "Moodboard sonore + note intention 300 mots", "frek_signal": "FREK-WORK"},
            {"code": "FMS-01-M03", "name": "Fondamentaux du son — écoute active", "duration_h": 6, "stade": "pousse", "hook": "Même chanson 3 mix différents", "deliverable": "Analyse écrite de 3 titres avec grille", "frek_signal": "FREK-SCORE"},
            {"code": "FMS-01-M04", "name": "Bio artiste trilingue FR/EN/KR", "duration_h": 5, "stade": "pousse", "hook": "5 bios artistes caribéens", "deliverable": "Bio trilingue validée par peer review", "frek_signal": "FREK-WORK"},
            {"code": "FMS-01-M05", "name": "Photo, image et présence visuelle", "duration_h": 6, "stade": "racine", "hook": "Before/after visuels FMS", "deliverable": "Kit presse 5 visuels + charte couleurs", "frek_signal": "FREK-WORK"},
            {"code": "FMS-01-M06", "name": "Premiers pas sur scène", "duration_h": 8, "stade": "racine", "hook": "Fail vs win sur scène filmés", "deliverable": "Vidéo performance 3 min + auto-évaluation", "frek_signal": "FREK-WORK"},
            {"code": "FMS-01-M07", "name": "Stratégie de sortie — single, EP, album", "duration_h": 7, "stade": "branches", "hook": "Timeline sortie réelle", "deliverable": "Plan de sortie 90 jours détaillé", "frek_signal": "FREK-WORK"},
            {"code": "FMS-01-M08", "name": "Construire sa fanbase — communauté organique", "duration_h": 7, "stade": "branches", "hook": "3 fanbases caribéennes analysées", "deliverable": "Stratégie communauté 3 mois avec KPIs", "frek_signal": "FREK-LINK"},
            {"code": "FMS-01-M09", "name": "Collaborations artistiques", "duration_h": 6, "stade": "arbre", "hook": "Featuring qui a explosé", "deliverable": "Mini-contrat de collaboration", "frek_signal": "FREK-LINK"},
            {"code": "FMS-01-M10", "name": "L'artiste entrepreneur", "duration_h": 6, "stade": "arbre", "hook": "Artiste-business étude cas", "deliverable": "Business plan artiste 3 ans", "frek_signal": "FREK-WORK"},
            {"code": "FMS-01-M11", "name": "Pitch label / investisseur", "duration_h": 4, "stade": "foret", "hook": "Bon vs mauvais pitch", "deliverable": "Pitch deck 10 slides + vidéo 3 min", "frek_signal": "FREK-CERT"},
            {"code": "FMS-01-M12", "name": "Showcase Factory Maker — atelier final", "duration_h": 4, "stade": "foret", "hook": "Showcase live captation", "deliverable": "Showcase public + review par pairs", "frek_signal": "FREK-CONTRIB"},
        ],
    },
    {
        "code": "FMS-02", "name": "Music Business Caribbean", "pole": "FMS",
        "duration_h": 54, "stades": ["pousse", "foret"], "cc": 54,
        "badge_name": "Music Business Caribbean Specialist",
        "prerequisites": "FMS-01 ou 1 an d'expérience artiste/label",
        "debouches": "Label manager CVLN, A&R, coordinateur LabelOS",
        "description": "Comprendre l'écosystème du business musical caribéen. Zouk, gwo-ka, reggae, marchés antillais, guyanais et diaspora.",
        "objective_strategic": "Combler le manque de connaissance des mécanismes économiques musicaux dans la diaspora.",
        "contexts": ["EXTERNAL", "BRIDGE"],
        "audience_levels": ["INTERMEDIAIRE", "AVANCE", "PROFESSIONNEL"],
        "positioning_note": "Formation professionnelle valable sans CVLN, puis passerelle vers LabelOS, FMS, KORA et missions de contribution.",
        "bridge_entities": ["LabelOS", "FMS", "KORA"],
        "job_truth": {
            **JOB_TRUTH_TEMPLATE,
            "market_name": "Chargé de production / label manager musique",
            "cvln_name": "Label manager CVLN / coordinateur LabelOS",
            "sectors": ["industrie musicale", "édition", "distribution", "export culturel"],
            "technical_skills": ["droits musicaux", "distribution digitale", "contrats", "financement", "export"],
            "evidence": ["note marché", "stratégie distribution", "analyse contrats", "dossier financement", "plan export"],
            "external_version": {"transferable_skills": ["structuration label", "gestion catalogue", "négociation", "modèles économiques"], "market_tools": ["DSP", "agrégateurs", "SACEM", "SCPP", "ADAMI"], "market_practices": ["release planning", "gestion des droits", "export"], "outcomes": ["A&R", "label manager", "coordinateur distribution"]},
            "bridge": {"cvln_entities": ["LabelOS", "FMS", "KORA"], "missions": ["audit catalogue", "plan export", "coordination sortie"], "opportunities": ["mission LabelOS", "contribution FMS", "production KORA"], "contribution": "Transformer les compétences marché en preuves puis en missions CVLN."},
        },
        "economics": {**deepcopy(DEFAULT_ECONOMICS), "public_price_eur": 1400, "funding_options": ["entreprise", "OPCO/CPF à confirmer selon montage", "partenaire organisme de formation"]},
        "calibration_sources": DEFAULT_CALIBRATION_SOURCES,
        "modules": [
            {"code": "FMS-02-M01", "name": "Cartographie industrie musicale mondiale 2025", "duration_h": 5, "stade": "pousse", "hook": "Chiffres 2024 chocs", "deliverable": "Mind map annotée de l'industrie", "frek_signal": "FREK-WORK"},
            {"code": "FMS-02-M02", "name": "Spécificités caribéennes — Zouk, Reggae, Gwo-ka", "duration_h": 6, "stade": "pousse", "hook": "3 succès caribéens décortiqués", "deliverable": "Note marché 2 pages Caraïbe", "frek_signal": "FREK-WORK"},
            {"code": "FMS-02-M03", "name": "Droits — SACEM, SCPP, ADAMI en pratique", "duration_h": 5, "stade": "racine", "hook": "Chèque SACEM live", "deliverable": "Rapport droits personnel", "frek_signal": "FREK-SCORE"},
            {"code": "FMS-02-M04", "name": "Distribution digitale — DSP et agrégateurs", "duration_h": 6, "stade": "racine", "hook": "Believe vs IDOL comparés", "deliverable": "Stratégie distribution complète", "frek_signal": "FREK-WORK"},
            {"code": "FMS-02-M05", "name": "Modèles économiques — Stream, Live, Sync, Merch", "duration_h": 6, "stade": "branches", "hook": "Revenus 2024 chiffrés", "deliverable": "Simulateur revenus Excel", "frek_signal": "FREK-WORK"},
            {"code": "FMS-02-M06", "name": "Contrats musicaux — analyse et négociation", "duration_h": 6, "stade": "branches", "hook": "Contrat pièges vus", "deliverable": "Analyse 3 contrats + clauses", "frek_signal": "FREK-SCORE"},
            {"code": "FMS-02-M07", "name": "Financements — CNM, DAC, CTM, OIF, mécénat", "duration_h": 5, "stade": "arbre", "hook": "Grants réels remportés", "deliverable": "Dossier de financement complet", "frek_signal": "FREK-WORK"},
            {"code": "FMS-02-M08", "name": "Marché diaspora — Martinique, France, monde", "duration_h": 5, "stade": "arbre", "hook": "Voyage diaspora Paris/Londres", "deliverable": "Analyse marché diaspora 3 pages", "frek_signal": "FREK-WORK"},
            {"code": "FMS-02-M09", "name": "Monter un label — structures, statuts, ops", "duration_h": 5, "stade": "foret", "hook": "Label indé succès", "deliverable": "Dossier création de label", "frek_signal": "FREK-CERT"},
            {"code": "FMS-02-M10", "name": "Export musical — Afrique, US, Caraïbe anglophone", "duration_h": 5, "stade": "foret", "hook": "Export réussi étude cas", "deliverable": "Plan export 18 mois 2 marchés", "frek_signal": "FREK-CONTRIB"},
        ],
    },
    {"code": "FMS-03", "name": "Beatmaking & Production musicale", "pole": "FMS", "duration_h": 56, "stades": ["graine","arbre"], "cc": 56, "badge_name": "Beatmaker Certifié CVLN", "prerequisites": "Aucun", "debouches": "Producteur FMS, beatmaker catalogue, placements", "description": "Former tout curieux musical. Identifier oreille musicale, créativité, rigueur.", "objective_strategic": "Créer une école beatmaking caribéenne ancrée dans les grooves locaux.", "modules": [{"code": "FMS-03-M01", "name": "Anatomie d'un DAW", "duration_h": 7, "stade": "graine", "hook": "Session live studio", "deliverable": "Loop 4 mesures exportée", "frek_signal": "FREK-WORK"},{"code": "FMS-03-M02", "name": "Théorie musicale sans solfège", "duration_h": 7, "stade": "pousse", "hook": "3 accords 100 hits", "deliverable": "Grille harmonique personnelle", "frek_signal": "FREK-SCORE"},{"code": "FMS-03-M03", "name": "Drum programming — groove caribéen", "duration_h": 7, "stade": "pousse", "hook": "Groove zouk décortiqué", "deliverable": "5 patterns originaux", "frek_signal": "FREK-WORK"},{"code": "FMS-03-M04", "name": "Sampling créatif — éthique et transformation", "duration_h": 7, "stade": "racine", "hook": "Sample flip caribéen", "deliverable": "Beat + doc du sample transformé", "frek_signal": "FREK-WORK"},{"code": "FMS-03-M05", "name": "Sound design — synthèse et identité sonore", "duration_h": 7, "stade": "racine", "hook": "Signature sound producteurs", "deliverable": "Pack 30 sons originaux", "frek_signal": "FREK-WORK"},{"code": "FMS-03-M06", "name": "Mixage home studio", "duration_h": 7, "stade": "branches", "hook": "Mix pro vs amateur A/B", "deliverable": "Beat mixé prêt à diffuser", "frek_signal": "FREK-SCORE"},{"code": "FMS-03-M07", "name": "Catalogue et placements — pitcher ses beats", "duration_h": 7, "stade": "arbre", "hook": "Placement réussi", "deliverable": "Catalogue 10 beats prêts", "frek_signal": "FREK-CONTRIB"},{"code": "FMS-03-M08", "name": "Masterclass FMS — session studio réelle", "duration_h": 7, "stade": "arbre", "hook": "Studio réel Martinique", "deliverable": "Track co-produite complète", "frek_signal": "FREK-CERT"}]},
    {"code": "FMS-04", "name": "Branding artistique", "pole": "FMS", "duration_h": 36, "stades": ["pousse","arbre"], "cc": 36, "badge_name": "Branding Artist", "prerequisites": "Aucun", "debouches": "Directeur artistique, brand manager artiste", "description": "Construire une marque d'artiste durable et cohérente.", "objective_strategic": "Créer des identités visuelles caribéennes fortes qui s'exportent.", "modules": []},
    {"code": "FMS-05", "name": "Management d'artiste", "pole": "FMS", "duration_h": 32, "stades": ["pousse","arbre"], "cc": 32, "badge_name": "Artist Manager", "prerequisites": "FMS-01 recommandé", "debouches": "Manager, tour manager, coordinateur artistique", "description": "Le rôle réel du manager d'artiste, du booking aux finances.", "objective_strategic": "Structurer la profession de manager dans la diaspora.", "modules": []},
    {"code": "FMS-06", "name": "Production exécutive", "pole": "FMS", "duration_h": 28, "stades": ["arbre","foret"], "cc": 56, "badge_name": "Executive Producer Caribéen", "prerequisites": "FMS-02 + FMS-05", "debouches": "EP, senior A&R, directeur artistique holding", "description": "Devenir producteur exécutif culturel caribéen.", "objective_strategic": "Créer une génération de EPs caribéens capables de signer et développer.", "modules": []},
    # POLE 2 — KORA
    {"code": "KOR-01", "name": "Podcast Production", "pole": "KOR", "duration_h": 31, "stades": ["graine","branches"], "cc": 31, "badge_name": "Podcast Producer CVLN", "prerequisites": "Aucun", "debouches": "Producer KORA, animateur podcast diaspora", "description": "Créer un podcast caribéen professionnel, du concept au monétisation.", "objective_strategic": "Peupler KORA de voix caribéennes structurées.", "modules": []},
    {"code": "KOR-02", "name": "Media Storytelling & Cultural Broadcasting", "pole": "KOR", "duration_h": 28, "stades": ["pousse","arbre"], "cc": 28, "badge_name": "Cultural Broadcaster", "prerequisites": "Aucun", "debouches": "Journaliste culturel, storyteller KORA", "description": "Raconter la culture caribéenne avec justesse et impact.", "objective_strategic": "Créer un journalisme culturel caribéen indépendant.", "modules": []},
    # POLE 3 — GMD (Good Mood)
    {"code": "GMD-01", "name": "Festival & événementiel — Good Mood by DJ Sayd", "pole": "GMD", "duration_h": 52, "stades": ["graine","arbre"], "cc": 52, "badge_name": "Festival & Event Producer", "prerequisites": "Aucun", "debouches": "Coordinateur CC2026/CC2027, opérations Good Mood", "description": "Produire des festivals culturels caribéens de A à Z.", "objective_strategic": "Former l'équipe opérationnelle du festival CVLN.", "modules": []},
    # POLE 4 — SAY (DJ SAYD)
    {"code": "SAY-01", "name": "Personal Brand & Cultural Leadership — La voie DJ SAYD", "pole": "SAY", "duration_h": 48, "stades": ["pousse","foret"], "cc": 48, "badge_name": "Cultural Leader CVLN", "prerequisites": "Motivation forte + FREK-ID validé", "debouches": "Ambassadeur diaspora, leader d'entité", "description": "Construire un leadership culturel authentique et durable.", "objective_strategic": "Créer la nouvelle génération de leaders culturels caribéens.", "modules": []},
    # POLE 5 — KLT (Kiltikonet)
    {"code": "KLT-01", "name": "Fondamentaux de la médiation culturelle caribéenne", "pole": "KLT", "duration_h": 42, "stades": ["graine","racine"], "cc": 42, "badge_name": "Kiltikonet Ambassador", "prerequisites": "Aucun", "debouches": "Médiateur culturel, animateur d'atelier", "description": "Devenir ambassadeur de la médiation culturelle caribéenne.", "objective_strategic": "Créer un réseau de médiateurs certifiés à travers la diaspora.", "modules": []},
    {"code": "KLT-02", "name": "Montage et gestion de projets culturels", "pole": "KLT", "duration_h": 56, "stades": ["pousse","arbre"], "cc": 56, "badge_name": "Cultural Project Manager", "prerequisites": "KLT-01 recommandé", "debouches": "Chef de projet culturel, coordinateur événement", "description": "Piloter un projet culturel de l'idée à l'impact.", "objective_strategic": "Structurer la profession de chef de projet culturel caribéen.", "modules": []},
    {"code": "KLT-03", "name": "Stratégie institutionnelle et partenariats", "pole": "KLT", "duration_h": 44, "stades": ["racine","foret"], "cc": 66, "badge_name": "Institutional Strategist", "prerequisites": "KLT-01 + KLT-02", "debouches": "Représentant institutionnel, cultural diplomat", "description": "Naviguer OIF, UNESCO, CARIFESTA, DAC et fonds européens.", "objective_strategic": "Positionner Kiltikonet dans le paysage institutionnel mondial.", "modules": []},
    {"code": "KLT-04", "name": "Gouvernance associative et juridique culturelle", "pole": "KLT", "duration_h": 38, "stades": ["racine","arbre"], "cc": 38, "badge_name": "Governance Associative", "prerequisites": "Aucun", "debouches": "Trésorier, secrétaire général, DAF association", "description": "Loi 1901 et gestion associative culturelle en pratique.", "objective_strategic": "Assurer la conformité et la pérennité des structures culturelles.", "modules": []},
    {"code": "KLT-05", "name": "Kiltikonet comme plateforme — outils numériques et impact diaspora", "pole": "KLT", "duration_h": 40, "stades": ["pousse","foret"], "cc": 40, "badge_name": "Kiltikonet Platform Operator", "prerequisites": "KLT-01 + FRK-01 recommandé", "debouches": "Opérateur plateforme, community manager diaspora", "description": "Opérer Kiltikonet.fr comme infrastructure culturelle diasporique.", "objective_strategic": "Former les opérateurs de l'infrastructure numérique CVLN.", "modules": []},
    # POLE 6 — FRK
    {"code": "FRK-01", "name": "FREK Operator", "pole": "FRK", "duration_h": 31, "stades": ["graine","branches"], "cc": 31, "badge_name": "FREK Operator", "prerequisites": "Aucun", "debouches": "FREK Operator dans chaque entité CVLN", "description": "Opérer l'infrastructure FREK de traçabilité culturelle.", "objective_strategic": "Rendre FREK opérable dès 12 ans, jusqu'aux institutions.", "modules": [{"code": "FRK-01-M01", "name": "Pourquoi la confiance numérique est urgente", "duration_h": 4, "stade": "graine", "hook": "Deepfake caribéen", "deliverable": "Note de cadrage personnelle", "frek_signal": "FREK-WORK"},{"code": "FRK-01-M02", "name": "Anatomie d'une empreinte FREK", "duration_h": 4, "stade": "graine", "hook": "Empreinte live démo", "deliverable": "Schéma FREK annoté", "frek_signal": "FREK-SCORE"},{"code": "FRK-01-M03", "name": "FREK vs blockchain vs NFT vs DRM", "duration_h": 3, "stade": "pousse", "hook": "Débat comparatif", "deliverable": "Tableau comparatif argumenté", "frek_signal": "FREK-WORK"},{"code": "FRK-01-M04", "name": "Créer ses premières empreintes — Kiltikonet.fr", "duration_h": 5, "stade": "pousse", "hook": "Empreinte réelle en 3 min", "deliverable": "5 empreintes FREK documentées", "frek_signal": "FREK-WORK"},{"code": "FRK-01-M05", "name": "Gérer un catalogue FREK", "duration_h": 4, "stade": "racine", "hook": "Catalogue label indé", "deliverable": "Catalogue 20 œuvres taggées", "frek_signal": "FREK-WORK"},{"code": "FRK-01-M06", "name": "FREK dans le workflow créatif quotidien", "duration_h": 4, "stade": "racine", "hook": "Journée type producteur FREK", "deliverable": "Protocole FREK personnel", "frek_signal": "FREK-WORK"},{"code": "FRK-01-M07", "name": "Détecter et signaler des violations", "duration_h": 3, "stade": "branches", "hook": "Vol créatif décortiqué", "deliverable": "Simulation de signalement", "frek_signal": "FREK-SCORE"},{"code": "FRK-01-M08", "name": "FREK-ID et ce qu'il débloque dans CVLN", "duration_h": 4, "stade": "branches", "hook": "Parcours d'un FREK-ID", "deliverable": "Profil FREK complet publié", "frek_signal": "FREK-CERT"}]},
    {"code": "FRK-02", "name": "Digital Provenance Specialist", "pole": "FRK", "duration_h": 28, "stades": ["branches","foret"], "cc": 42, "badge_name": "Digital Provenance Specialist", "prerequisites": "FRK-01", "debouches": "Expert FREK senior, consultant provenance", "description": "Devenir notaire numérique des œuvres culturelles diasporiques.", "objective_strategic": "Créer une expertise juridique nouvelle autour de FREK.", "modules": []},
    {"code": "FRK-03", "name": "Archivage culturel sécurisé", "pole": "FRK", "duration_h": 22, "stades": ["pousse","arbre"], "cc": 22, "badge_name": "Cultural Archivist", "prerequisites": "FRK-01", "debouches": "Archiviste CVLN, gestionnaire patrimoine CIP", "description": "Archiver le patrimoine caribéen avec FREK et standards UNESCO.", "objective_strategic": "Sauvegarder l'oralité caribéenne pour les générations futures.", "modules": []},
    # POLE 7 — LOS (LabelOS)
    {"code": "LOS-01", "name": "Label Operations Manager", "pole": "LOS", "duration_h": 42, "stades": ["pousse","arbre"], "cc": 42, "badge_name": "Label Operations Manager", "prerequisites": "FMS-02 recommandé", "debouches": "Ops manager, catalog manager", "description": "Opérer un label indépendant complet avec LabelOS et Brain.", "objective_strategic": "Créer des managers de label augmentés par l'IA.", "modules": []},
    {"code": "LOS-02", "name": "Metadata & Catalog Management", "pole": "LOS", "duration_h": 26, "stades": ["pousse","arbre"], "cc": 26, "badge_name": "Metadata Specialist", "prerequisites": "Aucun", "debouches": "Metadata specialist labels et distributeurs", "description": "Maîtriser ISRC, ISWC, DDEX pour récupérer les royalties perdues.", "objective_strategic": "Récupérer les royalties perdues de la diaspora caribéenne.", "modules": []},
    {"code": "LOS-03", "name": "AI-Assisted Label Workflow", "pole": "LOS", "duration_h": 26, "stades": ["pousse","arbre"], "cc": 26, "badge_name": "AI Label Operator", "prerequisites": "LOS-01 recommandé", "debouches": "AI ops label, workflow architect", "description": "Automatiser un label avec CVLN Brain et LabelOS.", "objective_strategic": "Positionner les labels caribéens à la pointe de l'IA.", "modules": []},
    # POLE 8 — BRN (CVLN Brain)
    {"code": "BRN-01", "name": "Strategic Ecosystem Design", "pole": "BRN", "duration_h": 32, "stades": ["branches","foret"], "cc": 64, "badge_name": "Ecosystem Strategist", "prerequisites": "3 formations CVLN complétées", "debouches": "Stratège CVLN, directeur d'entité, IPO 2028", "description": "Concevoir et piloter un écosystème économique culturel.", "objective_strategic": "Former les prochains architectes d'écosystèmes caribéens.", "modules": []},
    {"code": "BRN-02", "name": "AI Creative Operations", "pole": "BRN", "duration_h": 32, "stades": ["graine","arbre"], "cc": 32, "badge_name": "AI Creative Operator", "prerequisites": "Aucun", "debouches": "AI operator CVLN, capsule trainer", "description": "Utiliser l'IA générative ancrée dans une identité caribéenne.", "objective_strategic": "Créer une école caribéenne d'IA créative distincte.", "modules": [{"code": "BRN-02-M01", "name": "IA créative en 2026 — état honnête", "duration_h": 5, "stade": "graine", "hook": "Diaporama outils 2025", "deliverable": "Veille 10 outils commentés", "frek_signal": "FREK-WORK"},{"code": "BRN-02-M02", "name": "Prompt créatif — image, son, texte, vidéo", "duration_h": 6, "stade": "pousse", "hook": "Prompt A/B en direct", "deliverable": "Portfolio 20 créations avec prompts", "frek_signal": "FREK-WORK"},{"code": "BRN-02-M03", "name": "IA et identité culturelle — ne pas trahir", "duration_h": 5, "stade": "racine", "hook": "IA qui blanchit un visuel", "deliverable": "Charte IA culturelle personnelle", "frek_signal": "FREK-SCORE"},{"code": "BRN-02-M04", "name": "Intégrer l'IA dans la production musicale", "duration_h": 5, "stade": "racine", "hook": "Track co-générée live", "deliverable": "Projet musique IA documenté", "frek_signal": "FREK-WORK"},{"code": "BRN-02-M05", "name": "IA pour communication et campagnes CVLN", "duration_h": 5, "stade": "branches", "hook": "Campagne IA vs standard", "deliverable": "Campagne IA complète livrée", "frek_signal": "FREK-CONTRIB"},{"code": "BRN-02-M06", "name": "CVLN Brain en pratique — 4 endpoints", "duration_h": 6, "stade": "arbre", "hook": "Brain live", "deliverable": "Projet réel appliqué à Brain", "frek_signal": "FREK-CERT"}]},
    {"code": "BRN-03", "name": "Cultural Intelligence Systems", "pole": "BRN", "duration_h": 24, "stades": ["branches","foret"], "cc": 48, "badge_name": "Cultural Intelligence Architect", "prerequisites": "BRN-01 ou BRN-02", "debouches": "Data architect culturel, directeur observatoire CVLN", "description": "Concevoir des systèmes d'intelligence culturelle.", "objective_strategic": "Doter la Caraïbe d'observatoires culturels souverains.", "modules": []},
    # POLE 9 — AGR
    {"code": "AGR-01", "name": "Transformation agroalimentaire et branding caribéen", "pole": "AGR", "duration_h": 40, "stades": ["pousse","arbre"], "cc": 40, "badge_name": "Agroalimentaire Premium", "prerequisites": "Aucun", "debouches": "Production manager CVL Culinary Innovations", "description": "Transformer les ressources locales en produits premium exportables.", "objective_strategic": "Créer une filière agroalimentaire caribéenne premium.", "modules": []},
    # POLE 10 — BCH
    {"code": "BCH-01", "name": "Blockchain culturelle et tokenisation", "pole": "BCH", "duration_h": 36, "stades": ["pousse","arbre"], "cc": 36, "badge_name": "Cultural Blockchain Specialist", "prerequisites": "FRK-01 recommandé", "debouches": "CVLN Blockchain operator, tokenomics architect", "description": "Tokeniser les actifs culturels caribéens (musique, art, identité).", "objective_strategic": "Architecte de l'économie numérique souveraine caribéenne.", "modules": []},
    # POLE 11 — HOS
    {"code": "HOS-01", "name": "Hospitality, espaces créatifs et expérience immersive", "pole": "HOS", "duration_h": 44, "stades": ["pousse","arbre"], "cc": 44, "badge_name": "Creative Hospitality Manager", "prerequisites": "Aucun", "debouches": "Manager de lieu hybride CVLN, résidence coordinator", "description": "Concevoir des lieux hybrides caribéens studio/résidence/hospitalité.", "objective_strategic": "Créer les tiers-lieux culturels de la Caraïbe.", "modules": []},
    # POLE 12 — GRP
    {"code": "GRP-01", "name": "Ecosystem Entrepreneurship", "pole": "GRP", "duration_h": 28, "stades": ["arbre","foret"], "cc": 84, "badge_name": "Ecosystem Entrepreneur", "prerequisites": "SAY-01 + BRN-01", "debouches": "Co-entrepreneur CVLN, directeur d'entité, candidat IPO 2028", "description": "Entrepreneur d'écosystèmes culturels au niveau holding.", "objective_strategic": "Former les co-fondateurs des prochaines entités CVLN.", "modules": []},
    {"code": "GRP-02", "name": "Cultural Economy & Strategic Partnerships", "pole": "GRP", "duration_h": 26, "stades": ["branches","foret"], "cc": 52, "badge_name": "Cultural Economy Strategist", "prerequisites": "KLT-03 recommandé", "debouches": "Directeur des partenariats CVLN Group", "description": "Maîtriser la political economy de la culture caribéenne.", "objective_strategic": "Faire scaler CVLN de la Martinique au monde en 36 mois.", "modules": []},
    # POLE 13 — CIP
    {"code": "CIP-01", "name": "Standardisation, archivage et gouvernance culturelle", "pole": "CIP", "duration_h": 30, "stades": ["racine","foret"], "cc": 60, "badge_name": "CIP Referent", "prerequisites": "FRK-02 recommandé", "debouches": "Référent CIP Foundation, architecte gouvernance CVLN", "description": "Concevoir les standards de certification culturelle caribéenne.", "objective_strategic": "Doter la Caraïbe de son propre référentiel ISO culturel.", "modules": []},
]



def _apply_academy_os_defaults() -> None:
    for formation in FORMATIONS:
        formation.setdefault("contexts", ["INTERNAL", "BRIDGE"] if "CVLN" in formation.get("debouches", "") else ["EXTERNAL", "BRIDGE"])
        formation.setdefault("audience_levels", ["INTERMEDIAIRE"])
        formation.setdefault("positioning_note", "Legacy intelligent à recalibrer : conserver la vision CVLN et expliciter versions interne, externe et passerelle.")
        formation.setdefault("bridge_entities", [formation.get("pole")])
        formation.setdefault("job_truth", {**deepcopy(JOB_TRUTH_TEMPLATE), "cvln_name": formation.get("debouches"), "outcomes": [formation.get("debouches", "")]})
        formation.setdefault("economics", {**deepcopy(DEFAULT_ECONOMICS)})
        formation.setdefault("calibration_sources", list(DEFAULT_CALIBRATION_SOURCES))
        formation["reconciliation_flags"] = []
        if formation.get("duration_h") != formation.get("cc"):
            formation["reconciliation_flags"].append({
                "type": "HOURS_CC_MISMATCH",
                "message": f"{formation['code']} affiche {formation.get('duration_h')} h pour {formation.get('cc')} CC : à qualifier comme bonus, intensif ou correction."
            })


_apply_academy_os_defaults()

# ------------- BADGES -------------
BADGES = [
    {"code": "BADGE-DECOUVERTE", "name": "Découverte", "tier": "decouverte", "color": "#A37D62", "description": "Entrée écosystème, FREK-ID créé, communauté CVLN.", "cc_threshold": 0, "pole": None, "icon": "sparks"},
    {"code": "BADGE-PARCOURS-10", "name": "Premier parcours", "tier": "decouverte", "color": "#F59E0B", "description": "10 CC accumulés — la voie s'ouvre.", "cc_threshold": 10, "pole": None, "icon": "path"},
    {"code": "BADGE-CC2026-INVITE", "name": "Invité CC2026", "tier": "pole", "color": "#E05A33", "description": "30 CC — invitation à l'événement fondateur CC2026.", "cc_threshold": 30, "pole": None, "icon": "ticket"},
    {"code": "BADGE-MISSION-FIRST", "name": "Première mission", "tier": "pole", "color": "#15803D", "description": "50 CC — première mission freelance dans une entité CVLN.", "cc_threshold": 50, "pole": None, "icon": "briefcase"},
    {"code": "BADGE-SENIOR", "name": "CVLN Senior", "tier": "senior", "color": "#C2410C", "description": "100 CC — livrable pro, éligibilité missions longues.", "cc_threshold": 100, "pole": None, "icon": "star"},
    {"code": "BADGE-EXECUTIVE", "name": "CVLN Executive", "tier": "executive", "color": "#B45309", "description": "150 CC — leadership stratégique, vision globale.", "cc_threshold": 150, "pole": None, "icon": "crown"},
    {"code": "BADGE-FORET", "name": "CVLN Forêt", "tier": "foret", "color": "#064E3B", "description": "300 CC — formateur certifié, patrimoine vivant.", "cc_threshold": 300, "pole": None, "icon": "tree"},
    {"code": "BADGE-EQUITY", "name": "CVLN Founder Circle", "tier": "foret", "color": "#7C2D12", "description": "500 CC — accès discussions equity / holding.", "cc_threshold": 500, "pole": None, "icon": "gem"},
]


# ------------- MISSIONS -------------
MISSIONS = [
    {"code": "MIS-FMS-01", "title": "Prod caribéenne pour KORA", "description": "Produis une capsule sonore de 60 secondes ancrée dans un genre caribéen pour une diffusion KORA.", "pole": "FMS", "cc_reward": 15, "stade_required": "pousse", "entity": "KORA", "status_type": "featured"},
    {"code": "MIS-KLT-01", "title": "Atelier médiation en pied d'immeuble", "description": "Anime un atelier culturel caribéen d'1h dans un quartier de la diaspora. Livrable : reportage 5 min + retour d'expérience.", "pole": "KLT", "cc_reward": 20, "stade_required": "pousse", "entity": "Kiltikonet", "status_type": "open"},
    {"code": "MIS-FRK-01", "title": "20 empreintes FREK pour un artiste", "description": "Aide un artiste caribéen à déposer 20 empreintes FREK sur son catalogue. Livrable : dossier de preuve + retour signé.", "pole": "FRK", "cc_reward": 25, "stade_required": "racine", "entity": "FREK", "status_type": "urgent"},
    {"code": "MIS-BRN-01", "title": "Charte IA culturelle pour Kiltikonet", "description": "Rédige une charte d'usage IA respectueuse de l'identité caribéenne pour Kiltikonet.", "pole": "BRN", "cc_reward": 30, "stade_required": "branches", "entity": "Kiltikonet", "status_type": "open"},
    {"code": "MIS-GMD-01", "title": "Coordinateur bénévole CC2026", "description": "Rejoins l'équipe de coordination du festival CVLN CC2026 — deux jours sur site.", "pole": "GMD", "cc_reward": 40, "stade_required": "racine", "entity": "Good Mood", "status_type": "featured"},
    {"code": "MIS-LOS-01", "title": "Audit metadata 50 tracks", "description": "Nettoie et normalise la metadata de 50 tracks d'un artiste caribéen. Livrable : rapport DDEX + delta royalties estimé.", "pole": "LOS", "cc_reward": 25, "stade_required": "pousse", "entity": "LabelOS", "status_type": "open"},
    {"code": "MIS-SAY-01", "title": "Manifeste de leader culturel", "description": "Rédige et publie ton manifeste de leader culturel caribéen (1 page + vidéo 2 min).", "pole": "SAY", "cc_reward": 20, "stade_required": "pousse", "entity": "DJ SAYD", "status_type": "open"},
    {"code": "MIS-HOS-01", "title": "Concept tiers-lieu caribéen", "description": "Propose un concept complet de tiers-lieu créatif caribéen (10 pages + budget).", "pole": "HOS", "cc_reward": 35, "stade_required": "racine", "entity": "CVLN Hospitality", "status_type": "open"},
]


# ------------- INJECT DETAILED MODULES INTO FORMATIONS -------------
# 25 formations shipped as "coming_soon" get their detailed modules injected here.
# Only fills empty `modules` lists — never overwrites existing detailed modules
# (so FMS-01/02/03, FRK-01 and BRN-02 remain untouched).
from seed_modules import EXTRA_MODULES  # noqa: E402
from catalog_cartography import apply_catalog_cartography  # noqa: E402
from external_calibration import apply_external_calibration  # noqa: E402

for _f in FORMATIONS:
    if not _f.get("modules") and _f["code"] in EXTRA_MODULES:
        _f["modules"] = EXTRA_MODULES[_f["code"]]

apply_catalog_cartography(FORMATIONS)
apply_external_calibration(FORMATIONS)
