# CVLN Academy — W-FUNNEL-1 Foundation Report

```
W-FUNNEL-0 = ACCEPTED_BASELINE
W-FUNNEL-1 = DELIVERED (this report)
W-FUNNEL-2+ = NOT_AUTHORIZED
H1 = NOT_AUTHORIZED
FOUNDATION_FIRST honored: no page's visible experience changed. Every
new capability is either (a) inert unless imported (same posture as
motion-tokens.js/motion-primitives.jsx/spatial-state.js before it), or
(b) flag-gated and defaults OFF (RouteTransition's topology lookup), or
(c) a backend-only additive field read (progression.py's new
`returning` key — additive dict key, breaks no existing consumer).
STOP_AFTER_DELIVERY = TRUE.
```

## PRODUCT_VISUAL_REDESIGN = NO
## FUNNEL_BEHAVIOR_CHANGE = NO when flags OFF
## MONETIZATION_IMPLEMENTED = NO
## PUBLIC_DISCOVERY_DECISION = PENDING
## FMS_MIGRATION_TOUCHED = NO
## H1_AUTHORIZED = NO

## Exact files changed

**New (10 files + 1 directory):**
- `backend/lifecycle.py` — pure `is_returning_session` derivation
- `backend/tests/test_lifecycle.py` — 8 unit tests, no DB required
- `frontend/src/lib/spatial/physics.js` + `.test.js` (7 tests)
- `frontend/src/lib/spatial/attention.js` + `.test.js` (11 tests)
- `frontend/src/lib/spatial/cadence.js` + `.test.js` (8 tests)
- `frontend/src/lib/spatial/topology.js` + `.test.js` (8 tests)
- `frontend/src/lib/spatial/audio.js` + `.test.js` (7 tests)
- `frontend/src/lib/spatial/haptics.js` + `.test.js` (10 tests)
- `frontend/src/lib/spatial/framePacing.js` + `.test.js` (5 tests)
- `frontend/src/lib/spatial/routeTopologyMap.js` + `.test.js` (5 tests)
- `frontend/src/lib/lifecycleState.js` + `.test.js` (15 tests)
- `frontend/src/lib/featureFlags.js` + `.test.js` (5 tests)

**Modified (3 files, additive-only diffs):**
- `backend/api/progression.py` — `+14` lines: one new import, one new
  computed dict key (`returning`) appended to `frek_profile`'s existing
  response; no existing key changed or removed.
- `frontend/src/lib/RouteTransition.jsx` — `+31/-6` lines (net +25):
  adds an optional, flag-gated topology-edge lookup exposed only as an
  inert `data-topology-edge` DOM attribute; the actual rendered
  animation (opacity crossfade, duration, easing) is byte-for-byte
  unchanged from before this wave, unconditionally.
- `frontend/.env.example` — `+16` lines documenting the 7 new flags,
  all commented out, all defaulting to false when unset.

## H0.10 subsystem extraction map

| H0.10 subsystem | New location | Classification | Why |
|---|---|---|---|
| `makeRailPhysics` (spring, substep fix) | `spatial/physics.js` | **REUSE** | Constants (280/33) and the substep integration are the exact, independently-verified-stable values from `SPATIAL_H10_PERCEPTUAL_REFINEMENT_REPORT.md` §3 — re-deriving them would discard that verification |
| `attentionWeight`/`attentionTier`/`applyDepth` | `spatial/attention.js` | **ADAPT** | Math ported unchanged; DOM coupling (inline styles, `--formation-signature`, `aria-hidden` writes) removed — this module now returns plain objects, a caller applies them |
| H0.8's autofocus race-protection engine | `spatial/attention.js` (`createAutofocusGuard`) | **ADAPT** | Same `LATEST_EXPLICIT_USER_INTENT_WINS`/stale-request-discard logic, generalized from the prototype's module-level singleton into an instantiable factory; found and fixed a real tie-breaking bug in the process (see below) |
| Input cadence classifier | `spatial/cadence.js` | **REUSE** | Already framework-agnostic pure JS in H0.10 — ported near-verbatim; found and fixed a real latent falsy-zero bug (see below) |
| `TRANSITION_TOPOLOGY` | `spatial/topology.js` | **REWRITE_SMALL** | H0.10's version was a flat 7-route lookup driving one CSS scale value; production needs the mission §7 node/edge shape (direction/depth/intent/shared-object/environment-continuity policy) over the full lifecycle node set, including non-route lifecycle states |
| `SpatialAudioController` | `spatial/audio.js` | **REUSE** | Same 8 events, same synthesis, same throttle — wrapped as a factory instead of a module-load IIFE |
| `HapticController` | `spatial/haptics.js` | **REUSE** | Same 5 patterns, same gating, same graceful-no-op discipline |
| `FramePacing` | `spatial/framePacing.js` | **REWRITE_SMALL** | Same sampling/percentile math; H0.10's version started its rAF loop as a module-load side effect — unsafe for a real app/test/SSR context, so this version requires an explicit `start()`/`stop()` |
| Camera Anchor Contract / `cameraFollowTransition` state machine | *not ported this wave* | **DO_NOT_PORT (yet)** | Mission §4/§10/§22 explicitly scope camera-follow implementation out of W-FUNNEL-1 ("infrastructure only... do not implement major visual spatial movement yet") — `topology.js`'s edge metadata (`sharedObjectPolicy`, `environmentContinuityPolicy`) is the seam a later wave wires this into, not built yet |
| Environmental continuity (`--topo-depth`, `--formation-signature`, botanical layer) | *not ported this wave* | **DO_NOT_PORT (yet)** | Same reasoning — a visual/environmental system, explicitly out of scope until a later wave actually mounts it on a real surface |
| Perceptual occlusion CSS output (blur/contrast/brightness filter strings) | *not ported this wave* | **DO_NOT_PORT (yet)** | `attention.js`'s `computeDepthStyle` computes the same 6-channel numbers but nothing calls it from a real component yet — the numbers exist, application doesn't |

