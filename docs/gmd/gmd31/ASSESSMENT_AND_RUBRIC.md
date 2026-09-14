# GMD-31 — Assessment & Rubric

Structure identique à `../gmd21/ASSESSMENT_AND_RUBRIC.md` (N1 40% /
N2 30% / livrable 30%).

## Compétences évaluées

| Compétence | Description |
|---|---|
| C1 | Littéracie du payload (`source`, `interaction_type`, `identifier`, `event`) |
| C2 | Littéracie du calendrier de retry (5 backoffs exacts, seuil `failed`) |
| C3 | **Discipline de frontière** — jamais confondre `frek_service.py` (Good Mood) avec `backend/services/frek_core.py` (cette Academy) |

## Rubric (0–4 par compétence)

| Niveau | Description |
|---|---|
| 0 | Confond les deux systèmes FREK, ou invente une route de relance manuelle |
| 1 | Backoffs approximatifs, pas les valeurs exactes |
| 2 | Payload correct mais calendrier de retry imprécis |
| 3 | Complet et vérifié, imprécision mineure tolérée |
| 4 | Cite `frek_service.py` ligne par ligne pour chaque affirmation |

## Règle éliminatoire (C3 spécifiquement)

**C3 est éliminatoire** — un candidat qui confond les deux systèmes
FREK échoue automatiquement cette formation, quel que soit le reste de
la copie, car c'est exactement le risque de
`CROSS_DOMAIN_CONTAMINATION` que ce Master Package existe pour
prévenir.

## Seuil de passage

Moyenne ≥ 2.5/4, C3 jamais à 0.
