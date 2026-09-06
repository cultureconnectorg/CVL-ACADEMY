# CVLN Academy Master — Manifest

```
Structure of docs/cvln_academy_master/ — 24 files across 12 folders,
plus 11 raw source CSVs preserved verbatim.
```

```
docs/cvln_academy_master/
  00_GOVERNANCE/
    TAXONOMY.md
    ACCESS_LEVELS.md
    AUTHORIZATION_MODEL.md
    BUILD_METHOD.md
    QUALITY_GATES.md
  10_PORTFOLIO/
    MASTER_INDEX.md
    PORTFOLIO_MAP.md
    CONTEXT_MATRIX.md
    RECONCILIATION_MATRIX.md
    raw/
      Master_Catalogue.csv (812 rows)
      External_Market.csv (437 rows)
      Internal_CVLN.csv (220 rows)
      Cross_Ecosystem.csv (153 rows)
      Operator_Roles.csv (130 rows)
      Habilitations.csv (71 rows)
      Access_Levels.csv (7 rows)
      Missions_Pipelines.csv (10 rows)
      Coverage_Gaps.csv (6 rows)
      Taxonomy.csv (9 rows)
      Dashboard.csv (29 rows, source spreadsheet's own summary view)
  20_EXTERNAL/
    EXTERNAL_DOMAINS_INDEX.md
  30_INTERNAL/
    INTERNAL_DOMAINS_INDEX.md
  40_OPERATOR_ROLES/
    ROLE_REGISTRY.md
  50_AUTHORIZATIONS/
    AUTHORIZATION_REGISTRY.md
  60_CROSS_ECOSYSTEM/
    CROSS_ECOSYSTEM_MAP.md
  70_EVIDENCE/
    EVIDENCE_ARCHITECTURE.md
  80_MISSIONS/
    MISSIONS_PIPELINES.md
  90_SPATIAL/
    SPATIAL_RELATIONSHIP_MAP.md
  95_GAPS/
    REPO_TRUTH_AUDIT.md
    GAP_REGISTER.md
  99_REPORTS/
    W0_AUDIT_REPORT.md
    MANIFEST.md (this file)
    CHANGELOG.md
```

## Regenerate raw/ from source

```
python3 -c "
import pandas as pd
xl = pd.ExcelFile('CVLN_Academy_Cartographie_2D_Master.xlsx')
for s in xl.sheet_names:
    xl.parse(s).to_csv(f'{s}.csv', index=False)
"
```

Source file: `CVLN_Academy_Cartographie_2D_Master.xlsx` (uploaded by
the Founder, not committed to the repo — the CSVs in `raw/` are its
full, lossless snapshot at the time of this audit).
