# FRK-71 — Banque N2 (cas appliqués)

## Cas 1 — Classification d'une affirmation de capacité

Le candidat reçoit une affirmation (« FREK v3 a été prouvé en
matériel ») et doit la classer correctement contre l'échelle propre du
corpus.

**Critère éliminatoire :** valider une affirmation de niveau 3
(ingénierie/matériel prouvé) pour FREK v3.

## Cas 2 — Frontière `frek_core.py`

Le candidat doit expliquer pourquoi `frek_core.py` (Academy, FRK-01/58)
et `frek_v3` (frekcoreAout2026) restent deux couches distinctes du même
produit éventuel, jamais fusionnées dans une évaluation de maturité.

**Critère éliminatoire :** fusionner les deux couches dans une seule
évaluation de maturité.

## Cas 3 — Confusion intégration/maturité

Un relecteur affirme que, puisque FREK v3 n'est lié à aucun FREKCORE
en production (`NOT_PRODUCTION_INTEGRATED`), sa classification devrait
être rétrogradée en dessous d'`ARCHITECTURE_LEVEL_2`. Le candidat doit
corriger cette confusion en distinguant précisément l'axe de maturité
architecturale (verrouillée, Level 2) de l'axe d'intégration en
production (absent, statut différent).

**Critère éliminatoire :** accepter la rétrogradation proposée par le
relecteur sans corriger la confusion entre les deux axes.
