# FRK-36 — Banque N2 (cas appliqués)

## Cas 1 — Conception d'un flux de capture authentique

Le candidat conçoit un flux de capture avec preuve d'intégrité
embarquée dès l'origine (ex. signature au moment de la capture),
comme discipline marché-générale, sans référence à FREKRAW.

**Critère éliminatoire :** ajouter une preuve d'intégrité après la
capture plutôt qu'à l'origine.

## Cas 2 — Discipline `NEEDS_REPO_AUDIT`

Le candidat doit rédiger une note expliquant pourquoi aucune
affirmation sur le fonctionnement réel de FREKRAW ne peut être faite
aujourd'hui, malgré sa mention dans `FREK_01_75_RECONCILIATION.md`.

**Critère éliminatoire :** affirmer un comportement précis de FREKRAW.

## Cas 3 — Distinction `NEEDS_REPO_AUDIT` / `NEEDS_EXPERT_REVIEW`

Un relecteur confond `NEEDS_REPO_AUDIT` (FRK-36, FREKRAW introuvable)
avec `NEEDS_EXPERT_REVIEW` (FRK-10/14/73, contenu nécessitant une
revue experte). Le candidat doit corriger précisément cette confusion
en expliquant pourquoi ces deux statuts n'ont pas la même origine ni
la même conséquence sur la certifiabilité du package.

**Critère éliminatoire :** fusionner les deux statuts sans les
distinguer, ou affirmer que `NEEDS_REPO_AUDIT` bloquerait la
complétude du package FRK-36.
