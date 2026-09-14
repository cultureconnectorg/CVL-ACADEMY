# KOR-05 — Quality Gates

| Gate | Cible | Résultat |
|---|---|---|
| `COMPETENCY_COVERAGE` | 100% | **100%** (10/10) |
| `MODULE_COVERAGE` | 100% | **100%** (10/10) |
| `ASSESSMENT_COVERAGE` | 100% | **100%** |
| `EVIDENCE_COVERAGE` | 100% | **100%** |
| `ORPHAN_SKILL` | 0 | **0** |
| `ORPHAN_MODULE` | 0 | **0** |
| `ASSESSMENT_WITHOUT_RUBRIC` | 0 | **0** |
| `FAKE_KORA_CAPABILITY` | 0 | **0** — limite d'échelle de C8 explicitement reconnue, jamais comblée |
| `FAKE_FREK_PROOF` | 0 | **0** |
| `UNRESOLVED_CRITICAL_BOUNDARY` | 0 | **0** — tension #7 (`KOR-13`) posée en `REFERENTIAL.md` §5 |

## Détail ASSESSMENT_COVERAGE

| Competency | N1 | N2 | Terminal |
|---|---|---|---|
| C1 | `Q-N1-01` | — | — |
| C2 | — | `E-N2-01` | — |
| C3 | `Q-N1-02` | — | — |
| C4 | — | `E-N2-02` | — |
| C5 | — | `E-N2-03` | — |
| C6 | `Q-N1-03` | — | — |
| C7 | — | `E-N2-04` | — |
| C8 | `Q-N1-04` | — | — |
| C9 | — | `E-N2-05` | — |
| C10 | — | — | `KOR05-A01` |

`CORE_BUILD = COMPLETE`, `FULL_CURRICULUM = COMPLETE`, `FULLY_COMPLETE
= FALSE` au niveau `KORA` global.
