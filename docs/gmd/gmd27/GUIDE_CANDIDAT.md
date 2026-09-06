# GMD-27 — Guide Candidat

## Avant de commencer

GMD-21 requis.

## Ce que tu dois savoir faire

Gérer un `Product` (merch) via CRUD réel, distinguer clairement
`Product` de `Volume` (GMD-22), et savoir que créer un produit ne le
rend pas automatiquement vendable — une synchronisation Stripe réelle
(`_sync_stripe_item`, préfixe `gm_`) est nécessaire.

## Comment réviser

1. Lis `server.py` lignes 133-150, 165-188, 440-467, 489-510.
2. Fais les 10 questions de `BANQUE_N1.md`.
3. Traite les 3 cas de `BANQUE_N2.md`.

## Piège le plus fréquent

Croire que `GET /admin/merch` filtre les produits inactifs comme le
fait `GET /merch` — ce n'est pas le cas.

## Règle absolue

N'invente jamais une route ou un mécanisme (activation de prix,
filtre admin) absent du code réel.
