# RAIL 2 — Master → Runtime Academy Integration Report

```
Branch: claude/cvln-academy-canonical-fms
Founder instruction (2026-09-06), verbatim intent: "Objectif : faire en
sorte que le Master pédagogique ne reste pas dans docs/. Décide de
l'architecture d'intégration la plus simple qui respecte le runtime
existant. Ne refais pas le backend ni le modèle de données si une
extension additive suffit. [...] La chaîne cible est : Learning ->
Skill -> Evidence -> Assessment -> Certification -> Qualification ->
Opportunity -> Mission. [...] Gate de sortie : au moins une formation
canonique complète est suivable de bout en bout dans le runtime réel."
NO_LEGACY_REWRITE = TRUE — respected: zero existing collection, model,
route, or page was modified in a way that changes its prior behavior.
Every touch to a pre-existing file is additive (a new field with a
backward-compatible default, a new import line, one new function call
inside an existing `if passed:` block).
```

## 1. Problem statement

Rail 1 closed the full 812-object Master 2D cartography: every
CVLN-Academy domain (FMS, Kiltikonet, KORA, FREK, Agent Factory,
CyberSecure, Blockchain, LabelOS, Gala, Hospitality, Founder/Group/
Fondation, Cross-CVLN, Good Mood/DJ Sayd, Wallet) now carries either
real built pedagogical content or an honest, explicit blocker — but that
content lives in `docs/`. Two prior tickets (ACA-0006 for FMS, "branchage
complet de Kiltikonet" for KLT) already proved the pattern for
connecting one such corpus to the real runtime; Rail 2 asks for the same
connection to close the actual functional chain a learner walks:
**Learning → Skill → Evidence → Assessment → Certification →
Qualification → Opportunity → Mission** — end to end, in running code,
for at least one real formation.

## 2. Existing-runtime inventory (before this ticket)

| Chain link | Real, working code | Gap |
|---|---|---|
| **Learning** | `lx.py` (7-phase engine), `db.progress`, `fms_canonical`/`klt_canonical` (two of three domain corpora already runtime-bound) | KORA (`docs/kor/`) not yet bound |
| **Skill** | `skills/models.py::Skill`, `skills/progression.py::register_skill` | — |
| **Evidence** | `skills/models.py::EvidenceEntry` (append-only, sha256), `record_evidence` | — |
| **Assessment** | `certification/models.py::Rubric`/`RubricCriterion` — real FMS Rubric Master doctrine (0–4 scale, eliminatory criteria, mention caps) already reconciled | — |
| **Certification** | `certification/service.py::start_attempt`/`submit_attempt`/`grade_attempt`, jury signature, PDF attestation, FREK-CERT signal, wallet credit | — |
| **Qualification** | *(none)* | **Missing link** |
| **Opportunity** | *(none)* | **Missing link** |
| **Mission** | `models.py::Mission`/`UserMission`, `api/missions.py` | Zero eligibility gating — any authenticated user can accept any mission |

Five of the eight links already existed as real, previously-reconciled
code. This pass's actual scope is therefore narrow and additive: bind
one more docs corpus (KORA) into the runtime exactly like FMS/KLT
already are, then build the two genuinely missing links
(Qualification, Opportunity) and wire them into the existing
certification/mission code with the smallest possible additive touch.

## 3. The five core decisions

### 3.1 — `backend/kor_canonical/` binds KORA, following the KLT precedent exactly

Named `kor_canonical`, not the more generic `master_canonical` the
brief's own prose uses — the brief's "Master pédagogique" names the
*entire* docs corpus (every Rail-1 domain), but this pass only binds
one domain into the runtime. `fms_canonical`/`klt_canonical` are both
domain-prefixed, one package per corpus; `kor_canonical` follows that
precedent rather than claiming a scope it doesn't cover. A future pass
binding another domain (FRK, AGF, CYB, ...) gets its own
`<domain>_canonical` package the same way — never a single package that
silently tries to parse every corpus's own conventions.

Mechanically this is klt_canonical's own pattern, reused file-for-file
(`models.py`/`parser.py`/`provenance.py`/`import_pipeline.py`/
`read_model.py`/`progress.py`/`__init__.py`), because KORA's real
`docs/kor/korXX/` file convention (module header fence, skill registry
table, `case/`/`guides/`/`assessments/`/`skills/`/`templates/`
subtrees) is — module for module — the same convention KLT uses,
confirmed against `docs/kor/kor01/`, `kor02/`, and `kor03/`'s real
files this session. No ZIP upload (same situation as KLT): `POST
/kor-canonical/import` scans `docs/kor/` directly on the server
filesystem (`kor_canonical.provenance.default_docs_dir()`, overridable
via `KOR_DOCS_DIR`).

**One real invariant this package computes differently than KLT's**:
KLT's `fully_complete` reads a formation's own BUILT/BLOCKED status
column — a column KOR's skill registries never carry (confirmed across
KOR-01/02/03: always 5 columns, no status column). So
`kor_canonical.read_model` derives `fully_complete` from a different,
still-real check: every skill row's module reference must resolve to a
module that was actually imported for that formation. A registry
naming a module that wasn't found makes `fully_complete=False` and
lists the offending skill in `unresolved_skill_ids` — never silently
ignored, never a bare `True` constant.

