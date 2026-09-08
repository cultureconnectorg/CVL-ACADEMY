# WAL-24 — Guide Correcteur

## Avant de noter

Ouvre `backend/wallet/passes.py` et les routes `/wallet/pass/apple`,
`/wallet/pass/google` de `backend/api/wallet.py` à côté de la copie.

## Ce que tu vérifies en priorité

1. Le candidat affirme-t-il qu'une route renvoie une erreur 501 ? C'est
   faux — vérifié par `grep` — applique la règle éliminatoire.
2. A-t-il correctement identifié le comportement réel (200 +
   `"status": "unsigned"`) ?
3. Nomme-t-il précisément les dépendances de signature manquantes par
   plateforme (WWDR/Pass Type ID pour Apple, compte Issuer pour
   Google) ?

## Ce que tu ne fais pas

Tu ne notes pas sur intuition produit — seulement sur le code réel.
