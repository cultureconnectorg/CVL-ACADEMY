# WAL-28 — Guide Candidat

## Avant de commencer

Prérequis : `WAL-19`, `WAL-21`.

## Ce que tu dois savoir faire

Récupérer et interpréter l'historique réel des transactions, expliquer
honnêtement la force réelle (et les limites) de l'append-only comme
garantie d'audit, et exécuter un cross-check de solde réel.

## Comment réviser

1. Relis `list_transactions()` dans `backend/wallet/service.py`, et
   `reconcile_wallet_balance()` (WAL-21).
2. Fais les 8 questions de `BANQUE_N1.md`.
3. Traite les 2 cas de `BANQUE_N2.md`.

## Piège le plus fréquent

Qualifier ce ledger de "tamper-evident" ou "infalsifiable" — l'append-
only garantit qu'aucun code réel ne modifie/supprime une transaction,
mais ce n'est pas une preuve cryptographique (pas de signature, pas de
hash chain). Les deux ne sont jamais la même affirmation.

## Règle absolue

Ne propose jamais de modifier une transaction existante pour corriger
un écart de solde — utilise toujours `reconcile_wallet_balance()`
(WAL-21) — élimination automatique sinon.
