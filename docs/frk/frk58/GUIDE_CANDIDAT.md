# FRK-58 — Guide Candidat

## Avant de commencer

Prérequis : FRK-01.

## Ce que tu dois savoir faire

Expliquer précisément le comportement remote/local fallback de
`frek_core.py`, la validation des signaux, la résolution des paliers,
et distinguer honnêtement cette intégration Academy du vrai cluster
architecture `frek_v3` (FRK-71→75).

## Comment réviser

1. Relis `backend/services/frek_core.py` toi-même.
2. Fais les 9 questions de `BANQUE_N1.md`.
3. Traite les 3 cas de `BANQUE_N2.md`.

## Piège le plus fréquent

Affirmer qu'une panne réseau bloque l'utilisateur, ou confondre ce
module fin avec le vrai `frekcoreAout2026`/`frek_v3` plus mature.

## Règle absolue

N'invente jamais un comportement d'erreur ou une intégration
inexistante — élimination automatique.
