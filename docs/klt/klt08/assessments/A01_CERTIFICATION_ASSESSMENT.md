# KLT08-A01 — Assessment certificatif

```
ASSESSMENT_ID: KLT08-A01
NAMESPACE: distinct de FMS et des autres formations KLT.
NIVEAU: N2/N3, terminal (= module M07)
COUVERTURE = COMPLÈTE — 7/7 compétences (C1-C7). Mise à jour 2026-09-07 :
C4 construite sur le schéma réel vérifié du Network Kiltikonet,
désormais couverte par cette certification.
```

## Objectif

Prouver que le candidat peut auditer, à l'échelle réseau, plusieurs
opérateurs Kiltikonet en héritant explicitement de la méthode déjà
validée à l'échelle association, suivre honnêtement l'état réel de
conformité agrégé sur le schéma vérifié, sans jamais dépasser le rôle
de recommandation.

## Ce que l'assessment vérifie (et ce qu'il ne vérifie pas)

Vérifie l'articulation de `C1` à `C7`, y compris `C4` (suivi de
conformité réseau agrégée sur le schéma réel vérifié du Network, sans
jamais fabriquer une connexion live). **Ne vérifie pas** une connexion
live Academy↔Network réel — cette connexion n'existe pas et n'est
jamais simulée. Ne vérifie pas non plus l'audit d'une association
individuelle isolée (`KLT-04`/M13 reste la référence, réutilisée par
héritage), le déploiement d'opérateurs (`KLT-07`), la médiation terrain
(`KLT-01`), ni la gestion de projet (`KLT-02`).

## Format du dossier professionnel attendu

| Section | Contenu attendu | Origine |
|---|---|---|
| Échelle | Note de cadrage échelle | M01 |
| Grille | Grille d'audit réseau | M02 |
| Consolidation | Vue consolidée réseau | M03 |
| Conformité | Fiche de suivi de conformité (schéma réel vérifié) | M04 |
| Formation | Support de formation opérateurs | M05 |
| Recommandations | Note de recommandations | M06 |
| Non-conformité | Rapport de non-conformité réseau | M07 |

## Conditions d'échec explicites

- La grille d'audit réseau ne fait aucune référence explicite à la
  méthode `KLT-04`/M13 (M02) → non conforme, éliminatoire.
- La vue consolidée lisse une disparité réelle plutôt que de la
  préserver (M03) → éliminatoire.
- Une recommandation est formulée comme une instruction impérative
  (M06) → éliminatoire.
- Une non-conformité est corrigée directement par le candidat plutôt que
  documentée et escaladée (M07) → éliminatoire.
- Une donnée de conformité réseau agrégée est présentée comme réellement
  observée en direct alors qu'elle est `PEDAGOGICAL_ILLUSTRATIVE`, ou
  fabriquée en l'absence de donnée réelle (M04) → éliminatoire.

## Ce que la réussite délivre — et ne délivre pas

Évaluation **Academy complète** (7/7 compétences). **Aucun badge
existant** pour `KLT-08` — formation `NEW`, sans legacy. Ni RNCP, ni
preuve d'une connexion live Academy↔Network réel (`FULLY_COMPLETE`
reste `FALSE`).
