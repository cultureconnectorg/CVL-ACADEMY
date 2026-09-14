# WAL-20 — Guide Correcteur

## Avant de noter

Ouvre `backend/wallet/models.py` et `service.py` à côté de la copie,
en particulier le `if/elif` de `credit()` (lignes ~88-90).

## Ce que tu vérifies en priorité

1. Le candidat classe-t-il correctement chaque devise vers son champ
   réel (`jcc_balance`, `token_balance`, ou aucun pour `eur`) ?
2. A-t-il inventé une fonction de conversion CC↔JCC ? Applique la règle
   éliminatoire sans exception.
3. Distingue-t-il correctement `cc_credits` (Academy) de `jcc_balance`
   (Wallet) ?

## Ce que tu ne fais pas

Tu ne notes pas sur intuition produit — seulement sur le code réel.
