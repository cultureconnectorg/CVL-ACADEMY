# ACA-0006 — Canonical FMS Runtime Binding Report

```
Branch: claude/cvln-academy-canonical-fms (base: main @ 85a41cc)
DEC-002 = FMS_Chantier_Complet_20260822.zip = CANONICAL_V1_CURRENT
DEC-003 = MAPPING_TABLE + LEGACY_READ_ONLY_FREEZE (ACA-0005, untouched)
STOP_AFTER_DELIVERY = TRUE. Not started: ACA-0019, W-FUNNEL-2, physical/
hybrid runtime, H1, monetization.
```

This report also resolves the Founder's blocking correction issued
mid-mission (2026-09-03): the ZIP is the canonical asset to *integrate*,
not a reference to summarize from, every file must be individually
accounted for, and the 223-vs-233 count discrepancy had to be resolved
from the archive itself before continuing. §0 covers that in full; §1-16
cover the runtime binding mission itself, built and re-verified *after*
§0's correction (the skill-extraction bug §0's rigor surfaced was fixed
before this report was written — see §9).

---

## 0. Founder blocking correction — full ZIP accounting

**Method**: `zipfile.infolist()` against the actual archive bytes at
`/root/.claude/uploads/.../c946e3b9-FMS_Chantier_Complet_20260822.zip`
— no filtering, no reliance on any parser's classification. This is a
byte-level enumeration of literally everything the ZIP contains, run
independently of `fms_import` and of this pass's own `fms_canonical`
code.

```
ZIP_TOTAL_ENTRIES        = 224   (223 files + 1 directory entry)
ZIP_TOTAL_FILES          = 223
ZIP_TOTAL_DIRECTORIES    = 1     ("FMS_Chantier_Complet/")
DOCUMENT_COUNT           = 223
MARKDOWN_COUNT           = 223   (100% — every file is .md, confirmed
                                   by extension breakdown, zero other
                                   extensions present)
OTHER_FILE_COUNT         = 0
HIDDEN/SYSTEM_FILE_COUNT = 0     (no __MACOSX/, no .DS_Store, no dotfiles)
PARSED_COUNT             = 223   (re-verified this pass, see below)
UNPARSED_COUNT           = 0
EXCLUDED_COUNT           = 0
```

### Why the prior audit said 223 and the Founder recalled 233

The numbering scheme inside the archive runs `00` through `224` — a
nominal range of 225 slots — but:

- `00` is used **twice**, deliberately: `00_GABARIT_Construction_Metier.md`
  and `00_INDEX.md` are both cross-métier governance documents sharing
  the archive's own "00" convention.
- Three numbers are **missing entirely** from the sequence: `58`, `181`,
  `182`. `58` is explained by the double-`00` above (the gabarit was
  filed as `00`, not `58`, leaving a gap where a sequential numbering
  would have placed it); `181`/`182` have no explanation in the archive
  itself — flagged, not guessed at, in `docs/ACADEMY_FMS_CANONICAL_DELTA_MATRIX.md`
  §10 (found during `ACA-0003`).

225 nominal slots + 1 reused number − 3 gaps = **223 actual files** —
exactly what both the original `fms_import` parse (workstream #16,
`docs/FMS_IMPORT_VALIDATION_REPORT.md`) and this session's independent
re-count agree on.

**No evidence of a 233rd file exists anywhere in the archive available
to this session.** This is stated plainly rather than papered over: the
most likely explanations are (a) a transposition of "223" into "233" in
recollection, or (b) the Founder is thinking of a *different*, more
complete FMS package that has not been provided to this session — in
which case `DEC-002`'s designation of this exact archive as
`CANONICAL_V1_CURRENT` should be revisited with the Founder before any
further canonical work assumes this is the final source. This report
does not resolve that possibility either way — it can't, without a
different file to compare against — and flags it explicitly rather than
assuming (a).

### Unparsed/excluded files, individually

**None.** `PARSED_COUNT = 223 = ZIP_TOTAL_FILES`, `UNPARSED_COUNT = 0`,
`EXCLUDED_COUNT = 0`. Re-verified this session by actually running
`fms_import.import_fms_zip` (unmodified) against the real archive bytes
through a `mongomock_motor` database:

