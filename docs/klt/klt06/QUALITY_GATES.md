# KLT-06 — Quality Gates (avant FREEZE)

| Gate | Cible | Résultat | Preuve |
|---|---|---|---|
| `COMPETENCY_COVERAGE` (buildable) | 100% de 5/7 | **100% de 5/7** | C1-C4, C7 dans `skills/SKILL_ID_REGISTRY.md` ; C5/C6 explicitement `BLOCKED`, pas comptés comme couverts |
| `MODULE_COVERAGE` (buildable) | 100% de 5/7 | **100%** | 5/5 modules buildable écrits (M01-M04, M07) |
| `ASSESSMENT_COVERAGE` (buildable) | 100% | **100%** | Chaque compétence buildable a ≥1 item — voir tableau ci-dessous |
| `EVIDENCE_COVERAGE` (buildable) | 100% | **100%** | 5/5 lignes réelles dans `skills/EVIDENCE_MODEL.md` |
| `ORPHAN_SKILL` | 0 | **0** | Chaque `KLT06.SKILL.Cxx` buildable pointe module + assessment + evidence |
| `ORPHAN_MODULE` | 0 | **0** | Chaque module a une compétence unique |
| `ASSESSMENT_WITHOUT_RUBRIC` | 0 | **0** | `KLT06-A01` a `RUBRIC.md` |
| `FAKE_OBSERVATORY` | 0 | **0** | Aucune donnée Observatory simulée pour combler M05/M06 ; `M05`/`M06` explicitement `BLOCKED`, pas construits |
| `BLOCKED_COMPETENCY_MISREPRESENTED` (gate propre à KLT-06) | 0 | **0** | `C5`/`C6` marquées `BLOCKED` partout (référentiel, registre, evidence, certification, guides) — jamais présentées comme couvertes |
| `PARTIAL_CERTIFICATION_DISCLOSED` (gate propre à KLT-06) | 100% | **100%** | `A01_CERTIFICATION_ASSESSMENT.md`, `CERTIFICATION_MODEL.md`, guide candidat déclarent tous explicitement la couverture partielle |
| `FULLY_COMPLETE` | `FALSE` | **`FALSE`** | 2/7 compétences (`C5`,`C6`) `BLOCKED` — ce gate reste `FALSE` tant qu'elles ne sont pas réellement connectées à Observatory, pas seulement rédigées ; toute déclaration `TRUE` sans reconnexion réelle serait une violation de ce gate |

## Détail `ASSESSMENT_COVERAGE` (buildable)

| Compétence | N1 | N2 | Terminal |
|---|---|---|---|
| C1 | `Q-N1-01`, `Q-N1-02` | — | — |
| C2 | `Q-N1-03`, `Q-N1-04` | `E-N2-01` | — |
| C3 | `Q-N1-05`, `Q-N1-06` | `E-N2-02` | — |
| C4 | `Q-N1-07`, `Q-N1-08` | `E-N2-03` | — |
| C7 | `Q-N1-09`, `Q-N1-10` | `E-N2-04` | `KLT06-A01` |

## Verdict

Tous les gates au vert pour le périmètre buildable (5/7). Le gate le
plus important de cette formation (`BLOCKED_COMPETENCY_MISREPRESENTED =
0`) est vérifié à chaque niveau du package, pas seulement affirmé une
fois en introduction.
