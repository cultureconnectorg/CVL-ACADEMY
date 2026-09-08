# FMS-18 — Guide Candidat

## Avant de commencer

Littératie FMS-07 recommandée (même couche `/os`), non requise.

## Ce que tu dois savoir faire

Lire les KPI du command-center en distinguant chiffre réel et
`INSUFFICIENT_DATA`, opérer le registre d'intégrations écosystème
sans jamais affirmer une connexion inexistante, et utiliser
l'audit-log réel.

## Comment réviser

1. Lis `REFERENTIAL.md` §Repo truth (`command_center`,
   `ECOSYSTEM_INTEGRATIONS`, `/os/audit-log`) toi-même.
2. Fais les 7 questions de `BANQUE_N1.md`.
3. Traite les 3 cas de `BANQUE_N2.md`.

## Piège le plus fréquent

Confondre le `/os/command-center` de `fms-os/fms` avec le "Command
Center"/"CVL Brain" de l'écosystème CVLN — deux systèmes distincts
qui partagent un nom.

## Règle absolue

N'affirme jamais qu'une intégration `NOT_CONNECTED` est connectée, et
ne fusionne jamais les deux systèmes "Command Center" — élimination
automatique.
