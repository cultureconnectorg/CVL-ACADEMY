# KLT08-A01 — Assessment certificatif (partiel)

```
ASSESSMENT_ID: KLT08-A01
NAMESPACE: distinct de FMS et des autres formations KLT.
NIVEAU: N2/N3, terminal du périmètre buildable (= module M07)
COUVERTURE = PARTIELLE — 6/7 compétences (C1-C3, C5-C7). C4 (BLOCKED,
Compliance non implémentée) n'est PAS couverte par cette certification.
```

## Objectif

Prouver que le candidat peut auditer, à l'échelle réseau, plusieurs
opérateurs Kiltikonet en héritant explicitement de la méthode déjà
validée à l'échelle association, sans jamais dépasser le rôle de
recommandation.

## Ce que l'assessment vérifie (et ce qu'il ne vérifie pas)

Vérifie l'articulation de `C1`, `C2`, `C3`, `C5`, `C6`, `C7`. **Ne
vérifie pas** `C4` (suivi de conformité réseau agrégée réelle) — hors
périmètre tant que `Compliance` reste `NOT_IMPLEMENTED`. Ne vérifie pas
non plus l'audit d'une association individuelle isolée (`KLT-04`/M13
reste la référence, réutilisée par héritage), le déploiement
d'opérateurs (`KLT-07`), la médiation terrain (`KLT-01`), ni la gestion
de projet (`KLT-02`).

## Format du dossier professionnel attendu

| Section | Contenu attendu | Origine |
|---|---|---|
| Échelle | Note de cadrage échelle | M01 |
| Grille | Grille d'audit réseau | M02 |
| Consolidation | Vue consolidée réseau | M03 |
| Formation | Support de formation opérateurs | M05 |
| Recommandations | Note de recommandations | M06 |
| Non-conformité | Rapport de non-conformité réseau | M07 |
| Réflexif | Ce que ce parcours ne couvre pas (C4) et pourquoi | tous |

## Conditions d'échec explicites

- La grille d'audit réseau ne fait aucune référence explicite à la
  méthode `KLT-04`/M13 (M02) → non conforme, éliminatoire.
- La vue consolidée lisse une disparité réelle plutôt que de la
  préserver (M03) → éliminatoire.
- Une recommandation est formulée comme une instruction impérative
  (M06) → éliminatoire.
- Une non-conformité est corrigée directement par le candidat plutôt que
  documentée et escaladée (M07) → éliminatoire.
- Une donnée de conformité réseau agrégée est simulée à un moment
  quelconque du dossier → éliminatoire.

## Ce que la réussite délivre — et ne délivre pas

Évaluation **Academy partielle** (6/7 compétences). **Aucun badge
existant** pour `KLT-08` — formation `NEW`, sans legacy. Ni RNCP, ni
certification complète tant que `C4` reste `BLOCKED`.
