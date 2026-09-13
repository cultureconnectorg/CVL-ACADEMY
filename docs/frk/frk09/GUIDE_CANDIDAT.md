# FRK-09 — Guide Candidat

## Avant de commencer

Prérequis : FRK-08 (DID & Verifiable Credentials). Cette formation
enseigne le cycle de vie d'identité réel (émission/rotation/
révocation) et la récupération/réconciliation — jamais attribué à
FREK-ID, qui n'a aucun de ces mécanismes.

## Ce que tu dois savoir faire

Concevoir un cycle de vie d'identité complet (émission, rotation,
révocation), expliquer un schéma de récupération réel et son compromis
de sécurité, et décrire un scénario de réconciliation — et articuler
précisément, pour chacun des trois mécanismes, le gap avec FREK-ID.

## Comment réviser

1. Lis `REFERENTIAL.md` §Objectives et §Modules.
2. Fais les 11 questions de `BANQUE_N1.md`.
3. Traite les 3 cas de `BANQUE_N2.md`.

## Piège le plus fréquent

Affirmer, même partiellement, qu'un FREK-ID peut être rotationné,
révoqué, ou récupéré aujourd'hui — aucun de ces mécanismes n'existe
dans `mint_frek_id()`, et l'élimination est automatique. Second piège :
confondre les trois stades du cycle de vie entre eux.

## Règle absolue

N'affirme jamais qu'un mécanisme de rotation, révocation, ou
récupération existe pour FREK-ID — aucun des trois n'est implémenté.
