# FRK-42 — Banque N2 (cas appliqués)

## Cas 1 — Conception d'un transport de preuve hors-ligne

Le candidat conçoit un format d'artefact de preuve auto-vérifiable
(signature embarquée) conçu pour transiter par un support physique
déconnecté.

**Critère éliminatoire :** proposer un artefact qui perd sa
vérifiabilité une fois hors réseau.

**Critères de notation :** l'artefact porte sa propre preuve
d'intégrité (signature embarquée ou détachée) et reste vérifiable sans
accès réseau à la réception.

## Cas 2 — Discipline CVLN-gap

Le candidat doit expliquer pourquoi aucun système CVLN n'implémente ce
transport aujourd'hui.

**Critère éliminatoire :** affirmer qu'un système CVLN implémente le
transport de preuve hors-ligne.

## Cas 3 — Séquence multi-artefacts avec artefact manquant

Trois artefacts de preuve chaînés par hash doivent être transportés
ensemble via clé USB. À la réception, un des trois artefacts manque.
Conçois un mécanisme qui permette au récepteur de détecter ce manque
sans se fier au support de transport.

**Critères de notation :** propose un chaînage par hash où chaque
artefact référence le hash du précédent ; une rupture dans la chaîne
(hash référencé absent) signale explicitement le manque, plutôt que
d'accepter silencieusement une séquence incomplète comme complète.
Élimination si le candidat propose un mécanisme qui fait confiance au
comptage de fichiers sur le support plutôt qu'à une preuve
cryptographique de complétude.
