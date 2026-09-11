# CVLN Academy — Excel Registry

Date: 2026-09-11
Repository baseline: `main` @ `4d5d071616ba3a28ab630a33a6288bcc1013ebfb`
Mission: M1 — authoritative inventory only. This document does **not** claim implementation completeness.

## Rules

- `CORE_CANONICAL`: workbook that directly carries Academy requirements/data that must be reconciled against code/runtime/tests.
- `SUPPORTING_SOURCE`: Academy workbook that informs architecture/governance/content but is not one of the five core line-by-line audit tables.
- `SUPERSEDED`: older version retained for lineage only.
- `DERIVED_AUDIT`: workbook generated from source workbooks/repo evidence; never treated as a new source of product requirements.
- `EXACT_COPY`: duplicate binary copy of a canonical workbook; never counted twice.
- A workbook is not considered implemented merely because an audit workbook exists.

## A. Core canonical workbooks

| ID | Workbook | Principal sheet | Principal data volume | Sheets | Role | Status |
|---|---|---|---:|---:|---|---|
| XL-CORE-001 | `CVLN_Academy_Cartographie_2D_Master.xlsx` | `Master_Catalogue` | 812 catalogue rows (`A1:H813` incl. header) | 11 | Academy 2D catalogue + market/internal/ecosystem/operator/habilitation mapping | CORE_CANONICAL |
| XL-CORE-002 | `CVLN_Academy_Master_Economie_3D_DECIDE_V1.xlsx` | `Mapping_812` | 812 economic mappings (`A1:Y813` incl. header) | 15 | Economic truth, pricing, monetisation, unit economics and economic decisioning for the 812 catalogue items | CORE_CANONICAL |
| XL-CORE-003 | `CVLN_Academy_Protocols_Rules_Doctrines_Integration_Master_V1.xlsx` | `Protocol Master` | 227 protocol/rule/doctrine records (`A1:O229`: title + header + 227 records) | 7 | Governance/protocol/rule/doctrine build requirements and integration map | CORE_CANONICAL |
| XL-CORE-004 | `CVLN_Academy_Spatial_Learning_Claude_Binary_Master_UPDATED_2026-09-07.xlsx` | `MASTER_REQUIREMENTS` | 137 requirements (`A1:N138` incl. header) | 9 | Spatial Learning binary requirements, motion state machine, release gates and execution protocol | CORE_CANONICAL |
| XL-CORE-005 | `CVLN_Academy_Master_Integration_Matrix_FINAL_No_Duplicates_V2.xlsx` | `Master Integration Matrix` | 105 capability rows (`A1:AA107`: title + header + 105 records) | 17 | Cross-cutting production-readiness integration matrix: governance, legal, privacy, security, accounting, risk, quality, expert access and production gates | CORE_CANONICAL |

Core principal rows to reconcile line-by-line: **2,093** (= 812 + 812 + 227 + 137 + 105).

> Important: historical audit sheet sizes may show `Protocol Audit A1:O228` and `Integration Audit A1:Q106`; these include their audit header rows. The canonical source-table record counts above are based on the source workbook layouts, not on audit worksheet height labels.

## B. Supporting Academy source workbooks

| ID | Workbook | Principal sheet / volume | Sheets | Role | Status |
|---|---|---|---:|---|---|
| XL-SUP-001 | `CVLN_Academy_Expert_Tech_Master_Dossier.xlsx` | `MASTER_REQUIREMENTS` `A1:P232` | 13 | Expert technical dossier; 231 requirement rows plus architecture guardrails, motion system, test matrix and release gates | SUPPORTING_SOURCE |
| XL-SUP-002 | `CVLN_Agent_Secondment_Protocol_Academy.xlsx` | `SECONDMENT_REGISTRY` `A1:J22` | 12 | Agent-secondment governance, assignments, permissions, ownership and return protocol | SUPPORTING_SOURCE / external Agent Factory dependency |
| XL-SUP-003 | `CVLN_Academy_OS_Binary_Master_Plan_2026-09-03.xlsx` | `MASTER_BINARY_PLAN` `A1:O32` | 6 | Academy OS binary execution plan, rules, gates and founder decisions | SUPPORTING_SOURCE |
| XL-SUP-004 | `CVLN_Academy_Kiltikonet_Formation_Master_Plan.xlsx` | `Plan modules` `A1:J68` | 6 | Kiltikonet formation/document production plan within Academy scope | SUPPORTING_SOURCE |
| XL-SUP-005 | `CVLN_Academy_Spatial_Learning_Claude_Binary_Master.xlsx` | `MASTER_REQUIREMENTS` `A1:N138` | 7 | Pre-2026-09-07 Spatial workbook | SUPERSEDED by XL-CORE-004 |
| XL-SUP-006 | `CVLN_Academy_Master_Economie_3D.xlsx` | predecessor of `...DECIDE_V1` | 15-equivalent family | Earlier 3D economy workbook | SUPERSEDED by XL-CORE-002 |
| XL-SUP-007 | `CVLN_Academy_Master_Integration_Matrix_Production_Readiness_V1.xlsx` | `Master Integration Matrix` `A1:AA99` | 14 | Earlier production-readiness integration matrix | SUPERSEDED by XL-CORE-005 |

