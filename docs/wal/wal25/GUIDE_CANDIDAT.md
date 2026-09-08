# WAL-25 — Guide Candidat

## Avant de commencer

Prérequis : `WAL-19`.

## Ce que tu dois savoir faire

Décrire le catalogue réel (8 articles seedés, vendeurs réels nommés) et
le flux d'achat idempotent réel du produit externe `djsayd/CVLN-Wallet`.

## Comment réviser

1. Étudie le repo-truth déjà établi (`REFERENTIAL.md` §Repo truth) sur
   `MARKETPLACE_ITEMS` et `POST /marketplace/buy`.
2. Fais les 9 questions de `BANQUE_N1.md`.
3. Traite les 2 cas de `BANQUE_N2.md`.

## Piège le plus fréquent

Inventer un article ou un vendeur absent du catalogue réel — les 8
articles réels et leurs vendeurs nommés sont les seuls qui existent.

## Règle absolue

N'invente jamais un article/vendeur, et n'affirme jamais un double
débit possible malgré l'idempotence réelle — élimination automatique.
