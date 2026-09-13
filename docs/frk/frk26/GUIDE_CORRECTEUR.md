# FRK-26 — Guide Correcteur

## Avant de noter

Relis `REFERENTIAL.md` §Objectives et §Modules — en particulier
l'exigence d'acyclicité et d'horodatage des arêtes de dérivation.

## Ce que tu vérifies en priorité

1. Le graphe conçu est-il réellement acyclique pour toutes les arêtes
   de dérivation ?
2. Chaque arête de dérivation porte-t-elle un horodatage ?
3. Le candidat distingue-t-il correctement arêtes de dérivation
   (acycliques) et autres relations (potentiellement cycliques) ?
4. Affirme-t-il, explicitement ou implicitement, qu'un système CVLN
   maintient un graphe de provenance réel ? Applique la règle
   éliminatoire sans exception si oui.

## Ce que tu ne fais pas

Tu ne notes jamais sur une intuition personnelle des graphes —
seulement sur l'acyclicité/horodatage réels du graphe conçu et sur
l'absence de système CVLN inventé.
