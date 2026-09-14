# WAL-26 — Assessment & Rubric

Structure identique à `docs/wal/wal19/ASSESSMENT_AND_RUBRIC.md` (N1 40%
/ N2 30% / livrable 30%, même `../CERTIFICATION_MODEL.md`).

## Compétences évaluées

| Compétence | Description |
|---|---|
| C1 | Cycle de vie du settlement (`PENDING→SUBMITTED`, retry-safe re-submit) |
| C2 | Littéracie des cas de réconciliation (3 résolutions réelles, jamais une 4e inventée) |
| C3 | Auditabilité réelle via correlation IDs et `emit_event` |

## Rubric (0–4 par compétence)

| Niveau | Description |
|---|---|
| 0 | Invente une 4e résolution de réconciliation, ou propose de créer un second settlement manuellement après un crash |
| 1 | Confond `RESOLVED` et `ACCEPTED_DIFFERENCE` |
| 2 | Cycle de vie correct mais sans citer `settlement_transition`/`financial_state_history` |
| 3 | Complet et vérifié, imprécision mineure tolérée |
| 4 | Cite `server.py` (`settlement_transition`/`emit_event`) ligne par ligne |

## Règle éliminatoire

Toute invention d'une résolution de réconciliation absente des 3 réelles,
ou toute proposition de contourner un état bloqué par la création
manuelle d'un second settlement, entraîne un 0 automatique.

## Seuil de passage

Moyenne ≥ 2.5/4, aucune compétence à 0 par élimination.
