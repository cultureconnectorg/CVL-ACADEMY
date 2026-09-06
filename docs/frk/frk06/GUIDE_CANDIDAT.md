# FRK-06 — Guide Candidat

## Avant de commencer

Prérequis : FRK-01, FRK-58.

## Ce que tu dois savoir faire

Tracer le comportement exact de `mint_frek_id()` (distant puis
fallback local), et refuser toute extension de portée vers DID/VC ou
la révocation.

## Comment réviser

1. Relis `mint_frek_id()` dans `frek_core.py`.
2. Fais les 8 questions de `BANQUE_N1.md`, traite les 3 cas de
   `BANQUE_N2.md`.

## Piège le plus fréquent

Confondre ce simple compteur avec une architecture d'identité complète
(DID/VC) — territoire séparé de FRK-07/08/09.

## Règle absolue

N'invente jamais une révocation, une rotation, ou une équivalence
DID/VC — élimination automatique.
