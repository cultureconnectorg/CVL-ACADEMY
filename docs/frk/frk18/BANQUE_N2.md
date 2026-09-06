# FRK-18 — Banque N2 (cas appliqués)

## Cas 1 — Vérification d'une preuve OpenTimestamps

Le candidat reçoit un fichier `.ots` simplifié et doit décrire les
étapes de vérification (hash local, chemin Merkle, confirmation
Bitcoin) sans outil automatique.

**Critère éliminatoire :** valider une preuve sans vérifier le chemin
Merkle jusqu'à la transaction Bitcoin.

## Cas 2 — Discipline CVLN-gap

Le candidat doit rédiger une note expliquant pourquoi CVLN ne peut pas
revendiquer aujourd'hui un ancrage OpenTimestamps réel, malgré la
proximité conceptuelle avec `issue_proof()`.

**Critère éliminatoire :** affirmer qu'un système CVLN utilise
OpenTimestamps.
