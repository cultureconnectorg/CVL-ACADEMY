# FRK-44 — Banque N2 (cas appliqués)

## Cas 1 — Conception d'une réconciliation post-déconnexion

Le candidat conçoit un mécanisme de détection et résolution de conflits
après une reconnexion, en citant FRK-43 par référence pour la
livraison persistante sous-jacente.

**Critère éliminatoire :** redéfinir les fondamentaux de FRK-43 au lieu
de les citer.

**Critères de notation :** le mécanisme détecte réellement une
divergence d'état (pas seulement l'absence de livraison) et propose
une résolution cohérente.

## Cas 2 — Choix de stratégie de réconciliation

Le candidat doit justifier le choix d'une stratégie de réconciliation
(ex. last-write-wins vs. résolution manuelle) selon le contexte donné,
en identifiant explicitement le compromis accepté.

**Critère éliminatoire :** choisir une stratégie sans en identifier le
compromis.

## Cas 3 — Compteur partagé concurrent

Deux appareils déconnectés incrémentent chacun de leur côté un même
compteur partagé (ex. nombre de vues). À la reconnexion, quelle
stratégie de réconciliation est appropriée, et pourquoi last-write-wins
serait-il inadapté ici ?

**Critères de notation :** identifie qu'un compteur additif se prête à
une structure CRDT (ex. compteur PN-Counter) où les incréments des
deux appareils s'additionnent correctement, plutôt qu'un écrasement.
Explique que last-write-wins perdrait silencieusement l'incrément de
l'appareil "perdant", ce qui est incorrect pour un compteur cumulatif.
Élimination si le candidat recommande last-write-wins sans en signaler
l'inadéquation pour ce cas précis.
