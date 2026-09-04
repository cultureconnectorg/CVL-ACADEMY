# Canonical Kiltikonet Runtime Binding Report — "branchage complet de Kiltikonet"

```
Branch: claude/cvln-academy-canonical-fms
Founder authorization (2026-09-04): "Continue le branchage complet de
Kiltikonet." — following exactly the non-destructive pattern already
proven for FMS (ACA-0006, docs/ACADEMY_FMS_CANONICAL_RUNTIME_BINDING_
REPORT.md).
DB_FORMATIONS_MUTATION = FORBIDDEN — respected: this package never
reads, writes, or imports `db.formations`. seed_data.py untouched.
STOP_AFTER_DELIVERY = TRUE.
```

## What "branchage" means here

Until this ticket, the entire Kiltikonet corpus (KLT-01→08, `docs/klt/`)
was documentation only — real, industrial-depth, but inert: no code
read it, no API served it, no route or page rendered it. "Branchage
complet" connects it to the actual Academy runtime, exactly as ACA-0006
did for the FMS canonical archive: a new, additive, read-only package
(`backend/klt_canonical/`) that scans the real files, persists a
structured read model to a **new** collection, and serves it through a
**new** API router and **new** frontend pages — the legacy `db.
formations` catalogue, `seed_data.py`, and every existing route/page
stay byte-for-byte untouched.

## Why FMS's ZIP-upload pattern needed one real adaptation

