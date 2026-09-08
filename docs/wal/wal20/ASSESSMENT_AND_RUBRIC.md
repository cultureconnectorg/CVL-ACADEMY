# WAL-20 — Assessment & Rubric

Structure identique à `docs/wal/wal19/ASSESSMENT_AND_RUBRIC.md` (N1 40%
/ N2 30% / livrable 30%, même `../CERTIFICATION_MODEL.md`).

## Compétences évaluées

| Compétence | Description |
|---|---|
| C1 | Classification correcte d'une transaction par devise (`jcc`/`token`/`eur`) et par modèle propriétaire (`WalletAccount` vs `User.cc_credits`) |
| C2 | Discipline de non-conversion CC↔JCC — jamais inventée |
| C3 | Frontière WAL-20 (classification) vs WAL-21 (mécanique du ledger) |

## Rubric (0–4 par compétence)

| Niveau | Description |
|---|---|
| 0 | Invente une fonction de conversion CC↔JCC ou affirme qu'une transaction `eur` incrémente un solde qui n'existe pas |
| 1 | Confond `cc_credits` et `jcc_balance` comme un seul champ |
| 2 | Classification correcte mais sans expliquer le cas `eur` (absence d'incrémentation) |
| 3 | Complet et vérifié, imprécision mineure tolérée |
| 4 | Cite `models.py`/`service.py` ligne par ligne, y compris le `if/elif` de `credit()` |

## Règle éliminatoire

Toute fonction de conversion CC↔JCC inventée, ou toute affirmation
qu'une transaction `eur` met à jour un solde `WalletAccount`, entraîne
un 0 automatique.

## Seuil de passage

Moyenne ≥ 2.5/4, aucune compétence à 0 par élimination.
