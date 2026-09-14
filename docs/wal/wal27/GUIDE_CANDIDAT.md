# WAL-27 — Guide Candidat

## Avant de commencer

Prérequis : `WAL-19`.

## Ce que tu dois savoir faire

Nommer exactement les 3 kill-switches globaux réels du produit externe
`djsayd/CVLN-Wallet`, et distinguer le kill-switch global du gel de
carte par utilisateur — deux mécanismes à des échelles différentes,
jamais confondus.

## Comment réviser

1. Étudie le repo-truth déjà établi (`REFERENTIAL.md` §Repo truth) sur
   `PUT /admin/kill-switch` et `/card/freeze`/`unfreeze`.
2. Fais les 8 questions de `BANQUE_N1.md`.
3. Traite les 2 cas de `BANQUE_N2.md`.

## Piège le plus fréquent

Confondre le kill-switch global `"card"` (affecte tous les
utilisateurs) avec le gel de carte individuel `/card/freeze` (affecte
un seul compte) — les deux existent pour des échelles d'incident
différentes.

## Règle absolue

N'invente jamais un 4e kill-switch, et ne confonds jamais les deux
mécanismes d'échelle — élimination automatique.
