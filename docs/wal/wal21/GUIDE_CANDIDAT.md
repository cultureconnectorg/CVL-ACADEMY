# WAL-21 — Guide Candidat

## Avant de commencer

Prérequis : `WAL-19`.

## Ce que tu dois savoir faire

Dérouler de mémoire le mécanisme réel de `credit()` (pre-check, insert,
mise à jour du cache, idempotence à deux niveaux), expliquer la
discipline append-only, et savoir quand et pourquoi
`reconcile_wallet_balance()` intervient.

## Comment réviser

1. Relis `backend/wallet/service.py` en entier, en particulier le
   docstring de `credit()` et `reconcile_wallet_balance()`.
2. Fais les 10 questions de `BANQUE_N1.md`.
3. Traite les 3 cas de `BANQUE_N2.md`.

## Piège le plus fréquent

Proposer de "corriger" ou modifier une transaction déjà insérée — le
ledger est append-only, aucune fonction de mise à jour n'existe. La
seule réponse correcte à une erreur déjà enregistrée est une nouvelle
transaction compensatoire.

## Règle absolue

N'invente jamais une garantie ACID multi-document, et ne propose jamais
de modifier/supprimer une transaction existante — élimination
automatique.
