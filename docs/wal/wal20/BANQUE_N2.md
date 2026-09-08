# WAL-20 — Banque N2 (cas appliqués)

## Cas N2-1 — Transaction `eur` sans mise à jour de solde

**Situation** : un ticket support signale qu'une transaction `eur` a
bien été enregistrée dans `wallet_transactions`, mais qu'aucun solde
`WalletAccount` n'a bougé — le rapporteur suspecte un bug.

**Décision attendue** : expliquer que ce n'est pas un bug — le code de
`service.py` n'incrémente `jcc_balance`/`token_balance` que pour les
devises `jcc`/`token` ; une transaction `eur` reste volontairement sans
branche d'incrémentation dans le schéma actuel, à distinguer d'un défaut
réel.

**Critères de notation** : cite précisément le `if/elif` de `service.py`
(30%), ne conclut pas à un bug sans l'avoir vérifié dans le code (40%,
éliminatoire si absent), propose de vérifier la spécification voulue
plutôt que de corriger à l'aveugle (30%).

## Cas N2-2 — Proposition de fusionner CC et JCC

**Situation** : un product manager propose de fusionner `cc_credits` et
`jcc_balance` en un seul champ "pour simplifier le reporting."

**Décision attendue** : refuser la fusion technique, en citant le
docstring de `models.py` — CC est la monnaie pédagogique interne
propre à l'Academy, JCC est le ledger cross-écosystème CVLN — deux
objets à but différent, jamais fusionnés dans le code réel.

**Critères de notation** : refus de la fusion (50%, éliminatoire si
absent), citation du docstring réel (30%), proposition d'une
alternative de reporting qui garde les deux champs distincts (20%).

---

**Couverture** : 2 cas, couvrant M1 (classification par devise) et M2
(discipline de non-conversion).
