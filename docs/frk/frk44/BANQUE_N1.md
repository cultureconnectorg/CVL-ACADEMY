# FRK-44 — Banque N1 (formatif)

Réserve `FRK44.SKILL.*`.

## Extension de FRK-43 (M1/M3)

1. Comment la récupération après déconnexion et la réconciliation de
   synchronisation étendent-elles les fondamentaux de store-and-forward
   de FRK-43 ?
2. Pourquoi cette formation réutilise FRK-43 par référence plutôt que
   de le redéfinir ?

## Conflits de synchronisation (M1)

3. Qu'est-ce qu'un conflit de synchronisation (deux mises à jour
   concurrentes après reconnexion) et pourquoi une simple reprise du
   store-and-forward ne suffit-elle pas à le résoudre ?

## Stratégies de réconciliation (M2)

4. Décris la stratégie "last-write-wins" et son compromis. (Simple,
   mais peut écraser silencieusement des données concurrentes
   légitimes sans que l'utilisateur en soit conscient)
5. Décris la résolution manuelle et son compromis. (Sûre — un humain
   décide — mais coûteuse en friction et ne passe pas à l'échelle avec
   un taux de conflit élevé)
6. Décris les CRDT (Conflict-free Replicated Data Types) et leur
   compromis. (Fusion automatique via une fonction commutative
   mathématiquement fondée, évitant perte de données et friction, mais
   limitée aux structures de données qui admettent une formulation
   CRDT, avec une complexité de conception ajoutée)
7. Une stratégie de réconciliation peut-elle être présentée comme sans
   compromis ? (Non — élimination si affirmé)

## Corrigé indicatif

1. FRK-43 garantit la livraison malgré les pannes ; FRK-44 ajoute la
   détection et résolution des divergences d'état après une période de
   déconnexion prolongée.
2. Réutiliser par référence évite la duplication et garde FRK-43 comme
   source unique de vérité pour les fondamentaux de livraison
   persistante.
3. Le store-and-forward garantit la livraison, pas la cohérence entre
   deux versions concurrentes d'un même état — un mécanisme de
   réconciliation distinct est nécessaire.
4. Voir ci-dessus.
5. Voir ci-dessus.
6. Voir ci-dessus.
7. Non — chaque stratégie a un compromis, toujours identifiable.
