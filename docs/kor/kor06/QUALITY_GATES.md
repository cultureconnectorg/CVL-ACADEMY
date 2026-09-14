# KOR-06 — Quality Gates

| Gate | Cible | Résultat |
|---|---|---|
| `COMPETENCY_COVERAGE` | 100% | **100%** (9/9) |
| `MODULE_COVERAGE` | 100% | **100%** (9/9) |
| `ASSESSMENT_COVERAGE` | 100% | **100%** |
| `EVIDENCE_COVERAGE` | 100% | **100%** |
| `ORPHAN_SKILL` | 0 | **0** |
| `ORPHAN_MODULE` | 0 | **0** |
| `ASSESSMENT_WITHOUT_RUBRIC` | 0 | **0** |
| `FAKE_KORA_CAPABILITY` | 0 | **0** — véhicule Anba Tonèl Host, jamais présenté comme KORA |
| `FAKE_FREK_PROOF` | 0 | **0** |
| `UNRESOLVED_CRITICAL_BOUNDARY` | 0 | **0** — tension #2 (`KOR-14`) posée en `REFERENTIAL.md` §5 |

## Détail ASSESSMENT_COVERAGE

| Competency | N1 | N2 | Terminal |
|---|---|---|---|
| C1 | `Q-N1-01` | — | — |
| C2 | `Q-N1-02` | — | — |
| C3 | — | `E-N2-01` | — |
| C4 | `Q-N1-03` | — | — |
| C5 | — | `E-N2-02` | — |
| C6 | — | `E-N2-03` | — |
| C7 | — | `E-N2-04` | — |
| C8 | `Q-N1-04` | — | — |
| C9 | — | — | `KOR06-A01` |

## Verdict et note produit

`CORE_BUILD = COMPLETE`, `FULL_CURRICULUM = COMPLETE`. Au niveau
produit KORA (distinct du niveau pédagogique) : `KORA_PRODUCT_GAP`
documenté en `REFERENTIAL.md` §6 (DSP/CDN/monitoring/multi-territoires
= `CAPABILITY_NOT_IMPLEMENTED`), alimentera le
`KORA_PRODUCT_CAPABILITY_GAP_MAP` final. `FULLY_COMPLETE = FALSE` au
niveau `KORA` global.
