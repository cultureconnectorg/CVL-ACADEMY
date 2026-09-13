# FRK-75 — Guide Candidat

## Avant de commencer

Prérequis : FRK-71 ; FRK-13 recommandé. Apprends l'ingénierie de
vérificateur de référence sur ce package réel et testé
(`reference_verifier/`).

## Ce que tu dois savoir faire

Lire une sortie de test réelle et distinguer précisément ce qui est
prouvé (cette implémentation Python) de ce qui ne l'est pas
(l'agnosticisme de la spécification), sans jamais confondre ce package
avec `issue_proof()` (FRK-13).

## Comment réviser

1. Lis `REFERENTIAL.md` §Objectives et §Modules.
2. Fais les 8 questions de `BANQUE_N1.md`.
3. Traite les 3 cas de `BANQUE_N2.md`.

## Piège le plus fréquent

Affirmer que les 16 tests prouvent l'agnosticisme d'implémentation de
la spécification — élimination automatique. Second piège : fusionner
`reference_verifier/` (frek_v3) avec `issue_proof()` (FRK-13, Academy).

## Règle absolue

Les 16 tests prouvent cette implémentation, jamais l'agnosticisme de
la spécification.
