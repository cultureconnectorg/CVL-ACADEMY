# WAL-25 — Assessment & Rubric

Structure identique à `docs/wal/wal19/ASSESSMENT_AND_RUBRIC.md` (N1 40%
/ N2 30% / livrable 30%, même `../CERTIFICATION_MODEL.md`).

## Compétences évaluées

| Compétence | Description |
|---|---|
| C1 | Littéracie du catalogue réel (8 articles seedés, champs réels, vendeurs réels nommés) |
| C2 | Littéracie du flux d'achat idempotent (`idem_begin`/`idem_finish`, `atomic_spend`, `add_transaction`) |
| C3 | Frontière produit externe vs Academy — catalogue statique, jamais un système de listing dynamique |

## Rubric (0–4 par compétence)

| Niveau | Description |
|---|---|
| 0 | Invente un article/vendeur absent du catalogue réel, ou affirme un double débit possible malgré l'idempotence |
| 1 | Confond catalogue statique et système de listing dynamique |
| 2 | Flux d'achat correct mais sans citer `idem_begin`/`idem_finish` |
| 3 | Complet et vérifié, imprécision mineure tolérée |
| 4 | Cite `server.py` (`MARKETPLACE_ITEMS`/`idem_begin`/`atomic_spend`) ligne par ligne |

## Règle éliminatoire

Toute invention d'un article ou vendeur absent du catalogue réel, ou
toute affirmation qu'un double-clic peut double-débiter malgré
l'idempotence réelle, entraîne un 0 automatique.

## Seuil de passage

Moyenne ≥ 2.5/4, aucune compétence à 0 par élimination.
