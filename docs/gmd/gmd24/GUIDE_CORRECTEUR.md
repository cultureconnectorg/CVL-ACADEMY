# GMD-24 — Guide Correcteur

## Avant de noter

Ouvre `server.py` (lignes 115-131, 489-560, 574-620, 657-716).

## Ce que tu vérifies en priorité

1. Le candidat distingue-t-il le check `remaining` au checkout (non
   atomique) de l'incrément `$inc` sur `sold` au webhook (la vraie
   protection) ? C'est le piège central de cette formation.
2. A-t-il inventé un verrou de réservation, une contrainte email
   générique, ou un log d'audit séparé ? Applique la règle éliminatoire
   sans exception si oui.
3. Le diagramme M3 pointe-t-il correctement vers GMD-26/28/31/32 ?

## Ce que tu ne fais pas

Tu ne notes pas sur intuition produit — seulement sur le code réel.
