# KOR-08 — Quality Gates

| Gate | Cible | Résultat |
|---|---|---|
| `COMPETENCY_COVERAGE` | 100% | **100%** (9/9) |
| `MODULE_COVERAGE` | 100% | **100%** (9/9) |
| `ASSESSMENT_COVERAGE` | 100% | **100%** |
| `EVIDENCE_COVERAGE` | 100% | **100%** |
| `ORPHAN_SKILL` | 0 | **0** |
| `ORPHAN_MODULE` | 0 | **0** |
| `ASSESSMENT_WITHOUT_RUBRIC` | 0 | **0** |
| `FAKE_KORA_CAPABILITY` | 0 | **0** |
| `FAKE_FREK_PROOF` | 0 | **0** |
| `NO_DUPLICATE_CURRICULUM` (vs LabelOS) | 0 violation | **0** — M01/M02 posent explicitement le renvoi, jamais un doublon ISRC/ISWC/DDEX |
| `UNRESOLVED_CRITICAL_BOUNDARY` | 0 | **0** — tension #10 (la plus forte de la carte) traitée par la règle d'application KORA, `REFERENTIAL.md` §5 |

## Détail ASSESSMENT_COVERAGE

| Competency | N1 | N2 | Terminal |
|---|---|---|---|
| C1 | `Q-N1-01` | — | — |
| C2 | `Q-N1-02` | — | — |
| C3 | — | `E-N2-01` | — |
| C4 | `Q-N1-03` | — | — |
| C5 | — | `E-N2-02` | — |
| C6 | — | `E-N2-03` | — |
| C7 | `Q-N1-04` | — | — |
| C8 | — | `E-N2-04` | — |
| C9 | — | — | `KOR08-A01` |

`CORE_BUILD = COMPLETE`, `FULL_CURRICULUM = COMPLETE`, `FULLY_COMPLETE
= FALSE` au niveau `KORA` global.
