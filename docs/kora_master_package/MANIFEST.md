# KORA Master Package — Manifest

Inventaire exhaustif du corpus documentaire `docs/kor/`.

## Comptage par formation (vérifié par `find docs/kor/korXX -type f | wc -l`)

| Formation | Fichiers | Modules |
|---|---|---|
| `kor01` | 30 | 14 |
| `kor02` | 28 | 12 |
| `kor03` | 29 | 11 |
| `kor04` | 27 | 9 |
| `kor05` | 28 | 10 |
| `kor06` | 27 | 9 |
| `kor07` | 27 | 9 |
| `kor08` | 27 | 9 |
| `kor09` | 29 | 11 |
| `kor10` | 28 | 10 |
| `kor11` | 31 | 13 |
| `kor12` | 31 | 13 |
| `kor13` | 31 | 13 |
| `kor14` | 32 | 14 |
| `kor15` | 30 | 12 |
| **Total** | **435** | **169** |

Plus `docs/kor/README.md` (index de corpus, hors formations) = **436**
fichiers sous `docs/kor/`.

## Structure type d'une formation (18 fichiers fixes + N modules)

```
docs/kor/korXX/
  REFERENTIAL.md
  00_BLUEPRINTS.md
  case/CASE.md
  case/CASE_COMPETENCY_MATRIX.md
  case/TRACEABILITY_MATRIX.md
  modules/M01_*.md … M{N}_*.md
  assessments/N1_QUESTION_BANK.md
  assessments/N2_EVALUATIONS.md
  assessments/A01_CERTIFICATION_ASSESSMENT.md
  assessments/RUBRIC.md
  skills/SKILL_ID_REGISTRY.md
  skills/EVIDENCE_MODEL.md
  guides/CANDIDATE_GUIDE.md
  guides/CORRECTOR_GUIDE.md
  guides/JURY_GUIDE.md
  templates/TEMPLATES.md
  CERTIFICATION_MODEL.md
  QUALITY_GATES.md
  INTEGRATION_ACADEMY_PACKAGE_NOTE.md
```

14 fichiers fixes + 3 fichiers `case/` + N fichiers `modules/` = 17 + N
par formation (KOR-01/02 suivent un schéma proche mais antérieur, avec
quelques variantes de nommage historiques — voir leurs
`INTEGRATION_ACADEMY_PACKAGE_NOTE.md` respectifs).

## Régénérer la liste exhaustive

```
find docs/kor -type f | sort
```

Cette commande produit la liste complète des 436 chemins — non
recopiée ligne à ligne ici pour éviter une duplication inutile d'un
inventaire déjà dérivable de l'arborescence réelle.

## Master Package lui-même

17 fichiers sous `docs/kora_master_package/` (ce document inclus),
plus `docs/KORA_PRODUCT_CAPABILITY_GAP_MAP.md` à la racine `docs/`.
