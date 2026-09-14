# FRK-60 — Guide Candidat

## Avant de commencer

Aucun prérequis. Apprends le pont conceptuel FREK↔Intelligence
OS/Agent Infrastructure comme relation architecturale documentée,
jamais comme un système qui fonctionne aujourd'hui.

## Ce que tu dois savoir faire

Documenter les exigences d'une future intégration (schéma d'échange,
authentification mutuelle, contrat d'erreur partagé) sans jamais
affirmer qu'elle existe, et expliquer précisément pourquoi
`frek_core.py` (client interne) et `services/integrations/registry.py`
(configuration écosystème générique) sont chacun, séparément,
insuffisants pour constituer cette intégration.

## Comment réviser

1. Lis `REFERENTIAL.md` §Objectives et §Modules.
2. Fais les 8 questions de `BANQUE_N1.md`.
3. Traite les 3 cas de `BANQUE_N2.md`.

## Piège le plus fréquent

Confondre la coexistence des deux artefacts dans le dépôt avec une
intégration en cours de câblage — élimination automatique. Second
piège : croire qu'un seul des deux stubs (interne ou écosystème)
suffirait à lui seul.

## Règle absolue

Les deux côtés du pont restent `CAPABILITY_NOT_IMPLEMENTED` — jamais
présenté comme fonctionnel.
