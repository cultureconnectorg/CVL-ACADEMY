"""ACA-0005 §9 — Initial lineage matrix.

Generates one `NO_EQUIVALENCE` record per legacy FMS module (53 total,
`FMS-01`..`FMS-06`, read live from `seed_data.FORMATIONS` — never a
hardcoded copy that could drift from what the app actually serves),
paired positionally against the same-numbered canonical module (from
`FMS_Chantier_Complet_20260822.zip`, titles captured during the
`ACA-0003` delta audit — see `docs/ACADEMY_FMS_CANONICAL_DELTA_MATRIX.md`
§2 for the full FMS-01 title list and the method).

**Why every seeded record is `NO_EQUIVALENCE`, never `RELATED`:**
mission §9 allows `RELATED` "seulement si une preuve textuelle réelle
justifie" it. Establishing that rigorously, module-by-module, across 53
legacy modules is a real pedagogical judgment call this pass is not
authorized to make on its own (`PEDAGOGICAL_EQUIVALENCE_INFERENCE =
FORBIDDEN`) — it belongs to the Founder/pedagogy team using this same
`module_lineage` collection's `update_lineage` API, with real evidence,
after this seed exists. The evidence text on every seeded record names
both titles side by side specifically so that follow-up review is easy.

**Idempotent by construction**: each record's `lineage_id` is derived
deterministically from its own (legacy code, canonical code, version) —
re-running this seed never creates duplicates and, critically, never
overwrites a record a human has since edited via the API (upsert only
inserts when the id doesn't exist yet; it never updates).
"""

from __future__ import annotations

import hashlib
import logging
from typing import Dict, List, Tuple

from db import db
from seed_data import FORMATIONS

from .models import CANONICAL_VERSION_CURRENT, ModuleLineage

logger = logging.getLogger("cvln.fms_lineage")

SEED_CREATED_BY = "system:aca-0005-initial-matrix"

# Canonical module titles captured during the ACA-0003 delta audit
# (`docs/ACADEMY_FMS_CANONICAL_DELTA_MATRIX.md`), read directly from
# `Master_Module_Map.md` for each métier in `FMS_Chantier_Complet_20260822.zip`.
# Position in each list is the module number (index 0 == M01).
CANONICAL_MODULE_TITLES: Dict[str, List[str]] = {
    "FMS-01": [
        "Introduction au métier d'Artist Development",
        "Comprendre le diagnostic artistique",
        "Réaliser un diagnostic artistique encadré",
        "Clarifier un univers artistique",
        "Positionner un artiste sur le marché",
        "Construire le fond narratif",
        "Diagnostic artistique autonome",
        "Univers & Identité : arbitrage de directions concurrentes",
        "Positionnement stratégique différenciant",
        "Storytelling : fond narratif complet",
        "Roadmap & trajectoire de développement",
        "Dossier de présentation complet (pitch, bio, artist statement)",
        "Artist Development multi-projets : priorisation des diagnostics et trajectoires",
        "Spécialisation Caraïbe & Diaspora",
        "Artist Development dans l'écosystème CVLN (module Bridge)",
    ],
    "FMS-02": [
        "Introduction au métier de Music Business",
        "Comprendre l'analyse économique d'un projet artistique",
        "Réaliser une analyse de marché encadrée",
        "Lire et négocier un contrat structurant",
        "Construire un premier business model",
        "Cartographier une stratégie de distribution",
        "Choisir une structure juridique adaptée",
        "Analyse de marché autonome (V2)",
        "Contrat défendu (négociation argumentée)",
        "Business model & financement défendus",
        "Stratégie de distribution complète",
        "Structuration juridique complète",
        "Dossier complet + Pitch (simulation d'examen, sans certification)",
        "Music Business multi-projets (Avancé, optionnel)",
        "Spécialisation Export International (optionnel)",
        "Music Business dans l'écosystème CVLN (module Bridge, optionnel)",
    ],
    "FMS-03": [
        "Introduction au métier de Music Production",
        "Bases du DAW et de la production",
        "Recevoir et lire une direction artistique",
        "Composition & Arrangement encadrés",
        "Production sonore encadrée",
        "Enregistrement & Édition encadrés",
        "Mixage & Mastering encadrés",
        "Direction artistique autonome (V2)",
        "Composition & Arrangement défendus",
        "Production sonore défendue",
        "Enregistrement & Édition sous pression",
        "Mixage & Mastering sous standards contestés",
        "Livraison complète + Documentation (simulation d'examen, sans certification)",
        "Mixage & Mastering avancés, production multi-styles (Avancé, optionnel)",
        "Production dans les esthétiques Caraïbe/diaspora (Spécialisation, optionnel)",
        "Music Production dans l'écosystème CVLN (Bridge — FREKansla)",
    ],
    "FMS-04": [
        "Introduction au métier d'Artist Branding",
        "Théorie de la marque appliquée aux artistes",
        "Recevoir une identité & construire une brand platform encadrée",
        "Direction visuelle encadrée",
        "Stratégie éditoriale encadrée",
        "Stratégie réseaux sociaux encadrée",
        "Conception de campagne encadrée",
        "Brand platform autonome (V2)",
        "Direction visuelle défendue",
        "Stratégie éditoriale défendue",
        "Réseaux sociaux sous pression de viralité",
        "Campagne face à un partenariat incohérent",
        "Dossier complet + Défense (simulation d'examen, sans certification)",
        "Gestion de crise et communication de marque (Avancé, optionnel)",
        "Codes visuels et culturels Caraïbe/diaspora (Spécialisation, optionnel)",
        "Artist Branding dans l'écosystème CVLN (Bridge)",
    ],
    "FMS-05": [
        "Introduction au métier d'Artist Management",
        "Bases de la gestion de projet appliquée à un artiste",
        "Recevoir le cadre & planning encadré",
        "Négociation opérationnelle encadrée",
        "Coordination encadrée",
        "Budget opérationnel encadré",
        "Arbitrage d'opportunités encadré",
        "Planning autonome (V2)",
        "Négociation défendue",
        "Coordination défendue",
        "Budget sous pression",
        "Arbitrage sous pression réelle",
        "Dossier complet + Défense (simulation d'examen, sans certification)",
        "Tour Management & gestion de crise (Avancé, optionnel)",
        "Release Management ou marché Caraïbe/diaspora (Spécialisation, optionnel)",
        "Artist Management dans l'écosystème CVLN (Bridge)",
    ],
    "FMS-06": [
        "Introduction au métier d'Executive/Cultural Production",
        "Logique d'un projet culturel",
        "Conception de projet encadrée",
        "Ingénierie de financement encadrée",
        "Gouvernance encadrée",
        "Gestion des risques encadrée",
        "Arbitrage de portefeuille encadré",
        "Conception de projet autonome (V2)",
        "Financement défendu",
        "Gouvernance défendue",
        "Pilotage sous risque réel",
        "Arbitrage de portefeuille sous pression réelle",
        "Cultural Venture Board (simulation d'examen, sans certification)",
        "Pilotage multi-projets & Expert/Executive (Avancé, optionnel)",
        "Coopération Caraïbe/diaspora & Développement territorial (Spécialisation, optionnel)",
        "Executive Production dans l'écosystème CVLN (Bridge)",
    ],
}


