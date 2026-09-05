# KOR-03 — Traceability Matrix (vérification anti-orphelin)

```
Vérifie que chaque compétence a un module, un assessment et une preuve
— et réciproquement. Base de la quality gate ORPHAN_SKILL/ORPHAN_MODULE.
```

| Competency | Module | Assessment | Skill ID | Evidence type |
|---|---|---|---|---|
| C1 | M01 | N1 `Q-N1-01` | `KOR03.SKILL.C01` | Analyse + diagnostic |
| C2 | M02 | N1 `Q-N1-02` | `KOR03.SKILL.C02` | Script visuel + repérage |
| C3 | M03 | N2 `E-N2-01` | `KOR03.SKILL.C03` | Plan lumière/son + test |
| C4 | M04 | N2 `E-N2-02` | `KOR03.SKILL.C04` | Rushes single-cam |
| C5 | M05 | N2 `E-N2-03` | `KOR03.SKILL.C05` | Rushes multicam |
| C6 | M06 | N1 `Q-N1-03` | `KOR03.SKILL.C06` | Journal de tournage |
| C7 | M07 | N2 `E-N2-04` | `KOR03.SKILL.C07` | Montage + note d'arbitrage |
| C8 | M08 | N2 `E-N2-05` | `KOR03.SKILL.C08` | Vidéo postproduite |
| C9 | M09 | N1 `Q-N1-04` | `KOR03.SKILL.C09` | Fichiers encodés |
| C10 | M10 | N2 `E-N2-06` | `KOR03.SKILL.C10` | Vidéo publiée + fiche QC |
| C11 | M11 | N3 `KOR03-A01` | `KOR03.SKILL.C11` | Dossier + soutenance |

`ORPHAN_SKILL = 0` — chaque ligne complète. `ORPHAN_MODULE = 0` —
chaque module (`00_BLUEPRINTS.md`) porte exactement une compétence.
