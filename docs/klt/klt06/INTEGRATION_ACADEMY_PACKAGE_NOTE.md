# KLT-06 — Note d'intégration Academy (package, pas import)

```
NO_RUNTIME_BINDING_YET. Voir klt01/INTEGRATION_ACADEMY_PACKAGE_NOTE.md
pour le raisonnement complet. KLT-06 n'existe pas en base (db.formations)
— formation NEW, contrairement à KLT-01→05 qui ont un code legacy déjà
seedé. Un futur import ne créerait qu'une formation partielle (5/7
compétences), à documenter explicitement comme telle.
```

Même structure que les formations précédentes, namespace
`KLT06.SKILL.Cxx` distinct. Aucun fichier de `fms_import/`/
`fms_canonical/` modifié. Points ouverts identiques, non traités ici —
plus un point propre à `KLT-06` : tout import futur devra soit importer
une formation explicitement `PARTIAL` (5/7 modules), soit attendre la
construction de `M05`/`M06` — jamais présenter une formation complète
avant que `C5`/`C6` le soient réellement.
