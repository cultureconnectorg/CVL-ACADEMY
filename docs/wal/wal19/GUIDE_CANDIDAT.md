# WAL-19 — Guide Candidat

## Avant de commencer

Aucun prérequis — c'est le point d'entrée du corpus WAL.

## Ce que tu dois savoir faire

Dessiner de mémoire la carte réelle du ledger Wallet de cette Academy,
distinguer CC de JCC, et distinguer ce ledger interne du vrai produit
externe `djsayd/CVLN-Wallet`.

## Comment réviser

1. Lis `backend/wallet/models.py`, `service.py`, `backend/api/
   wallet.py` toi-même.
2. Fais les 12 questions de `BANQUE_N1.md`.
3. Traite les 3 cas de `BANQUE_N2.md`.

## Piège le plus fréquent

Confondre ce ledger simple et additif avec le vrai produit financier
externe `djsayd/CVLN-Wallet` (holds/maker-checker/idempotency) — ce
sont deux systèmes distincts, jamais liés.

## Règle absolue

N'invente jamais une route de crédit direct, un transfert, ou une
fusion CC/JCC — élimination automatique.
