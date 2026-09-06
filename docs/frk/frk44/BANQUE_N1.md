# FRK-44 — Banque N1 (formatif)

Réserve `FRK44.SKILL.*`.

1. Comment la récupération après déconnexion et la réconciliation de
   synchronisation étendent-elles les fondamentaux de store-and-forward
   de FRK-43 ?
2. Qu'est-ce qu'un conflit de synchronisation (deux mises à jour
   concurrentes après reconnexion) et pourquoi une simple reprise du
   store-and-forward ne suffit-elle pas à le résoudre ?
3. Cite une stratégie de réconciliation (ex. last-write-wins,
   résolution manuelle, CRDT) et explique un compromis qu'elle implique.
4. Pourquoi cette formation réutilise FRK-43 par référence plutôt que
   de le redéfinir ?

## Corrigé indicatif

1. FRK-43 garantit la livraison malgré les pannes ; FRK-44 ajoute la
   détection et résolution des divergences d'état après une période de
   déconnexion prolongée.
2. Le store-and-forward garantit la livraison, pas la cohérence entre
   deux versions concurrentes d'un même état — un mécanisme de
   réconciliation distinct est nécessaire.
3. Last-write-wins est simple mais peut silencieusement écraser des
   données légitimes ; la résolution manuelle est sûre mais coûteuse en
   friction utilisateur — chaque stratégie a un compromis.
4. Réutiliser par référence évite la duplication et garde FRK-43 comme
   source unique de vérité pour les fondamentaux de livraison
   persistante.
