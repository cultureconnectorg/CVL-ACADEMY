# FRK-34 — Banque N1 (formatif)

Réserve `FRK34.SKILL.*`.

1. Qu'est-ce que le suivi d'identité d'une œuvre (work/track/album) au
   niveau de la provenance, et pourquoi diffère-t-il de la gestion de
   catalogue/droits (LabelOS LOS-02) ?
2. Pourquoi LabelOS lui-même n'a « zéro empreinte dépôt » aujourd'hui
   (`REPO_REGISTRY.md`) — qu'est-ce que cela implique pour la
   frontière de cette formation ?
3. Donne un exemple concret de « preuve d'identité d'une œuvre » (ex.
   hash + métadonnées structurelles) qui ne dit rien sur les droits
   qui lui sont attachés.
4. Pourquoi une fusion identité/catalogue serait-elle une erreur
   structurelle, même si LabelOS existait demain avec un vrai
   LOS-02 ?

## Corrigé indicatif

1. L'identité de l'œuvre répond à « qu'est-ce que c'est, comment le
   reconnaître » ; le catalogue/droits répond à « qui le possède, sous
   quelles conditions » — deux fonctions distinctes.
2. LabelOS n'a aucune implémentation observable — la frontière reste
   donc conceptuelle et préventive, pas basée sur un système réel à
   éviter de dupliquer.
3. Un hash de contenu + empreinte structurelle identifie l'œuvre sans
   jamais mentionner qui en détient les droits.
4. Même avec un LOS-02 réel, l'identité de l'œuvre resterait une
   fonction technique séparée de la gestion commerciale/légale du
   catalogue — les fusionner casserait la séparation des
   responsabilités.
