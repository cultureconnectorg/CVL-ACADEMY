# WAL-28 — Assessment & Rubric

Structure identique à `docs/wal/wal19/ASSESSMENT_AND_RUBRIC.md` (N1 40%
/ N2 30% / livrable 30%, même `../CERTIFICATION_MODEL.md`).

## Compétences évaluées

| Compétence | Description |
|---|---|
| C1 | Récupération et interprétation de l'historique réel (`list_transactions()`) |
| C2 | Honnêteté de la force d'audit — append-only ≠ tamper-evident cryptographique |
| C3 | Cross-check de solde réel, réparation via `reconcile_wallet_balance()` (WAL-21), jamais une modification du ledger |

## Rubric (0–4 par compétence)

| Niveau | Description |
|---|---|
| 0 | Qualifie le ledger de "tamper-evident"/"infalsifiable" au sens cryptographique, ou propose de modifier une transaction pour corriger un écart |
| 1 | Confond append-only et preuve cryptographique sans le nommer explicitement |
| 2 | Cross-check correct mais sans citer `reconcile_wallet_balance()` comme chemin de réparation |
| 3 | Complet et vérifié, imprécision mineure tolérée |
| 4 | Cite `service.py` ligne par ligne, y compris la frontière honnête de la force d'audit |

## Règle éliminatoire

Toute qualification du ledger comme cryptographiquement infalsifiable,
ou toute proposition de modifier une transaction existante pour
corriger un écart, entraîne un 0 automatique.

## Seuil de passage

Moyenne ≥ 2.5/4, aucune compétence à 0 par élimination.