## C. Derived audit / execution workbooks

These are evidence and work-management artifacts. They must **not** be counted as new source requirements.

| Workbook | Key sheets | Classification |
|---|---|---|
| `CVLN_Academy_Excel_to_Repo_Truth_Audit_v0_1.xlsx` | Spatial Audit `A1:K138`; Integration Audit `A1:M106`; Protocol Audit `A1:K228`; Catalogue Truth `A1:I813`; Economy Truth `A1:L813` | DERIVED_AUDIT |
| `CVLN_Academy_Audit_Excel_Code_Implantation_HEAD_f9f2c50.xlsx` | Spatial `A1:O138`; Integration `A1:Q106`; Protocol `A1:O228`; Catalogue `A1:M813`; Economy `A1:P813` | DERIVED_AUDIT |
| `CVLN_Academy_Audit_Execution_Backlog_HEAD_f9f2c50.xlsx` | same five audit domains + `Execution Backlog A1:J40` | DERIVED_AUDIT |
| `CVLN_Academy_Audit_Execution_Backlog_HEAD_f9f2c50(1).xlsx` | copy of execution-backlog artifact | DERIVED_AUDIT / COPY CANDIDATE |
| `CVLN_ACADEMY_EXECUTION_BACKLOG.csv` | execution backlog export | DERIVED_AUDIT / EXPORT |

## D. Confirmed exact duplicate binaries

SHA-256 comparison confirmed these copies are byte-for-byte identical to their canonical originals and must not increase workbook counts:

- `CVLN_Academy_Cartographie_2D_Master(2).xlsx` = `CVLN_Academy_Cartographie_2D_Master.xlsx`
- `CVLN_Academy_Protocols_Rules_Doctrines_Integration_Master_V1(1).xlsx` = `CVLN_Academy_Protocols_Rules_Doctrines_Integration_Master_V1.xlsx`
- `CVLN_Academy_Spatial_Learning_Claude_Binary_Master_UPDATED_2026-09-07(1).xlsx` = `CVLN_Academy_Spatial_Learning_Claude_Binary_Master_UPDATED_2026-09-07.xlsx`
- `CVLN_Academy_Master_Integration_Matrix_FINAL_No_Duplicates_V2(1).xlsx` = `CVLN_Academy_Master_Integration_Matrix_FINAL_No_Duplicates_V2.xlsx`

`CVLN_Academy_Cartographie_2D_Master(1).xlsx` and `CVLN_Academy_Master_Economie_3D(1).xlsx` remain lineage/copy candidates until binary-hash comparison is recorded; they are not counted as additional canonical sources.

## E. Repository truth

At the baseline above, the Git tree itself contains **no `.xlsx` blobs**. The repository contains implementation code, audit documents and CI references to the source workbooks. For example, the Spatial CI runs line-by-line traceability for the 137 Spatial requirements, while code comments reference the Expert Tech Master Dossier / `MOTION_SYSTEM` sheet.

Therefore the authoritative Excel contract currently spans two evidence locations:

1. source workbooks retained outside the Git tree;
2. repository code/tests/audit documents that claim or prove implementation.

Mission 2 must bridge those two locations explicitly instead of assuming that presence in `/docs` means the workbook row is implemented.

## M1 completion gate

- [x] Repository identified: `cultureconnectorg/CVL-ACADEMY`
- [x] Git baseline recorded
- [x] Five core canonical workbooks isolated
- [x] Core source table sizes recorded
- [x] Supporting/superseded workbooks separated from core
- [x] Derived audits separated from source requirements
- [x] Known exact duplicate binaries excluded from canonical count
- [x] Canonical core row total established: **2,093 principal records**
- [x] No claim made about coding/runtime/test completeness

**M1 STATUS: COMPLETE**
