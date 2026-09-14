# FRK-44 — Guide Candidat

## Avant de commencer

Prérequis recommandé : FRK-43. Apprends la récupération/synchronisation/
réconciliation après déconnexion, en réutilisant FRK-43 par référence.

## Ce que tu dois savoir faire

Concevoir un mécanisme de détection de conflit post-reconnexion,
choisir une stratégie de réconciliation (last-write-wins, résolution
manuelle, CRDT) adaptée au contexte, et en identifier explicitement le
compromis.

## Comment réviser

1. Relis `docs/frk/frk43/REFERENTIAL.md` (fondamentaux, prérequis).
2. Lis `REFERENTIAL.md` §Objectives et §Modules de cette formation.
3. Fais les 7 questions de `BANQUE_N1.md`.
4. Traite les 3 cas de `BANQUE_N2.md`.

## Piège le plus fréquent

Choisir une stratégie de réconciliation sans en identifier le
compromis — élimination automatique. Second piège : redéfinir les
fondamentaux de FRK-43 au lieu de les citer.

## Règle absolue

Chaque stratégie de réconciliation a un compromis — ne la présente
jamais comme gratuite.
