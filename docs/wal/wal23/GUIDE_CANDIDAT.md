# WAL-23 — Guide Candidat

## Avant de commencer

Prérequis : `WAL-19`.

## Ce que tu dois savoir faire

Expliquer le déroulé réel d'un virement du produit externe
`djsayd/CVLN-Wallet` (résolution du destinataire, débit atomique,
ledger, double journalisation), et pourquoi cette Academy n'a aucune
fonction de virement.

## Comment réviser

1. Étudie le repo-truth déjà établi (`REFERENTIAL.md` §Repo truth) sur
   `POST /v1/entity/transfer`.
2. Fais les 8 questions de `BANQUE_N1.md`.
3. Traite les 2 cas de `BANQUE_N2.md`.

## Piège le plus fréquent

Proposer de simuler un virement dans cette Academy via deux appels
`credit()` séparés — ce n'est jamais atomique, et ce n'est pas le
mécanisme réel enseigné ici.

## Règle absolue

N'affirme jamais que cette Academy peut exécuter un virement réel —
élimination automatique.