def _canonical_module_code(formation_code: str, position_index: int) -> str:
    """`FMS-01`, 0 -> `FMS01-M01` — canonical's own no-hyphen convention
    (confirmed in `fms_import/module_map.py`'s own regex)."""
    metier_no = formation_code.split("-")[-1]
    return f"FMS{metier_no}-M{position_index + 1:02d}"


def _deterministic_id(legacy_code: str, canonical_code: str, version: str) -> str:
    digest = hashlib.sha256(
        f"{legacy_code}|{canonical_code}|{version}".encode()
    ).hexdigest()[:24]
    return f"seed-aca0005-{digest}"


def build_initial_records() -> List[ModuleLineage]:
    """Pure function — no I/O. Returns the records `seed_initial_matrix`
    would write, for tests and for review before writing anything."""
    records: List[ModuleLineage] = []
    by_code = {f["code"]: f for f in FORMATIONS}

    for formation_code, canonical_titles in CANONICAL_MODULE_TITLES.items():
        legacy_formation = by_code.get(formation_code)
        if not legacy_formation:
            logger.warning(
                "initial_matrix: %s not found in seed_data.FORMATIONS", formation_code
            )
            continue

        for position_index, legacy_module in enumerate(
            legacy_formation.get("modules", [])
        ):
            if position_index >= len(canonical_titles):
                # Legacy has fewer modules than canonical at every métier
                # (docs/ACADEMY_FMS_CANONICAL_DELTA_MATRIX.md §1) — never
                # fabricate a canonical pairing past the legacy list's own
                # length in the other direction (irrelevant here, legacy
                # is always shorter, kept as a defensive bound).
                break

            canonical_code = _canonical_module_code(formation_code, position_index)
            canonical_title = canonical_titles[position_index]
            legacy_code = legacy_module["code"]
            legacy_title = legacy_module["name"]

            record = ModuleLineage(
                lineage_id=_deterministic_id(
                    legacy_code, canonical_code, CANONICAL_VERSION_CURRENT
                ),
                legacy_formation_code=formation_code,
                legacy_module_code=legacy_code,
                canonical_formation_code=formation_code,
                canonical_module_code=canonical_code,
                canonical_version=CANONICAL_VERSION_CURRENT,
                relation="NO_EQUIVALENCE",
                status="active",
                created_by=SEED_CREATED_BY,
                evidence=(
                    f"Positional pairing only (position {position_index + 1}), "
                    f"not equivalence: legacy '{legacy_title}' vs canonical "
                    f"'{canonical_title}' are different pedagogy — see "
                    f"docs/ACADEMY_FMS_CANONICAL_DELTA_MATRIX.md §2."
                ),
                notes=(
                    "Seeded by ACA-0005 initial matrix. Reviewable/upgradeable "
                    "to RELATED or MANUAL_EQUIVALENCE via the lineage API by "
                    "an authorized human with real evidence — never inferred "
                    "automatically."
                ),
            )
            records.append(record)

    return records


async def seed_initial_matrix() -> Tuple[int, int]:
    """Idempotent: inserts only records whose deterministic id doesn't
    already exist. Never updates or overwrites an existing record — a
    record a human has since edited via the API keeps that edit forever,
    even across repeated seed runs. Returns (inserted, skipped)."""
    records = build_initial_records()
    inserted = 0
    skipped = 0
    for record in records:
        result = await db.module_lineage.update_one(
            {"lineage_id": record.lineage_id},
            {"$setOnInsert": record.model_dump()},
            upsert=True,
        )
        if result.upserted_id is not None:
            inserted += 1
        else:
            skipped += 1
    logger.info(
        "module_lineage initial matrix: %d inserted, %d already present",
        inserted,
        skipped,
    )
    return inserted, skipped
