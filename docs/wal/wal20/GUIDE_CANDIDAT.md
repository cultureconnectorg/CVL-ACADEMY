# WAL-20 — Guide Candidat

## Avant de commencer

Prérequis : `WAL-19`.

## Ce que tu dois savoir faire

Classer correctement toute transaction par devise (`jcc`/`token`/`eur`)
et par modèle propriétaire, et expliquer pourquoi aucune conversion
CC↔JCC n'existe dans le code réel.

## Comment réviser

1. Relis `backend/wallet/models.py` et `service.py`, en particulier le
   `if/elif` de `credit()`.
2. Fais les 8 questions de `BANQUE_N1.md`.
3. Traite les 2 cas de `BANQUE_N2.md`.

## Piège le plus fréquent

Supposer qu'une transaction `eur` met à jour un solde `WalletAccount`
comme les transactions `jcc`/`token` — ce n'est pas le cas dans le
schéma réel actuel.

## Règle absolue

N'invente jamais une fonction de conversion CC↔JCC — élimination
automatique.
