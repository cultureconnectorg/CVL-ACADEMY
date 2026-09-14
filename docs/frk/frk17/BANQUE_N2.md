# FRK-17 — Banque N2 (cas appliqués)

## Cas 1 — Vérification d'un jeton d'horodatage

Le candidat reçoit un jeton RFC 3161 simplifié et doit identifier les
éléments qui permettent de le vérifier (autorité, hash, signature) et
ceux qui manqueraient pour le rendre non vérifiable.

**Critère éliminatoire :** valider un jeton sans vérifier la signature
de l'autorité.

**Critères de notation :** identifie correctement les 4 champs requis
et exécute la vérification de signature, pas seulement une lecture des
champs.

## Cas 2 — Confusion avec `issue_proof()`

Le candidat doit expliquer par écrit pourquoi remplacer un jeton RFC
3161 par un identifiant `PROOF-{uuid}` de `frek_core.py` ferait perdre
toute garantie d'ancrage temporel vérifiable.

**Critère éliminatoire :** présenter les deux comme équivalents.

## Cas 3 — Falsification a posteriori d'une date locale

Un document local affiche "créé le 3 janvier 2024" dans ses métadonnées
de fichier. Explique pourquoi cette date seule ne constitue aucune
preuve opposable, et ce qu'il faudrait ajouter pour la rendre
vérifiable.

**Critères de notation :** explique que les métadonnées de fichier
sont modifiables par quiconque a accès au fichier, sans aucune trace
vérifiable — il faudrait un horodatage RFC 3161 (hash du document +
signature TSA) obtenu au moment de la création pour rendre la date
opposable. Élimination si le candidat affirme que la date de métadonnée
seule suffit comme preuve.
