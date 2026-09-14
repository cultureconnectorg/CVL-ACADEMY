# FRK-68 — Assessment & Rubric

Structure identique à `docs/frk/frk01/ASSESSMENT_AND_RUBRIC.md` (N1
40% / N2 30% / livrable 30%, même `../CERTIFICATION_MODEL.md`).

## Compétences évaluées

| Compétence | Description |
|---|---|
| C1 | Littératie `db.frek_signals` (cette Academy) |
| C2 | Littératie des statuts d'outbox (Good Mood) et du schedule de retry |
| C3 | Discipline des trois systèmes séparés |

## Rubric (0–4 par compétence)

| Niveau | Description |
|---|---|
| 0 | Fusionne les trois tables en un pipeline unique, ou invente un retry infini |
| 1 | Attribue une entrée à la mauvaise table/système |
| 2 | Littératie correcte mais schedule de retry imprécis |
| 3 | Complet et vérifié, imprécision mineure tolérée |
| 4 | Cite `frek_core.py`/`docs/gmd/gmd31`/`gmd32` ligne par ligne |

## Règle éliminatoire

Toute fusion des trois systèmes, ou tout mécanisme de retry inventé,
entraîne un 0 automatique.

## Seuil de passage

Moyenne ≥ 2.5/4, aucune compétence à 0 par élimination.
