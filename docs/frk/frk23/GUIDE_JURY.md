# FRK-23 — Guide Jury

## Rôle du jury

Copie limite (2.0–2.5) ou contestation d'une élimination.

## Ce que le jury vérifie en priorité

1. L'élimination porte-t-elle sur une vraie dépendance cachée à `.fk`
   (même implicite), et non une simple imprécision de vocabulaire ?
2. Le modèle proposé est-il réellement réutilisable indépendamment du
   format, même si la formulation est maladroite ?

## Décision du jury

N'assouplit jamais la règle éliminatoire pour une copie par ailleurs
techniquement solide — l'absence de dépendance à `.fk` est non
négociable, y compris les dépendances implicites.

## Ce que le jury ne fait pas

Ne délivre aucune compétence liée à FRK-21/22 — ces formations restent
`BLOCKED_PRODUCT_DEPENDENCY` et hors de portée. Seule
`FRK23.SKILL.*` est en jeu.
