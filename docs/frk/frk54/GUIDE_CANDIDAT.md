# FRK-54 — Guide Candidat

## Avant de commencer

Aucun prérequis. Apprends la conception de bus d'événements/webhooks/
contrats d'intégration, illustrée par le vrai `events.py` de l'Academy
— jamais présenté comme infrastructure FREK ou surface webhook.

## Ce que tu dois savoir faire

Concevoir un contrat d'intégration webhook versionné avec
compatibilité ascendante, et distinguer précisément un bus
d'événements interne d'un webhook externe.

## Comment réviser

1. Lis `REFERENTIAL.md` §Objectives et §Modules.
2. Fais les 8 questions de `BANQUE_N1.md`.
3. Traite les 3 cas de `BANQUE_N2.md`.

## Piège le plus fréquent

Présenter `events.py` comme une infrastructure webhook ou FREK —
élimination automatique. Second piège : faire évoluer un schéma
d'événement sans mécanisme de compatibilité ascendante.

## Règle absolue

`events.py` reste le bus interne propre à cette Academy — jamais une
infrastructure d'intégration externe.
