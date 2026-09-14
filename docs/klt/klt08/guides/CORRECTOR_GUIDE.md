# KLT08_CORRECTOR_GUIDE

## Rôle

Évaluer `M01`-`M07` par critère observable (7/7 modules, mise à jour
2026-09-07).

## Points de vigilance spécifiques

| Module | Vigilance particulière |
|---|---|
| M01 | L'audit d'association déjà mené (`KLT-04`/M13) est-il réutilisé, pas reproduit à l'identique ? |
| M02 | Chaque critère de la grille est-il explicitement rattaché à la méthode `KLT-04`/M13 ? |
| M03 | Les disparités réelles entre opérateurs sont-elles préservées, pas lissées ? |
| M04 | Chaque donnée de la fiche de conformité cite-t-elle un endpoint/collection réel ? Aucun score fabriqué en l'absence de données ? |
| M05 | Le support de formation explique-t-il le "comment", pas seulement le "quoi" ? |
| M06 | Chaque recommandation reste-t-elle une proposition, jamais une instruction ? |
| M07 | La non-conformité est-elle documentée et escaladée, jamais corrigée directement par le candidat ? |

## Vigilance transversale — `NO_FAKE_LIVE_CONNECTION` et héritage `KLT-04`/M13

À aucun moment un livrable ne doit laisser entendre qu'une donnée de
conformité réseau agrégée a été consultée **en direct** aujourd'hui —
le schéma réel vérifié peut être cité, mais tout score manipulé doit
rester explicitement `PEDAGOGICAL_ILLUSTRATIVE` — ni qu'une méthode
d'audit a été réinventée sans référence à `KLT-04`/M13. Si un livrable le
suggère, même implicitement, le signaler explicitement au candidat.

## Ce que le correcteur ne fait pas

Ne pas évaluer une compétence hors mandat (audit d'association isolée
sans héritage, déploiement d'opérateurs, médiation, budget projet).
