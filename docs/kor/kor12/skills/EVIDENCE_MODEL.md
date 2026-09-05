# KOR-12 — Evidence Model

| Compétence | EVIDENCE_TYPE (`DATA_ANALYSIS`-shaped) | VERIFICATION_RULE | READY_FOR_FREK_PROOF |
|---|---|---|---|
| C1 | `EVENT_PLAN` | événements pertinents et non intrusifs | `FALSE` |
| C2 | `DASHBOARD_SPEC` | pas de métrique de vanité | `FALSE` |
| C3 | `DATA_QUALITY_REPORT` | problème identifié et corrigé | `FALSE` |
| C4 | `AUDIENCE_BEHAVIOR_NOTE` | limites d'échantillon explicites | `FALSE` |
| C5 | `COHORT_ANALYSIS` | critère de découpage défendable | `FALSE` |
| C6 | `RETENTION_REPORT` | pas de sur-généralisation | `FALSE` |
| C7 | `TREND_NOTE` | tendance distinguée du bruit | `FALSE` |
| C8 | `CONTENT_PERFORMANCE_REPORT` | multi-critères, jamais un seul chiffre | `FALSE` |
| C9 | `RECOMMENDATION_CONCEPT_NOTE` | aucune capacité réelle affirmée | `FALSE` |
| C10 | `BIAS_ASSESSMENT_REPORT` | biais culturels explicitement traités | `FALSE` |
| C11 | `CULTURAL_INTELLIGENCE_NOTE` | lectures multiples avant conclusion | `FALSE` |
| C12 | `EDITORIAL_INSIGHT_NOTE` | éclaire, ne décide pas | `FALSE` |
| C13 | `DATA_INTELLIGENCE_CASE_FILE` | rubric §RUBRIC.md | `FALSE` |

`READY_FOR_FREK_PROOF = FALSE` partout — aucune télémétrie streaming
réelle n'existe dans ce repo.
`PRIVACY_LEVEL` : toute note utilisant des données de comportement
individuel simulées reste **sensible** si elle référence des personnes
identifiables du cas fil rouge.
