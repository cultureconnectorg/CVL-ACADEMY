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

## Cas 3 — Une future implémentation Rust échoue

Une implémentation Rust croisée est développée et échoue sur 2 des 16
vecteurs d'or que l'implémentation Python passait tous. Le candidat
doit expliquer ce que cet écart révèle précisément (une ambiguïté ou
une erreur soit dans la spécification, soit dans l'une des deux
implémentations — à investiguer) et pourquoi ce scénario, même
négatif, serait un progrès réel par rapport à la situation actuelle
(implémentation unique, jamais testée contre un tiers indépendant).

**Critère éliminatoire :** présenter cet échec hypothétique comme
disqualifiant la formation elle-même, plutôt que comme le
fonctionnement attendu du processus de validation croisée.
