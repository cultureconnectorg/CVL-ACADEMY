# KLT-02 — Note d'intégration Academy (package, pas import)

```
NO_RUNTIME_BINDING_YET. Même principe que klt01/INTEGRATION_ACADEMY_
PACKAGE_NOTE.md — voir ce document pour le raisonnement complet
(compatibilité structurelle avec fms_import/fms_canonical sans y
toucher, DOCUMENT_ONLY pour toute extension de schéma).
```

Ce package suit exactement la même structure que `KLT-01`
(`modules/`, `case/`, `assessments/`, `skills/`, `guides/`,
`templates/`) et le même namespace de skill IDs distinct
(`KLT02.SKILL.Cxx`). Aucun fichier de `fms_import/`/`fms_canonical/`
n'a été modifié pour produire ce package. Les points ouverts avant un
import réel (chemin d'import dédié, décision de stockage, résolution du
gap badge/skill-proof/opérateur) sont identiques à ceux nommés pour
`KLT-01` — non redécouverts ici, non traités.
