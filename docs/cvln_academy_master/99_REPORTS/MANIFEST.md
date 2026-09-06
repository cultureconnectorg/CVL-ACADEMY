# CVLN Academy Master — Manifest

```
Structure of docs/cvln_academy_master/ — 33 files across 13 folders,
plus 11 raw source CSVs preserved verbatim. All 812 Master 2D rows are
RECONCILED_NOT_BUILT (see 00_GOVERNANCE/QUALITY_GATES.md for the final
tally). The two decisions the Founder asked to close are closed
(FD-CVE-001, FD-CIP-001) — one distinct, pre-existing Founder decision
remains open (FRK-71, FREK v3 architecture, never covered by either
closure).
```

```
docs/cvln_academy_master/
  00_GOVERNANCE/
    TAXONOMY.md
    ACCESS_LEVELS.md
    AUTHORIZATION_MODEL.md
    BUILD_METHOD.md
    UPGRADE_PRINCIPLE.md
    QUALITY_GATES.md              — final gate tally, 812/812 reconciled
  10_PORTFOLIO/
    MASTER_INDEX.md
    PORTFOLIO_MAP.md
    CONTEXT_MATRIX.md
    RECONCILIATION_MATRIX.md      — per-domain status, one row per Master 2D domain
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
    FMS_07_18_RECONCILIATION.md                                    (12 rows)
    FREK_01_75_RECONCILIATION.md                                   (75 rows)
    WALLET_CVE_RECONCILIATION.md                                   (52 rows, incl. CVE — FD-CVE-001 closed)
    AGENT_FACTORY_IOS_BRAIN_CMD_LAURENTIA_RECONCILIATION.md        (109 rows)
    GOOD_MOOD_DJ_SAYD_RECONCILIATION.md                            (94 rows)
    CYBERSECURE_BLOCKCHAIN_GALA_HOSPITALITY_LABELOS_RECONCILIATION.md (214 rows)
  30_INTERNAL/
    INTERNAL_DOMAINS_INDEX.md
    KLT_09_20_RECONCILIATION.md                                    (12 rows)
    KORA_OP_X_RECONCILIATION.md                                    (19 rows)
    FOUNDER_CEO_GROUP_FONDATION_RECONCILIATION.md                  (158 rows, incl. CIP/Fondation — FD-CIP-001 closed)
  40_OPERATOR_ROLES/
    ROLE_REGISTRY.md               — 130/130 Operator_Roles indexed by domain
  50_AUTHORIZATIONS/
    AUTHORIZATION_REGISTRY.md      — 71/71 Habilitations, all CANDIDATE
  60_CROSS_ECOSYSTEM/
    CROSS_ECOSYSTEM_MAP.md
    XCV_TRANSVERSAL_RECONCILIATION.md                              (67 rows)
  70_EVIDENCE/
    EVIDENCE_ARCHITECTURE.md
  80_MISSIONS/
    MISSIONS_PIPELINES.md
  90_SPATIAL/
    SPATIAL_RELATIONSHIP_MAP.md
  95_GAPS/
    REPO_TRUTH_AUDIT.md
    GAP_REGISTER.md                — G1-G11
  100_ECONOMY/
    ECONOMIC_MODEL.md              — 7 engines, ECO-001->045, offers, margins, policies, roadmap (DECIDED_V1)
    raw/
      Mapping_812.csv (812 rows — per-object economic packaging/pricing/gate)
      Offres_Economiques.csv, Pricing_V1.csv, Unit_Economics.csv (20 SKUs)
      Decisions_Fondateur.csv (ECO-001->045)
      Economie_Domaines.csv (27 domains), Valeur_Interne.csv, Learning_to_Work.csv
      Sources_Methodo.csv, B2B_B2G.csv, Plan_36M.csv, Policies.csv,
      Roadmap_Monetisation.csv, Hypotheses.csv, Dashboard.csv
  99_REPORTS/
    W0_AUDIT_REPORT.md
    MANIFEST.md (this file)
    CHANGELOG.md                   — full commit history of the reconciliation arc
```

## Domain row accounting (812/812)

FMS 12 + FREK 75 + Kiltikonet (KLT-09→20) 12 + Wallet+CVE 52 + KORA
(internal/cross) 19 + Agent Factory/AF-X/Laurentia/IOS/Brain/CMD/
Intelligent Operations 109 + Good Mood+DJ Sayd 94 + CyberSecure+
Blockchain+Tokenomics+Gala+Hospitality+LabelOS 214 + Founder/CEO+CVLN
Group+Fondation Cœurvolan 158 + Cross-CVLN/XCV 67 = **812**.

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

## Next phase

**W6** — real pedagogical referentials, built by wave, per the order
and discipline set out in `99_REPORTS/CHANGELOG.md`. This Master
Package's reconciliation layer (`RECONCILED_NOT_BUILT`) is the
canonical entry point for W6 — it is never rebuilt or re-derived.
