# FRK-53 — Banque N2 (cas appliqués)

## Cas 1 — Conception d'un SDK générique

Le candidat conçoit une bibliothèque cliente (types, gestion d'erreur,
retry) pour une API générique, en citant FRK-52 par référence pour la
conception d'API sous-jacente.

**Critère éliminatoire :** redéfinir les fondamentaux de FRK-52 au lieu
de les citer.

**Critères de notation :** modèles typés, erreurs traduites en
exceptions actionnables, politique de retry distinguant erreurs
sûres/non sûres à retenter.

## Cas 2 — Discipline CVLN-gap héritée

Le candidat doit confirmer qu'aucun SDK FREK public n'existe
aujourd'hui, cohérent avec le constat de FRK-52.

**Critère éliminatoire :** affirmer l'existence d'un SDK FREK public.

## Cas 3 — Écriture non-idempotente en échec réseau

Un appel SDK vers une API générique pour créer une ressource échoue
avec un timeout réseau. L'appelant ne sait pas si la ressource a été
créée côté serveur avant le timeout. Le SDK doit-il retenter
automatiquement cet appel ?

**Critères de notation :** non par défaut — explique que sans clé
d'idempotence côté serveur, un retry automatique risque une création
en double ; le SDK doit soit exposer explicitement le risque à
l'appelant, soit exiger une clé d'idempotence pour permettre un retry
sûr. Élimination si le candidat propose un retry automatique aveugle
pour une écriture non-idempotente.
