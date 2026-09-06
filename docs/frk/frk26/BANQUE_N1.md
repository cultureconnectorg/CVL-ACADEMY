# FRK-26 — Banque N1 (formatif)

Réserve `FRK26.SKILL.*`.

1. Qu'est-ce qu'un graphe de relations et pourquoi un graphe de
   provenance en est-il un cas particulier (nœuds = entités/versions,
   arêtes = relations de dérivation/production) ?
2. Pourquoi un modèle relationnel classique (tables) peine-t-il à
   représenter des chaînes de provenance profondes et variables ?
3. Pourquoi aucun système CVLN n'implémente aujourd'hui un vrai graphe
   de provenance — quelle discipline « CVLN-gap » s'applique ?
4. Cite un élément structurel indispensable à tout graphe de
   provenance (ex. horodatage de chaque arête, direction non-cyclique
   pour la dérivation) et justifie-le.

## Corrigé indicatif

1. Un graphe de provenance trace qui a produit/dérivé quoi, à partir
   de quoi — cas particulier de graphe de relations orienté vers la
   traçabilité.
2. Les tables relationnelles gèrent mal les chaînes de longueur
   variable et les relations many-to-many profondes sans jointures
   explosives.
3. Aucun système du dépôt CVLN ne maintient un graphe de provenance
   réel — le sujet reste enseigné comme discipline de conception
   marché-générale.
4. Une arête de dérivation doit être acyclique et horodatée pour
   garantir qu'une chaîne de provenance reste interprétable dans le
   temps.
