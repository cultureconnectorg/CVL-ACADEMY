# W2-C — CVLN_FOCUS_FIELD v1 — REPORT

```
STATUS = IMPLEMENTED_NOT_INTEGRATED (same honest status W1-C's
         RouteTransition carried before W2-A mounted it)
```

Built as a reusable primitive, not mounted on any page in this tranche.
W2-D ("Formation discovery only") is the natural, already-authorized
place it gets applied to a real screen — building it there directly
without a standalone, independently-tested component first would have
made the discovery-screen change harder to review and the primitive
itself unreusable elsewhere.

## Behavior contract delivered

```
TARGET          -> APPROACH   (scale 1.03, y -4)
SECONDARY       -> RECEDE     (opacity 0.55, saturate 0.7 — never 0)
RELATED_CONTEXT -> REVEAL     (existing Reveal primitive, unchanged)
IDLE            -> CALM       (scale 1, y 0, opacity 1, saturate 1)
```

A field item is **one continuous `motion.div`** across all three roles —
not a nested swap between the standalone `Approach`/`Recede` components
from `motion-primitives.jsx` (W1-B), which are separate component types
and would unmount/remount on every role change, losing the animated
interpolation. `deriveFocusRole(id, focusedId)` is a pure function with
no React/motion dependency, so the field's core rule — "what role does
item X play given the current target" — is unit-tested directly, the
same pattern `spatial-state.js`/`.test.js` established in W1-D.

## Forbidden list — compliance, one line each

| Forbidden | How this file avoids it |
|---|---|
| `NO_GENERIC_SCALE_HOVER` | Role comes only from `focusedId` (click/keyboard selection via `useFocusField`); no `onMouseEnter`/`:hover` anywhere in the file |
| `NO_EXCESSIVE_CARDS` | Zero visual chrome of its own — no background/border/shadow; `className` is entirely the caller's |
| `NO_PILLS_AS_HIERARCHY` | Hierarchy is expressed only via the computed scale/opacity/saturation, never a badge/pill element |
| `NO_DECORATIVE_3D` | 2D transforms only (`scale`, `y`) — no `rotateX`/`rotateY`/`perspective` |
| `NO_PARTICLE_BACKGROUND` | No canvas, no particle system — DOM/CSS motion only |
| `NO_WEBGL` | Same — framer-motion over regular DOM elements |
| `NO_PLAYSTATION_COPY` | No menu chrome, icon carousel, or layout prescribed at all — purely behavioral, the caller supplies all visual design |

## REQ_ID table

| REQ_ID | BEFORE | CHANGE | FILES | RUNTIME_PROOF | TEST | PERF | A11Y | REGRESSION | STATUS |
|---|---|---|---|---|---|---|---|---|---|
| SL-FOCUSFIELD-01 (role derivation) | No reusable target/secondary/idle concept existed anywhere in the codebase | `deriveFocusRole(id, focusedId)` pure function + `FOCUS_FIELD_VARIANTS` frozen variant map | `frontend/src/lib/CvlnFocusField.jsx` | — (pure function, proven by unit test) | `CvlnFocusField.test.js`: IDLE/TARGET/SECONDARY correctness, "exactly one target, never two," variant shape (idle neutral, secondary never reaches 0 opacity, only target has a scale/position shift) — 7 tests | O(1) per item, no measurable cost | N/A (no DOM yet) | None — new file, zero imports | VERIFIED (logic) — DOM/motion behavior not yet runtime-proven, honestly, since nothing is mounted; that proof is W2-D's job once this is on a real screen |
| SL-FOCUSFIELD-02 (`FocusFieldItem`) | — | Thin `motion.div` wrapper consuming `deriveFocusRole` + the central motion tokens (APPROACH duration for target/idle, RECEDE duration for secondary, matching each role's own semantic pacing) | `CvlnFocusField.jsx` | — | Covered indirectly via the pure-function tests above; not yet mounted so no E2E | — | — | None — zero imports | IMPLEMENTED_NOT_INTEGRATED |
| SL-FOCUSFIELD-03 (`useFocusField`) | — | Minimal uncontrolled focus-state hook (`focusedId`, `focus(id)`, `clear()`) — no hover state exposed at all | `CvlnFocusField.jsx` | — | Not unit-tested in isolation (trivial `useState` wrapper); will be exercised via E2E once mounted in W2-D | — | — | None | IMPLEMENTED_NOT_INTEGRATED |
| SL-FOCUSFIELD-04 (`FocusFieldContext`) | — | Named wrapper over the existing `Reveal` primitive (W1-B), unchanged behavior, just a field-scoped name | `CvlnFocusField.jsx` | — | Inherits `Reveal`'s own existing correctness (no new logic added) | — | — | None | IMPLEMENTED_NOT_INTEGRATED |

## Test run (this tranche)

- `npx eslint src e2e playwright.config.js` → clean.
- `CI=true npx craco test --watchAll=false` → **13/13 Jest unit tests passing** (5 pre-existing `spatial-state.test.js` + 7 new `CvlnFocusField.test.js`).
- `CI=true yarn build` → compiled successfully, `main.js` gzip **unchanged at 167.81 kB** — confirms the new file is genuinely unimported anywhere yet.
- `npx playwright test` → **33/33 still passing**, unmodified — this tranche mounts nothing, so no new E2E coverage is expected or claimed here.

## Regression check

`git status --porcelain` before commit showed exactly 2 new files:
`CvlnFocusField.jsx` and `CvlnFocusField.test.js`. No existing file
touched, no backend/DB/FMS file touched.