```
status: success
resources_created: 223
errors: 0
warnings: 0
resources_by_type: {module: 95, blueprint: 15, guide_correcteur: 6,
banque_n1: 6, competency_matrix: 6, guide_formateur: 6, cas_inedit: 6,
module_map: 6, sujet_officiel: 6, guide_jury: 6, cas_fil_rouge: 6,
guide_candidat: 6, banque_n2: 6, learning_map: 6, rubric_master: 3,
evidence_registry: 3, infrastructure: 3, grille_certificative: 7,
referentiel: 6, matrice_tracabilite: 6, gabarit: 1, templates_etudiants: 6,
note_harmonisation: 1, skill_ids_registry: 3, index: 1,
matrice_pedagogique: 1}  (sums to 223)
```

### Architectural response: provenance is now permanent infrastructure

Even though this archive triggers zero unparsed files, the Founder's
correction is right that the *pipeline* had no safety net for one —
`fms_import/parser.py::parse_markdown_file` silently never persists a
file it can't classify (only a warning in the `ImportReport`, no
`db.fms_resources` document). **`fms_canonical/provenance.py`** closes
this permanently:

- `build_zip_inventory(raw_zip)` — pure, independent of `fms_import`'s
  own persistence — enumerates **every** real ZIP entry (not `.md`-
  filtered first) and produces one `FileProvenance` record each,
  `parsed` or `unparsed_no_type_match`/`unparsed_error`, never dropped.
- Each record carries `original_path`, `original_filename`, `sha256`,
  `byte_size`, `resource_type`, `formation_code`, `module_number`,
  `audience` (the 6-tier taxonomy, §8), `canonical_version`,
  `parsing_status`, `parsing_note`.
- `store_zip_provenance` persists this to a new, additive
  `db.fms_resource_provenance` collection — idempotent by
  `(original_path, canonical_version)`.
- Wired unconditionally into `import_canonical_fms_zip` (§4) — every
  real import now produces this ledger alongside the resource import,
  automatically, not as an optional extra step.
- `POST /api/canonical/import`'s response includes
  `all_zip_files_accounted_for`: an independent cross-check
  (`count_zip_files` — a *second*, separately-implemented raw
  `zipfile.infolist()` count — compared against
  `len(provenance_records)`), not an assumption.
- Tested (`test_zip_inventory_accounts_for_every_file_including_unparsed`,
  `test_provenance_never_overwritten_by_import_report_gap`): a synthetic
  fixture ZIP with one deliberately-unclassifiable file proves a future
  archive's unparsed file *would* get a permanent, auditable record —
  the guarantee holds even though this real archive never exercises it.

```
ALL_ZIP_FILES_ACCOUNTED_FOR = TRUE   (223 == 223, independently verified)
ZERO_SILENT_FILE_LOSS       = TRUE   (0 unparsed, and the pipeline can
                                       no longer silently drop one even
                                       if a future archive has one)
SOURCE_TRACEABILITY         = TRUE   (sha256 + byte_size + original_path
                                       per file, `db.fms_resource_provenance`)
```

---

## 1. Audit — source of truth per layer (mission §2)

