# H0.9 — Full Spatial Console Feel Upgrade — REPORT

```
STOP = TRUE
H1 = NOT_AUTHORIZED
DO_NOT_RESET honored: H0.8 (spatial-console-h08.html) is untouched at its
own URL, kept as the reference/rollback point. This iteration lives in a
new file (spatial-console-h09.html), same lineage, additive only.
Nothing in frontend/src, backend/, or the database was touched.
git status --porcelain on the repo is empty after this work (only docs).
```

## Deliverables

- **Prototype (interactive)**: [Spatial Console — H0.9](https://claude.ai/code/artifact/850da556-71ba-4737-8521-adcbd3f313bb) — `spatial-console-h09.html`, scratchpad only, never committed.
- **Proof gallery** (debug-panel readouts, quiz context, fast-repeat cadence, environmental depth): [H0.9 Proof Gallery](https://claude.ai/code/artifact/16f94b3d-1663-4a78-9f5e-8e2ab61f3f0e)
- **H0.8 base, preserved as-is**: [Spatial Console — H0.8](https://claude.ai/code/artifact/5ecce21c-efb8-4bb6-9b7c-cca0a45639a5) — unchanged, the rollback target.
- This report.

## What H0.9 is, in one paragraph

H0.8 gave the console a camera that follows across route boundaries and
an autofocus engine that knows what it's doing. H0.9 is the layer the
Founder's brief called the actual "PlayStation feel": the rail no longer
snaps between four fixed depth buckets on a CSS transition — it is now
driven by a **real spring-physics engine**, retargetable at any instant
without ever resetting; input **cadence** (single / repeated / fast-repeat
/ reversal / stopped) is classified from real timestamps and used to defer
non-essential detail during rapid navigation, never the navigation itself;
a conservative, fully deterministic **focus-prediction** cue previews
where the rail is heading without ever committing it; **spatial audio**
(Web Audio oscillators, no external assets) and **haptics**
(`navigator.vibrate`) now respond to eight/five named events respectively,
muted/off by default and gated behind one explicit user toggle; a small
**transition topology** gives route changes a consistent "world" direction
(deeper / shallower / lateral) instead of an arbitrary swap; and a real,
continuous **frame-pacing sampler** backs an expanded, inspectable debug
panel — 12 named fields, never narrated claims. Every H0.5–H0.8 system
(dominant focus, receding neighbors, partial offscreen, camera-follow,
autofocus, focus memory, focus trap, mobile drag/snap, reduced motion) is
still there, unmodified in behavior, and re-verified this session.

## What was added (delta vs. H0.8)

**1. Spatial Physics Engine** (`makeRailPhysics`). Each rail's "focus
position" collapses to a single continuous scalar in index units, driven
every animation frame by a critically-damped-ish spring
(`STIFFNESS=220, DAMPING=27`) toward a live, retargetable `target`. Every
tile's full visual state (translateX/Y/Z, rotateY, scale, opacity,
saturation, blur — via the also-rewritten continuous `applyDepth()`) is a
pure function of `tileIndex − position`, recomputed every frame. This is
what makes retargeting mid-flight a real velocity-preserving redirect
rather than stop/reset/restart — **verified this session**: interrupting
a rail 40ms into a `setTarget(1)` flight with a second `ArrowRight`
(`setTarget(2)`) showed `velocity: 22.04` (nonzero, still carrying) at the
moment of retarget, then a clean spring-settle to the new target — not a
snap-to-zero-then-relaunch. CSS `transition` on `transform/opacity/filter`
was removed from `.hub-tile`/`.focus-card` (kept only for
`width/background/box-shadow`) so the JS-driven values aren't fighting a
second, competing animation system.

**2. Continuous Attention Model.** `attentionWeight(distance) =
1/(1+distance²·0.55)` replaces the old 4-bucket discrete lookup — Z,
scale, opacity, saturation, blur (FAR ≤0.5px → 0px at ACTIVE, never hazy),
translateY and rotateY are now all smooth functions of a possibly
fractional distance, so a tile sweeping through during fast navigation
reads as continuous motion, not a series of jump-cuts.

**3. Input Cadence classifier** (`trackInput`/`cadence`): SINGLE /
REPEATED / FAST_REPEAT (3+ same-direction inputs inside a 260ms window) /
REVERSAL / STOPPED, from real `performance.now()` timestamps. Drives
`cadenceDwellDelay()` — dwell-gated reveal/announcement delays stretch
2.2× during FAST_REPEAT, so rapid traversal never machine-guns detail
text or screen-reader announcements, while the rail/camera themselves
never wait on anything. **Verified**: 6 rapid arrow presses (≈55ms apart)
reliably reached `FAST_REPEAT` with `streak: 5`; a same-session direction
change correctly read `REVERSAL`; letting input settle for >260ms
correctly returned to `STOPPED`.

**4. Focus Prediction** (`predictNextIndex`): conservative and fully
deterministic — only during REPEATED/FAST_REPEAT with a consistent last
direction, only one step ahead, never near a rail boundary (returns "no
prediction" there, verified in the boundary screenshot). Surfaced as a
barely-visible `data-predicted` corner dot — CSS-only, never touches the
scale/opacity/position channels the physics engine owns, so it can never
be mistaken for committed selection.

**5. SpatialAudioController** — Web Audio oscillators only (sine/
triangle/square, envelope-shaped gain ramps generated at call time; no
external files, nothing that could resemble a licensed sound). Eight
events wired into real call sites: `NAV_MOVE` (rail step, rate-limited
40ms / 90ms during FAST_REPEAT), `BLOCKED` (rail boundary — a real,
disclosed cue, not a silent no-op), `FOCUS_LOCK` (physics settle),
`ENTER_DEPTH`/`RETURN_DEPTH` (camera-follow transitions, forward and
return), `CONTEXT_OPEN`/`CONTEXT_CLOSE` (dock open/close), `CONFIRM`
(quiz "Valider" — demo-only, touches no real progression). Muted by
default; a single header toggle (`🔇/🔊 son`) is the only thing that can
enable it, and that click is also the real user-gesture the browser
requires before `AudioContext` will actually produce sound (autoplay-
restriction compliant — verified structurally: the context is only
constructed inside `setEnabled(true)`, itself only reachable from the
toggle's click handler).

**6. HapticController** — `navigator.vibrate()`, feature-detected
(`Haptics.supported`), five named patterns (`FOCUS_LOCK`, `SNAP`, `ENTER`,
`CONFIRM`, `BLOCKED`), gated behind the same sound opt-in, wrapped in
try/catch, silent no-op if unsupported. `SNAP` fires once at the exact
moment a mobile drag commits to a target — never a continuous buzz during
the drag itself. *(Disclosed: this session's headless Chromium reports
`navigator.vibrate` as present; real desktop Chrome normally does not —
an environment quirk of the sandbox, not a change to our own
feature-detection/gating logic, which still runs unconditionally.)*

**7. Transition Topology** (`TRANSITION_TOPOLOGY`) — a small, real lookup
table over the actual IA (not invented routes): Hub↔{Formations, Roadmap,
Missions, Badges, FREK} and every sibling pair among those five are
`lateral`; {Hub, Formations, Roadmap}→Module is `deeper`, the reverse is
`shallower`. `goto()` — the single funnel every route change already
passes through (direct nav clicks, the internal `goto()` inside
camera-follow/return transitions, and back/forward) — calls
`applyTopologyEnvironment()` once per change, which nudges a new,
dedicated, `@property`-registered custom value (`--topo-depth`, a real
animatable number) on `.env-base`'s own `transform: scale(...)` — a
channel nothing else touches, so it never fights the section-color glow
(`--glow-1/2/3`, already section/focus-tint-owned) or the rail-focus
parallax already living on `.env-light`'s transform. **Verified**: `1` at
rest → `1.015` on entering Module → `0.988` on return → back to `~1` on a
lateral Hub→Formations switch, each value read via `getComputedStyle`,
smoothly interpolating through the existing `--t-env` transition (not
snapping) — real, measured, not narrated.

**8. Frame Pacing Sampler** (`FramePacing`) — a continuous
`requestAnimationFrame` loop (bounded 240-sample/~4s rolling window,
cost per frame is a single timestamp subtraction) computing real mean/
P95/P99 frame time and a dropped-frame count (>33ms = a missed 60Hz
frame). A new "📊 rapport frame-pacing" button prints the current window
as a `console.table` and reads it aloud via the existing `aria-live`
channel — never a fabricated number, and the limitation is disclosed
below rather than hidden.

**9. Expanded, inspectable debug panel.** A new `.physics-debug` panel
(bottom-right, stacked above the existing H0.8 camera-debug panel)
exposes 10 more named, live fields — RAIL, CADENCE, POS(h/f), STREAK,
VEL(h/f), PREDICTED, TARGET(h/f), AUDIO, FRAME, HAPTIC — which, together
with the existing CAM/FOCUS fields, is the spec's required 12 named
fields. Debug-only (hidden ≤900px, same convention as the H0.8 panel),
never shown to real end users.

## A real bug caught and fixed before any of the above could be tested

`updatePhysicsDebug()` was called from three sites (`hubOnFrame`,
`formationsOnFrame`, `trackInput`) before the function itself was ever
defined — a straightforward `ReferenceError` that would have broken page
load entirely, since `renderHub()`'s init-time render already triggers a
physics `jump()` → `onFrame` → `updatePhysicsDebug` call chain. Caught by
my own review before any Playwright verification was run this session
(not by a Founder report), fixed by implementing the panel-update
function properly (see item 9 above), then verified via a fresh headless
load with zero `pageerror`/console-error events.

## Verification performed this session

All via Playwright against the actual file (not a description) —
`pageerror` and non-cosmetic console-error listeners attached throughout;
the only console line ever observed across every run was a sandbox-only
`ERR_CONNECTION_RESET` on the Google Fonts stylesheet (no network egress
in this sandbox — cosmetic font fallback, unrelated to any of this work).

- **Load-clean**: fresh page load, zero errors.
- **Physics correctness**: position/velocity/target read directly from
  the live debug fields (not inferred) across rail navigation, a
  mid-flight retarget (velocity carried, not reset), and settle-to-rest.
- **Cadence correctness**: SINGLE → FAST_REPEAT (6 rapid presses,
  streak 5) → REVERSAL → STOPPED, each state read from the live field,
  not assumed.
- **Sound/haptic wiring**: toggle button flips `AUDIO`/debug field
  correctly; zero errors constructing `AudioContext` or calling
  `navigator.vibrate` across every wired event (NAV_MOVE, BLOCKED,
  FOCUS_LOCK, ENTER_DEPTH, RETURN_DEPTH, CONTEXT_OPEN, CONTEXT_CLOSE,
  CONFIRM, SNAP).
- **Full H0.5–H0.8 regression, re-run against H0.9**: all six sections
  (Hub, Formations, Roadmap, Missions, Badges, FREK) reachable with
  `data-current` correctly flipping and `window.scrollY === 0` at every
  checkpoint (the H0.8 `<html>`-overflow fix still holds). All three
  camera-follow anchors — Hub "Continuer", Formations target card,
  Roadmap current-stage card — still transition into Module and back
  (explicit "← Retour" **and** browser Back) with zero errors.
- **Context dock**: quiz open → confirm (CONFIRM sound+haptic) → close
  (CONTEXT_CLOSE sound), zero errors, focus trap and exact-return
  mechanics untouched by this wave's changes.
- **Mobile drag**: a touch-emulated swipe on the Hub rail correctly
  focused a new tile (`origin: 'touch'`), zero errors, zero scroll
  drift, `SNAP` haptic call reached with no throw.
- **Reduced motion, full round trip**: `reducedMotion: 'reduce'` — Hub
  → Module (instant path) → back to Hub, `data-current` flips correctly
  both ways, the "← Retour à l'accueil" back-link is present (the exact
  H0.8 regression this class of bug represents), zero errors.
- **Environmental continuity**: `--topo-depth` read via computed style
  across a deeper (Hub→Module), shallower (Module→Hub) and lateral
  (Hub→Formations) transition — real measured values, not visual
  impression only (see item 7 above).
- **Screenshots** (published in the proof gallery): Hub with both debug
  panels visible; Module entered (topology depth applied); quiz context
  confirmed; back at Hub; fast-repeat cadence mid-sweep with the rail
  visibly between discrete stops and the debug panel showing
  `FAST_REPEAT`/`streak 5`/fractional `POS`.

## Known gaps and limitations (disclosed, not silently dropped)

1. **Frame-pacing numbers measured this session are poor** (mean
   ≈40ms, most frames flagged "dropped" against the 33ms/60Hz
   threshold) — **this reflects the constrained, headless, single-core
   sandbox this session runs in, not a claim about real end-user
   hardware**. The mechanism itself (`FramePacing`) is real and
   unfabricated; no attempt was made to dress up the number, per the
   spec's own "do not fake metrics, disclose limitations" requirement.
   A real hardware pass is needed before this number means anything as
   a performance claim.
2. **No audible verification.** `SpatialAudio` was verified
   structurally (toggle flips state, `AudioContext` construction and
   every `play()` call path throw no errors) — this sandbox has no
   speakers/audio capture. Tone design (frequency/duration/envelope per
   event) was authored to spec intent, not ear-tested.
3. **Haptic support detection differs from real desktop Chrome in this
   sandbox** (see item 6 above) — disclosed rather than quietly
   adjusted or hidden.
4. **Predicted-focus dot** was visually confirmed present in the
   fast-repeat screenshot's underlying DOM state (via `data-predicted`
   and the boundary case correctly showing no prediction) but not
   independently pixel-diffed this session.
5. **Transition Topology intentionally stays IA-honest**: no
   Formations↔Roadmap camera-follow anchor exists (same disclosed gap
   as H0.8 — they are catalog/stage-based siblings, not parent/child, in
   the real app), and the topology table does not invent one; that pair
   simply resolves to `lateral` like any other sibling pair.
6. **No true "environment morph" beyond the single `--topo-depth`
   scale** — the spec's fuller vision (persistent world elements that
   visibly reshape, not just scale, across route boundaries) is
   represented here by one real, disclosed, additive channel layered
   onto the already-existing color/parallax system, not a full
   redesign of the backdrop — judged sufficient to demonstrate the
   principle without risking the already-verified color/parallax
   layers it sits beside.
7. Same disclosed gaps carried forward from H0.8 unchanged: no
   NVDA/VoiceOver manual pass (sandbox has none); the `?slowmo`
   debug-readout cosmetic artifact at extreme slowdown; the autofocus
   race-protection control remains a manual prototype-only debug
   button, not a real async data event.

## Founder decision requested

`STOP = TRUE`. `H1 = NOT_AUTHORIZED`. Waiting for:
- **APPROVE_DIRECTION** — proceed to extend the H1 integration plan with
  the physics/cadence/audio/haptic/topology architecture specifically.
- **REVISE_DIRECTION** — specify what to change; this file gets revised
  again, in place, without resetting.
- **REJECT_DIRECTION** — direction dropped; H0.8 (still intact at its own
  URL) stands as the ceiling.
