# WAL-27 — Assessment & Rubric

Structure identique à `docs/wal/wal19/ASSESSMENT_AND_RUBRIC.md` (N1 40%
/ N2 30% / livrable 30%, même `../CERTIFICATION_MODEL.md`).

## Compétences évaluées

| Compétence | Description |
|---|---|
| C1 | Littéracie des 3 kill-switches globaux réels, jamais un 4e inventé |
| C2 | Discipline d'échelle — kill-switch global vs. gel de carte par utilisateur, jamais confondus |
| C3 | Littéracie de la trace d'audit (`KillSwitch.Toggled`) |

## Rubric (0–4 par compétence)

| Niveau | Description |
|---|---|
| 0 | Invente un 4e kill-switch, ou confond le switch global `"card"` avec un gel de carte individuel |
| 1 | Recommande l'outil de mauvaise échelle pour un incident (gel individuel pour un incident global, ou inversement) |
| 2 | Distinction correcte mais sans citer l'audit `KillSwitch.Toggled` |
| 3 | Complet et vérifié, imprécision mineure tolérée |
| 4 | Cite `server.py` (validation exacte des 3 noms, `audit(...)`) ligne par ligne |

## Règle éliminatoire

Toute invention d'un 4e kill-switch, ou toute confusion entre le
kill-switch global et le gel de carte par utilisateur, entraîne un 0
automatique.

## Seuil de passage

Moyenne ≥ 2.5/4, aucune compétence à 0 par élimination.
