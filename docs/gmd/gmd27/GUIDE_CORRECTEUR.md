# GMD-27 — Guide Correcteur

## Avant de noter

Ouvre `server.py` (lignes 133-150, 165-188, 440-467, 489-510).

## Ce que tu vérifies en priorité

1. Le candidat distingue-t-il `GET /merch` (filtré `active`) de
   `GET /admin/merch` (non filtré) ?
2. A-t-il cité les vrais préfixes `gm_`/`gmtt_` plutôt qu'un mécanisme
   inventé de distinction ticket/merch ?
3. A-t-il inventé une route "activer le prix" ou un mécanisme absent ?
   Applique la règle éliminatoire sans exception.

## Ce que tu ne fais pas

Tu ne notes pas sur intuition produit — seulement sur le code réel.
