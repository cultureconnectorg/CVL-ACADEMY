# FRK-27 — Banque N2 (cas appliqués)

## Cas 1 — Conception d'un knowledge graph culturel

Le candidat conçoit une ontologie minimale (types de nœuds, types de
relations) pour un domaine culturel donné, en citant FRK-26 par
référence pour la structure de graphe sous-jacente.

**Critère éliminatoire :** redéfinir les fondamentaux de graphe de
FRK-26 au lieu de les citer.

**Critères de notation :** types de nœuds et de relations réellement
distincts et sémantiquement porteurs de sens (pas de simples labels
génériques).

## Cas 2 — Frontière avec un modèle relationnel

Le candidat doit expliquer pourquoi une requête d'inférence
(« trouve toutes les œuvres influencées indirectement par X ») serait
difficile en SQL relationnel classique mais naturelle sur un knowledge
graph.

**Critère éliminatoire :** ne pas percevoir la différence de nature
entre les deux modèles.

## Cas 3 — Ambiguïté de type de relation

Dans l'ontologie conçue au Cas 1, une même paire d'entités (Œuvre,
Créateur) pourrait être reliée par "créée par" ou par "attribuée à"
(attribution incertaine). Explique pourquoi distinguer ces deux
relations typées importe pour la fiabilité des inférences ultérieures.

**Critères de notation :** identifie qu'une inférence traitant "créée
par" et "attribuée à" comme équivalentes propagerait une incertitude
d'attribution comme un fait établi — la distinction typée doit être
préservée pour que toute requête d'inférence en aval reste fiable.
Élimination si le candidat fusionne les deux relations sans
justification.
