# FRK-03 — Assessment & Rubric

Structure identique à `docs/frk/frk01/ASSESSMENT_AND_RUBRIC.md` (N1
40% / N2 30% / livrable 30%, même `../CERTIFICATION_MODEL.md`).

## Compétences évaluées

| Compétence | Description |
|---|---|
| C1 | Littératie des headers `FREK_PROOF_MAPPING` réels |
| C2 | Opération des effets de bord (`db.frek_signals`, `db.counters`) |
| C3 | Discipline `READY_FOR_FREK_PROOF = FALSE` |

## Rubric (0–4 par compétence)

| Niveau | Description |
|---|---|
| 0 | Invente une ancre externe vérifiable, ou affirme `READY_FOR_FREK_PROOF = TRUE` sans preuve |
| 1 | Confond l'intention de signal (header) avec une preuve vérifiée |
| 2 | Littératie correcte mais imprécision sur les effets de bord réels |
| 3 | Complet et vérifié, imprécision mineure tolérée |
| 4 | Cite `frek_core.py`/un header KOR réel ligne par ligne |

## Règle éliminatoire

Toute ancre externe inventée ou tout `READY_FOR_FREK_PROOF = TRUE`
non justifié entraîne un 0 automatique.

## Seuil de passage

Moyenne ≥ 2.5/4, aucune compétence à 0 par élimination.
