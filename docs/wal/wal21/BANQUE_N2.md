# WAL-21 — Banque N2 (cas appliqués)

## Cas N2-1 — Un déploiement a planté juste après une remise de badge

**Situation** : un rapport d'incident signale qu'un déploiement backend
a crashé juste après qu'un utilisateur ait reçu un badge — le solde
`jcc_balance` affiché semble en retard par rapport à ce que la
transaction devrait donner.

**Décision attendue** : ne jamais modifier ou réinsérer la transaction
existante ; appeler `reconcile_wallet_balance()` pour cet utilisateur,
qui recalculera le solde depuis le ledger réel — c'est exactement le
scénario que cette fonction est conçue pour réparer.

**Critères de notation** : identifie correctement le scénario (crash
entre insert et mise à jour du cache) (40%), ne propose jamais de
modifier le ledger lui-même (30%, éliminatoire si absent), appelle
`reconcile_wallet_balance()` comme réparation, pas une nouvelle
transaction manuelle (30%).

## Cas N2-2 — Appel `credit()` retenté après un timeout réseau

**Situation** : un service appelant signale un timeout réseau lors d'un
appel à `credit()` pour un événement `economic_event_id="badge:BADGE-
042"`, et retente l'appel identique quelques secondes plus tard. Le
manager s'inquiète d'un double crédit.

**Décision attendue** : rassurer — le pre-check `(user_id,
economic_event_id)` plus l'index unique garantissent qu'un second appel
identique renvoie la transaction déjà créée par le premier, jamais une
seconde. Aucune action corrective n'est nécessaire.

**Critères de notation** : cite le mécanisme réel à deux niveaux
(pre-check + index unique) (50%, éliminatoire si absent), n'invente pas
une inquiétude de double crédit non fondée (30%), explique la
frontière honnête (pas une transaction ACID multi-document) si demandé
(20%).

## Cas N2-3 — Demande de "corriger" une transaction erronée

**Situation** : un manager demande de "corriger le montant" d'une
transaction déjà insérée, qui s'avère erronée suite à un bug amont.

**Décision attendue** : refuser de modifier ou supprimer la transaction
existante (le ledger est append-only, aucune fonction de mise à jour
n'existe) ; proposer d'insérer une nouvelle transaction compensatoire
(`credit()` avec un montant négatif et un `economic_event_id` distinct)
plutôt qu'une modification rétroactive.

**Critères de notation** : refus de modifier/supprimer (50%,
éliminatoire si absent), proposition d'une transaction compensatoire
avec un `economic_event_id` distinct (30%), justification par la
discipline append-only (20%).

---

**Couverture** : 3 cas, couvrant M1/M2 (idempotence), M3 (append-only),
M4 (réconciliation).
