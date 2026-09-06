# FRK-30 — Banque N1 (formatif)

Réserve `FRK30.SKILL.*`.

1. Comment l'ingénierie de pipeline d'empreinte (extraction → vecteur
   de traits → stockage/indexation) étend-elle les fondations
   conceptuelles de FRK-29 ?
2. Pourquoi la conception d'un vecteur de traits (dimensionnalité,
   normalisation) est-elle une compétence d'ingénierie distincte de la
   simple connaissance conceptuelle des invariants (FRK-29) ?
3. Pourquoi cette formation réutilise FRK-29 par référence plutôt que
   de re-décrire ses fondamentaux ?
4. Donne un exemple de choix d'ingénierie (ex. réduction de
   dimensionnalité) qui affecte la robustesse d'un pipeline
   d'empreinte, sans référence à un système CVLN.

## Corrigé indicatif

1. FRK-29 pose les concepts (quoi extraire, pourquoi) ; FRK-30 construit
   le pipeline concret (comment extraire, stocker, indexer) —
   passage de la théorie à la pratique d'ingénierie.
2. Concevoir un vecteur de traits implique des choix concrets
   (dimensionnalité, normalisation, format de stockage) que la seule
   connaissance conceptuelle ne couvre pas.
3. Réutiliser par référence évite la duplication et garde FRK-29 comme
   source unique de vérité pour les fondamentaux.
4. Une réduction de dimensionnalité trop agressive peut faire perdre
   des traits distinctifs, réduisant la capacité de discrimination du
   pipeline — décision purement générale, indépendante de CVLN.
