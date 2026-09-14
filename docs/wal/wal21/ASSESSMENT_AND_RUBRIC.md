# WAL-21 — Assessment & Rubric

Structure identique à `docs/wal/wal19/ASSESSMENT_AND_RUBRIC.md` (N1 40%
/ N2 30% / livrable 30%, même `../CERTIFICATION_MODEL.md`).

## Compétences évaluées

| Compétence | Description |
|---|---|
| C1 | Déroulé réel de `credit()` (pre-check, insert, mise à jour du cache) |
| C2 | Mécanisme d'idempotence réel (pre-check + index unique + `DuplicateKeyError`), frontière honnête (pas d'ACID multi-document) |
| C3 | Discipline append-only — jamais de modification/suppression d'une transaction existante |
| C4 | Chemin de réparation réel (`reconcile_wallet_balance()`) — quand l'utiliser, ce qu'il ne fait pas |
| C5 | Frontière single-entry vs double-entry, jamais confondue avec WAL-03 |

## Rubric (0–4 par compétence)

| Niveau | Description |
|---|---|
| 0 | Propose de modifier ou supprimer une transaction existante, ou invente une transaction ACID multi-document |
| 1 | Confond le pre-check et l'index unique comme un seul mécanisme redondant |
| 2 | Déroulé correct mais sans citer le mécanisme d'idempotence à deux niveaux |
| 3 | Complet et vérifié, imprécision mineure tolérée |
| 4 | Cite `service.py` ligne par ligne, y compris `reconcile_wallet_balance()` |

## Règle éliminatoire

Toute proposition de modifier/supprimer une transaction existante, ou
toute affirmation d'une garantie ACID multi-document non réelle,
entraîne un 0 automatique.

## Seuil de passage

Moyenne ≥ 2.5/4, aucune compétence à 0 par élimination.
