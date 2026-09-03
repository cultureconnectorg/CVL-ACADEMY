# H0.8 — Camera-Follow Transitions + Autofocus Engine — REPORT

```
STOP = TRUE
H1 = NOT_AUTHORIZED
DO_NOT_RESET honored: H0.7 (spatial-console-h07.html) is untouched at its
own URL, kept as the reference/rollback point. This iteration lives in a
new file (spatial-console-h08.html), same lineage, additive only.
Nothing in frontend/src, backend/, or the database was touched.
git status --porcelain on the repo is empty after this work (only docs).
```

## Deliverables

- **Prototype (interactive)**: [Spatial Console — H0.8](https://claude.ai/code/artifact/5ecce21c-efb8-4bb6-9b7c-cca0a45639a5) — `spatial-console-h08.html`, scratchpad only, never committed.
- **Frame-sequence proof** (0/20/40/60/80/100%, both directions): [Camera-Follow Frame Sequence](https://claude.ai/code/artifact/4e239d00-09ed-48e4-8eae-a5bae33f3f0f)
- **H0.7 base, preserved as-is**: [Spatial Console — Camera Iteration](https://claude.ai/code/artifact/98782933-48c0-4c4e-b429-6bafe4201aec)
- This report.

## What was added (delta vs. H0.7)

**1. Camera Anchor Contract** — a real typed object (`makeAnchorContract()`) carrying `anchor_id / source_route / destination_route / source_rect / destination_rect / camera_from / camera_target / camera_origin_from / camera_origin_target / depth_from / depth_target / entry_path / return_path / reduced_motion_fallback`, built for every camera-follow transition rather than each route improvising its own behavior.

**2. Generic `cameraFollowTransition()`** replacing the one-off `flipHeroTransition()` from H0.6/H0.7. It now drives **two** camera objects together: the cloned anchor text (the visible thread across the route boundary, as before) **and**, new in H0.8, `main.stage`'s own `perspective-origin` — the one DOM node that survives every route swap, since only `.view` children's `data-current` toggles. The camera locks to the source anchor's screen position *before* anything moves, then pans on to the destination anchor's position once it mounts — never reset to a canonical default between the two (`CAMERA_RESET_BETWEEN_ROUTES = FORBIDDEN`, verified: the same `perspective-origin` value carries continuously from lock to pan, no snap to 50% in between).

**3. Camera transition state machine** — `IDLE → INTENT → LOCKING → FOLLOWING → CROSSING → REVEALING → SETTLING`, plus `RETURNING` for the inverse. A `cameraToken` counter implements retarget/cancel: every step checks `myToken === cameraToken` before proceeding, so a newer transition silently supersedes an older one in flight (`LATEST_USER_INTENT_WINS`, verified by interrupting a transition mid-flight with a new navigation — no error, no visual artifact, no queued backlog). This orchestrates the *same* motion vocabulary already in place (FOCUS/APPROACH/RECEDE/REVEAL/RETURN) — it is not a second system.

**4. Three real camera anchors into Module**, each a new *interaction* on already-displayed data (not a new business feature — no new routes, no new pedagogy, no invented "M02" concept the current data model doesn't have):
   - Hub "Continuer" tile → Module (upgraded from H0.6/H0.7's flip).
   - Roadmap's **current** stage card → Module (new: the card is now clickable/`Enter`-able, with a "Entrer dans le module →" affordance that only appears on the current stage).
   - Formations' **target** card, on a second click/Enter (mirroring the Hub tile's focus-then-activate pattern) → Module.

**5. Return path**, both ways: an explicit **"← Retour…"** link on the Module view (label adapts to which anchor was used: accueil/feuille de route/formations) *and* the browser Back button — both drive the same `cameraReturnTransition()`, which re-resolves the returning anchor fresh in its new context rather than assuming stale coordinates, then hands focus back to it exactly.

**6. Focus / Autofocus Engine** (spec §40-68) — `focusState {focusedObjectId, focusedRoute, focusedIndex, focusOrigin, focusReason}` as the single source of truth, distinct from `document.activeElement` (DOM_FOCUS) and the camera state machine (CAMERA_FOCUS):
   - Route-entry priority chain: restored previous focus → the learner's actual current domain object (`RECOMMENDED_FORMATION_ID`, the formation the in-progress module belongs to) → first valid fallback. Never `FORMATIONS[0]` blindly — it happens to resolve to index 0 in this illustrative data, disclosed as coincidence, not the reason.
   - **Real, testable async race protection** — not just documented prose. A manual "⟲ tester race autofocus" debug control (bottom-right, prototype-only) fires a genuinely delayed (800ms) synthetic background recommendation. Verified both ways this session: with no interaction, it applies; with an explicit keyboard choice made after the request but before it resolves, it is discarded (`lastExplicitIntentAt > requestedAt` check) — confirmed via the visible focus-state debug readout, not assumed.
   - `focusRequestId` counter discards any request superseded by a newer one (`STALE_AUTOFOCUS_REQUEST = DISCARD`).
   - **PREFOCUS**: hover on a rail tile applies a subtle `data-prefocus` filter cue only — never changes route, never steals keyboard focus (verified: `pointerover`/`pointerout` handlers touch only a CSS attribute).
   - **Smart, non-forcing centering**: `centerInRail()` now only repositions the rail if the newly-focused tile has actually left a 38–58% focal zone — `AUTOFOCUS != ALWAYS_CENTER`, composition is preserved when the change is small.
   - **Dwell-gated screen-reader announcements**: rail-focus announcements (already dwell-gated for visual reveal in H0.6) now also gate the `aria-live` text itself — rapid →→→→ traversal no longer fires an announcement per keystroke, only once focus settles.
   - **Context autofocus**: opening Quiz/Mission/Mentor/Proof focuses the first meaningful control (e.g. the first quiz radio) when one exists, falling back to the dock's own heading — not reflexively the close button as in H0.6/H0.7.
   - **Real focus trap** while a context is open: Tab/Shift+Tab cycles within the dock only, released to the exact opener on close (unchanged, already-proven mechanism).
   - **Mobile continuous camera during drag**: `perspective-origin` now tracks live finger position every `pointermove`, not only after release — depth-role recomputation still commits at release only (disclosed scope limit: per-pixel scale/adjacent-approach during drag is not implemented, only the camera pan is continuous).

**7. Focus Memory extended**: `depthMemory` now also stores each rail's `scrollLeft` (`railOffset`) alongside the focused id, restored together on return — not DOM-focus-only.

**8. Deterministic proof-capture hook**: `?slowmo=N` multiplies every CSS motion token and the two JS-driven `clone.animate()` durations by N, letting Playwright capture reliable intermediate frames of a 420ms transition instead of guessing a wait time. Used to produce the frame-sequence gallery linked above. Default behavior (no query param) is completely untouched.

## Two real bugs found and fixed during this session's own verification

Both caught by the automated `window.scrollY` check that has been part of this verification battery since the H0.6 pass — not by visual inspection.

**1. `<html>` lacked its own `overflow:hidden`.** Only `<body>` had it. Once the Module view's content (8 phase rows) grew taller than the viewport, the outer document scrolled regardless of `body`'s setting — a **latent bug present since H0.6/H0.7** that simply hadn't been exercised by a tall-enough view in prior verification passes (confirmed by reproducing the identical issue, ~144px, on the untouched H0.7 file). Root-caused and fixed at the source: `html, body { overflow: hidden; }`.

**2. Native click-focus on a context-opening button** (e.g. `#phase-quiz`) stayed focused while its ancestor (the Module view) received the new, deeper recede transform — this is real, browser-native "keep the focused element in view" behavior reacting to the element's geometry changing under a `translateZ`'d ancestor, unrelated to any `.focus()` call of mine (confirmed: the scroll event's `document.activeElement` at the moment of firing was the invoking `<button>`, not any element my own code had touched yet). Fixed by blurring `document.activeElement` at the very start of `enterContext()`, before the recede transform is applied — the dock's own focus lands correctly a moment later via the existing `requestAnimationFrame` call.

## Transition Matrix

| Transition | Anchor | Camera continuity | Verified this session |
|---|---|---|---|
| Hub "Continuer" → Module | `hub-continue` (tile title) | Full: lock → pan → settle | ✅ scroll-clean, back-link correct, browser Back correct |
| Roadmap current stage → Module | `roadmap-current` (stage name) | Full: lock → pan → settle | ✅ scroll-clean, back-link correct, browser Back correct, **frame-sequence proof captured (0-100%, both directions)** |
| Formations target card → Module | `formation-target` (card `h3`) | Full: lock → pan → settle | ✅ scroll-clean, back-link correct |
| Module → its origin (explicit "← Retour" link) | reverses the entry anchor | Full: lock → pan → settle | ✅ all three origins produce the correct label and land correctly |
| Module → its origin (browser Back) | reverses the entry anchor | Full: lock → pan → settle | ✅ `popstate` correctly routes through `cameraReturnTransition`, `pushHistory:false` (verified the history stack isn't corrupted — Back then Forward round-trips correctly) |
| Any rapid re-navigation mid-transition | n/a | Retargeted, not queued | ✅ interrupted a Hub→Module flight 50ms in with a direct hash jump elsewhere — no error, no orphaned clone |
| Hub/Formations/Roadmap ↔ Missions/Badges/FREK | none | Crossfade only (unchanged from H0.6/H0.7) | not re-verified this pass — no code touched these paths |
| Formations → Roadmap, or any pair not listed above | — | **Not implemented** | **Deferred, disclosed** — this pairing does not exist as a real route in this prototype's IA (Formations is a catalog, Roadmap is stage-based; they're siblings, not parent/child, in the real app too). Inventing that navigation would be a new business/IA feature, forbidden by this iteration's own scope. |

## Performance & accessibility observations

No `pageerror` events across the full battery (rail navigation, all 3 forward anchors, both return paths — explicit link and browser Back — mid-flight interruption, all 4 context types × open/close, reduced motion toggle, mobile drag, autofocus race in both outcomes). No new `requestAnimationFrame` loop — every camera step is either a discrete `element.style` write in response to an input event or a single `element.animate()` call; the token-check pattern is what makes retargeting instant rather than a real animation-cancel API call, and this was sufficient (no visual snapping observed). Focus trap and context-autofocus verified via `document.activeElement` inspection, not just visual review. Not measured this session (same disclosed gap as prior reports): real FPS/CLS/LCP trace.

## Known gaps (disclosed, not silently dropped)

1. Formations→Module and Roadmap→Module now have full camera-follow; **Formations→Roadmap is not a real transition in this prototype's IA** and was not invented.
2. Mobile drag drives the camera (`perspective-origin`) continuously, but depth-role recompute (scale/adjacent-approach) still commits only at release — a partial implementation of "MOBILE DRAG MUST DRIVE CAMERA CONTINUOUSLY," disclosed rather than overclaimed.
3. The `?slowmo` debug readout can show a stale camera-state label for the final ~1 settle-buffer step when heavily slowed down (the two short post-animation `setTimeout` buffers are not themselves scaled by the slowmo multiplier) — a cosmetic artifact of the proof-capture harness only, not present at real (1×) speed.
4. No screen-reader (NVDA/VoiceOver) manual pass — this sandbox has none available; the dwell-gating and focus-trap logic were verified structurally (DOM/attribute inspection), not by ear.
5. The autofocus race-protection control is a manual prototype-only debug button, not a real background data event — deliberately, since an *automatic* timer-driven focus jump even 800ms after idle would itself risk violating `CALM_BY_DEFAULT` during casual review; a real H1 implementation would trigger it from an actual async event (e.g. a data refresh), not a timer.

## Founder decision requested

`STOP = TRUE`. `H1 = NOT_AUTHORIZED`. Per the acceptance tests in the brief:
- `CAMERA_FOLLOW_TRANSITION`, `AUTOFOCUS_ENGINE`, `FOCUS_MEMORY`, `RETARGETING`, `RETURN_CAMERA_PATH` — all proven this session, per the table and race-protection results above.

Waiting for:
- **APPROVE_DIRECTION** — proceed to plan H1 integration, extending `docs/SPATIAL_H1_INTEGRATION_PLAN.md` with this camera/autofocus engine specifically.
- **REVISE_DIRECTION** — specify what to change; this file gets revised again, in place, without resetting.
- **REJECT_DIRECTION** — direction dropped; H0.7 (still intact at its own URL) stands as the ceiling.
