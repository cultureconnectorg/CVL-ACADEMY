# Kiltikonet Master Portfolio Map

```
Vue unique des 5 formations construites + 3 planifiées. Chiffres
recomptés sur le corpus réel (find/grep), pas recopiés d'un README.
```

| `KLT_CODE` | `TITLE` | `TARGET_ROLE` (ROME) | `PURPOSE` | `LEVEL` | `CONTEXT` (`db.formations`) | `MODULE_COUNT` | `COMPETENCY_COUNT` | `ASSESSMENT_MODEL` | `CERTIFICATION_MODEL` | `PRODUCT_DEPENDENCIES` | `STATUS` | `VALIDATION_STATUS` |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `KLT-01` | Médiateur culturel | `k1213`/`k1206`, confiance `high` | Concevoir et conduire une médiation culturelle de terrain | Fondamentaux | `EXTERNAL, BRIDGE` | 11 | 11 | N1(15)+N2(8)+`KLT01-A01` | Academy, `badge=DISPLAY_ONLY_LEGACY` | Culture Connect, Network, Observatory, FREK | `BUILT` | `NOT_VALIDATED` |
| `KLT-02` | Chef de projet culturel | `k1808`/`e1107`, `high` | Piloter un projet culturel du cadrage au bilan | Professionnalisation | `EXTERNAL, BRIDGE` | 11 | 11 | N1(13)+N2(6)+`KLT02-A01` | Academy, `badge=DISPLAY_ONLY_LEGACY` | Network, Observatory | `BUILT` | `NOT_VALIDATED` |
| `KLT-03` | Partenariats institutionnels culturels | `k1808`/`k1802`, `medium` | Construire et défendre une stratégie institutionnelle | Avancé | `INTERNAL, EXTERNAL, BRIDGE` | 12 | 12 | N1(13)+N2(6)+`KLT03-A01` | Academy, `badge=DISPLAY_ONLY_LEGACY` | Network, Observatory, Pro space | `BUILT` | `NOT_VALIDATED` — priorité experte (institutions réelles) |
| `KLT-04` | Gouvernance des organisations et réseaux culturels | `k1808`/`k1604`, `low` | Assurer la gouvernance associative et son extension réseau | Professionnalisation → Opérationnel | `EXTERNAL, BRIDGE` (`PROPOSE_CHANGE +INTERNAL`, non appliqué) | 14 | 14 | N1(13)+N2(5)+`KLT04-A01` | Academy, `badge=DISPLAY_ONLY_LEGACY` | Network, Compliance, Audits | `BUILT` | `NOT_VALIDATED` — priorité experte (droit/fiscal) |
| `KLT-05` | Opérateur Kiltikonet / Cultural Platform Operator | `e1124`/`k1808`, `medium` | Opérer une présence numérique culturelle dans les limites d'un rôle | Opérationnel | `INTERNAL, BRIDGE` (`PROPOSE_CHANGE +EXTERNAL`, non appliqué) | 11 | 11 | N1(12)+N2(5)+`KLT05-A01` | Academy, `badge=DISPLAY_ONLY_LEGACY`, `OPERATOR_AUTHORIZATION=NOT_GRANTED` | Core platform, Auth/RBAC, Badges/NFC, Observatory, Admin/alerts | `BUILT` | `NOT_VALIDATED` |
| `KLT-06` | Analyste Observatory / Cultural Data Analyst | — | Lire et analyser les signaux du réseau Kiltikonet | Avancé | non défini | 0 | 0 | — | — | Observatory (bloquant) | `PLANNED` | `N/A` |
| `KLT-07` | Responsable déploiement territorial culturel | — | Déployer des opérateurs sur de nouveaux territoires | Avancé | non défini | 0 | 0 | — | — | Network (bloquant) | `PLANNED` | `N/A` |
| `KLT-08` | Responsable qualité, conformité & audit réseau | — | Auditer la conformité à l'échelle réseau | Avancé | non défini | 0 | 0 | — | — | Compliance/Audits (bloquant) | `PLANNED` | `N/A` |

## Totaux (corpus construit, KLT-01→05)

```
FORMATIONS_BUILT = 5
MODULES_TOTAL = 59  (11+11+12+14+11)
COMPETENCIES_TOTAL = 59  (une par module, 1:1 partout)
DOCUMENTS_TOTAL = 139  (27+27+28+30+27)
N1_QUESTIONS_TOTAL = 66  (15+13+13+13+12)
N2_EVALUATIONS_TOTAL = 30  (8+6+6+5+5)
CERTIFICATION_ASSESSMENTS = 5  (un KLTxx-A01 par formation)
```

## Ce que ce tableau ne dit pas — à lire dans les documents dédiés

`VALIDATION_STATUS = NOT_VALIDATED` est un statut unique et volontairement
grossier ici — le détail (quels éléments précis, classés `VERIFIED` /
`NEEDS_CURRENT_SOURCE` / `NEEDS_EXPERT_REVIEW` / `OUTDATED` /
`UNRESOLVED`) vit dans `91_VALIDATION/EXTERNAL_VALIDATION_REGISTER.md`
et `91_VALIDATION/KILTIKONET_FIELD_VALIDATION_REGISTER.md`. Ne jamais
lire `STATUS = BUILT` comme une garantie de validité métier —
`STRUCTURAL_COMPLETENESS != EXTERNAL_VALIDATION`, voir `README.md`.
