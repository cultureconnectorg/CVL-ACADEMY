# FRK-14 — Banque N2 (cas appliqués, formatif)

Usage formatif uniquement — `NEEDS_EXPERT_REVIEW` non levé. Aucun cas
n'ouvre de voie certifiante.

## Cas 1 — Rupture de chaîne non documentée

Un artefact passe entre trois systèmes sans journal d'aucun transfert.
Le candidat doit identifier où la chaîne casse et pourquoi cela rend
l'artefact non probant, indépendamment de son intégrité technique.

**Critère éliminatoire :** confondre « le hash est bon » avec « la
chaîne est intacte ».

## Cas 2 — Confusion avec `issue_proof()`

Le candidat doit expliquer pourquoi le stub `issue_proof()` de
`frek_core.py` (`PROOF-{uuid}`, aucune chaîne de custody réelle) ne
peut en aucun cas servir d'exemple de chaîne de custody fonctionnelle.

**Critère éliminatoire :** présenter `issue_proof()` comme une
implémentation réelle de chaîne de custody.
