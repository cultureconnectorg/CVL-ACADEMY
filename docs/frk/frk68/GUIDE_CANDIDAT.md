# FRK-68 — Guide Candidat

## Avant de commencer

Prérequis : FRK-01, FRK-58, FRK-03.

## Ce que tu dois savoir faire

Lire `db.frek_signals` et les deux outbox Good Mood réels, jamais les
fusionner en un pipeline d'audit unique, et connaître le schedule de
retry exact.

## Comment réviser

1. Relis `emit_signal()` dans `frek_core.py`, et `docs/gmd/gmd31`/
   `gmd32` en entier.
2. Fais les 7 questions de `BANQUE_N1.md`, traite les 3 cas de
   `BANQUE_N2.md`.

## Piège le plus fréquent

Fusionner les trois tables réelles en une seule métrique d'audit
"FREK."

## Règle absolue

Ne fusionne jamais les trois systèmes distincts, n'invente jamais un
mécanisme de retry supplémentaire — élimination automatique.