FMS's canonical archive is a file a human uploads (`POST /canonical/
import`, multipart). Kiltikonet has no such archive — `docs/klt/`
already lives unpacked in this repo. So `POST /klt-canonical/import`
takes no file: it scans `docs/klt/kltXX/` directly on the server
filesystem (`klt_canonical.provenance.default_docs_dir()`, overridable
via `KLT_DOCS_DIR` for deployments where `docs/` isn't a sibling of
`backend/`). Same idempotent-upsert guarantee, same exhaustive
provenance ledger, same additive-only posture — different trigger.

## The one invariant this whole package exists to enforce structurally

The Founder's instruction from earlier this session ("on ne doit pas
déclarer KLT-06/07/08 FULLY_COMPLETE tant que leurs compétences
bloquées ne sont pas réellement connectées") is not re-asserted here in
prose — it is **computed, live, at import time**, from each formation's
own `skills/SKILL_ID_REGISTRY.md`:

```python
# klt_canonical/read_model.py
skill_rows = registry_doc.get("skill_rows", [])
blocked_skill_ids = [r["skill_id"] for r in skill_rows if r["status"] == "BLOCKED"]
fully_complete = len(blocked_skill_ids) == 0
```

`fully_complete` is a field on `CanonicalKltFormation`, never a
hardcoded constant. KLT-01→05's registries carry 5 columns (no status
column at all — every skill real and built); KLT-06/07/08's registries
carry an explicit 6th status column with real `BLOCKED` rows. The
parser (`klt_canonical.parser.parse_skill_registry`) reads both shapes
correctly (verified against all 8 real files, see Testing §).
`get_canonical_klt_module` never fabricates a module for a `BLOCKED`
skill — `KLT06-M05`/`KLT06-M06`/`KLT07-M04`/`KLT08-M04` resolve to
`None`, exactly matching the real absence documented in each
formation's `modules/MODULES_STATUS.md`.

## What was built

### Backend — `backend/klt_canonical/` (7 modules, ~1470 lines incl. tests)

| File | Role |
|---|---|
| `models.py` | Pydantic read models — `CanonicalKltFormation`, `CanonicalKltModule`, `CanonicalKltSkill`, `KltFileProvenance`. `KLT_CONTEXTS` reproduces the real `KLT-0008` decision (`EXTERNAL`/`INTERNAL`) and legacy `catalog_cartography.py` contexts (`KLT-01/02/04/05`) — never invented. |
| `parser.py` | Pure functions: classify a file by its real path convention, extract a module's header-block fields, extract skill registry rows (both column shapes). No I/O. |
| `provenance.py` | Exhaustive file inventory — every real file under `docs/klt/kltXX/`, parsed or not, hashed (sha256) and recorded to `db.klt_resource_provenance`. Zero silent loss, same discipline as FMS's provenance ledger. |
| `import_pipeline.py` | `import_klt_docs()` — scans the tree, persists to `db.klt_resources` (idempotent upsert by `source_file`), records an import run to `db.klt_imports`. |
| `read_model.py` | `get_canonical_klt_formation`/`_module`, `list_canonical_klt_formations`/`_modules`/`_skills` — the derived-`fully_complete` machinery. Read-only. |
| `progress.py` | `db.klt_canonical_progress` — separate collection, same rationale as `fms_canonical/progress.py` (never shares `db.progress`'s namespace). |
| `__init__.py` | Public surface. |

**API** — `backend/api/klt_canonical.py` (new router, registered
additively in `backend/api/__init__.py`), prefix `/klt-canonical`,
mirrors `api/canonical.py` route-for-route: `GET /formations`, `GET
/formations/{code}`, `GET /formations/{code}/modules`, `GET
/formations/{code}/modules/{module_code}`, `GET /formations/{code}
/skills` (includes `BLOCKED` rows deliberately — the one endpoint that
lets a client render "5/7 built, 2 blocked" honestly), `POST
/formations/{code}/modules/{module_code}/viewed`, `GET
/progress/mine`, `POST /import` (admin-only), `GET /provenance`
(staff-only).

### Frontend — additive pages, new route tree `/kiltikonet-canonical`

`lib/canonicalKltApi.js` (thin client), `lib/canonicalKltDisplay.js`
(pure display logic, unit-tested — 12 tests), `pages/
CanonicalKltFormations.js` / `CanonicalKltFormationDetail.js` /
`CanonicalKltModuleView.js` — mirror the FMS canonical pages exactly,
with one addition the Founder's invariant requires: every formation
card and detail page states its real completeness
(`formatKltCompletenessLabel`) — a `PARTIAL` formation is never
rendered as if it were `COMPLETE`, and the detail page lists every
`BLOCKED` skill with its real reason. Registered in `App.js` alongside
the existing `/canonical` routes, zero change to any legacy route.

## Testing

`backend/tests/test_klt_canonical.py` — 16 tests, run against the
**real** `docs/klt/` tree (not a synthetic fixture, unlike FMS's suite
— there is no upload step to fixture around) via
`mongomock_motor.AsyncMongoMockClient`:

```
16 passed in ~3s
```

Covers: every real file accounted for (provenance count == disk count),
`KLT-01`→`05` all `fully_complete=True`, `KLT-06`/`07`/`08` all
`fully_complete=False` with the exact real blocked skill IDs
(`KLT06.SKILL.C05`/`C06`, `KLT07.SKILL.C04`, `KLT08.SKILL.C04`), skill
counts matching registry ground truth per formation, a blocked skill
never resolving to a fabricated module, module content matching the
real file, numeric (not lexicographic) module ordering, the full
8-formation list, `contexts` matching the real `KLT-0008` decision, the
legacy-badge flag, progress idempotency, and a structural guarantee
(grepped, not just asserted at runtime) that no file in this package
ever writes `db.formations.`/`db.progress.`/imports `seed_data`.

Full regression, this ticket's changes only:
- Backend: `black`/`isort`/`flake8` clean; `pytest` — 129/129 passed
  (`backend_test.py`'s live-HTTP-server tests excluded, same pre-
  existing environment limitation as every prior ticket this session).
- Frontend: `craco test` — 129/129 passed (16 suites, +12 new);
  `craco build` — compiles clean, 3 new lazy-loaded chunks for the 3
  new pages, zero new warnings.

## What this does NOT do

- **No `db.formations` write, ever** — grep-verified structurally
  (`test_no_module_here_imports_db_formations_collection`), not just
  asserted in prose.
- **No badge, no certification claim beyond what each formation's real
  `CERTIFICATION_MODEL.md` already states** — `has_legacy_badge`/
  `certification_scope` are read model annotations, not new
  credentials.
- **No live import has been triggered against a real MongoDB in this
  sandbox** — same `CODE_PATH_VERIFIED` vs `REAL_MONGO_IMPORT_VERIFIED`
  distinction ACA-0006 named for FMS: no live MongoDB exists here. The
  mechanism is proven correct against `mongomock` and the real files on
  disk; a production deployment still needs to call `POST /klt-
  canonical/import` once against its real database.
- **No unblocking of the 4 `BLOCKED` competencies** — `fully_complete`
  stays computed from the real registries; nothing in this package
  could flip it without those registries themselves being rewritten
  after a real Observatory/Network/Compliance connection exists.
- **No Observatory/Network/Compliance connection** — out of scope,
  unchanged from every prior ticket's finding (these systems have zero
  footprint in this repo).

## Verification

```bash
git status --short
#  M backend/api/__init__.py                       (router registration only)
#  M frontend/src/App.js                            (route registration only)
# ?? backend/api/klt_canonical.py
# ?? backend/klt_canonical/
# ?? backend/tests/test_klt_canonical.py
# ?? frontend/src/lib/canonicalKltApi.js
# ?? frontend/src/lib/canonicalKltDisplay.js
# ?? frontend/src/lib/canonicalKltDisplay.test.js
# ?? frontend/src/pages/CanonicalKlt*.js
```

Zero file under `docs/klt/`, `backend/seed_data.py`,
`backend/api/formations.py`, or any other legacy route touched.

`STOP = TRUE.` No live-database import triggered, no unblocking
attempted, no further chantier started.
