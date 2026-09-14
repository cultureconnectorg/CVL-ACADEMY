# FRK-43 — Guide Candidat

## Avant de commencer

Aucun prérequis. Apprends le store-and-forward (discipline générale),
illustré par l'exemple réel de Good Mood — jamais présenté comme
infrastructure FREK.

## Ce que tu dois savoir faire

Concevoir un mécanisme de livraison persistante avec backoff
progressif et dead-letter, ancré dans le calendrier réel de Good Mood
(`[30s, 2m, 10m, 1h, 6h]`).

## Comment réviser

1. Lis `REFERENTIAL.md` §Objectives et §Modules.
2. Fais les 8 questions de `BANQUE_N1.md`.
3. Traite les 3 cas de `BANQUE_N2.md`.

## Piège le plus fréquent

Présenter l'outbox de Good Mood comme une infrastructure FREK —
élimination automatique. Second piège : concevoir un retry à
intervalle fixe plutôt qu'un backoff progressif.

## Règle absolue

Aucune tentative de retry ne se poursuit indéfiniment sans mécanisme
de dead-letter après épuisement du calendrier.
