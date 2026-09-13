# FRK-20 — Guide Jury

## Rôle du jury

Copie limite (2.0–2.5) ou contestation d'une élimination.

## Ce que le jury vérifie en priorité

1. L'élimination porte-t-elle sur une vraie dépendance réseau (ou une
   confusion franche avec `is_remote_enabled()`), et non une simple
   imprécision de vocabulaire ?
2. Le candidat a-t-il réellement conçu une vérification locale
   autosuffisante, même si la formulation est maladroite ?

## Décision du jury

N'assouplit jamais la règle éliminatoire pour une copie par ailleurs
techniquement solide — une conception réellement locale est non
négociable, pas un habillage réseau.

## Ce que le jury ne fait pas

Ne délivre aucune compétence liée à `frek_core.py` par extension
automatique — seule `FRK20.SKILL.*` est en jeu, et uniquement pour la
vérification offline-first.