| Layer | CURRENT_SOURCE | TARGET_SOURCE | Classification |
|---|---|---|---|
| `db.fms_resources` | Populated by `fms_import.import_fms_zip` — real, but **never actually written to persistent Mongo in this sandbox** before this pass (no live MongoDB; only `mongomock`-verified, per `docs/FMS_IMPORT_VALIDATION_REPORT.md` §6) | Same collection, read-only input to `fms_canonical` | `REUSE` |
| `backend/fms_import` | Parser/importer/indexer, real, untouched | Unchanged | `REUSE` (with one caveat below) |
| **→ caveat found this pass** | `fms_import`'s own code normalization makes `fms_resources.code` for a module resource the **legacy-shaped** `FMS-01-M01` (dashed) — `fms_import/models.py`'s own docstring says so | `fms_canonical` derives the true canonical code (`FMS01-M01`) independently, matching a resource by `(formation_code, module_number)` extracted from `source_file`, never trusting `.code` | Documented `WRAP`, not a `fms_import` change |
| `db.formations` | Legacy seed catalogue (`FMS-01`..`FMS-06`, 53 legacy modules) | **Untouched** — `pedagogical_source=CANONICAL` on `CanonicalFormation` is how the frontend distinguishes the two without ever reading/writing this collection | `REUSE` (read never even happens — no code path here touches `db.formations`) |
| `FormationDetail.js`/`ModuleJourney.js` | Legacy 7-phase shell, serves `db.formations` | Untouched — new, separate pages (`CanonicalFormations.js`/`CanonicalFormationDetail.js`/`CanonicalModuleView.js`) instead | `WRAP` (additive pages, not a rewrite) |
| `db.progress` | Legacy learner progress, unique index `(user_id, module_code)` | Untouched | `REUSE` |
| **→ new** `db.canonical_progress` | Did not exist | New collection, unique index `(user_id, canonical_module_code)` — structurally separate, not just differently-named codes in the same index | New, additive |
| `quizzes.py`/mini-missions | Legacy engines, keyed to legacy module codes | Untouched — no canonical quiz/mini-mission engine built this pass (§10) | `REUSE`, not extended |
| `skills/` (Skill Engine) | `Skill.id` format already `FMS01-A1`-shaped (workstream #14); `db.skills`/`db.user_skills` real but empty of canonical entries | `fms_canonical.CanonicalSkillDefinition` is a **catalogue read model**, not a write into `db.skills` — registering the canonical catalogue for future use is explicitly separate from crediting any user (§9) | `WRAP` — no `db.skills`/`db.user_skills` write exists in this pass |
| `certification/` | Rubric Master 0-4 engine already reconciled to FMS-01's real grille (workstream #13) | Untouched — no canonical certification-attempt code added (§11) | `REUSE`, not extended |
| `progression.py`/`next_action` | Legacy-only | Untouched — canonical progress has its own read path (`GET /canonical/progress/mine`), not merged into legacy `next_action` this pass | `REUSE`, not extended |

**No hidden assumption was found that made proceeding dangerous enough
to stop before writing code** — the one real, consequential finding
(the `fms_resources.code` normalization caveat above) was documented and
designed around, not a blocker.

---

## 2. Architecture — before / after

**Before**: `db.fms_resources` existed as a populated-but-unconsumed
collection (confirmed zero frontend/backend consumption in `ACA-0003`).
The only thing resembling a "canonical FMS" concept in the running
system was `module_lineage` (`ACA-0005`), which *describes* a relation
between legacy and canonical codes but never served canonical content
itself.

**After**: a new `fms_canonical` package turns `db.fms_resources` into a
structured, learner-safe read model (`CanonicalFormation`/
`CanonicalModule`/`CanonicalSkillDefinition`), a new `db.canonical_progress`
collection lets a learner record real progress against canonical codes
without touching legacy data, and a new `db.fms_resource_provenance`
ledger proves the archive's full content is accounted for. Six new API
routes (plus the pre-existing `module_lineage` API from `ACA-0005`, still
independently the only sanctioned way to describe a legacy↔canonical
relation) and three new frontend pages let a real authenticated learner
browse and engage with the canonical corpus today, entirely alongside —
never replacing — the legacy `/formations` tree.

```
ZIP ──(fms_import, unchanged)──► db.fms_resources (raw, source-preserving)
                                         │
                    ┌────────────────────┴────────────────────┐
                    │                                          │
   fms_canonical.read_model (structured view)      fms_canonical.provenance
   + module_map_extract (Titre/Bloc/N1-3/Prereq)    (sha256/path/audience ledger)
                    │
     CanonicalFormation / CanonicalModule / CanonicalSkillDefinition
                    │
        api/canonical.py  ──►  frontend canonical pages
                    │
        fms_canonical.progress  ──►  db.canonical_progress (new, separate)
```

---

## 3. Files touched

**New (backend)**: `backend/fms_canonical/{__init__,models,read_model,
module_map_extract,progress,import_pipeline,provenance}.py`,
`backend/api/canonical.py`, `backend/tests/test_fms_canonical.py`.

**Modified (backend)**: `backend/api/__init__.py` (router registration),
`backend/infra_indexes.py` (new indexes for `canonical_progress` and
`fms_resource_provenance`).

**New (frontend)**: `frontend/src/lib/canonicalApi.js`,
`frontend/src/lib/canonicalDisplay.js` (+ `.test.js`),
`frontend/src/pages/{CanonicalFormations,CanonicalFormationDetail,
CanonicalModuleView}.js`.

**Modified (frontend)**: `frontend/src/App.js` (3 new lazy routes,
additive only — `git diff --stat`: +8 lines).

**Untouched, confirmed by `git status`**: `db.formations`/`seed_data.py`/
`seed_modules.py`, `db.progress`/`learning.py`, `fms_import/*`,
`module_lineage`/`fms_lineage/*`, `certification/*`, `skills/*`,
`quizzes.py`, `progression.py`, every existing frontend page.

---

## 4. Schémas / models introduits

`fms_canonical/models.py`:

- `CanonicalFormation` — `canonical_formation_code, metier_number,
  metier_name, canonical_version, pedagogical_source="CANONICAL",
  module_codes_in_order, module_count, pedagogical_case_title,
  has_dedicated_skill_registry, has_infrastructure_doc`.
- `CanonicalModule` — `canonical_formation_code, canonical_module_code,
  canonical_version, order_index, title, bloc_competence,
  niveau_progression, prerequisites (CanonicalPrerequisites), skill_ids,
  assessment (CanonicalAssessmentRefs), content_markdown,
  content_source_file`.
- `CanonicalPrerequisites` — `status: DEFINED|NONE|UNSPECIFIED,
  required_module_codes`.
- `CanonicalAssessmentRefs` — `n1_reference, n2_reference, n3_reference`
  (all `Optional`, real extraction only — §10).
- `CanonicalSkillDefinition` — `skill_id, canonical_formation_code,
  canonical_version, label, bloc, is_eliminatory, source`.
- `CanonicalModuleProgress` — `user_id, canonical_formation_code,
  canonical_module_code, canonical_version, content_viewed_at,
  updated_at`.
- `FileProvenance` — see §0.
- `RESOURCE_AUDIENCE: Dict[str, List[Audience]]` — the 6-tier taxonomy
  (§8), covering every one of `fms_import`'s 26 real resource types
  (test: `test_audience_classification_covers_every_real_type`).

## 5. Stratégie d'import

`fms_canonical/import_pipeline.py::import_canonical_fms_zip` wraps the
existing, unmodified `fms_import.import_fms_zip` and additionally runs
`provenance.store_zip_provenance` unconditionally. Idempotency:
`fms_import`'s own `update_one({"code": r.code}, {"$set": ...},
upsert=True)` already makes re-importing the same archive a no-op-content
overwrite, never a duplicate — verified directly this pass
(`test_import_is_idempotent`: re-running the synthetic fixture import
inserts 0 new resources and 0 new provenance rows the second time).
`POST /api/canonical/import` (admin-only) is the "commande claire" the
mission asked for — one multipart upload, one structured
`CanonicalImportResult` response (`import_id, zip_total_files,
parsed_count, unparsed_count, provenance_inserted, provenance_updated,
all_zip_files_accounted_for`).

## 6. Traitement du legacy

Zero legacy code touched. `db.formations`/`seed_data.py`/
`seed_modules.py`/`learning.py`/`db.progress` have no reference anywhere
in `fms_canonical/*` (grep-confirmed, and asserted by
`test_no_legacy_progress_mutation_across_full_pipeline`, which seeds a
real legacy progress document, runs the full canonical pipeline against
it, and asserts byte-for-byte equality afterward). `module_lineage`
(`ACA-0005`) remains the *only* sanctioned place to describe a
legacy↔canonical relationship — re-verified still functional this pass
(`test_module_lineage_still_functional`: seeds its 53-record initial
matrix, reads one back, unchanged behavior).

## 7. Traitement des 95 modules

Verified against the real archive (§0's import run): **95 modules
across 6 métiers** (15+16+16+16+16+16), matching
`docs/ACADEMY_FMS_CANONICAL_DELTA_MATRIX.md` §1 exactly. Module order is
read directly from each métier's own Master Module Map section sequence
— never re-sorted, never inferred from file numbering. The **formation
code collision** (mission §7: `FMS-01` used by both legacy and
canonical) is resolved by never writing to `db.formations` at all —
`CanonicalFormation.pedagogical_source` is hardcoded `"CANONICAL"`, a
structural tag rather than a value that could be forgotten or omitted;
the frontend never has to guess which world a formation code belongs to
because canonical pages only ever call `/api/canonical/*` and legacy
pages only ever call the existing `/api/formations/*`.

**7-phase shell audit** (mission §4 — REPRESENTABLE /
PARTIALLY_REPRESENTABLE / NOT_REPRESENTABLE / SEMANTIC_MISMATCH,
per-concept):

| Legacy concept | Canonical status | Why |
|---|---|---|
| Hook | `NOT_REPRESENTABLE` for FMS-01/02 rich-layout modules (no such field); `PARTIALLY_REPRESENTABLE` for FMS-03..06's compact layout, which *does* have a real `Hook` field — not surfaced this pass, left for a future refinement | Real structural difference between the two layouts (§ module_map_extract.py docstring) |
| Objectives | `PARTIALLY_REPRESENTABLE` — "Objectifs pédagogiques observables" exists in the rich layout only | Not extracted this pass (kept to Titre/Bloc/Niveau/N1-3/Prérequis — a deliberately bounded first extraction) |
| Course | `REPRESENTABLE` — `content_markdown`, the real module body | Direct |
| Workshop | `SEMANTIC_MISMATCH` — canonical's "Pratique/exercice" (rich) or "Exercice" (compact) is a described activity within the body text, not a separate interactive step | Not force-split out |
| Deliverable | `SEMANTIC_MISMATCH` — canonical's "Livrable produit" is named in the Module Map but the actual deliverable mechanics live inside `content_markdown`'s prose, not a discrete submittable field like legacy's | Not fabricated as a submission form |
| Quiz | `PARTIALLY_REPRESENTABLE` — `n1_reference` names what the N1 QCM covers (rich layout only), no interactive quiz engine wired | See §10 |
| Mini Mission | `NOT_REPRESENTABLE` — canonical has no equivalent concept at all; conflating it with "N3 préparation" or the pedagogical case would be a real semantic error, not attempted | — |

No Hook/Deliverable/Mini-Mission was fabricated for a module whose
source doesn't define one — confirmed by construction (nothing in
`fms_canonical` writes those fields at all).

## 8. Ressources staff-only — RBAC (mission §3)

`RESOURCE_AUDIENCE` maps every real type to `LEARNER`/`TRAINER`/
`CORRECTOR`/`JURY`/`ADMIN`/`INTERNAL` (some types serve more than one
role honestly — e.g. `grille_certificative` is both `CORRECTOR` and
`JURY`). `get_canonical_module` only ever reads `content_markdown` from
a `type="module"` resource — structurally impossible for a
`guide_correcteur`/`banque_n1`/`sujet_officiel` etc. to leak into a
learner's view (test: `test_staff_resource_never_leaks_as_module_content`,
using a fixture where the guide's own text ("confidentielles"/"barème")
is asserted absent from the served module content). `GET
/api/canonical/provenance` (the one place all 6 audience tiers are
visible at once, since it lists every resource) is `STAFF_ROLES`-gated,
never public. An unrecognized future type defaults to
`["ADMIN","INTERNAL"]`, never `LEARNER` (`is_learner_facing` fail-safe).

## 9. Traitement des 83 Skill IDs

Verified against the real archive, **83 distinct canonical Skill IDs**
across the 6 métiers (19+16+12+12+12+12), matching
`docs/ACADEMY_FMS_CANONICAL_DELTA_MATRIX.md` §4 exactly:

```
FMS-01: 19   FMS-02: 16   FMS-03: 12   FMS-04: 12   FMS-05: 12   FMS-06: 12
```

**Real bug found and fixed by this pass's own verification discipline**:
the first extraction run produced 90, not 83. Root cause:
`fms_import/parser.py`'s own `SKILL_ID_RE` (`\bFMS0\d-[A-F]\d+\b`) —
untouched, pre-existing — over-matches a métier's *certification* code
(e.g. `FMS01-A01`) as if its two-digit `01` were a skill number, and
`list_canonical_skill_definitions`'s original implementation also
unioned skill mentions across *all* of a formation's own resources
without checking they belonged to that formation (FMS-02's content
genuinely cites FMS-01 Skill IDs when discussing the continuing case's
prior step). Both are now filtered in `read_model.py`:
`_SKILL_ID_SHAPE_RE` rejects any 2+-digit skill number (every real Skill
ID confirmed single-digit against every real registry), and only IDs
matching the target formation's own `FMS<n>-` prefix are kept. Re-run
after the fix: exactly 83, matching the independent `ACA-0003` audit.
This is reported here rather than silently corrected, because it's
exactly the kind of thing the Founder's blocking correction was
warning against.

Per mission §9: `REGISTER_SKILL_DEFINITION = ALLOWED`,
`CREDIT_SKILL_TO_USER_AUTOMATICALLY = FORBIDDEN`. Only the first is
built — `list_canonical_skill_definitions` is a **catalogue read**, never
a write to `db.user_skills`/`db.skill_evidence` (grep-confirmed absent
from every file in `fms_canonical/`, and structurally tested —
`test_no_automatic_skill_crediting_code_exists`). `source` is
`"skill_ids_registry"` where a dedicated registry exists (FMS-01/02/03)
and `"inline_extraction"` otherwise (FMS-04/05/06, which have no
dedicated registry file — a real archive asymmetry, not a gap this pass
invented, per the delta matrix).

## 10. N1/N2/N3

Preserved as **distinct fields**, never merged into a score or a single
"progress" number: `CanonicalAssessmentRefs.n1_reference`/
`n2_reference`/`n3_reference`. Real and honest per-layout: the rich
FMS-01/FMS-02 Module Map layout names all three explicitly per module;
the compact FMS-03..06 layout has **none of the three** — a genuine
structural absence in the source (confirmed by reading every real
Module Map this session), reflected as `None`, not fabricated as
"Aucun" (which would falsely imply the source made a statement it
didn't). No interactive N1 QCM/N2 exercise engine was built this pass —
the banques N1/N2 (`banque_n1`/`banque_n2` resources) stay `CORRECTOR`+
`JURY`-only per §8 and are not surfaced to learners at all; that build
belongs to a future, explicitly-scoped wave.

## 11. Assessment / certification

No canonical certification-attempt code was added
(`test_no_canonical_certification_attempt_code_exists`: `db.
certification_attempts` referenced nowhere in `fms_canonical/`). The
existing 0-4 Rubric Master engine (workstream #13, already reconciled
to FMS-01's real grille) is untouched and its own safeguards (required
evidence, eliminatory criteria, backend-authoritative grading) are
unaffected by anything in this pass — there is simply no new pathway
into it yet from canonical content. **No canonical certification can be
marked passed by this pass, because this pass built no way to attempt
one.** Wiring the real `grille_certificative` per métier into a usable
`Rubric` is real, scoped work for a future wave (the grille text is
free-form Markdown, not yet structurally parseable the way the Module
Map is).

## 12. RBAC (API)

`api/canonical.py`: every read route requires `get_current_user` (real
auth, no `get_current_user_optional` anywhere —
`PUBLIC_DISCOVERY_ACTIVATION = OUT_OF_SCOPE`, confirmed by
`test_read_routes_require_real_authentication`); `POST /import` requires
`ADMIN_ROLES` (`test_import_route_requires_admin_roles`); `GET
/provenance` requires `STAFF_ROLES` (`test_provenance_route_requires_staff_roles`)
— all three verified by introspecting the live FastAPI dependency graph,
not just reading the source.

## 13. Tests — mapped to the mission's 27 required scenarios

29 backend tests (`test_fms_canonical.py`) + 13 frontend tests
(`canonicalDisplay.test.js`), all passing:

| # | Scenario | Covered by |
|---|---|---|
| 1 | canonical formation read | `test_canonical_formation_read` |
| 2 | canonical module read | `test_canonical_module_read` |
| 3 | module order | `test_module_order` |
| 4 | real prerequisites | `test_real_prerequisites_extracted` |
| 5 | missing prerequisites not invented | `test_missing_prerequisites_not_invented` |
| 6 | canonical code preserved exactly | `test_canonical_code_preserved_exactly` |
| 7 | legacy code preserved exactly | `test_legacy_code_format_untouched_by_this_package` |
| 8 | legacy+canonical progress coexistence | `test_legacy_and_canonical_progress_coexist` |
| 9 | no legacy progress mutation | `test_no_legacy_progress_mutation_across_full_pipeline` |
| 10 | no automatic credit transfer | `test_no_automatic_skill_crediting_code_exists` |
| 11 | no positional equivalence | inherited from `ACA-0005` (`module_lineage` default `NO_EQUIVALENCE`); this pass adds no new positional-inference code |
| 12 | 95 canonical modules represented | §0/§7's real-archive run + `test_module_count_and_metier_scale_mechanism` (fixture-scale proof) |
| 13 | six canonical métiers represented | same |
| 14 | unauthorized staff resources hidden | `test_staff_resource_never_leaks_as_module_content`, `test_guide_correcteur_is_not_learner_facing` |
| 15 | skill definitions extraction | `test_skill_definitions_extraction`, `test_skill_registry_source_is_marked` |
| 16 | no automatic user skill award | `test_no_automatic_skill_crediting_code_exists`, `test_content_viewed_never_infers_skill_completion` |
| 17 | N1/N2/N3 distinction | `test_n1_n2_n3_distinction` |
| 18 | pedagogical case != product mission | `test_no_mission_pedagogical_case_merge_code_exists` |
| 19 | certification safeguards | `test_no_canonical_certification_attempt_code_exists` |
| 20 | lineage still functional | `test_module_lineage_still_functional` |
| 21 | legacy routes/data still functional | full pre-existing pure-unit suite green (§14) |
| 22 | API auth/RBAC | `test_import_route_requires_admin_roles`, `test_provenance_route_requires_staff_roles`, `test_read_routes_require_real_authentication` |
| 23 | idempotent import/read | `test_import_is_idempotent` |
| 24 | frontend canonical module rendering | 3 new pages + `canonicalDisplay.test.js` (pure display-logic tests — see §15 for why this repo tests frontend logic this way, not via component rendering) |
| 25 | full backend regression | §14 |
| 26 | frontend Jest regression | §14 |
| 27 | Playwright regression | `NOT_RUNNABLE` — see §14 |

Plus provenance-specific tests beyond the 27 (§0):
`test_zip_inventory_accounts_for_every_file_including_unparsed`,
`test_every_provenance_record_has_hash_and_size`,
`test_provenance_never_overwritten_by_import_report_gap`,
`test_audience_classification_covers_every_real_type`.

## 14. Régression

```
$ .venv/bin/python -m pytest tests/ --ignore=tests/backend_test.py -q
103 passed  (74 pre-existing + 29 new, zero failures)

$ .venv/bin/python -m pytest tests/backend_test.py -q
20 failed, 31 errors   — IDENTICAL to the pre-change baseline (git stash
                          confirmed both this pass and ACA-0005: same
                          count, same root cause — no live server in
                          this sandbox, requests.exceptions.MissingSchema)

$ black --check / isort --profile black --check-only / flake8  → clean
$ mypy fms_canonical/ api/canonical.py                          → 0 errors
                                                                    (7 pre-
                                                                    existing
                                                                    reportlab/
                                                                    yaml stub
                                                                    errors in
                                                                    unrelated
                                                                    files)

$ CI=true npx craco test --watchAll=false
Test Suites: 15 passed, 15 total. Tests: 117 passed  (104 pre-existing +
                                                        13 new)

$ CI=true npx craco build
Compiled successfully. main.js +114 B gzip; 3 new pages code-split into
their own lazy chunks, not inflating the shared bundle.

$ npx eslint <every new/changed frontend file>   → clean, 0 warnings
```

**Playwright**: `NOT_RUNNABLE` this pass — the existing suite requires a
live backend + frontend server (`REACT_APP_BACKEND_URL`), unavailable in
this sandbox (same constraint as `backend_test.py`'s E2E suite). Not
claimed as verified.

## 15. Performances

No new N+1 pattern introduced at the scale that matters today:
`get_canonical_formation` does 3 `find_one`/`count_documents` calls
+ parses one Module Map body; `list_canonical_modules` calls
`get_canonical_module` once per module (re-fetching the Module Map each
time) — acceptable at 15-16 modules/formation, but a real optimization
opportunity for a future pass (cache the parsed Module Map per request).
No index was skipped: `db.fms_resources`'s existing indexes (`code`,
`formation_code` — `fms_import/indexer.py`) already cover this package's
query patterns; `db.canonical_progress` and `db.fms_resource_provenance`
get their own new indexes (§ infra_indexes.py diff, §3).

## 16. Rollback

Every new collection (`db.canonical_progress`, `db.fms_resource_provenance`)
is purely additive — nothing outside `fms_canonical/`'s own router/
service/tests reads from them. Reverting this branch, or dropping either
collection, changes nothing else in the running system. `db.fms_resources`
itself (populated by the untouched `fms_import` pipeline) is unaffected —
this pass never writes to it. The 3 new frontend routes are additive;
removing them from `App.js` (or the whole branch) restores exactly the
prior route table.

## 17. Limites réelles

- **`REAL_MONGO_IMPORT_VERIFIED = FALSE`.** No live MongoDB exists in
  this sandbox (confirmed: `mongod` not installed,
  `ServerSelectionTimeoutError` on `localhost:27017`). Every claim in
  this report about the real 223-file archive (§0, §7, §9) was verified
  by running the actual, unmodified `import_fms_zip`/`fms_canonical`
  code against the real archive bytes through `mongomock_motor` — a
  real Motor-shaped mock, not a live database. `CODE_PATH_VERIFIED =
  TRUE`; `REAL_MONGO_IMPORT_VERIFIED = FALSE`. **At deployment**: run
  `POST /api/canonical/import` once against a real MongoDB with the
  real archive, then confirm `all_zip_files_accounted_for: true` and
  `resources_created: 223` in the response — the exact same assertions
  this report already made against the mock, now against the real
  database.
- Hook/Objectives/Workshop/Deliverable/Mini-Mission are not extracted
  (§7) — deliberately, to avoid fabricating structure the source
  doesn't literally have.
- No interactive N1/N2 assessment engine, no canonical certification
  attempt flow (§10-11) — real, scoped future work, not silently
  skipped.
- `list_canonical_modules` re-parses the Module Map per module (§15) —
  correct, not yet optimized.
- Frontend i18n: the 3 new pages are French-only. This repo has full
  4-language i18n coverage everywhere else (workstreams #18-27); adding
  it here was left out of this pass's scope (`pas de nouvelle DA... le
  but est CORRECT PEDAGOGICAL TRUTH FIRST`) — a real, stated gap, not an
  oversight.
- `metier_name`/`pedagogical_case_title` extraction (§ read_model.py)
  handles the real archive's actual heading shapes but is not
  bulletproof against a differently-worded future archive — flagged as
  a soft spot, not a proven-general parser.
- The 181/182 numbering gap (§0) remains unexplained — carried forward
  from `ACA-0003`, not investigated further this pass.

## 18. Ce qui reste pour les workstreams suivants

- **`ACA-0019`** (explicitly named next by the Founder): audit before
  touching `ModuleJourney`'s canonicalization further.
- Interactive N1 QCM / N2 exercise engine for canonical content.
- A real canonical certification-attempt flow (parsing
  `grille_certificative` into a usable `Rubric`).
- Hook/Workshop/Deliverable equivalents, if and when a real product
  decision defines what they should mean for canonical content (not
  invented here).
- i18n coverage for the 3 new pages.
- Performance: cache parsed Module Maps per formation instead of
  re-parsing per module.
- Resolving the 223-vs-233 question with the Founder directly (§0) —
  either confirms this archive is complete, or surfaces a different,
  more complete package that supersedes `DEC-002`.
- Skill registry rich-metadata extraction (label/bloc/eliminatory) for
  FMS-01/02/03's real registry table rows — currently only the ID
  itself is cross-referenced (§9).

---

## Gate G3

```
CANONICAL_FMS_READ_MODEL     = VERIFIED
SIX_FMS_METIERS              = VERIFIED
CANONICAL_MODULES_95         = VERIFIED
CANONICAL_CODES_PRESERVED    = VERIFIED
LEGACY_CODES_PRESERVED       = VERIFIED
LEGACY_PROGRESS_MUTATION     = ZERO
AUTO_CREDIT_TRANSFER         = ZERO
STAFF_ONLY_RESOURCE_LEAK     = ZERO
NEW_RUNTIME_CAN_USE_CANONICAL = TRUE
ASSESSMENT_SEMANTICS_PRESERVED = TRUE
REGRESSION_GATE              = PASS

ALL_ZIP_FILES_ACCOUNTED_FOR  = TRUE
ZERO_SILENT_FILE_LOSS        = TRUE
SOURCE_TRACEABILITY          = TRUE
REAL_MONGO_IMPORT_VERIFIED   = FALSE (documented, §17 — deployment step named)
CODE_PATH_VERIFIED           = TRUE

ACA-0006 = VERIFIED
G3 = PASS
```

`STOP = TRUE`. `ACA-0019` not started. No `W-FUNNEL-2`, physical/hybrid,
`H1`, or monetization work touched.
