# CVLN Academy — Mission 2: line-by-line classification

Date: 2026-09-11

Mission 2 scope: decompose every principal row from the five canonical Academy workbooks identified by `docs/EXCEL_REGISTRY.md`. This mission classifies source requirements/data only. It does **not** assert CODED, WIRED, RUNTIME, TESTED or CI status.

## Result

| Domain | Canonical records | Stable ID range | Status |
|---|---:|---|---|
| Catalogue 2D | 812 | `ACA-CAT-0001` → `ACA-CAT-0812` | CLASSIFIED |
| Economy 3D | 812 | `ACA-ECO-0001` → `ACA-ECO-0812` | CLASSIFIED |
| Protocol / Rules / Doctrines | 227 | `ACA-PRT-0001` → `ACA-PRT-0227` | CLASSIFIED |
| Spatial Learning | 137 | `ACA-SPA-0001` → `ACA-SPA-0137` | CLASSIFIED |
| Master Integration Matrix | 105 | `ACA-INT-0001` → `ACA-INT-0105` | CLASSIFIED |
| **TOTAL** | **2,093** | **2,093 unique stable IDs** | **M2 COMPLETE** |

## Stable-ID contract

Stable IDs are sequential inside a canonical workbook and are bound to the source workbook + source sheet + physical Excel row + source key. They are independent from product implementation paths. Mission 3 must use these stable IDs as the join key between Excel evidence and code/runtime evidence.

Prefixes:

- `ACA-CAT-*`: `CVLN_Academy_Cartographie_2D_Master.xlsx` / `Master_Catalogue`
- `ACA-ECO-*`: `CVLN_Academy_Master_Economie_3D_DECIDE_V1.xlsx` / `Mapping_812`
- `ACA-PRT-*`: `CVLN_Academy_Protocols_Rules_Doctrines_Integration_Master_V1.xlsx` / `Protocol Master`
- `ACA-SPA-*`: `CVLN_Academy_Spatial_Learning_Claude_Binary_Master_UPDATED_2026-09-07.xlsx` / `MASTER_REQUIREMENTS`
- `ACA-INT-*`: `CVLN_Academy_Master_Integration_Matrix_FINAL_No_Duplicates_V2.xlsx` / `Master Integration Matrix`

## Classification families

The classification is deliberately semantic and conservative. It does not infer implementation.

- Catalogue: `CATALOGUE_FORMATION`, `CATALOGUE_CERTIFICATION`, `CATALOGUE_MISSION`, `CATALOGUE_ITEM`.
- Economy: `ECONOMIC_INTERNAL_VALUE`, `ECONOMIC_B2G`, `ECONOMIC_B2B`, `ECONOMIC_PUBLIC_OFFER`, `ECONOMIC_MAPPING`.
- Protocol: `GOVERNANCE_DOCTRINE`, `GOVERNANCE_PROTOCOL`, `GOVERNANCE_RULE`, `GOVERNANCE_POLICY`, `GOVERNANCE_REQUIREMENT`.
- Spatial: product, governance, motion, accessibility, navigation and test requirement classes.
- Integration: domain + build-type classes such as `INTEGRATION_GOVERNANCE_EXTEND`, `INTEGRATION_LEGAL_BUILD`, `INTEGRATION_SECURITY_CONNECT`.

## Extraction validation

The source XLSX XML was read directly after a first high-level inspection path truncated large worksheets. The final extraction was rejected until the exact canonical counts were recovered:

```text
CATALOGUE   812
ECONOMY     812
PROTOCOL    227
SPATIAL     137
INTEGRATION 105
TOTAL       2093
UNIQUE IDS  2093/2093
```

A full Mission 2 workbook and machine-readable exports were generated from this validated extraction. Artifact checksums at generation time:

- `CVLN_Academy_Mission2_Line_Classification.xlsx` SHA-256 `e42ef711785ac71446777c5dfee65b236c1ff31b85f554fdc168f86844b8a138`
- `CVLN_Academy_M2_Line_Classification.csv` SHA-256 `3d8de350887e0c185d472c8d12bb8bba1532e3f0315464ef5665a99e02f5a873`
- compact stable index SHA-256 `66e7f973ac8d1886ece89c34d0492f8beccedaaf4672ea828fe30d3c35560fe5`

## Mission 3 handoff schema

Each classified record contains:

- `stable_id`
- `domain`
- `source_workbook`
- `source_sheet`
- `source_excel_row`
- `source_key`
- `title`
- `classification`
- `classification_status`
- `source_status`
- `priority`
- full source-row payload

Mission 3 must append evidence fields rather than mutate M2 semantics: `implementation_disposition`, `code_paths`, `api_paths`, `runtime_surface`, `data_store`, `test_paths`, `evidence_status`, and `gap_reason`.

**M2 STATUS: COMPLETE — 2,093/2,093 source records classified, 2,093/2,093 stable IDs unique.**
