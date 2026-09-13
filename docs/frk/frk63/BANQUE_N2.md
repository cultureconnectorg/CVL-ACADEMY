# FRK-63 — Banque N2 (cas appliqués)

## Cas 1 — Conception d'une preuve géographique

Le candidat conçoit un mécanisme de preuve d'origine géographique
(coordonnées signées, horodatage) pour un actif culturel, sans
référence à une stratégie commerciale.

**Critère éliminatoire :** intégrer une décision de stratégie
commerciale/droits dans le mécanisme de preuve.

**Critères de notation :** coordonnées, horodatage et hash de l'actif
liés cryptographiquement ; garanties précisément énoncées (localisation
authentique, rien sur le contenu ni les droits).

## Cas 2 — Frontière KOR-15

Le candidat doit expliquer pourquoi son mécanisme de preuve resterait
identique quelle que soit la stratégie commerciale par territoire
choisie (ou l'absence de KOR-15).

**Critère éliminatoire :** fusionner preuve géographique et stratégie
territoriale.

## Cas 3 — Utilisation abusive de la preuve géographique

Une équipe commerciale propose d'utiliser directement le mécanisme de
preuve géographique FRK-63 pour déterminer automatiquement quels
droits de distribution s'appliquent à un actif selon sa localisation
d'origine. Explique pourquoi cette proposition mélange deux altitudes
distinctes, et ce que tu proposerais à la place.

**Critères de notation :** identifie que la preuve géographique
(fait technique vérifiable) ne peut jamais déterminer automatiquement
une conséquence de droits (décision business/légale) — c'est
exactement la fusion que la frontière FRK-63/KOR-15 interdit. Propose
que la preuve géographique serve d'*intrant* à une décision de droits
prise séparément par un processus KOR-15 (ou équivalent), jamais
qu'elle la détermine directement. Élimination si le candidat valide la
proposition commerciale telle quelle.
