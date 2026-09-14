# GMD-23 — Guide Correcteur

## Avant de noter

Ouvre `server.py` (lignes 99-114, 312-394) à côté de la copie.

## Ce que tu vérifies en priorité

1. Le candidat cite-t-il la vraie porte `status == "on_sale"` (vérifiée
   dans `payments/checkout`) comme critère de "prêt à vendre," plutôt
   qu'une supposition ?
2. A-t-il inventé une valeur de `status`, une route, ou un mécanisme de
   remboursement/annulation automatique ? Si oui, applique la règle
   éliminatoire sans exception.
3. Le M2 runbook est-il vérifié (capture/log/raisonnement complet), pas
   seulement affirmé ?

## Ce que tu ne fais pas

Tu ne notes pas sur une intuition produit — seulement sur le code réel
cité ci-dessus.
