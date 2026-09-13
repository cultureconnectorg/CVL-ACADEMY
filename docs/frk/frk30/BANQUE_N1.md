# FRK-30 — Banque N1 (formatif)

Réserve `FRK30.SKILL.*`.

## Extension de FRK-29 (M1)

1. Comment l'ingénierie de pipeline d'empreinte (extraction → vecteur
   de traits → stockage/indexation) étend-elle les fondations
   conceptuelles de FRK-29 ?
2. Pourquoi cette formation réutilise FRK-29 par référence plutôt que
   de re-décrire ses fondamentaux ?

## Conception du vecteur de traits (M2)

3. Pourquoi la conception d'un vecteur de traits (dimensionnalité,
   normalisation) est-elle une compétence d'ingénierie distincte de la
   simple connaissance conceptuelle des invariants (FRK-29) ?
4. Que doit équilibrer le choix de dimensionnalité d'un vecteur de
   traits ? (Le pouvoir discriminant — assez de dimensions pour
   distinguer des actifs réellement différents — contre le coût de
   stockage/calcul)
5. Pourquoi une normalisation est-elle nécessaire ? (Pour que les
   valeurs de traits restent comparables entre différentes extractions)

## Stockage et indexation (M1)

6. Que doit permettre un schéma de stockage/indexation d'empreintes à
   l'échelle ? (Une recherche efficace, ex. plus proches voisins, sans
   parcourir linéairement tout le stockage)

## Choix d'ingénierie et robustesse (M1)

7. Donne un exemple de choix d'ingénierie (ex. réduction de
   dimensionnalité) qui affecte la robustesse d'un pipeline
   d'empreinte, sans référence à un système CVLN.
8. Que risque une réduction de dimensionnalité trop agressive ? (Perdre
   des traits distinctifs, réduisant la capacité de discrimination du
   pipeline)

## Corrigé indicatif

1. FRK-29 pose les concepts (quoi extraire, pourquoi) ; FRK-30 construit
   le pipeline concret (comment extraire, stocker, indexer) —
   passage de la théorie à la pratique d'ingénierie.
2. Réutiliser par référence évite la duplication et garde FRK-29 comme
   source unique de vérité pour les fondamentaux.
3. Concevoir un vecteur de traits implique des choix concrets
   (dimensionnalité, normalisation, format de stockage) que la seule
   connaissance conceptuelle ne couvre pas.
4. Le pouvoir discriminant contre le coût de stockage/calcul.
5. Pour que les valeurs de traits restent comparables entre différentes
   extractions.
6. Une recherche efficace (plus proches voisins ou équivalent).
7. Une réduction de dimensionnalité trop agressive peut faire perdre
   des traits distinctifs, réduisant la capacité de discrimination du
   pipeline — décision purement générale, indépendante de CVLN.
8. Voir 7.
