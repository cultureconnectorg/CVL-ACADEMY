# KLT-06 — Note d'intégration Academy (package, pas import)

```
NO_RUNTIME_BINDING_YET. Voir klt01/INTEGRATION_ACADEMY_PACKAGE_NOTE.md
pour le raisonnement complet. KLT-06 n'existe pas en base (db.formations)
— formation NEW, contrairement à KLT-01→05 qui ont un code legacy déjà
seedé. Mise à jour 2026-09-07 : formation désormais structurellement
complète (7/7 compétences) — un futur import créerait une formation
complète, pas partielle.
```

Même structure que les formations précédentes, namespace
`KLT06.SKILL.Cxx` distinct. Aucun fichier de `fms_import/`/
`fms_canonical/` modifié. Points ouverts identiques, non traités ici.

Point propre à `KLT-06`, mis à jour : la formation est désormais
structurellement complète (`STRUCTURAL_STATUS = COMPLETE`, 7/7
modules), y compris `C5`/`C6` construites sur le schéma réel vérifié de
l'Observatory Kiltikonet (`cultureconnectorg/Kiltikonet-Aout2026`).
`FULLY_COMPLETE` reste néanmoins `FALSE` : ce champ désigne
spécifiquement une **connexion live** Academy↔Kiltikonet-Aout2026 en
production, qui n'existe toujours pas — Academy n'a aucun client ni
credentials pour interroger cette API. Un futur import doit donc
présenter une formation **structurellement complète mais sans
connexion runtime live**, jamais l'un pour l'autre.
