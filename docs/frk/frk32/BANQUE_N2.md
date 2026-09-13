# FRK-32 — Banque N2 (cas appliqués)

## Cas 1 — Capture technique d'un signal de consentement

Le candidat conçoit le flux technique d'enregistrement d'un événement
de consentement (horodatage, canal, version des conditions présentées)
sans traiter de sa gouvernance légale.

**Critère éliminatoire :** mélanger capture technique et gouvernance de
consentement (Fondation Cœurvolan §18).

**Critères de notation :** le flux capture uniquement des faits
techniques (quand, comment), sans aucune décision de qui peut
consentir ou sous quelles conditions.

## Cas 2 — Double frontière

Le candidat doit expliquer, sur un exemple concret, pourquoi ce
vocabulaire n'est ni `VALID_SIGNALS` (`frek_core.py`) ni la doctrine de
gouvernance Fondation Cœurvolan §18 — trois choses distinctes.

**Critère éliminatoire :** fusionner l'une des deux frontières.

## Cas 3 — Appareil non reconnu, consentement en attente

Un utilisateur se connecte depuis un nouveau type d'appareil, et son
consentement pour une nouvelle fonctionnalité est en attente. Le
candidat doit modéliser les deux signaux distinctement (signal de
device, signal de capture de consentement) sans jamais les fusionner
en un seul événement, ni les confondre avec `VALID_SIGNALS`, ni statuer
sur si le consentement est légalement valide.

**Critères de notation :** deux signaux séparés et clairement typés
(device vs. consentement) ; aucune référence à `FREK-*` ; aucune
décision sur la validité légale du consentement. Élimination si le
candidat fusionne les deux signaux ou statue sur la légalité.