**A genuine, deliberately unresolved discrepancy found this pass**:
`docs/kor/README.md` states `KOR-03`→`KOR-15` are
`NEW_CANONICAL_TARGET` / `CURRICULUM_BUILT = FALSE`, yet real module and
skill-registry files exist on disk for those formations today (content
that evidently post-dates that README, consistent with Rail 1's later
812-object closure work, which is out of scope for this ticket to
adjudicate). `kor_canonical` does not silently trust either claim: the
import pipeline imports whatever real files it finds, records every
file's provenance regardless of formation, and lets `fully_complete`
speak for each formation independently. **Only `KOR-01` was driven
end-to-end through this runtime binding and verified — see §5.** The
other 14 formations' real completeness is left an open question for a
future ticket, exactly the same "explicit blocker, never invented"
posture as every other domain closed in Rail 1.

### 3.2 — `canonical_common/` — a real internal-duplication fix, not new scope

Finding: `fms_canonical/models.py` and `klt_canonical/models.py` each
independently defined the exact same `Audience` Literal and the exact
same `resource_audience()`/`is_learner_facing()` fail-safe-default
logic, parametrized only by a domain-specific `RESOURCE_AUDIENCE` dict.
Two copies of the same enum and the same lookup behavior is precisely
the "plusieurs documents représentent le même objet" duplication the
Rail 2 brief asks to avoid — at the *code* level, not just the docs
level the rest of this engagement has focused on until now.

Extracted to `backend/canonical_common/audience.py`: one `Audience`
type, one fail-safe `resource_audience`/`is_learner_facing`/
`learner_facing_types`/`staff_only_types` set of generic functions,
parametrized by whatever domain-specific mapping the caller passes in.
`fms_canonical/models.py` and `klt_canonical/models.py` were edited to
delegate to it — same public function names, same signatures, same
fail-safe default (`["ADMIN", "INTERNAL"]` for an unrecognized type),
verified behavior-identical by direct import smoke-test. No caller of
either package needed to change. `kor_canonical/models.py` uses the
same shared source from the start — the third domain never gets its own
fourth copy.

### 3.3 — `backend/qualification/` — the one new package this rail actually adds

