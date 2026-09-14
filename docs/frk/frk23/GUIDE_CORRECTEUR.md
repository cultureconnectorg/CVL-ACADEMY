# FRK-23 — Guide Correcteur

## Avant de noter

Relis `REFERENTIAL.md` §Objectives et §Modules — en particulier la
distinction modélisation/sérialisation et la frontière `.fk`.

## Ce que tu vérifies en priorité

1. Le modèle proposé a-t-il des entités/attributs/relations pertinents
   et réutilisables, indépendamment de tout format ?
2. Le candidat justifie-t-il un choix de structure par une supposition
   sur l'encodage `.fk` (dépendance cachée) ? Applique la règle
   éliminatoire sans exception si oui, même implicite.
3. La note de frontière `.fk` est-elle explicite et correcte ?

## Ce que tu ne fais pas

Tu ne notes jamais sur une intuition personnelle de la modélisation de
données — seulement sur la pertinence réelle du schéma et sur
l'indépendance réelle vis-à-vis de `.fk`.
