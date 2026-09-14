# WAL-22 — Assessment & Rubric

Structure identique à `docs/wal/wal19/ASSESSMENT_AND_RUBRIC.md` (N1 40%
/ N2 30% / livrable 30%, même `../CERTIFICATION_MODEL.md`).

## Compétences évaluées

| Compétence | Description |
|---|---|
| C1 | Cycle de vie réel d'un coffre (création, mouvement in/out, fermeture) — `djsayd/CVLN-Wallet` |
| C2 | Discipline de ledger-posting — chaque mouvement est une écriture double-entry balancée, jamais une mise à jour brute |
| C3 | Frontière produit externe vs Academy — jamais un accès opérationnel réel prétendu |

## Rubric (0–4 par compétence)

| Niveau | Description |
|---|---|
| 0 | Affirme un accès opérationnel réel Academy au produit externe, ou qu'un coffre crée de la valeur ex nihilo |
| 1 | Confond mouvement de coffre et mise à jour brute d'un champ |
| 2 | Cycle de vie correct mais sans citer `ledger_post` |
| 3 | Complet et vérifié, imprécision mineure tolérée |
| 4 | Cite `server.py` (`atomic_spend`/`apply_user_balance`/`ledger_post`) ligne par ligne |

## Règle éliminatoire

Toute affirmation d'un accès opérationnel réel de cette Academy au
produit externe `djsayd/CVLN-Wallet`, ou toute affirmation qu'un coffre
crée de la valeur sans réallocation, entraîne un 0 automatique.

## Seuil de passage

Moyenne ≥ 2.5/4, aucune compétence à 0 par élimination.
