# CVE-12 — Assessment & Rubric

Structure identique à `../cve02/ASSESSMENT_AND_RUBRIC.md` (N1 40% /
N2 30% / livrable 30%, même `../CERTIFICATION_MODEL.md`).

## Compétences évaluées

| Compétence | Description |
|---|---|
| C1 | Les 3 axes réseau exacts (§3.2) et leur justification |
| C2 | Facteur de vélocité comme signal de croissance réseau |
| C3 | Discipline de périmètre — aucune mesure de centralité de graphe n'existe dans le spec |

## Rubric (0–4 par compétence)

| Niveau | Description |
|---|---|
| 0 | Invente une mesure de centralité de graphe, ou classe un mauvais axe comme réseau |
| 1 | Axes ou justification imprécis |
| 2 | Axes corrects mais discipline de périmètre absente |
| 3 | Complet et vérifié, imprécision mineure tolérée |
| 4 | Cite §3.2 précisément, renvoie vers CVE-07 sans re-dériver |

## Règle éliminatoire

Toute mesure de centralité de graphe inventée, ou tout axe mal classé
comme réseau, entraîne un 0 automatique.

## Seuil de passage

Moyenne ≥ 2.5/4, aucune compétence à 0 par élimination.
