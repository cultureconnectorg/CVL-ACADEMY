# WAL-27 — Banque N2 (cas appliqués)

## Cas N2-1 — Incident de fraude sur les cartes

**Situation** : un incident de fraude touche potentiellement de
nombreux comptes carte. Un manager demande de "geler les comptes
suspects un par un" via `/card/freeze`.

**Décision attendue** : recommander plutôt le kill-switch global
`"card"` — un incident à large échelle nécessite un arrêt global
immédiat, pas un gel compte par compte qui laisse une fenêtre
d'exposition sur les comptes non encore identifiés ou créés pendant
l'incident.

**Critères de notation** : recommande le bon outil pour l'échelle de
l'incident (50%, éliminatoire si confondu), distingue clairement les
deux mécanismes (30%), cite l'audit `KillSwitch.Toggled` comme trace
attendue (20%).

## Cas N2-2 — Proposition d'un 4e kill-switch

**Situation** : un product manager propose d'ajouter un 4e kill-switch
nommé `"transfers"` pour un futur incident de virement.

**Décision attendue** : expliquer que le système réel valide
exactement 3 noms (`withdrawals`, `card`, `agents`) — tout autre nom
est rejeté avec un 400 ; ajouter un 4e switch nécessiterait un
changement de code réel côté produit externe, pas une simple
configuration.

**Critères de notation** : cite l'ensemble exact des 3 switches
validés (50%, éliminatoire si absent), explique que ceci nécessite un
changement de code, pas une configuration (30%), ne prétend jamais
pouvoir l'activer soi-même (20%).

---

**Couverture** : 2 cas, couvrant M2 (distinction d'échelle) et M1
(ensemble exact des switches).
