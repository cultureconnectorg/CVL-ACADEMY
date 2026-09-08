# WAL-23 — Assessment & Rubric

Structure identique à `docs/wal/wal19/ASSESSMENT_AND_RUBRIC.md` (N1 40%
/ N2 30% / livrable 30%, même `../CERTIFICATION_MODEL.md`).

## Compétences évaluées

| Compétence | Description |
|---|---|
| C1 | Déroulé réel du virement (`POST /v1/entity/transfer`, résolution du destinataire, débit atomique, ledger, double journalisation) |
| C2 | Discipline de débit atomique (`atomic_entity_spend`) — garantie base de données, jamais applicative seule |
| C3 | Frontière produit externe vs Academy — `credit()` n'a aucune notion de virement |

## Rubric (0–4 par compétence)

| Niveau | Description |
|---|---|
| 0 | Affirme que cette Academy peut exécuter un virement réel, ou que deux appels `credit()` équivalent à un virement atomique |
| 1 | Confond débit atomique et simple décrément applicatif |
| 2 | Déroulé correct mais sans citer `atomic_entity_spend` |
| 3 | Complet et vérifié, imprécision mineure tolérée |
| 4 | Cite `server.py` (`atomic_entity_spend`/`ledger_post`/`log_entity_tx`) ligne par ligne |

## Règle éliminatoire

Toute affirmation que cette Academy peut exécuter un virement réel, ou
que deux appels `credit()` séparés équivalent à un virement atomique,
entraîne un 0 automatique.

## Seuil de passage

Moyenne ≥ 2.5/4, aucune compétence à 0 par élimination.
