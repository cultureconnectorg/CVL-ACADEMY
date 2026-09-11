# CVLN Academy — Mission 3 corrected: relational Excel → product truth

Date: 2026-09-11
Repository baseline: `main` @ `37e4446ac2112cf344de26da096d5053f7ddbc4e`

## Why this replaces the previous M3

The previous audit made two invalid inferences:

1. `no direct 1:1 proof found` was treated as `NOT_IMPLEMENTED`;
2. the 812 Catalogue rows and the 812 Economy rows were counted as 1,624 independent product features.

Both are wrong. PR #12 has been closed as superseded and must not be used for implementation decisions.

## Correct source model

### Catalogue + Economy are one object graph

The two source sheets contain exactly the same 812 `Code` values: **812/812 exact key intersection, zero missing keys on either side**.

Therefore:

`Catalogue object (812)` → `Economy enrichment (same 812 objects)`

Economy is not another 812 product capabilities.

Catalogue source lifecycle:

- `CANDIDATE`: 781
- `PARTIAL_RETRIEVAL`: 30
- `REQUIRES_RECONCILIATION`: 1

Economy source lifecycle:

- `Economic status = DECIDED_V1`: 811
- `Economic status = DECIDED_HOLD`: 1
- `Pricing status = DECIDED_V1`: 812
- `Décision économique = ECONOMIC_POLICY_FIXED`: 812

These statuses are source truth. `CANDIDATE` must never be translated into `NOT_IMPLEMENTED` automatically.

### Protocol layer

227 cross-cutting protocol/rule/doctrine records. Source-declared repository state:

- `NOT_CREATED`: 205
- `PARTIAL`: 18
- `FOUNDATION`: 4

This is retained as source current-state until a semantic repo trace proves a stronger state. A keyword miss is not sufficient to downgrade a row.

### Spatial layer

137 cross-cutting Spatial requirements. The source workbook still says `TO IMPLEMENT` for all 137, but the repository now contains a dedicated traceability registry and CI.

`./scripts/spatial-requirements.mjs` registers exactly 137 IDs and gives every prefix an `implementation`, `runtime`, and `tests` evidence group.

`./scripts/spatial-requirements.test.mjs` asserts:

- exactly 137 unique requirement IDs;
- an evidence group for every ID;
- non-empty implementation/runtime/test evidence arrays;
- every referenced evidence path exists;
- additional content-level assertions for selected requirements.

`.github/workflows/spatial-excel-ci.yml` runs the dedicated `137 Excel requirements` traceability job plus frontend/backend checks.

Correct M3 statement: **137/137 Spatial rows have registered traceability evidence paths.** This is stronger than `UNMAPPED`, but it is not the same claim as 137 independently semantically verified behaviours.

### Integration layer

105 cross-cutting production-readiness capabilities. Source current state:

- `BUILD`: 86
- `FOUNDATION`: 17
- `PARTIAL`: 2

Source status:

- `BUILD`: 86
- `PARTIAL`: 17
- `CONNECT`: 2

`BUILD` is an instruction/build type, not proof that no reusable implementation exists. These rows must be semantically traced against current services before reclassification.

## Current runtime product layer

The current application is not empty. `backend/seed_data.py` declares **30 formations / 13 poles** and provides a real `economics` shape on formation records. `backend/models.py` contains `FormationEconomics`. `backend/catalog_cartography.py` enriches the current 30-formation seed with contexts, audiences, delivery formats, bridge data, economics/calibration information.

That runtime layer is **not automatically identical** to the 812-object target/reference cartography.

This distinction matters because the repository already contains proof that equal-looking codes can carry incompatible semantics. `docs/SPATIAL_LEARNING_W0.5_FMS_SOURCE_AUDIT.md` documents an explicit FMS collision: the same `FMS-01-Mxx` identifiers exist in the current seed and the canonical FMS corpus with different pedagogical content. Therefore code equality alone is forbidden as an implementation proof.

## Correct M3 graph

```text
812 Catalogue objects
       │
       └── 1:1 Economy enrichment (812/812 verified)

       ├── Protocol layer:    227 cross-cutting requirements
       ├── Spatial layer:     137 cross-cutting requirements
       └── Integration layer: 105 cross-cutting capabilities

Current runtime Academy
       ├── 30 formations / 13 poles
       ├── FormationEconomics schema
       ├── current cartography/calibration engine
       ├── learning/progression/certification/etc. engines
       └── Spatial 137-ID traceability + CI
```

Before semantic deduplication between Protocol / Spatial / Integration, the 2,093 source rows represent **1,281 logical nodes**, not 2,093 independent features:

- 812 Academy catalogue objects (with Economy attached 1:1)
- 227 Protocol nodes
- 137 Spatial nodes
- 105 Integration nodes

## M3 status vocabulary from now on

- `SOURCE_CANDIDATE`: source proposes an object; no implementation conclusion.
- `SOURCE_PARTIAL`: source itself declares partial/foundation state.
- `TRACEABILITY_REGISTERED`: repo contains explicit traceability evidence for the source ID.
- `SEMANTIC_MATCH_CONFIRMED`: source and runtime object have been compared and mean the same thing.
- `SEMANTIC_CONFLICT`: same/similar key but different meaning/content.
- `UNMAPPED`: semantic trace not yet established.
- `NOT_IMPLEMENTED_CONFIRMED`: allowed only after target intent is established **and** repo/runtime absence is positively demonstrated.
- `REFERENCE_ONLY` / `DOC_ONLY`: explicitly non-runtime source material.

`UNMAPPED != NOT_IMPLEMENTED`.

## Mission 3 completion

M3 now establishes the relationship model required before Mission 4. It intentionally does **not** produce a fabricated global implementation percentage.

- [x] 812 Catalogue ↔ 812 Economy relationship verified 1:1 by source key
- [x] Source lifecycle/status preserved instead of overwritten by inference
- [x] Protocol / Spatial / Integration separated as cross-cutting layers
- [x] Current runtime Academy acknowledged as an independent current-state layer
- [x] Spatial 137-ID repo traceability acknowledged
- [x] Code-collision risk acknowledged; key equality is not semantic proof
- [x] Previous 1,902 `NOT_IMPLEMENTED` conclusion withdrawn and PR #12 closed

**M3 CORRECTED STATUS: COMPLETE AS A RELATIONAL MAPPING BASELINE.**

The next implementation audit must compare logical nodes to runtime semantically, not count spreadsheet rows as features.