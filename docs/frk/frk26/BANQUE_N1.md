# FRK-26 — Banque N1 (formatif)

Réserve `FRK26.SKILL.*`.

## Fondamentaux de graphe (M1)

1. Qu'est-ce qu'un graphe de relations et pourquoi un graphe de
   provenance en est-il un cas particulier (nœuds = entités/versions,
   arêtes = relations de dérivation/production) ?
2. Pourquoi un modèle relationnel classique (tables) peine-t-il à
   représenter des chaînes de provenance profondes et variables ?

## Structure du graphe de provenance (M2)

3. Cite un élément structurel indispensable à tout graphe de
   provenance (ex. horodatage de chaque arête, direction non-cyclique
   pour la dérivation) et justifie-le.
4. Pourquoi une arête de dérivation doit-elle rester acyclique ? (Une
   chaîne où A dérive de B et B dérive, même transitivement, de A est
   logiquement incohérente)
5. Toutes les arêtes d'un graphe de relations doivent-elles être
   acycliques ? (Non — seules les arêtes de dérivation portent cette
   exigence, car la dérivation implique un ordre temporel avant/après ;
   une relation comme "collaborateur de" peut être symétrique ou
   cyclique)

## Discipline de gap (M3)

6. Pourquoi aucun système CVLN n'implémente aujourd'hui un vrai graphe
   de provenance — quelle discipline « CVLN-gap » s'applique ?
7. Un candidat peut-il affirmer qu'un système CVLN maintient un graphe
   de provenance réel ? (Non — élimination automatique si affirmé)

## Corrigé indicatif

1. Un graphe de provenance trace qui a produit/dérivé quoi, à partir
   de quoi — cas particulier de graphe de relations orienté vers la
   traçabilité.
2. Les tables relationnelles gèrent mal les chaînes de longueur
   variable et les relations many-to-many profondes sans jointures
   explosives.
3. Une arête de dérivation doit être acyclique et horodatée pour
   garantir qu'une chaîne de provenance reste interprétable dans le
   temps.
4. Une chaîne où A dérive de B et B dérive, même transitivement, de A
   est logiquement incohérente.
5. Non — seules les arêtes de dérivation ; d'autres relations peuvent
   être symétriques ou cycliques.
6. Aucun système du dépôt CVLN ne maintient un graphe de provenance
   réel — le sujet reste enseigné comme discipline de conception
   marché-générale.
7. Non — élimination automatique si affirmé.
