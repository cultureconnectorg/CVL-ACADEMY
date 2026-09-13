# FRK-17 — Guide Candidat

## Avant de commencer

Aucun prérequis. Apprends l'horodatage de confiance marché-général
(RFC 3161) comme discipline réelle et indépendante de CVLN.

## Ce que tu dois savoir faire

Expliquer le modèle de confiance TSA-tierce, la structure d'un jeton
RFC 3161 (hash + horodatage + identité TSA + signature), et vérifier
manuellement un jeton simplifié sans outil.

## Comment réviser

1. Lis `REFERENTIAL.md` §Objectives et §Modules.
2. Fais les 8 questions de `BANQUE_N1.md`.
3. Traite les 3 cas de `BANQUE_N2.md`.

## Piège le plus fréquent

Présenter `issue_proof()` (FRK-13) comme équivalent à un horodatage de
confiance — élimination automatique, l'écart est total. Second piège :
valider un jeton sans vérifier la signature de l'autorité.

## Règle absolue

`issue_proof()` (FRK-13) n'est jamais un horodatage de confiance —
c'est un stub.
