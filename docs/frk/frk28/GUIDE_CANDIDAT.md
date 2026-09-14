# FRK-28 — Guide Candidat

## Avant de commencer

Aucun prérequis. Apprends l'architecture événementielle de provenance
(discipline générale), en utilisant `events.py` de l'Academy comme
exemple pédagogique de pub/sub — jamais comme registre de provenance.

## Ce que tu dois savoir faire

Concevoir un registre d'événements append-only et chaîné
techniquement (pas seulement documenté comme tel), et distinguer
précisément un bus pub/sub en mémoire d'un registre de provenance
persistant.

## Comment réviser

1. Lis `REFERENTIAL.md` §Objectives et §Modules.
2. Fais les 8 questions de `BANQUE_N1.md`.
3. Traite les 3 cas de `BANQUE_N2.md`.

## Piège le plus fréquent

Confondre `events.py` avec un registre de provenance — élimination
automatique. Second piège : proposer un registre append-only "par
convention" sans mécanisme technique qui l'impose réellement.

## Règle absolue

Aucune correction d'un événement erroné ne se fait par réécriture ou
suppression — toujours par événement compensatoire.
