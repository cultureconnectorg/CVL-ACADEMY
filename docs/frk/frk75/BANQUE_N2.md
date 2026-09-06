# FRK-75 — Banque N2 (cas appliqués)

## Cas 1 — Lecture de sortie de tests réels

Le candidat reçoit une sortie de test simulée (16/16 tests passants
contre des vecteurs d'or) et doit énoncer précisément ce qui est prouvé
(cette implémentation Python) vs. ce qui ne l'est pas (l'agnosticisme
d'implémentation de la spécification).

**Critère éliminatoire :** affirmer que la spécification elle-même est
prouvée correcte par ces tests seuls.

## Cas 2 — Frontière FRK-13

Le candidat doit expliquer pourquoi `reference_verifier/` (frek_v3) et
`issue_proof()` (`frek_core.py`, Academy) ne peuvent jamais être
présentés comme le même système ou au même niveau de maturité.

**Critère éliminatoire :** fusionner `reference_verifier/` et
`issue_proof()`.
