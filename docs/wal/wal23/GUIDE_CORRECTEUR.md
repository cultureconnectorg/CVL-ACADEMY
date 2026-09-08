# WAL-23 — Guide Correcteur

## Avant de noter

Relis `REFERENTIAL.md` §Repo truth (routes réelles de
`djsayd/CVLN-Wallet`) à côté de la copie.

## Ce que tu vérifies en priorité

1. Le candidat cite-t-il correctement le déroulé du virement
   (résolution, débit atomique, ledger, double journalisation) ?
2. A-t-il cité `atomic_entity_spend` comme mécanisme de débit ?
3. A-t-il affirmé un accès opérationnel réel, ou proposé une simulation
   non atomique via `credit()` ? Applique la règle éliminatoire sans
   exception.

## Ce que tu ne fais pas

Tu ne notes pas sur intuition produit — seulement sur le repo-truth
déjà établi.
