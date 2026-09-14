# WAL-23 — Banque N2 (cas appliqués)

## Cas N2-1 — Deux virements simultanés depuis le même compte

**Situation** : un manager s'inquiète que deux virements simultanés
depuis la même entité, dont la somme dépasse le solde disponible,
puissent tous deux réussir et créer un solde négatif.

**Décision attendue** : rassurer — `atomic_entity_spend` garantit
l'atomicité au niveau base de données ; un seul des deux virements peut
réussir si leur somme dépasse le solde disponible, jamais les deux.

**Critères de notation** : cite `atomic_entity_spend` et la garantie
d'atomicité réelle (50%, éliminatoire si absent), explique la
différence avec un simple décrément applicatif (30%), ne prétend
jamais que cette Academy peut exécuter ce virement (20%).

## Cas N2-2 — Confusion avec `credit()` de cette Academy

**Situation** : un développeur propose d'ajouter un "virement" en
appelant deux fois `credit()` (une fois négatif pour l'expéditeur, une
fois positif pour le destinataire) dans le `backend/wallet/` de cette
Academy.

**Décision attendue** : expliquer que `credit()` n'a aucune notion de
transfert atomique entre deux comptes — deux appels séparés ne sont
pas une opération atomique et risquent une incohérence en cas d'échec
entre les deux ; le vrai mécanisme de transfert n'existe que dans
`djsayd/CVLN-Wallet`, jamais dans cette Academy.

**Critères de notation** : identifie l'absence d'atomicité de
l'approche proposée (50%, éliminatoire si absent), distingue
clairement les deux systèmes (30%), ne présente jamais cette
proposition comme équivalente au vrai mécanisme (20%).

---

**Couverture** : 2 cas, couvrant M2 (atomicité) et M3 (frontière
produit).
