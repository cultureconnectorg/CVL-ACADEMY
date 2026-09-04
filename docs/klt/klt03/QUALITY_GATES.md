# KLT-03 — Quality Gates (avant FREEZE)

| Gate | Cible | Résultat | Preuve |
|---|---|---|---|
| `COMPETENCY_COVERAGE` | 100% | **100%** | 12/12 (`C1`-`C12`) dans `skills/SKILL_ID_REGISTRY.md` |
| `MODULE_COVERAGE` | 100% | **100%** | 12/12 modules écrits |
| `ASSESSMENT_COVERAGE` | 100% | **100%** | Chaque compétence a ≥1 item N1/N2/terminal — voir tableau ci-dessous |
| `EVIDENCE_COVERAGE` | 100% | **100%** | 12/12 lignes dans `skills/EVIDENCE_MODEL.md` |
| `ORPHAN_SKILL` | 0 | **0** | Chaque `KLT03.SKILL.Cxx` pointe module + assessment + evidence |
| `ORPHAN_MODULE` | 0 | **0** | Chaque module a une compétence unique |
| `ASSESSMENT_WITHOUT_RUBRIC` | 0 | **0** | `KLT03-A01` a `RUBRIC.md` |
| `CERTIFICATION_WITHOUT_EVIDENCE` | 0 | **0** | `KLT03-A01` exige le registre de preuves |
| `FAKE_KILTIKONET_FEATURE` | 0 | **0** | Aucune dépendance présentée comme opérationnelle au-delà du réel |
| `FAKE_OBSERVATORY` | 0 | **0** | M10 nomme explicitement l'absence, aucune donnée simulée |
| `UNSOURCED_INSTITUTIONAL_FACT` (gate propre à KLT-03) | 0 | **0** | Chaque module institution-spécifique (M02-M05) porte `SOURCE_STATUS = PEDAGOGICAL_ILLUSTRATIVE` |

## Détail `ASSESSMENT_COVERAGE`

| Compétence | N1 | N2 | Terminal |
|---|---|---|---|
| C1 | `Q-N1-01` | `E-N2-02` | — |
| C2 | `Q-N1-02` | — | — |
| C3 | `Q-N1-11` | `E-N2-02` | — |
| C4 | — | `E-N2-01` | — |
| C5 | `Q-N1-03` | — | — |
| C6 | `Q-N1-04` | `E-N2-03` | — |
| C7 | `Q-N1-07` | `E-N2-04` | — |
| C8 | `Q-N1-09` | `E-N2-04` | — |
| C9 | `Q-N1-08` | `E-N2-05` | — |
| C10 | `Q-N1-12` | `E-N2-06` | — |
| C11 | `Q-N1-10` | — | — |
| C12 | — | — | `KLT03-A01` |

## Verdict

Tous les gates au vert, y compris le gate propre à `KLT-03`
(`UNSOURCED_INSTITUTIONAL_FACT = 0`) — la discipline `SOURCE_STATUS`
est appliquée à chaque module institution-spécifique (M02-M05), pas
seulement mentionnée en principe.
