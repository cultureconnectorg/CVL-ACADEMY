# FRK-55 — Banque N2 (cas appliqués)

## Cas 1 — Conception de standards transversaux

Le candidat conçoit une taxonomie d'erreur et un schéma de versionnage
unifiés, applicables à la fois à une API (FRK-52) et à un bus
d'événements (FRK-54), en citant les deux par référence.

**Critère éliminatoire :** redéfinir les fondamentaux de FRK-52 ou
FRK-54 au lieu de les citer.

**Critères de notation :** la taxonomie d'erreur et le schéma de
version sont identiques, quelle que soit la surface (API ou
événement).

## Cas 2 — Cohérence de version

Le candidat doit identifier un cas où un schéma de version divergent
entre API et événements causerait un bug d'intégration concret, et
proposer la correction.

**Critère éliminatoire :** proposer des schémas de version incohérents
sans le percevoir comme un problème.

## Cas 3 — Taxonomie d'erreur qui diverge silencieusement

Une équipe API ajoute un nouveau code d'erreur `RATE_LIMITED` pour ses
endpoints, tandis qu'une équipe événements ajoute séparément
`THROTTLED` pour le même type de situation dans les payloads d'échec
d'événement. Explique le problème et la correction à apporter.

**Critères de notation :** identifie que deux codes différents pour le
même type de situation brisent la cohérence transversale — un
consommateur doit gérer deux cas au lieu d'un. Propose une
gouvernance de taxonomie unique (un registre central de codes
d'erreur partagé entre les deux équipes) plutôt qu'une simple
renomination ponctuelle. Élimination si le candidat ne perçoit pas la
divergence comme un problème réel.
