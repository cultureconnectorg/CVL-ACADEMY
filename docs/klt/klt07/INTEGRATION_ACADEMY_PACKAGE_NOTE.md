# KLT-07 — Note d'intégration Academy (package, pas import)

```
NO_RUNTIME_BINDING_YET. Voir klt01/INTEGRATION_ACADEMY_PACKAGE_NOTE.md
pour le raisonnement complet. KLT-07 n'existe pas en base (db.formations)
— formation NEW, contrairement à KLT-01→05. Un futur import ne créerait
qu'une formation partielle (6/7 compétences), à documenter explicitement
comme telle.
```

Même structure que les formations précédentes, namespace
`KLT07.SKILL.Cxx` distinct. Aucun fichier de `fms_import/`/
`fms_canonical/` modifié. Points ouverts identiques, non traités ici —
plus un point propre à `KLT-07` : tout import futur devra soit importer
une formation explicitement `PARTIAL` (6/7 modules), soit attendre la
construction de `M04`, jamais présenter une formation complète avant que
`C4` le soit réellement.
