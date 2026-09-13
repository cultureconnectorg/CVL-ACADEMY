# FRK-30 — Banque N2 (cas appliqués)

## Cas 1 — Conception d'un pipeline d'empreinte

Le candidat conçoit un pipeline complet (extraction → vecteur →
stockage/indexation) pour un actif culturel, en citant FRK-29 par
référence pour les fondamentaux conceptuels.

**Critère éliminatoire :** redéfinir les fondamentaux de FRK-29 au lieu
de les citer.

**Critères de notation :** chaque étape (extraction, vecteur, stockage/
indexation) est présente et cohérente ; référence explicite à FRK-29
pour les fondamentaux.

## Cas 2 — Choix d'ingénierie et robustesse

Le candidat doit justifier un choix de dimensionnalité de vecteur de
traits et en évaluer l'impact sur la robustesse du pipeline.

**Critère éliminatoire :** proposer un pipeline sans justification
d'ingénierie (choix arbitraire non motivé).

## Cas 3 — Compromis stockage vs. discrimination

Un pipeline d'empreinte doit indexer 50 millions d'actifs culturels
avec un budget de stockage limité. Le candidat doit proposer un
compromis entre dimensionnalité du vecteur et capacité de stockage, en
justifiant les conséquences sur la capacité de discrimination.

**Critères de notation :** propose une réduction de dimensionnalité
réfléchie (ex. via une méthode de réduction reconnue) plutôt
qu'arbitraire, et articule explicitement le compromis discrimination/
coût — jamais présenté comme gratuit. Élimination si le candidat
affirme qu'une réduction de dimensionnalité n'a aucun coût sur la
discrimination.
