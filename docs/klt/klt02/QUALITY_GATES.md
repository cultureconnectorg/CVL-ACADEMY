# KLT-02 — Quality Gates (avant FREEZE)

| Gate | Cible | Résultat | Preuve |
|---|---|---|---|
| `COMPETENCY_COVERAGE` | 100% | **100%** | 11/11 (`C1`-`C11`) dans `skills/SKILL_ID_REGISTRY.md` |
| `MODULE_COVERAGE` | 100% | **100%** | 11/11 modules écrits (`modules/M01_*.md` à `M11_*.md`) |
| `ASSESSMENT_COVERAGE` | 100% | **100%** | Chaque compétence a ≥1 item N1 ou N2 ou l'assessment terminal — voir tableau ci-dessous |
| `EVIDENCE_COVERAGE` | 100% | **100%** | 11/11 lignes complètes dans `skills/EVIDENCE_MODEL.md` |
| `ORPHAN_SKILL` | 0 | **0** | Chaque `KLT02.SKILL.Cxx` pointe module + assessment + evidence |
| `ORPHAN_MODULE` | 0 | **0** | Chaque module a une compétence unique déclarée |
| `ASSESSMENT_WITHOUT_RUBRIC` | 0 | **0** | `KLT02-A01` a sa grille complète (`RUBRIC.md`) |
| `CERTIFICATION_WITHOUT_EVIDENCE` | 0 | **0** | `KLT02-A01` exige le registre de preuves comme pièce du dossier |
| `FAKE_KILTIKONET_FEATURE` | 0 | **0** | Aucune dépendance (Network, Observatory, Compliance) présentée comme opérationnelle au-delà de ce qui est réel |
| `FAKE_OBSERVATORY` | 0 | **0** | M09 nomme explicitement l'absence d'Observatory, aucune donnée simulée |

## Détail `ASSESSMENT_COVERAGE`

| Compétence | N1 | N2 | Terminal |
|---|---|---|---|
| C1 | `Q-N1-01` | — | — |
| C2 | `Q-N1-06` | — | — |
| C3 | `Q-N1-02` | `E-N2-04` | — |
| C4 | `Q-N1-03` | `E-N2-01` | — |
| C5 | `Q-N1-09` | `E-N2-02` | — |
| C6 | `Q-N1-11` | `E-N2-04` | — |
| C7 | `Q-N1-07` | `E-N2-03` | — |
| C8 | `Q-N1-10` | — | — |
| C9 | `Q-N1-08`, `Q-N1-12` | `E-N2-06` | — |
| C10 | `Q-N1-13` | — | — |
| C11 | — | — | `KLT02-A01` |

## Verdict

Tous les gates au vert. Chaque case vide (`C1`/`C2`/`C8`/`C10` sans item
N2, `C11` sans N1/N2) est un choix explicite, pas un trou non vu — même
discipline que `klt01/QUALITY_GATES.md`.