`QualificationDefinition` (admin-configured registry: "passing
certification X, optionally holding skills Y, earns qualification Z")
plus `Qualification` (a real, issued, append-only instance — same
durability discipline as `skills.models.EvidenceEntry`, sha256-hashed
issuance payload for FREK-readiness). Two collections
(`db.qualification_definitions`, `db.qualifications`), both new.

The one integration point into existing code is a single additive call
inside `certification/service.py::grade_attempt`'s pre-existing `if
passed:` block, immediately after the existing `wallet_credit(...)`
call:

```python
await maybe_issue_qualification(
    attempt.user_id, attempt.certification_code, attempt_id
)
```

`maybe_issue_qualification` is a pure no-op — returns `[]` — whenever no
`QualificationDefinition` names the certification code just passed.
Every certification flow that predates this ticket (FMS, GMD, WAL, ...)
therefore behaves identically to before; this was verified by running
the full pre-existing mongomock test tier (130 tests, see §5) both
before and after the change with zero regressions. Idempotent per
`(user_id, qualification_code)`: a retake or a re-grade never issues a
duplicate.

### 3.4 — Opportunity is not a new stored entity — it is `Mission.required_qualification_codes`

The chain sentence names "Opportunity" as a link, but the brief's own
"le runtime doit pouvoir représenter" list of nouns does not — deliberate,
read together with "Évite la duplication docs -> DB -> hardcoded
frontend" and "Utilise une seule source canonique quand plusieurs
documents représentent le même objet". A third representation of "what
a qualified learner is now eligible for" (alongside `Qualification`
itself and `Mission`) would be exactly the duplication the brief warns
against. Instead, Opportunity is modeled as a **computed eligibility
view** over the existing `Mission` model, via one new additive field:

```python
# models.py — Mission
required_qualification_codes: List[str] = Field(default_factory=list)
```

Default empty list = open to everyone = the exact behavior every
existing mission had before this field existed — fully
backward-compatible, zero migration needed. `api/missions.py::
list_missions` now annotates every returned mission with a computed
`eligible: bool` (`True` unconditionally when the list is empty; for a
signed-in user with a non-empty list, `qualification.has_any_of(user_id,
codes)`; `False` for an anonymous request against a gated mission) —
the catalogue stays fully browsable (a learner can see what to work
towards) rather than silently filtering. `accept_mission` enforces the
same gate as a real 403, not just a display hint.

### 3.5 — KOR-01 as the pilot formation

Chosen because it is the richest, most FMS-shaped Master Package corpus
of the three domains already runtime-bound or now bindable (14 modules,
14 one-to-one skills, a real fenced-metadata convention, a real
certification model, `PACKAGE_COMPLETE` status per `docs/kor/README.md`)
— and because, unlike FMS-01/KLT-01, none of its runtime chain had ever
been exercised end-to-end before this ticket, making it a genuine proof
rather than a formality.

## 4. The exact chain trace for KOR-01

1. **Learning** — `kor_canonical.import_kor_docs()` scans
   `docs/kor/kor01/`, persists 14 modules + 1 skill registry (+ every
   other real KOR-01 file, by provenance) to `db.kor_resources`;
   `get_canonical_kor_formation("KOR-01")` returns `fully_complete=True`,
   `module_count=14`.
2. **Skill** — the 14 real skill IDs (`KOR01.SKILL.C01`…`C14`) parsed
   from `skills/SKILL_ID_REGISTRY.md` are registered via
   `skills.progression.register_skill` (unmodified engine).
3. **Evidence** — two `record_evidence` calls per skill (a deliverable
   + a quiz entry, matching the engine's existing "2 entries ⇒ acquired"
   rule) bring all 14 to `state="acquired"`.
4. **Assessment** — a real `Rubric` for certification code `KOR01-A01`,
   one criterion per skill (`skill_id` set on each, so a pass records
   evidence back onto the Skill Engine — the existing
   `grade_attempt` loop, untouched).
5. **Certification** — `start_attempt` → `submit_attempt` →
   `grade_attempt` (max scores on all 14 criteria) → `passed=True`,
   `score_global=100.0`, FREK-CERT signal emitted, `academy.
   certification.passed` event published, wallet credited — all
   pre-existing, unmodified code paths.
6. **Qualification** — the same `grade_attempt` call additively issues
   `QUAL-KOR01-PRODUCTEUR-PODCAST` (a `QualificationDefinition`
   registered ahead of time naming `KOR01-A01`).
7. **Opportunity** — a real `Mission`
   (`MISSION-KORA-ANTENNE-LANBI`) with `required_qualification_codes=
   ["QUAL-KOR01-PRODUCTEUR-PODCAST"]` is `eligible=False` for the
   candidate before certification, `eligible=True` after — verified both
   ways, not just the positive case.
8. **Mission** — `accept_mission` rejects the candidate with a 403
   before certification, succeeds (`status="accepted"`, a real
   `db.user_missions` row) after.

All eight steps run as real code against `mongomock_motor.
AsyncMongoMockClient` (no live MongoDB in this sandbox — same
constraint every other canonical-runtime test in this repo already
documents) in `backend/tests/test_rail2_kor01_e2e.py::
test_kor01_full_chain_learning_to_mission`, asserting the actual
state at every link, including the negative case (ineligible/rejected
before certification) — not merely that no exception was raised.

## 5. What was built (file-by-file)

### Backend — `backend/canonical_common/` (2 files, new)

| File | Role |
|---|---|
| `audience.py` | `Audience` Literal + generic fail-safe `resource_audience`/`is_learner_facing`/`learner_facing_types`/`staff_only_types`. |
| `__init__.py` | Public surface. |

`fms_canonical/models.py` and `klt_canonical/models.py` edited to
delegate to it (behavior-identical, verified by smoke-test).

### Backend — `backend/kor_canonical/` (7 files, new, ~750 lines)

Same shape as `klt_canonical/`: `models.py`, `parser.py`,
`provenance.py`, `import_pipeline.py`, `read_model.py`, `progress.py`,
`__init__.py`. New collections: `db.kor_resources`,
`db.kor_resource_provenance`, `db.kor_imports`,
`db.kor_canonical_progress`. Never touches `db.formations`,
`seed_data.py`, `db.progress`.

### Backend — `backend/qualification/` (3 files, new)

`models.py` (`QualificationDefinition`, `Qualification`), `service.py`
(`register_definition`, `maybe_issue_qualification`,
`list_user_qualifications`, `is_qualified`, `has_any_of`),
`__init__.py`. New collections: `db.qualification_definitions`,
`db.qualifications`.

### Backend — additive edits to pre-existing files

| File | Change |
|---|---|
| `models.py` | `Mission.required_qualification_codes: List[str] = []` (new field, default empty). |
| `certification/service.py` | One import line + one `await maybe_issue_qualification(...)` call inside the existing `if passed:` block. |
| `api/missions.py` | `list_missions` now takes an optional current user and annotates each mission with computed `eligible`; `accept_mission` enforces the same gate as a 403. |
| `api/__init__.py` | Two new routers (`kor_canonical`, `qualification`) added to the existing aggregation loop. |

### Backend — new API routers

`api/kor_canonical.py` (prefix `/kor-canonical`, mirrors
`api/klt_canonical.py` route-for-route) and `api/qualification.py`
(prefix `/qualifications` — definition CRUD for admins, read-only
elsewhere; issuance is never a direct API call, only ever the
certification hook).

### Tests

`backend/tests/test_rail2_kor01_e2e.py` — the full chain proof (§4).
Full pre-existing mongomock-backed suite re-run: **130/130 passing**
(129 pre-existing + this new test), zero regressions.
`backend_test.py` (the live-HTTP-server suite) was not run — it
requires a running server + live MongoDB, neither available in this
sandbox; this is a pre-existing constraint of this environment, not
something this ticket changed (confirmed: it fails identically before
and after this ticket's changes, on connection errors, not assertion
failures).

## 6. RAIL 2 EXTENSION (2026-09-07) — "tout câbler, pas juste 1"

Founder instruction, same day as the pass above: "Finir rail 1 et 2
correctement avant de passer au rail 3" + "Je veux tout câbler et pas
juste 1" (Rail 2) + a request to verify Rail 1 domains against FMS's
own depth and to deliver a live preview. This section records what
that follow-up pass actually did — every item below is additive on top
of §1-5, nothing above was rewritten or reopened.

### 6.1 — `kor_canonical` verified against all 15 KOR formations, not just KOR-01

`KOR_FORMATION_CODES` already listed all 15 (§3.1) — this pass ran
`import_kor_docs()` against the real `docs/kor/` tree end-to-end and
read every formation back through `get_canonical_kor_formation`,
confirming the mechanism (not just the code path) generalizes:

```
KOR-01..KOR-10  fully_complete=True   (10/10, real MODULE_ID-headed modules, all skills resolved)
KOR-11..KOR-15  fully_complete=False  (5/5, real module files exist but in a lighter
                                        SKILL_ID-only convention — no MODULE_ID header,
                                        no PREREQUISITES/ASSESSMENT_LEVEL fields — the
                                        parser correctly does not synthesize a canonical
                                        module_code for a convention it wasn't taught,
                                        so these 5 formations honestly report 0 resolved
                                        modules rather than a false PACKAGE_COMPLETE)
```

This is the honest result, not a bug: `docs/kor/README.md` itself flags
KOR-11→15 as lighter-tier, and the runtime now proves that
independently, in live code, rather than only in a self-declared status
line — see `docs/ACADEMY_RAIL1_FMS_PARITY_COMPARISON.md` for the full
domain-by-domain comparison this finding feeds into. No parser change
was made to force these 5 formations to resolve — that would have
inflated their status to match KOR-01→10 without the underlying content
actually being there, which the whole engagement's discipline forbids.

### 6.2 — Frontend wiring: `kora-canonical` read-only pages, mirroring `kiltikonet-canonical`

Previously deferred, now closed: `frontend/src/pages/CanonicalKorFormations.js`,
`CanonicalKorFormationDetail.js`, `CanonicalKorModuleView.js` +
`lib/canonicalKorApi.js` + `lib/canonicalKorDisplay.js`, routed at
`/kora-canonical[/:formationCode[/:moduleCode]]` in `App.js` — file-for-file
the same shape as the existing `kiltikonet-canonical` pages (same
`Protected` wrapper, same "never imply complete when partial" contract:
a `PARTIAL` badge renders for any formation with `fully_complete=false`,
and the formation detail page additionally lists every skill whose
module reference never resolved, by skill ID). Verified live end-to-end
with a real running instance (§6.4) — not just component code that
compiles.

### 6.3 — A real, pre-existing bug found and fixed while building the live preview: `content_status` never seeded

`seed.py` upserts `seed_data.FORMATIONS`' raw dicts straight into
`db.formations` — none of those dicts carry a `content_status` key.
`Formation.content_status`'s Pydantic default ("published") only applies
when a `Formation(...)` model is constructed; it never applies to a
dict `$set`. Result: `GET /api/formations`'s anonymous-user filter
(`{"content_status": "published"}`) never matches any of the 30 seeded
formations, because Mongo's exact-match query never matches a field
that plain doesn't exist on the document. **This is a real bug in every
deployment of this codebase, not specific to this session's preview
setup** — confirmed by reading the exact query and seed code, not
inferred from the mock DB's behavior. Fixed with a one-time, additive
backfill in `seed.py` (`update_many({"content_status": {"$exists":
False}}, {"$set": {"content_status": "published"}})`) that only ever
touches formations missing the field — never overwrites an admin's real
draft/archived decision. Directly relevant to `ACA-0009` ("Activate
public formation discovery") on the task backlog, which this fix
resolves the backend half of.

### 6.4 — Live preview: what was actually run, and the one thing this sandbox cannot produce

The full stack was run for real in this sandbox — FastAPI backend +
React dev server + a real user registered/onboarded through the actual
API, driven with Playwright/Chromium (pre-installed in this
environment) through `/dashboard`, `/formations` (30 real formations,
proving §6.3's fix), `/canonical`, `/kiltikonet-canonical`,
`/kora-canonical` (all 15 formations, correctly graded), a KOR-01 module
page (`KOR01-M04`, full real content, prerequisite chain visible), and
`/missions` — screenshots delivered alongside this report.

**No live MongoDB was reachable to back this run** — confirmed
directly: `docker pull mongo` and the official MongoDB tarball download
both return `403 Forbidden` from this session's egress policy, and
Ubuntu's own apt repos don't carry a `mongodb-server` package. Rather
than block the preview on an unreachable dependency, `backend/db.py`
gained one additive, env-gated fallback: `MOCK_DB=1` swaps the real
`AsyncIOMotorClient` for `mongomock_motor.AsyncMongoMockClient` — the
exact same in-memory, Motor-API-compatible client every test in
`backend/tests/` already runs against, now wired to the *app* instead
of only test fixtures. Off by default; every other code path, including
every existing test, is untouched. `server.py`'s startup also gained an
`MOCK_DB`-gated auto-import of the real `docs/kor/` and `docs/klt/`
trees, so the preview shows real canonical content without a manual
admin action first.

**What this sandbox genuinely cannot do**: expose that running dev
server as a public, clickable URL. No tunnel binary is installed
(`ngrok`/`cloudflared`), the egress proxy explicitly does not support
tunneling clients, and no port-forwarding convention exists in this
remote container. This was verified, not assumed, before falling back
to screenshots — the honest limitation is the environment, not the
code: the backend and frontend are both real, running, and correct: a
locally-run copy of this repo (`MOCK_DB=1 uvicorn server:app` +
`yarn start`, or a real `MONGO_URL` and no `MOCK_DB`) reproduces exactly
what the screenshots show.

## 7. Explicitly still deferred / out of scope

- **KOR-11→15's actual module content** — real files exist in a
  lighter convention; bringing them to canonical/FMS depth is a content
  task (Rail 1's domain, not Rail 2's) before the runtime binding could
  ever honestly report `fully_complete=True` for them.
- **Every other Rail-1 domain** (FRK, AGF, CYB, BCI, GCF, HOS, LOS, CEO,
  GRP, FDC, XCV, SAY, GMD, WAL) — still not imported into the runtime.
  Binding one is a repeat of §3.1's pattern (one `<domain>_canonical`
  package), not a new architecture decision; none was requested this
  pass beyond KORA.
- **KOR-01's own `contexts` (INTERNAL/EXTERNAL/BRIDGE)** — still an
  empty list (`KOR_CONTEXTS = {}`), still unresolved for the same
  reason as before (§ unchanged from the original pass): no
  reconciliation ticket has ever fixed KOR's contexts, and legacy
  `seed_data.py` carries no `contexts` field for KOR-01/02 either.
- **A real public preview URL** — not obtainable from this remote
  sandbox (§6.4). Screenshots + a locally-reproducible setup are the
  honest substitute.
- **`QualificationDefinition.required_skill_ids`** (an optional extra
  gate beyond "certification X passed") is implemented but unused by
  the KOR-01 pilot definition — the certification pass alone is
  sufficient for `QUAL-KOR01-PRODUCTEUR-PODCAST`. Exercised in code, not
  yet exercised by a definition that actually sets it.

## 8. Verification summary

- `python3 -m pytest backend/tests/ --ignore=backend/tests/backend_test.py`
  → **130 passed** (129 pre-existing unmodified tests + 1 new Rail 2
  E2E test), 0 failed, 0 regressions. Re-run again after the §6
  extension (db.py/seed.py/server.py edits) — still 130/130.
- `pyflakes` clean on every new/edited file
  (`kor_canonical/`, `qualification/`, `canonical_common/`,
  `api/kor_canonical.py`, `api/qualification.py`, `api/missions.py`,
  `api/__init__.py`, `certification/service.py`, `models.py`,
  `tests/test_rail2_kor01_e2e.py`).
- `python3 -c "import api"` — the full FastAPI router aggregation
  (114 routes, including the two new routers) imports cleanly.
- Direct smoke-test of `kor_canonical` against the real `docs/kor/`
  tree (not a fixture): 435 real files found, 396 parsed, 15/15
  formations discovered, KOR-01 confirmed `fully_complete=True` with
  all 14 modules and 14 skills correctly ordered and cross-referenced
  (`M04`'s real `PREREQUISITES: M03` header resolves to
  `KOR01-M03`; `M01`'s real `PREREQUISITES: Aucun` resolves to `None`
  — never guessed).
- §6 extension: `eslint` clean on all 5 new frontend files + `App.js`;
  a real running backend (`MOCK_DB=1`) + frontend (`yarn start`)
  driven with Playwright through 9 real routes, screenshots delivered
  to the Founder alongside this report.

**Gate status**: MET, and re-verified against all 15 KOR formations
(not just the pilot) plus a live click-through. KOR-01 is followable
end-to-end — Learning → Skill → Evidence → Assessment → Certification
→ Qualification → Opportunity → Mission — in real, tested, and now
also visually verified runtime code, with zero legacy behavior changed
for FMS, KLT, GMD, WAL, or any pre-existing certification/mission flow
(the one behavior change, §6.3's `content_status` backfill, is a bug
fix that makes existing, already-`published`-by-intent formations
visible — never a new behavior).
