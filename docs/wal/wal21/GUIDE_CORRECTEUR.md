# WAL-21 — Guide Correcteur

## Avant de noter

Ouvre `backend/wallet/service.py` à côté de la copie, en particulier le
docstring de `credit()` et le corps de `reconcile_wallet_balance()`.

## Ce que tu vérifies en priorité

1. Le candidat cite-t-il le mécanisme d'idempotence à deux niveaux
   (pre-check + index unique) ?
2. Propose-t-il de modifier ou supprimer une transaction existante ?
   Applique la règle éliminatoire sans exception.
3. Distingue-t-il correctement `reconcile_wallet_balance()` (répare le
   cache, jamais le ledger) d'une correction manuelle ?

## Ce que tu ne fais pas

Tu ne notes pas sur intuition produit — seulement sur le code réel.
