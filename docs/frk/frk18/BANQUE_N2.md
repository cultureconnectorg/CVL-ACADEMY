# FRK-18 — Banque N2 (cas appliqués)

## Cas 1 — Vérification d'une preuve OpenTimestamps

Le candidat reçoit un fichier `.ots` simplifié et doit décrire les
étapes de vérification (hash local, chemin Merkle, confirmation
Bitcoin) sans outil automatique.

**Critère éliminatoire :** valider une preuve sans vérifier le chemin
Merkle jusqu'à la transaction Bitcoin.

**Critères de notation :** recalcule le hash local, reconstruit
correctement la racine Merkle via le chemin fourni, et confirme
explicitement la correspondance avec la transaction Bitcoin nommée.

## Cas 2 — Discipline CVLN-gap

Le candidat doit rédiger une note expliquant pourquoi CVLN ne peut pas
revendiquer aujourd'hui un ancrage OpenTimestamps réel, malgré la
proximité conceptuelle avec `issue_proof()`.

**Critère éliminatoire :** affirmer qu'un système CVLN utilise
OpenTimestamps.

## Cas 3 — Disparition du serveur calendrier

Le service calendrier OpenTimestamps qui a agrégé une preuve donnée
ferme définitivement un an après l'émission. Le détenteur de la preuve
peut-il encore la faire valoir ? Justifie.

**Critères de notation :** oui — explique que le serveur calendrier
n'était qu'une commodité d'agrégation, jamais une dépendance de
confiance ; la preuve reste vérifiable indépendamment via Bitcoin
(chemin Merkle + transaction publique), qui est l'ancre de confiance
réelle. Élimination si le candidat affirme que la preuve devient
invalide ou invérifiable sans le serveur d'origine.
