# KLT-13 — Note d'intégration Academy (package, pas import)

```
NO_RUNTIME_BINDING_YET. Voir klt01/INTEGRATION_ACADEMY_PACKAGE_NOTE.md
pour le raisonnement complet. KLT-13 n'existe pas en base
(db.formations) — formation NEW, comme KLT-06/07/08, contrairement à
KLT-01→05 qui ont un code legacy déjà seedé.
```

Même structure que les formations précédentes, namespace
`KLT13.SKILL.Cxx` distinct. Aucun fichier de `fms_import/`/
`fms_canonical/` modifié. Points ouverts identiques, non traités ici.

Point propre à `KLT-13` : la formation est construite complète dès le
départ (`STRUCTURAL_STATUS = COMPLETE`, 5/5 modules) — contrairement à
`KLT-06`/`07`/`08`, aucune compétence de cette formation ne dépend d'un
système externe réel vérifié mais non connecté (`BUILT_UNCONNECTED`
n'apparaît nulle part dans son registre de compétences), si bien que
`fully_complete` se calcule honnêtement à `TRUE` (même dérivation que
`KLT-01→05` dans `klt_canonical/read_model.py`). Ceci reste indépendant
de l'import en base `db.formations`, qui n'a pas eu lieu
(`NO_RUNTIME_BINDING_YET`) — un futur import créerait une formation déjà
entièrement construite, sans rien à reclassifier.
