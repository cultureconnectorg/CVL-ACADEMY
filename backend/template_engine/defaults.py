"""Default field definitions for the 6 template types (rule 8).

v1 content, editable later via the Admin CMS (rule 14) without a code
change — these are seeded once at startup (see seed.py) so every
deployment has a usable form for each type from day one.
"""

from __future__ import annotations

from typing import List

from .models import TemplateDefinition, TemplateFieldDef

DEFAULT_DEFINITIONS: List[TemplateDefinition] = [
    TemplateDefinition(
        type="diagnostic",
        title="Diagnostic",
        description="Où tu en es aujourd'hui, avant de commencer un parcours.",
        fields=[
            TemplateFieldDef(
                key="situation_actuelle",
                label="Situation actuelle",
                field_type="textarea",
                required=True,
            ),
            TemplateFieldDef(
                key="forces", label="Forces identifiées", field_type="list"
            ),
            TemplateFieldDef(
                key="freins", label="Freins / obstacles", field_type="list"
            ),
            TemplateFieldDef(
                key="objectif_principal",
                label="Objectif principal",
                field_type="text",
                required=True,
            ),
        ],
    ),
    TemplateDefinition(
        type="univers",
        title="Univers",
        description="Poser son univers artistique / professionnel.",
        fields=[
            TemplateFieldDef(
                key="pitch",
                label="Pitch en une phrase",
                field_type="text",
                required=True,
            ),
            TemplateFieldDef(
                key="references", label="Références / inspirations", field_type="list"
            ),
            TemplateFieldDef(key="valeurs", label="Valeurs portées", field_type="list"),
            TemplateFieldDef(
                key="public_cible", label="Public cible", field_type="textarea"
            ),
        ],
    ),
    TemplateDefinition(
        type="positionnement",
        title="Positionnement",
        description="Se situer par rapport au marché et à l'écosystème CVLN.",
        fields=[
            TemplateFieldDef(
                key="proposition_valeur",
                label="Proposition de valeur",
                field_type="textarea",
                required=True,
            ),
            TemplateFieldDef(
                key="concurrents_references",
                label="Concurrents / références marché",
                field_type="list",
            ),
            TemplateFieldDef(
                key="differenciation", label="Différenciation", field_type="textarea"
            ),
        ],
    ),
    TemplateDefinition(
        type="storytelling",
        title="Storytelling",
        description="Construire le récit qui porte le projet.",
        fields=[
            TemplateFieldDef(
                key="origine",
                label="Origine / déclencheur",
                field_type="textarea",
                required=True,
            ),
            TemplateFieldDef(
                key="tension", label="Tension / obstacle central", field_type="textarea"
            ),
            TemplateFieldDef(
                key="transformation",
                label="Transformation visée",
                field_type="textarea",
            ),
            TemplateFieldDef(key="message_cle", label="Message clé", field_type="text"),
        ],
    ),
    TemplateDefinition(
        type="roadmap",
        title="Roadmap",
        description="Le plan d'action à court/moyen terme.",
        fields=[
            TemplateFieldDef(
                key="etapes_30j",
                label="Étapes à 30 jours",
                field_type="list",
                required=True,
            ),
            TemplateFieldDef(
                key="etapes_90j", label="Étapes à 90 jours", field_type="list"
            ),
            TemplateFieldDef(
                key="ressources_necessaires",
                label="Ressources nécessaires",
                field_type="list",
            ),
            TemplateFieldDef(
                key="indicateurs_succes",
                label="Indicateurs de succès",
                field_type="list",
            ),
        ],
    ),
    TemplateDefinition(
        type="dossier",
        title="Dossier",
        description="Le dossier de synthèse final — ce qui accompagne une certification.",
        fields=[
            TemplateFieldDef(
                key="synthese",
                label="Synthèse du parcours",
                field_type="textarea",
                required=True,
            ),
            TemplateFieldDef(
                key="livrables_cles", label="Livrables clés produits", field_type="list"
            ),
            TemplateFieldDef(
                key="competences_demontrees",
                label="Compétences démontrées",
                field_type="list",
            ),
            TemplateFieldDef(
                key="prochaines_etapes",
                label="Prochaines étapes",
                field_type="textarea",
            ),
        ],
    ),
]
