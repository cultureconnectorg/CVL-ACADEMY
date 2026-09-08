# WAL-26 — Guide Candidat

## Avant de commencer

Prérequis : `WAL-19`, `WAL-21`.

## Ce que tu dois savoir faire

Décrire le cycle de vie réel d'un settlement et les 3 résolutions
réelles d'un cas de réconciliation du produit externe
`djsayd/CVLN-Wallet`, et expliquer ce qui rend ce système auditable.

## Comment réviser

1. Étudie le repo-truth déjà établi (`REFERENTIAL.md` §Repo truth) sur
   `settlement_transition` et les 3 résolutions.
2. Fais les 9 questions de `BANQUE_N1.md`.
3. Traite les 2 cas de `BANQUE_N2.md`.

## Piège le plus fréquent

Confondre `RESOLVED` (écart éliminé) et `ACCEPTED_DIFFERENCE` (écart
réel accepté, documenté) — les deux existent pour des raisons
différentes, jamais interchangeables.

## Règle absolue

N'invente jamais une 4e résolution de réconciliation, et ne propose
jamais de créer un second settlement manuellement pour contourner un
état bloqué — élimination automatique.
