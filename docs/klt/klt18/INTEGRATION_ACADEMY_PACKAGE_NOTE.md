# KLT-18 — Note d'intégration Academy (package, pas import)

```
NO_RUNTIME_BINDING_YET. Voir klt01/INTEGRATION_ACADEMY_PACKAGE_NOTE.md
pour le raisonnement complet. KLT-18 n'existe pas en base
(db.formations) — formation NEW, comme KLT-06/07/08/13, contrairement à
KLT-01→05 qui ont un code legacy déjà seedé.
```

Même structure que les formations précédentes, namespace
`KLT18.SKILL.Cxx` distinct. Aucun fichier de `fms_import/`/
`fms_canonical/` modifié. Points ouverts identiques, non traités ici.

Point propre à `KLT-18` : la formation étend `KLT-05`/C5,C7,C9 par
référence, sans jamais rouvrir ces modules ni les dupliquer. Un futur
import devra veiller à ce que `KLT-18` reste liée à `KLT-05` comme
prérequis logique de contexte (l'animation quotidienne, le support et la
lecture de signaux restant enseignés dans `KLT-05` seul), sans fusionner
les deux formations ni dupliquer leurs compétences. `STRUCTURAL_STATUS =
COMPLETE` (5/5 modules) et `FULLY_COMPLETE = TRUE` (aucune compétence ne
dépend d'un système externe non connecté, même dérivation que
`KLT-01→05`) — indépendamment de l'import en base `db.formations`, qui
n'a pas eu lieu (`NO_RUNTIME_BINDING_YET`).
