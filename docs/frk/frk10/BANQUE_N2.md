# FRK-10 — Banque N2 (littératie, non certifiante)

## Cas N2-1 — Application hors UE

Un candidat demande si eIDAS2/EUDI s'applique à un projet non-UE.
Réponds avec la discipline de juridiction.

**Critères de notation :** explique que ce cadre est spécifique à
l'UE/EEE (Règlement (UE) 2024/1183), jamais présenté comme universel.
Élimination si le candidat généralise sans réserve.

## Cas N2-2 — Certification sans expert

Un candidat veut être certifié FRK-10 sans révision d'expert
réglementaire. Explique pourquoi ce n'est pas possible aujourd'hui.

**Critères de notation :** cite `NEEDS_EXPERT_REVIEW` non résolu comme
blocage explicite ; précise que seule une vérification de littératie
existe, sans Skill ID délivré.

## Cas N2-3 — Divulgation sélective en pratique

Un relying party demande à un détenteur de wallet de prouver qu'il a
plus de 18 ans, sans révéler sa date de naissance exacte ni son
adresse. Explique comment SD-JWT permet cela techniquement.

**Critères de notation :** identifie que chaque attribut (âge, date de
naissance, adresse) est une disclosure hachée séparée dans le SD-JWT ;
le détenteur ne révèle que la disclosure nécessaire (ou un dérivé
prouvant "≥ 18 ans" si le schéma le permet) accompagnée du key-binding
JWT, sans exposer les autres disclosures ni la credential complète.
Élimination si le candidat décrit un partage de la credential entière.