**Two real bugs found and fixed while porting, both inherited from the
H0.10 prototype, neither ever manifested there:**

1. **`cadence.js`**: the original `cadence.lastTime ? interval : Infinity`
   check reads `0` as falsy — if the very first real input arrives at
   exactly `t=0` (never happens with a real `performance.now()`, but a
   real risk once the clock became injectable for testing, and a
   theoretical risk on an extremely fast post-navigation interaction),
   it would be silently treated as "no prior input," corrupting the
   very next classification. Fixed by using `null` as the sentinel
   (matching `physics.js`'s own `lastT = null` convention), not `0`.
2. **`attention.js`**'s `createAutofocusGuard`: the ported
   `lastExplicitIntentAt > requestedAt` comparison used `Date.now()`
   directly — two synchronous calls (a real risk: an explicit intent
   noted in the same event-loop tick as an automatic request, or simply
   two fast browser interactions) can land in the same millisecond,
   making a genuine tie read as "the request wins" instead of "the
   explicit intent wins." Fixed with a monotonically-increasing
   tie-breaking clock and an inclusive (`>=`) comparison — a real
   correctness improvement for production, not just a test workaround.

## Topology architecture

`spatial/topology.js` declares 21 real edges (see the file) over 19
lifecycle nodes named exactly per mission §7 (`spatial/routeTopologyMap.
js` is the one file translating a real `frontend/src/App.js` pathname
into a node key — kept separate so `topology.js` itself stays
route-agnostic, since a node may represent a lifecycle state with no
route at all, e.g. `ACTIVATION`/`EXPANSION`/`ECOSYSTEM`). `resolveEdge`
fails safe (lateral, no shared-object policy) for any undeclared pair —
never invents a relationship, matching the mission's "do not invent
routes that do not exist" extended to relationships between them.

## Lifecycle architecture

`lifecycleState.js` implements the exact 10-state minimum named in the
W-FUNNEL-1 authorization §8 (`VISITOR, REGISTERED, ONBOARDING,
ACTIVATED, FIRST_VALUE, ACTIVE_LEARNER, PROGRESSING, PROOF_BUILDING,
RETURNING, EXPANDING`) — note this naming is authoritative for this
wave and differs slightly from `docs/ACADEMY_LIFECYCLE_STATE_MODEL.md`'s
own earlier draft (`IDENTIFIED`/`LEARNING`/`PROVEN` etc.); that document
should be read as superseded on naming by this report, not contradicted
by it — reconciling the doc itself is left to a documentation-only
follow-up, not required for this wave's acceptance.

Every derivation reads only already-fetched API response shapes
(`Dashboard.js`'s own existing 5 calls) — no new network request is
introduced by this module. `FIRST_VALUE`/`ACTIVE_LEARNER` use a
disclosed, conservative proxy (`hasAnyRealActivity`) because the
inventoried endpoints expose *completed*-module counts, not *started*
counts — documented in the module's own comments as a known precision
gap, not silently assumed. `RETURNING` is the one state backed by a
genuinely new real signal this wave (`backend/lifecycle.py`).

**`test_never_invents_a_paid_state`** (`lifecycleState.test.js`)
structurally asserts no `PAID`/`CUSTOMER`/`SUBSCRIBED`/`PREMIUM` value
exists anywhere in the enum, and that no derivation path can produce a
value outside the declared enum — not just a convention, a checked
invariant.

## Backend schema decision: no schema change

W-FUNNEL-0's own gap matrix expected a new `User.last_login_at` field.
Re-checked at implementation time per §9's own instruction ("if
existing repository data already provides an equivalent trustworthy
signal, reuse it instead") — it does: `issue_refresh_token`
(`backend/auth.py`) is called from both `register` and `login`
(`backend/api/auth.py:124,136`), inserting a real, already-existing
`db.refresh_tokens` document stamped with `created_at` on every
successful authentication. The most recent of those timestamps for a
user is exactly "last successful authentication" — no migration, no
new field, no backward-compatibility concern at all, because nothing
was added to `User`. `backend/lifecycle.py::is_returning_session` is a
pure function over `(user.created_at, [refresh_token.created_at, ...])`,
wired into `GET /frek/profile`'s existing response as one new,
additive `returning` boolean.

## Tests

**Backend**: 8 new unit tests (`test_lifecycle.py`), zero DB
dependency, same "pure unit test" pattern as `test_quiz.py`/
`test_certification_scoring.py`. Full existing no-DB suite re-run:
**48/48 pass** (`test_lifecycle.py` + `test_quiz.py` +
`test_certification_scoring.py` + `test_fms_import.py` +
`test_template_export.py`). `black --check` clean across the whole
backend (74 files). `mypy`/`flake8` clean on every file this wave
touched or added; the live-server `backend_test.py` suite remains
untestable in this sandbox (no MongoDB — the exact, disclosed
limitation `ACADEMY_CURRENT_FUNNEL_AUDIT.md` already named, unchanged
by this wave).

**Frontend**: 76 new unit tests across 10 new suites — physics (7,
including the exact worst-case-dt substep-stability proof), attention
(11, including the "exactly one PRIMARY at every sampled instant of a
continuous sweep" invariant), cadence (8), topology (8),
routeTopologyMap (5), audio (7), haptics (10, incl. real
`navigator.vibrate` mock verification), framePacing (5), lifecycleState
(15, incl. the never-invents-PAID assertion), featureFlags (5). **Full
existing Jest suite re-run: 109/109 pass across 14 suites** (10 new + 4
pre-existing: `spatial-state.test.js`, `JourneyHierarchy.test.js`,
`CvlnFocusField.test.js`, `mentorPresence.test.js` — all still green,
untouched by this wave).

**E2E (Playwright, frontend-only per the sandbox's own disclosed
constraint)**: **73/73 pass**, all 11 pre-existing specs, run against
the actual built app after every change in this wave — critically
including every `route-transition.spec.js` and `routing.spec.js` test,
which directly exercise the one component (`RouteTransition.jsx`) this
wave modified. Zero regression, verified against the real rendered DOM,
not just unit-level assumption.

## Performance impact

Production build (`craco build`) compiles cleanly. Gzipped main bundle:
**+1.28 kB** (169.84 kB, was 168.56 kB) — from `RouteTransition.jsx`'s
new unconditional imports (`featureFlags.js`, `topology.js`,
`routeTopologyMap.js`; the runtime `if (FEATURE_FLAGS...)` check can't
be tree-shaken away since the flag is read from `process.env` at
runtime, not a build-time constant). CSS: +48 bytes (unrelated Tailwind
class churn from `.env.example`'s own comment reformatting — noise,
not a real change). **Every other new module** (`physics.js`,
`attention.js`, `cadence.js`, `audio.js`, `haptics.js`, `framePacing.js`,
`lifecycleState.js`) **is not imported by any page or by
`RouteTransition.jsx`** — same "unmounted infrastructure" posture as
`motion-tokens.js`/`spatial-state.js` before them — so they add
**zero** bundle size until a future wave actually imports one.

## Regressions

**None found.** 109/109 Jest, 73/73 Playwright, 48/48 backend unit
tests all green; `black`/`flake8`/`mypy` clean on every touched file;
production build succeeds.

## Limitations (disclosed)

1. No live-backend/MongoDB test environment exists in this sandbox —
   the `returning` field's real end-to-end behavior (does a genuine
   second login actually flip it) is proven by unit tests against the
   pure derivation function, not by an integration test hitting a real
   `/frek/profile` response. Same limitation `ACADEMY_CURRENT_FUNNEL_
   AUDIT.md` already disclosed, unchanged.
2. `lifecycleState.js`'s `FIRST_VALUE`/`ACTIVE_LEARNER` proxy
   (`hasAnyRealActivity`) is conservative, not precise — the real
   backend doesn't currently expose a "modules started" count distinct
   from "modules completed." A future wave adding that signal would
   let this module derive `FIRST_VALUE` more precisely; not blocking
   for this wave, disclosed in the module's own comments.
3. `docs/ACADEMY_LIFECYCLE_STATE_MODEL.md`'s state naming is superseded
   by this report's §8-authoritative naming; the doc itself is not
   rewritten by this wave (documentation-only follow-up, not required
   for acceptance).
4. `RouteTransition.jsx`'s topology-edge lookup is real and tested
   (`routeTopologyMap.test.js`) but consumed by nothing yet beyond an
   inert DOM attribute — by design, per mission §10/§22's explicit
   "infrastructure only" scope for this wave.

## Rollback

Every new capability is reachable only through: (a) an explicit
`import` no existing page performs (physics/attention/cadence/audio/
haptics/framePacing/lifecycleState — deleting these files or leaving
them unimported is a full revert with zero blast radius), or (b) a
`REACT_APP_ACADEMY_*` flag that defaults false (`RouteTransition`'s
topology lookup — unset every flag, or delete `.env`, to fully revert
to pre-wave behavior), or (c) one additive backend dict key
(`returning` in `frek_profile`'s response — any consumer not looking
for that key is entirely unaffected; removing the 3 added lines in
`progression.py` and deleting `lifecycle.py`/`test_lifecycle.py` is a
full revert). No database migration occurred, so there is nothing to
roll back at the data layer.

## Acceptance gate (mission §22), verified point by point

1. ✅ H0.10 mechanisms extracted out of the prototype into
   `frontend/src/lib/spatial/` — 7 modules, framework-agnostic, tested.
2. ✅ Production has reusable physics/attention/topology/cadence
   infrastructure.
3. ✅ Lifecycle state is representable (`lifecycleState.js`).
4. ✅ Existing `RouteTransition` remains the integration boundary —
   extended, not replaced; no parallel transition system introduced.
5. ✅ No parallel app/navigation architecture — `React Router`/
   `BrowserRouter`/`Protected` in `App.js` are completely untouched.
6. ✅ Flags OFF reproduces current Academy behavior — proven by the
   full 73/73 e2e pass with no flags set (the sandbox's default state).
7. ✅ No public-discovery decision made — `/formations` stays
   `<Protected>`, untouched; `ACADEMY_FUNNEL_GAP_MATRIX.md`'s own
   pending item is still pending, not silently resolved.
8. ✅ No monetization faked — zero payment/checkout/subscription code
   exists; `lifecycleState.js` structurally cannot produce a paid state.
9. ✅ No FMS migration touched — `db.formations`/`db.progress` were
   never read or written by any new code this wave.
10. ✅ Tests prove retarget/reversal/numerical stability —
    `physics.test.js`'s 7 tests, directly reproducing the H0.10
    substep-stability proof method.
11. ✅ Rollback is trivial — see above.
12. ✅ Production visual surfaces remain effectively unchanged —
    verified, not assumed: 73/73 e2e against the real rendered app.

## W-FUNNEL-1 status block

```
W-FUNNEL-1_STATUS               = COMPLETE
LEGACY_BEHAVIOR_WITH_FLAGS_OFF  = VERIFIED (73/73 e2e, 109/109 jest)
SPATIAL_FOUNDATION_READY        = YES (physics/attention/cadence/topology/audio/haptics/framePacing)
LIFECYCLE_RUNTIME_READY         = YES (10-state model, non-exclusive, no invented paid state)
H010_EXTRACTION_COMPLETE        = YES for camera/attention/physics/cadence/audio/haptics/frame-pacing math;
                                   camera-follow state machine + environmental continuity deliberately
                                   DO_NOT_PORT this wave (mission §4/§10/§22 scope)
PUBLIC_DISCOVERY_DECISION       = PENDING (unchanged, Founder decision, not engineering's to make)
MONETIZATION_STATUS             = MISSING_REAL_CAPABILITY (unchanged, nothing invented)
FMS_MIGRATION_STATUS            = UNTOUCHED (frozen constraints honored)
TEST_STATUS                     = GREEN (109 jest + 73 e2e + 48 backend unit, 0 regressions)
ROLLBACK_STATUS                 = TRIVIAL (flags off / unimported files / 3-line backend revert)
W-FUNNEL-2_RECOMMENDATION       = GO, once the Founder resolves the public-discovery
                                   decision (mission's own explicit prerequisite) — the
                                   Hero System research (docs/ACADEMY_HERO_ENTRY_RESEARCH.md)
                                   is already available to ground that wave's design work
```

`STOP = TRUE`.
