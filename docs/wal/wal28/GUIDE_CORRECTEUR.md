# WAL-28 — Guide Correcteur

## Avant de noter

Ouvre `backend/wallet/service.py` à côté de la copie, en particulier
`list_transactions()` et `reconcile_wallet_balance()`.

## Ce que tu vérifies en priorité

1. Le candidat qualifie-t-il le ledger de "tamper-evident"/
   "infalsifiable" sans distinction ? Applique la règle éliminatoire
   sans exception.
2. Propose-t-il de modifier une transaction existante pour corriger un
   écart ? Applique la règle éliminatoire sans exception.
3. Le cross-check M3 a-t-il été réellement exécuté, pas seulement
   décrit ?

## Ce que tu ne fais pas

Tu ne notes pas sur intuition produit — seulement sur le code réel.
