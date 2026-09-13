# FRK-23 — Guide Candidat

## Avant de commencer

Aucun prérequis. Apprends la modélisation d'objets culturels
(discipline générale), indépendante du format `.fk` (FRK-21/22,
bloqué — aucune spécification réelle n'existe dans ce dépôt).

## Ce que tu dois savoir faire

Concevoir un schéma d'objet culturel (entités, attributs, relations)
réutilisable indépendamment de tout format de sérialisation, et
expliquer précisément pourquoi ce schéma resterait valide même si
`.fk` n'est jamais spécifié.

## Comment réviser

1. Lis `REFERENTIAL.md` §Objectives et §Modules.
2. Fais les 8 questions de `BANQUE_N1.md`.
3. Traite les 3 cas de `BANQUE_N2.md`.

## Piège le plus fréquent

Faire dépendre ton modèle, même implicitement, d'une supposition sur
la façon dont `.fk` encoderait les données — élimination automatique.
Second piège : ne pas percevoir une dépendance cachée dans un choix de
structure.

## Règle absolue

Ton modèle ne doit jamais dépendre d'un format non spécifié — ni
explicitement, ni par supposition implicite.
