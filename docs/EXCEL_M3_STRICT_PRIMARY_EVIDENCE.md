# CVLN Academy — Mission 3 STRICT PRIMARY EVIDENCE

Baseline: `37e4446ac2112cf344de26da096d5053f7ddbc4e`

## Evidence rule

Mission 3 may conclude only from primary evidence:

- original Excel source workbooks;
- executable backend/frontend source code;
- routes, models, seeds, configuration and startup wiring;
- executable tests;
- GitHub Actions run/job results.

README files, audit reports, generated reports and prior status documents are navigation hints only. They cannot upgrade any implementation status.

## Catalogue + Economy relation

The original `Master_Catalogue` contains 812 rows. The original `Mapping_812` contains 812 rows. Their `Code` key sets are identical: 812/812 codes join 1:1.

Therefore the Economy workbook is an economic enrichment of the same 812 catalogue objects; it is not an additional set of 812 independent product features.

## Direct comparison to current runtime seed

The current executable seed is `backend/seed_data.py`; `backend/seed.py` upserts every seed formation into `db.formations` by code, and `backend/server.py` calls that seed at startup.

Comparison of the original 812 Catalogue rows to the 30 formation objects in `backend/seed_data.py` yields:

- exact code + exact title matches: **0**;
- same code but different title: **14**;
- no direct formation code in the current 30-formation seed: **798**.

Interpretation is deliberately conservative:

- same code + different title = `CODE_COLLISION_TITLE_DIFFERS`, not equivalence;
- no direct runtime code = `UNPROVEN`, not `NOT_IMPLEMENTED`.

No object is declared missing solely because it does not appear as a top-level formation code. A catalogue row may represent a métier, capability, module, internal qualification, role, mission, bridge or another layer requiring a different code path.

## Source lifecycle states retained

Original source workbooks declare:

- Catalogue: 781 `CANDIDATE`, 30 `PARTIAL_RETRIEVAL`, 1 `REQUIRES_RECONCILIATION`;
- Protocol Master: 205 `NOT_CREATED`, 18 `PARTIAL`, 4 `FOUNDATION` in `Repo Status`;
- Spatial Master: 137 `TO IMPLEMENT` source rows;
- Integration Matrix: 86 `BUILD`, 17 `FOUNDATION`, 2 `PARTIAL` in `Current State`.

These source states are not replaced by inferred repo states without direct code/test/runtime evidence.

## Spatial primary-evidence tiers

Primary executable sources are `scripts/spatial-requirements.mjs` and `scripts/spatial-requirements.test.mjs`.

- 137 requirement IDs are registered;
- 52 IDs have a dedicated `CONTENT_ASSERTIONS` semantic/static assertion;
- the other 85 are covered by evidence-path registration but do not have their own dedicated semantic assertion in that test;
- therefore those 85 are `PATH_TRACEABILITY_ONLY`, not individually verified implementation claims.

GitHub Actions run `34598290570` on the baseline SHA shows:

- `137 Excel requirements`: **PASS**;
- `Backend lint types tests`: **PASS**;
- `Frontend lint unit build`: **FAIL** at Production build;
- `Frontend Playwright runtime`: **FAIL** at Runtime E2E.

So the dedicated Spatial traceability job is green, while global CI/runtime is not green on the same SHA.

## Mission 3 strict conclusion

The previous global `1,902 NOT_IMPLEMENTED` conclusion is invalid and withdrawn.

At this stage, the defensible statuses are relationship/evidence statuses, not guessed implementation completeness:

- `EXACT_RUNTIME_ID_TITLE`;
- `CODE_COLLISION_TITLE_DIFFERS`;
- `UNPROVEN`;
- `DIRECT_CONTENT_ASSERTION`;
- `PATH_TRACEABILITY_ONLY`;
- source-declared lifecycle states until direct primary evidence permits an upgrade.

`UNPROVEN != NOT_IMPLEMENTED` remains mandatory.