# CVLN Academy — Mission 3: Excel → current `main` implementation mapping

Date: 2026-09-11

Audited repository baseline: `37e4446ac2112cf344de26da096d5053f7ddbc4e` (`main`).

Mission 3 classifies every one of the 2,093 canonical core Excel rows against the code that is actually present on current `main`. It does **not** inherit implementation verdicts from the historical `f9f2c50` audit branch: GitHub comparison shows that history is diverged from current `main`, so prior branch-only modules are not current evidence.

A final moving-head check was also performed. `main` advanced by four commits during the audit; those commits changed only `.github/workflows/spatial-excel-ci.yml`, `README.md`, `frontend/README.md`, and `frontend/e2e/README.md`. No application runtime file changed, so the row classifications remained unchanged and the baseline was moved to the newer SHA above.

## Status vocabulary

- `IMPLEMENTED`: current-main implementation/runtime/test evidence exists with a row-specific semantic assertion.
- `PARTIAL`: a real implementation destination exists, but the exact row/capability is only partially covered or the evidence is group-level.
- `NOT_IMPLEMENTED`: no exact current-main row-level runtime mapping is proven.
- `REFERENCE_ONLY`: principle/reference exists, but not as executable product behavior.
- `DOC_ONLY`: documentation/legal text exists without the requested runtime capability.

## Result

| Domain | Rows | IMPLEMENTED | PARTIAL | NOT_IMPLEMENTED | REFERENCE_ONLY | DOC_ONLY |
|---|---:|---:|---:|---:|---:|---:|
| Catalogue 2D | 812 | 0 | 0 | 812 | 0 | 0 |
| Economy 3D | 812 | 0 | 0 | 812 | 0 | 0 |
| Protocol / Rules / Doctrines | 227 | 0 | 29 | 193 | 2 | 3 |
| Spatial Learning | 137 | 52 | 85 | 0 | 0 | 0 |
| Integration Matrix | 105 | 0 | 19 | 85 | 0 | 1 |
| **TOTAL** | **2,093** | **52** | **133** | **1,902** | **2** | **4** |

## Critical finding — Catalogue 812 and Economy 812

The 812-line canonical source datasets are not present/imported 1:1 on current `main`. The current seed catalogue is still the 30-formation `backend/seed_data.py` catalogue documented by `docs/product/catalogue-cartography-report.md`.

There are 14 code collisions between the 812-line master and the current 30-formation seed (`FRK-01..03`, `LOS-01..03`, `GMD-01`, `GRP-01..02`, `SAY-01`, `BRN-01..03`, `HOS-01`), but **all 14 have different titles/semantics**. They are rejected as false-positive implementation matches. Example: Excel `FRK-01 = FREK Foundations & Cultural Trust Infrastructure`, while current seed `FRK-01 = FREK Operator`.

Historical audit anchors such as `docs/cvln_academy_master/10_PORTFOLIO/raw/Master_Catalogue.csv`, `docs/cvln_academy_master/100_ECONOMY/raw/Mapping_812.csv`, and `services/canonical_convergence.py` return 404 on current `main`; they are not accepted as evidence.

## Spatial Learning

Current `main` explicitly registers all 137 Spatial IDs in `scripts/spatial-requirements.mjs`. `scripts/spatial-requirements.test.mjs` verifies an implementation/runtime/test evidence set for each ID and adds row-specific semantic/content assertions for 52 IDs. Therefore:

- 52 rows = `IMPLEMENTED` for Mission 3 mapping.
- 85 rows = `PARTIAL`: evidence paths exist and are CI-traced, but the test is prefix/group-level rather than a row-specific semantic proof.

This is **not** a claim that all 137 are production-verified; Mission 3 maps code destinations, while later missions still validate runtime and CI on one final SHA.

## Legal changes detected on current main

Mission 3 incorporates the new legal gate rather than relying on stale source statuses. Current code includes:

- `backend/legal_policy.py` — versioned required legal bundle + document hashes.
- `backend/api/legal.py` — `/legal/requirements`, `/legal/accept`, version validation, signature hash, evidence fingerprint and persisted acceptance record.
- `frontend/src/pages/LegalAcceptance.jsx` — finger/mouse/stylus signature canvas and legal acceptance flow.
- `frontend/src/components/CookieConsent.jsx` — necessary/all cookie preference with a local versioned preference.

These create partial mappings for narrow legal/signature/version/consent capabilities, but they do **not** justify marking the broader Legal/Privacy/Trust engines as complete.

## Important current-main gaps

- No 812-row Catalogue runtime projection.
- No 812-row Economy runtime projection.
- No checkout/payment processor/subscription/invoice/accounting engine proven on current `main`.
- Attendance/emargement remains absent as an operational model; current delivery audit explicitly records no session/date/location/capacity/attendance record model.
- Most Integration Matrix capabilities remain target-state `BUILD`, not runtime behavior.
- Most protocol/rule/doctrine rows remain unimplemented as row-specific executable controls.

## Mission 3 closure rule

Every core row now has exactly one Mission 3 status and an implementation destination/evidence note in the generated full matrix artifact. `NOT_IMPLEMENTED` is an acceptable Mission 3 outcome: it is the truth that Mission 4 must act on.

**M3 STATUS: COMPLETE (classification/mapping), with implementation gaps intentionally preserved.**
