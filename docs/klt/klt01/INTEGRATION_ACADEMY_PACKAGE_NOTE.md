# KLT-01 — Note d'intégration Academy (package, pas import)

```
NO_RUNTIME_BINDING_YET. Aucun contrat d'import n'est autorisé à ce
stade. Cette note documente comment ce package SERAIT compatible avec
le moteur d'import existant, sans y toucher.
```

## Ce que ce document n'est pas

Ce n'est ni une spécification technique d'import, ni une extension de
schéma appliquée. Aucun fichier de `fms_import/`, `fms_canonical/`, ou
tout autre module runtime n'a été modifié pour produire ce package
(`NO_RUNTIME_BINDING`, `NO_FMS_MUTATION` — vérifié en §Validation du
rapport `KLT0004_KLT01_PEDAGOGICAL_BUILD_REPORT.md`).

## Compatibilité structurelle avec le moteur d'import FMS existant

Le moteur `fms_import`/`fms_canonical` attend, pour chaque formation, une
structure documentaire par type (référentiel, module, N1, N2, A0x,
rubric, guides, templates) qu'il classe par `resource_type` et par
`(formation_code, module_number)` (voir `fms_canonical/read_model.py`).
Ce package `KLT-01` suit une structure analogue :

| Ce package | Équivalent structurel FMS |
|---|---|
| `modules/M0X_*.md` | un module FMS par fichier |
| `assessments/N1_QUESTION_BANK.md` | banque N1 |
| `assessments/N2_EVALUATIONS.md` | évaluations N2 |
| `assessments/A01_CERTIFICATION_ASSESSMENT.md` | assessment certificatif Axx |
| `assessments/RUBRIC.md` | grille de correction |
| `skills/SKILL_ID_REGISTRY.md` | registre skill IDs |
| `guides/*.md` | guides candidat/correcteur/jury |
| `templates/TEMPLATES.md` | templates/livrables |
| `case/*.md` | cas fil rouge + case competency matrix |

## Là où une extension de schéma serait nécessaire — `DOCUMENT_ONLY`

Le parser `fms_import` normalise aujourd'hui les codes vers un format
`FMS-XX-MYY` (dashed, legacy-shaped — voir `fms_import/parser.py`,
comportement documenté dans `docs/ACADEMY_FMS_CANONICAL_DELTA_MATRIX.md`).
Ce comportement est **spécifique à FMS** et ne doit **jamais** être
étendu silencieusement pour reconnaître `KLT01.SKILL.Cxx` ou
`KLT01-MXX` — ce package utilise volontairement une forme de code
différente (§`skills/SKILL_ID_REGISTRY.md`, "Différence explicite avec
FMS") précisément pour ne jamais collisionner ni être happé par erreur
par une regex conçue pour FMS. Si un futur ticket autorise un import
réel de ce package, il devra soit écrire un chemin d'import dédié à
`KLT`, soit étendre `fms_import` de façon explicite et testée — jamais en
silence. **Ce document se limite à le signaler (`DOCUMENT_ONLY`)**, il ne
modifie aucun parser.

## Ce qui manquerait avant un import réel

- Un chemin d'import distinct (ou une extension explicite, testée, du
  chemin existant) reconnaissant le préfixe `KLT01.` sans jamais le
  confondre avec `FMS`.
- Une décision Founder sur le stockage (nouvelle collection `db.klt_
  resources` vs. réutilisation d'une collection existante) — non prise
  ici, hors scope `KLT-0004`.
- La résolution du gap `badge_name`/`SKILL_PROOF`/`OPERATOR_
  AUTHORIZATION` documenté dans `CERTIFICATION_MODEL.md` avant qu'un
  skill ID ne soit réellement adressable en base.

Aucun de ces points n'est traité ici — ils sont nommés pour qu'un futur
ticket d'import n'ait pas à les redécouvrir.
