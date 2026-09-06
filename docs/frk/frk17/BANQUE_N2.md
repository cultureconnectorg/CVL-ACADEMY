# FRK-17 — Banque N2 (cas appliqués)

## Cas 1 — Vérification d'un jeton d'horodatage

Le candidat reçoit un jeton RFC 3161 simplifié et doit identifier les
éléments qui permettent de le vérifier (autorité, hash, signature) et
ceux qui manqueraient pour le rendre non vérifiable.

**Critère éliminatoire :** valider un jeton sans vérifier la signature
de l'autorité.

## Cas 2 — Confusion avec `issue_proof()`

Le candidat doit expliquer par écrit pourquoi remplacer un jeton RFC
3161 par un identifiant `PROOF-{uuid}` de `frek_core.py` ferait perdre
toute garantie d'ancrage temporel vérifiable.

**Critère éliminatoire :** présenter les deux comme équivalents.
