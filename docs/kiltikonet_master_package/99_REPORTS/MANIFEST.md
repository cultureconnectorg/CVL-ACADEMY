# Manifest — CVLN Kiltikonet Master Package v1

```
Inventaire exhaustif des fichiers NOUVEAUX créés par ce ticket. Le
corpus pédagogique existant (docs/klt/, 140 fichiers avec README) n'est
pas reproduit ici — voir MASTER_INDEX.md pour y naviguer.
```

## Fichiers créés par ce ticket (26)

| # | Chemin (relatif à `docs/kiltikonet_master_package/`) | Rôle |
|---|---|---|
| 1 | `README.md` | Vue d'ensemble, provenance, structure |
| 2 | `00_MASTER/MASTER_INDEX.md` | Point d'entrée navigable |
| 3 | `00_MASTER/KILTIKONET_MASTER_PORTFOLIO_MAP.md` | Vue unique des 5+3 formations |
| 4 | `00_MASTER/CROSS_KLT_COMPETENCY_MAP.md` | 7 familles de compétences transversales |
| 5 | `00_MASTER/KILTIKONET_PROFESSIONAL_PATHWAY.md` | Progression entre métiers |
| 6 | `00_MASTER/MASTER_ASSESSMENT_ARCHITECTURE.md` | Consolidation N1/N2/A01/Rubrics |
| 7 | `00_MASTER/KILTIKONET_MASTER_SKILL_REGISTRY.md` | Les 59 skill IDs, verbatim |
| 8 | `00_MASTER/MASTER_EVIDENCE_MODEL.md` | 4 concepts de preuve distingués |
| 9 | `00_MASTER/CERTIFICATION_ARCHITECTURE.md` | 6 concepts de certification distingués |
| 10 | `00_MASTER/OPERATOR_AUTHORIZATION_ARCHITECTURE.md` | Architecture future, non implémentée |
| 11 | `01_KLT01_MEDIATEUR_CULTUREL/INDEX.md` | Pointeur + statut `KLT-01` |
| 12 | `02_KLT02_CHEF_PROJET_CULTUREL/INDEX.md` | Pointeur + statut `KLT-02` |
| 13 | `03_KLT03_PARTENARIATS_INSTITUTIONNELS/INDEX.md` | Pointeur + statut `KLT-03` |
| 14 | `04_KLT04_GOUVERNANCE_RESEAUX/INDEX.md` | Pointeur + statut `KLT-04` |
| 15 | `05_KLT05_OPERATEUR_KILTIKONET/INDEX.md` | Pointeur + statut `KLT-05` |
| 16 | `06_KLT06_PLANNED/PLANNED.md` | Emplacement futur, aucun contenu |
| 17 | `07_KLT07_PLANNED/PLANNED.md` | Emplacement futur, aucun contenu |
| 18 | `08_KLT08_PLANNED/PLANNED.md` | Emplacement futur, aucun contenu |
| 19 | `90_SHARED/KILTIKONET_CASE_UNIVERSE_MAP.md` | Cas fil rouge multi-métiers |
| 20 | `91_VALIDATION/EXTERNAL_VALIDATION_REGISTER.md` | `KLT-03`/`KLT-04` à sourcer/vérifier |
| 21 | `91_VALIDATION/KILTIKONET_FIELD_VALIDATION_REGISTER.md` | 4 niveaux de validation terrain |
| 22 | `92_INTEGRATION/KILTIKONET_ACADEMY_INTEGRATION_MAP.md` | Chemin d'import théorique |
| 23 | `92_INTEGRATION/KILTIKONET_PRODUCT_DEPENDENCY_MAP.md` | 8 domaines produit classifiés |
| 24 | `93_QUALITY/MASTER_QUALITY_GATES.md` | Gates locaux + transversaux |
| 25 | `99_REPORTS/MANIFEST.md` | Ce document |
| 26 | `99_REPORTS/CHANGELOG.md` | Historique des tickets |

Plus, à la racine `docs/` : `KILTIKONET_MASTER_PACKAGE_V1_REPORT.md`
(livrable final, hors arborescence du package lui-même, comme demandé).

## Fichiers du corpus pédagogique réutilisés (non copiés)

`docs/klt/klt01/` à `docs/klt/klt05/` (139 documents) + `docs/klt/
README.md` + `docs/KILTIKONET_KLT0001_CANONICAL_EDUCATION_MAP.md` à
`docs/KILTIKONET_KLT0004_KLT01_PEDAGOGICAL_BUILD_REPORT.md` (4
documents de gouvernance) — voir `MASTER_INDEX.md` pour la navigation
complète, aucun n'est dupliqué dans ce Master Package.

## Vérification d'intégrité

```bash
find docs/klt -type f | wc -l          # attendu : 140
find docs/klt/klt01 -type f | wc -l    # attendu : 27
find docs/klt/klt02 -type f | wc -l    # attendu : 27
find docs/klt/klt03 -type f | wc -l    # attendu : 28
find docs/klt/klt04 -type f | wc -l    # attendu : 30
find docs/klt/klt05 -type f | wc -l    # attendu : 27
find docs/kiltikonet_master_package -type f | wc -l  # attendu : 26
```

Résultats réels dans `docs/KILTIKONET_MASTER_PACKAGE_V1_REPORT.md`.
