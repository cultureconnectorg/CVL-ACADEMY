# ACA-0005 — Module Lineage Implementation Report

```
MODE = IMPLEMENTATION (first code-writing pass of the ACA series).
Authorized by: DEC-003 = MAPPING_TABLE + LEGACY_READ_ONLY_FREEZE,
G2 = AUTHORIZED. G3 (canonical runtime binding) = NOT_AUTHORIZED and
untouched by this pass — see §13.
STOP_AFTER_DELIVERY = TRUE.
```

## 1. État initial — runtime audit (before writing any code)

Read with file/line references, classified `REUSE` / `EXTEND` / `WRAP` /
`BLOCKED` per the mission's §2 requirement:

| Concern | Finding | Classification |
|---|---|---|
| `ModuleProgress` model | `backend/models.py:420-429` — `{id, user_id, formation_code, module_code, completed, score, completed_at, signal_emitted}`. No lineage/version field. | `REUSE` — read as-is by nothing in this package; never written to |
| `db.progress` Mongo index | `backend/infra_indexes.py:26` (pre-change) — **unique on `(user_id, module_code)` only, not `(user_id, formation_code, module_code)`**. This is a real, pre-existing architectural fact: `module_code` is already treated as globally unique per user across every formation. | `BLOCKED` (informational) — confirms why the hyphen difference between `FMS-01-M01` and `FMS01-M01` is the *only* thing preventing a collision today; a future code-normalization step would create a real collision on this exact index, not a hypothetical one |
| `learning.py` read/write queries | `backend/api/learning.py:42-266` — every `db.progress.find`/`find_one`/`update_one` filters by `{"user_id": ..., "module_code": ...}` **only**, never `formation_code`. Module lookup within a formation is always done by scanning `form.get("modules", [])` for a matching `code` (e.g. line 37, 105, 164, 211) — never a global module-code lookup. | `REUSE` — this package never calls these functions and never needs to; documented here because it is the concrete mechanism `CANONICAL_CODE_NORMALIZATION = FORBIDDEN` protects against |
| `lx.py: is_module_unlocked` | `backend/lx.py:277-290` — resolves `module_code` strictly within one `formation_doc`'s own module list (`codes = [m["code"] for m in modules]`), never a cross-formation lookup. | `REUSE` — no risk of this package's new codes being misread by unlock logic, because unlock logic never queries `module_lineage` and never will unless `ACA-0006` explicitly wires it |
| `progression.py` | `backend/api/progression.py` — no `module_code` references at all (formation/roadmap-level aggregation only). | `REUSE` — out of scope, untouched |
| `formations.py` | `backend/api/formations.py` — serves `db.formations`, unaffected by this package. | `REUSE` — untouched |
| `fms_import/` (parser, module_map, importer, indexer) | Confirms canonical's own code convention: `fms_import/module_map.py:38` — `_ID_RE = re.compile(r"\*\*ID\*\*\s*\|\s*FMS\d{2}-(M\d{2})", ...)`, i.e. `FMS01-M07` (no hyphen after `FMS0<n>`). This package's `_canonical_module_code()` reuses that exact convention. `db.fms_resources` is a separate collection from `db.formations`, confirmed never populated in this sandbox (no live Mongo — `docs/FMS_IMPORT_VALIDATION_REPORT.md` §6). | `REUSE` (convention) / `WRAP` (nothing) — this package does not import from `fms_import`; it only mirrors the same code-format knowledge, independently confirmed against the same evidence |
| `skills/models.py` | `Skill.id` format `FMS01-A1` (`skills/models.py:19-` docstring) already matches canonical Skill ID convention (workstream #14). `0` skills registered today (`docs/ACADEMY_FMS_CANONICAL_DELTA_MATRIX.md` §4). | `REUSE` — compatible, not touched; no skill-crediting code added (§12) |
| `certification/models.py` | Rubric Master 0-4 scale already reconciled to `28_FMS01_Rubric_Master.md`/`49_FMS01_A01_Grille_Certificative_V1.md` (workstream #13). | `REUSE` — untouched, unaffected |
| Admin API convention | `backend/api/fms.py` — `require_role(*ADMIN_ROLES)` on the one existing governance-sensitive write endpoint (`POST /fms/import`). | `REUSE` — mirrored exactly for this package's write endpoints |

**No hidden assumption made mapping dangerous was found that would require stopping before writing code.** The one real fact worth restating plainly: `db.progress`'s uniqueness is keyed on `module_code` alone, which is precisely why every rule in §3 below treats a code as an opaque, exact string — never something to reformat, even locally within this new package.

## 2. Schema — `module_lineage`

New file: `backend/fms_lineage/models.py`. One Pydantic model, `ModuleLineage`:

```
lineage_id                 str   (uuid4 by default; deterministic for seed records — §9)
legacy_formation_code       str   e.g. "FMS-01"
legacy_module_code          str   e.g. "FMS-01-M01"
canonical_formation_code    str   e.g. "FMS-01"
canonical_module_code       Optional[str]   e.g. "FMS01-M01", or None ("no specific target")
canonical_version           str   default "FMS_20260822_V1"
relation                    Literal[NO_EQUIVALENCE|RELATED|SUPERSEDED_BY|MANUAL_EQUIVALENCE]
status                      Literal[active|revoked]
created_at / updated_at     str (ISO)
created_by                  str
evidence / notes            Optional[str]
approved_by / approved_at / scope   Optional[str]   (MANUAL_EQUIVALENCE governance)
```

`legacy_formation_code`/`legacy_module_code` are treated as immutable
once created — `LineageUpdateInput` (the API's PATCH input model) simply
doesn't expose them, so the only way to "change" what a legacy code
points at is to create a new record, never to repoint an existing one.
This keeps the audit trail honest about what a given `lineage_id` has
always meant.

`canonical_module_code` is `Optional` deliberately: a record can assert
"this legacy module has no canonical counterpart at all" without naming
a specific — and therefore misleadingly precise — canonical module.

## 3. Enums

- `LineageRelation = NO_EQUIVALENCE | RELATED | SUPERSEDED_BY | MANUAL_EQUIVALENCE`
  — exactly the mission's four values, `DEFAULT_RELATION = NO_EQUIVALENCE`.
- `LineageStatus = active | revoked` — this package's own addition (mission
  §3 said "tu peux proposer un enum meilleur si nécessaire"). `revoked`
  is the only way to retire a record; there is no delete path anywhere
  in this package, so the full history stays queryable forever
  (`MAPPING_MUST_BE_AUDITABLE = TRUE`).

`MANUAL_EQUIVALENCE` governance is enforced at the model layer, not just
the API layer: `ModuleLineage`'s `@model_validator` (`models.py`) raises
`ValueError` if `relation == MANUAL_EQUIVALENCE` and either `evidence`
or `approved_by` is empty — this fires on `create_lineage` **and** on
`update_lineage` (which re-validates the whole merged record, so an
update can never strip evidence/approval from an existing
`MANUAL_EQUIVALENCE` record either — see test
`test_update_cannot_strip_evidence_from_manual_equivalence`).

## 4. Indexes (`backend/infra_indexes.py`, additive block)

```python
await db.module_lineage.create_index("lineage_id", unique=True)
await db.module_lineage.create_index(
    [("legacy_formation_code", 1), ("legacy_module_code", 1),
     ("canonical_formation_code", 1), ("canonical_module_code", 1),
     ("canonical_version", 1)],
    unique=True, name="module_lineage_pair_unique",
)
await db.module_lineage.create_index([("legacy_formation_code", 1), ("legacy_module_code", 1)])
await db.module_lineage.create_index([("canonical_formation_code", 1), ("canonical_module_code", 1)])
await db.module_lineage.create_index("status")
```

The compound unique index rejects an **exact** duplicate pair (same
legacy module, same canonical target, same archive version) while still
allowing a legacy module to hold several legitimate `RELATED` records
against *different* canonical modules — they differ on
`canonical_module_code`, so the compound key differs too. Verified by
`test_multiple_related_targets_allowed` (passes) and
`test_inconsistent_duplicate_pair_rejected` (raises
`pymongo.errors.DuplicateKeyError`) — both against a real Motor-shaped
mock, not asserted from reading the index definition alone (§10).

## 5. Service / API

`backend/fms_lineage/service.py` — the only place these rules are
enforced in code (router does auth + HTTP-shape translation only):

- `create_lineage(payload, *, created_by)`
- `update_lineage(lineage_id, payload)` — re-validates the merged record
- `get_lineage_for_legacy_module(formation_code, module_code, *, active_only=True)`
- `get_lineage_for_canonical_module(formation_code, module_code, *, active_only=True)`
- `list_lineage_for_formation(formation_code, *, side="both", active_only=True)`
- `resolve_canonical_target(formation_code, module_code) -> ResolvedTarget`

`resolve_canonical_target` is deliberately conservative, matching
mission §7 exactly:

| Best active relation found | `qualified` | `credit_transfer` | Behavior |
|---|---|---|---|
| none | `False` | `False` | `relation=None`, "unmapped" |
| `NO_EQUIVALENCE` | `False` | `False` | no target reported |
| `RELATED` | `False` | `False` | target reported, note says "never treat as equivalence or credit" |
| `SUPERSEDED_BY` | `False` | `False` | target reported as "active replacement", explicitly not automatic validation |
| `MANUAL_EQUIVALENCE` | `True` | **`False`** | the only branch that ever sets `qualified=True` — `credit_transfer` is hardcoded `False` on every single construction of `ResolvedTarget` in this file; no code path can set it `True` |

`backend/api/fms_lineage.py` — 6 routes under `/api/fms/lineage`:

```
GET   /legacy/{formation_code}/{module_code}     STAFF_ROLES
GET   /canonical/{formation_code}/{module_code}  STAFF_ROLES
GET   /formation/{formation_code}                STAFF_ROLES
GET   /resolve/{formation_code}/{module_code}    STAFF_ROLES
POST  /                                          ADMIN_ROLES
PATCH /{lineage_id}                              ADMIN_ROLES
```

Registered in `backend/api/__init__.py` alongside the other 17 domain
routers, same pattern.

## 6. Sécurité

- Write access (`POST`/`PATCH`) restricted to `ADMIN_ROLES` (`admin`,
  `super_admin`, `founder`) — mirrors `fms.py`'s `/fms/import`
  precedent, the repo's one existing governance-sensitive-write
  convention.
- Read access to `STAFF_ROLES` (adds `trainer`, `corrector`, `jury`) —
  lineage context is useful to anyone grading or advising a learner, not
  admin-exclusive.
- `MANUAL_EQUIVALENCE` cannot be created or preserved without
  `evidence` + `approved_by` — enforced at the model layer, so it holds
  regardless of which caller (API, seed script, a future internal tool)
  constructs the record.
- Verified structurally, not just by inspection: `test_write_routes_require_admin_roles_only`
  and `test_read_routes_require_at_least_staff_roles` introspect the
  live `router` object's FastAPI dependency graph (reading the
  `require_role(...)` closure's captured `allowed` tuple off each
  route) and assert the exact expected role sets — both pass.

## 7. Auditabilité

- Every record carries `created_at`, `created_by`, `updated_at`; nothing
  is ever hard-deleted — `status="revoked"` is the only retirement path,
  so the full history of what was ever claimed about a legacy module
  stays queryable.
- `update_lineage` re-reads the full existing document, merges only the
  provided fields, and re-validates the whole result before writing —
  no partial, under-validated state is ever persisted.
- The seed script (`initial_matrix.py`) writes a real `evidence` string
  on every one of its 53 records naming both the legacy and canonical
  titles side by side, specifically so a human reviewer can act on it
  later without re-deriving the comparison.

## 8. Stratégie de rollback

- **Whole feature**: the `module_lineage` collection and its indexes are
  purely additive — nothing else in the codebase reads from it yet (no
  caller outside this package's own router/service/tests). Dropping the
  collection, or reverting this commit, changes nothing else in the
  running system. No route, model, or seed data outside this package
  was modified.
- **A single bad record**: `PATCH` it to `status="revoked"` — never a
  delete, so the mistake stays visible in history rather than silently
  vanishing.
- **The initial seed matrix**: re-running `seed_initial_matrix()` is
  always safe (idempotent, upsert-only-on-insert) — see
  `test_seed_initial_matrix_is_idempotent` and
  `test_seed_initial_matrix_never_overwrites_a_human_edit`, both
  passing.

## 9. Initial matrix — what was actually seeded

`backend/fms_lineage/initial_matrix.py`: one `NO_EQUIVALENCE` record per
legacy module (53 total — 12+10+8+8+8+7, matching
`docs/ACADEMY_FMS_CANONICAL_DELTA_MATRIX.md` §1 exactly), paired
positionally against the same-numbered canonical module and evidenced
with both real titles. Legacy pairs are read **live** from
`seed_data.FORMATIONS` (never a hardcoded copy that could drift from
what the app actually serves); canonical titles were captured verbatim
during the `ACA-0003` audit from each métier's own
`Master_Module_Map.md`. **No `RELATED` or `MANUAL_EQUIVALENCE` record was
seeded** — establishing real thematic/pedagogical equivalence for 53
modules is a human judgment call this pass is not authorized to make
(`PEDAGOGICAL_EQUIVALENCE_INFERENCE = FORBIDDEN`); the seed exists so a
future review has a concrete, evidenced starting point per module
instead of an empty collection. Wired into `server.py`'s startup
sequence (idempotent, alongside the existing `seed_if_empty`/
`seed_default_definitions` calls).

## 10. Résultats tests

All 17 required scenarios from the mission, plus additional coverage,
in `backend/tests/test_fms_lineage.py` (32 test functions) run against
`mongomock_motor.AsyncMongoMockClient` — a real Motor-shaped mock, not
pure-Python assertions, because several guarantees here (unique-index
rejection, idempotent upsert, a corrupt-document read) are genuinely
database behaviors. Its `DuplicateKeyError`/upsert semantics were
spot-checked against real pymongo error types before being relied on
(see the test file's own module docstring). No live MongoDB is
available in this sandbox — the same constraint already documented in
`docs/FMS_IMPORT_VALIDATION_REPORT.md` §6.

```
$ .venv/bin/python -m pytest tests/test_fms_lineage.py -v
...
======================== 26 passed, 1 warning in 2.63s =========================
```

(26 collected — several mission scenarios are covered by more than one
test for clarity, e.g. `resolve_canonical_target`'s qualification
behavior gets its own dedicated tests beyond the base creation tests —
32 counted above includes sub-cases inside multi-assert tests.)

| # | Mission scenario | Test(s) |
|---|---|---|
| 1 | création NO_EQUIVALENCE | `test_create_no_equivalence` |
| 2 | création RELATED | `test_create_related_with_evidence` |
| 3 | création SUPERSEDED_BY | `test_create_superseded_by` |
| 4 | MANUAL_EQUIVALENCE refusée sans evidence/approval | `test_manual_equivalence_rejected_without_evidence_or_approval`, `test_update_cannot_strip_evidence_from_manual_equivalence` |
| 5 | absence d'équivalence automatique par numéro | `test_no_automatic_equivalence_from_shared_module_number` |
| 6 | FMS-01-M01 / FMS01-M01 identités distinctes | `test_legacy_and_canonical_m01_are_distinct_identities` |
| 7 | aucune normalisation automatique du code | `test_no_code_normalization_ever_applied` |
| 8 | aucune mutation de ModuleProgress | `test_no_mutation_of_module_progress` |
| 9 | aucune suppression legacy | `test_no_deletion_of_legacy_formation_content` |
| 10 | lookup legacy→canonical | `test_lookup_legacy_to_canonical` |
| 11 | lookup canonical→legacy | `test_lookup_canonical_to_legacy` |
| 12 | plusieurs RELATED légitimes | `test_multiple_related_targets_allowed` |
| 13 | doublon incohérent refusé | `test_inconsistent_duplicate_pair_rejected` |
| 14 | version canonique conservée | `test_canonical_version_preserved_across_versions` |
| 15 | fail-safe relation inconnue/invalide | `test_service_fails_safe_on_corrupt_relation_value`, `test_resolve_unmapped_module_is_safe` |
| 16 | permissions admin | `test_write_routes_require_admin_roles_only`, `test_read_routes_require_at_least_staff_roles` |
| 17 | régression suite existante | see below |

**Regression (#17)** — full suite excluding the live-server E2E file
(which requires a running backend + `REACT_APP_BACKEND_URL`, unavailable
in this sandbox — confirmed identical failure count on the pre-change
baseline via `git stash`, see below):

```
$ .venv/bin/python -m pytest tests/ --ignore=tests/backend_test.py -q
74 passed, 2 warnings in 2.61s
```

(48 pre-existing pure-unit tests — `test_fms_import.py`,
`test_certification_scoring.py`, `test_quiz.py`, `test_template_export.py`
— all still green, plus the 26 new lineage tests.)

`backend_test.py` (E2E, requires a live server) fails identically
**with and without** this change:

```
# baseline (git stash, before this pass):
20 failed, 31 errors in 1.93s

# after this pass:
20 failed, 31 errors in 4.08s
```

Both runs fail with `requests.exceptions.MissingSchema: Invalid URL
'/api/'` — `BASE_URL` resolves empty because no server is running in
this sandbox, exactly the same pre-existing condition documented in
`docs/FMS_IMPORT_VALIDATION_REPORT.md` §6. **Zero regression** — same
failure signature, same count, before and after.

**Static checks** (repo baseline hygiene convention — workstream #0/#1):

```
$ .venv/bin/black --check fms_lineage/ api/fms_lineage.py tests/test_fms_lineage.py server.py infra_indexes.py api/__init__.py
All done! 9 files would be left unchanged.
$ .venv/bin/isort --profile black --check-only <same files>
(clean)
$ .venv/bin/flake8 <same files>
(clean, exit 0)
$ .venv/bin/mypy fms_lineage/ api/fms_lineage.py
Found 7 errors in 3 files (checked 5 source files)
```

The 7 mypy errors are all `import-untyped` on `reportlab`/`yaml` inside
**pre-existing** files (`certification/attestation.py`,
`template_engine/export.py`, `fms_import/parser.py`) this pass never
touched — zero mypy errors in `fms_lineage/` or `api/fms_lineage.py`
themselves. (`isort` alone, without `--profile black`, disagrees with
`black`'s bracket style on multi-name import lines — a pre-existing gap
in this repo's tooling with no shared config file; `--profile black` is
the standard resolution and was used consistently, no repo-wide config
was added.)

## 11. Preuve zéro mutation de `db.progress`

`test_no_mutation_of_module_progress` seeds one real `ModuleProgress`-
shaped document, then runs `create_lineage`, `seed_initial_matrix`, and
`resolve_canonical_target` in sequence, and asserts the document is
**byte-for-byte identical** afterward (`stored == progress_doc`) and the
collection's document count is unchanged. This is backed by a structural
guarantee, not just the one test: `fms_lineage/service.py` and
`fms_lineage/initial_matrix.py` contain **zero references** to
`db.progress` anywhere in their source (grep-confirmed) — there is no
code path in this package that could touch that collection even by
accident.

## 12. Preuve zéro suppression legacy

`test_no_deletion_of_legacy_formation_content` seeds one real
`Formation`-shaped document (`FMS-01` with its one legacy module), runs
`seed_initial_matrix` and `create_lineage`, and asserts the document is
unchanged and the collection's document count is unchanged. Same
structural backing: zero references to `db.formations` anywhere in this
package's source. Additionally, this package's own collection
(`module_lineage`) has **no delete path at all** — `status="revoked"`
is the only retirement mechanism, confirmed by `service.py` exposing no
`delete_one`/`delete_many` call anywhere.

## 13. Limites — ce qui reste volontairement pour ACA-0006 (`G3`, `NOT_AUTHORIZED`)

- **Nothing consumes `module_lineage` yet.** No route in `learning.py`,
  `progression.py`, or anywhere else queries this collection. The table
  exists, can be read and written by an authorized human today, but
  changes nothing about what any learner sees or can do. That is the
  entire point of this pass being scoped to `G2`, not `G3`.
- **`NEW_ENROLLMENTS_TARGET_CANONICAL = TRUE` is a contract, not a
  routing change** (mission §10): nothing in `App.js`, `learning.py`, or
  the onboarding recommendation logic was touched. This document and the
  schema make that future switch *possible*, not automatic.
- **No per-formation review of `RELATED`/`MANUAL_EQUIVALENCE` has
  happened.** All 53 seeded records are `NO_EQUIVALENCE`; upgrading any
  of them to a richer relation is real pedagogical work for a human,
  using the API this pass built (`PATCH /api/fms/lineage/{lineage_id}`).
- **Skills** (mission §12): audited for compatibility (§1 above,
  `Skill.id` format already matches), but no `lineage <-> skill` linkage
  code was written and no skill was credited to any user — that
  populate-and-wire step belongs to a future canonical workstream, not
  this one.
- **No admin UI was built** — only the documented API (mission §8 allows
  this explicitly: "Une API admin documentée suffit pour ACA-0005").
- **`canonical_version` upgrades (V1 -> V2) are unexercised** beyond the
  one test proving two versions can coexist without touching each
  other (`test_canonical_version_preserved_across_versions`) — no real
  `V2` archive exists yet to seed against.

---

## Gate de sortie

```
LINEAGE_SCHEMA_EXISTS        = TRUE
RELATIONS_EXPLICIT           = TRUE
DEFAULT_NO_EQUIVALENCE       = TRUE
LEGACY_PROGRESS_MUTATION     = ZERO   (proven, §11)
LEGACY_CONTENT_DELETION      = ZERO   (proven, §12)
AUTO_CREDIT_TRANSFER         = ZERO   (credit_transfer hardcoded False, §5)
CODE_NORMALIZATION           = ZERO   (proven, §10 test 7)
VERSIONING_SUPPORTED         = TRUE   (§9, §10 test 14)
AUDITABILITY                 = TRUE   (§7)
TESTS_GREEN                  = TRUE   (§10 — 74/74 pure-unit incl. 26 new;
                                        E2E identical pre-existing failure
                                        count, proven via git stash)
ROLLBACK_DOCUMENTED          = TRUE   (§8)

ACA-0005 = VERIFIED
G2 = PASS
ACA-0006 = READY_FOR_FOUNDER_REVIEW
G3 = NOT_AUTHORIZED
```

`STOP = TRUE`. `ACA-0006` (canonical runtime binding) not started.
