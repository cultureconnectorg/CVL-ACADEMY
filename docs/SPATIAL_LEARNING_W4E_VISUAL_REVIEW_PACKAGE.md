# W4-E — Visual Human Review Package — REPORT

```
Real runtime captures only — no invented mockups. Every image in the
linked gallery is a Playwright screenshot of the actual production
build running at a real git snapshot.
```

## Gallery

**→ [Spatial Learning Review](https://claude.ai/code/artifact/dfabd8ff-6c50-491a-b323-e8728be06bb1)** —
24 screenshots (4 surfaces × 3 snapshots × 2 viewports), click any
thumbnail to enlarge.

## Method

1. **Snapshots**: `git checkout <commit> -- frontend/src` overlaid each
   snapshot's page code into the current working tree, leaving
   `frontend/e2e/` (the test infra and fixtures) at HEAD — this is valid
   because the API contracts those fixtures mock never changed across
   W1–W3; only motion wrappers were added around existing data reads.
   Three snapshots: `before_w2 = 91cd54a` (last commit before any Spatial
   Learning UI was mounted), `after_w2 = 3f97807` (end of W2), `after_w3
   = 72b5f5b` (current HEAD, end of W3).
2. **Build**: `yarn build` + `serve -s build` for each snapshot — the
   real, minified, production bundle, not the dev server (same
   methodology as W4-B, for the same reason: representative, not noisy).
3. **Capture**: Playwright, full-page screenshots, at `1280×800`
   (desktop) and `390×844` (mobile). Authenticated surfaces (Formations,
   Roadmap, ModuleJourney) use the same test-only fixture as the
   committed E2E suite (`e2e/fixtures/auth-fixture.js`) — no real backend
   or production data.
4. **Restore**: `git checkout HEAD -- frontend/src`, then a full
   regression (`eslint`, 28 Jest unit tests, `yarn build`, 73 Playwright
   E2E tests) re-run clean. `main.js`'s build hash matched byte-for-byte
   before and after the whole exercise (`main.04470aea.js`), confirming
   the working tree was restored exactly, not approximately.
5. **Gallery**: a single self-contained HTML page (all 24 images
   embedded as base64, 4.2 MB total, no external image hosting), grouped
   by surface with a Before W2 / After W2 / After W3 column per surface
   and a one-line, evidence-based caption per capture (drawn from the
   actual commits, not from memory).

## What the gallery shows, surface by surface

- **Landing**: flat, no-motion state (Before W2) → FOCUS on the active
  language pill + ENTER crossfade on the register/login mode swap
  (After W2, unchanged in W3 — Landing wasn't touched again).
- **Formations**: plain grid with only a CSS `:hover` affordance
  (Before W2) → pole filter and cards wrapped in `FocusFieldItem`,
  target/secondary roles driven by real DOM focus (After W2, unchanged
  in W3).
- **Roadmap**: static cards showing the literal **"Level N"** badge on
  every stage (Before W2 *and* After W2 — Roadmap wasn't touched in W2
  at all) → "Level N" removed, current stage spatially foregrounded via
  `FocusFieldItem` (After W3, W3-D).
- **ModuleJourney**: flat phase list with the Mentor FAB always visible,
  on every screen (Before W2 *and* After W2 — ModuleJourney wasn't
  touched in W2 either) → full CURRENT/ACQUIRED/NEXT/LOCKED depth
  hierarchy on the phase stepper, Mentor now only appears on this one
  screen (After W3, W3-A/W3-C).

Two of the four surfaces (Roadmap, ModuleJourney) show **no visual
change between Before W2 and After W2** — an accurate reflection of
scope, not a capture error: neither screen was touched until W3.

## Regression check

`git status --porcelain` after the restore showed nothing — the
`frontend/src` overlay-and-restore cycle left zero trace in the tracked
tree. No file under this report was committed except this document and
the gallery link; the 24 source PNGs and the gallery's own HTML live
only in the published Artifact and this session's scratchpad, not in
the repository (screenshots are not appropriate to commit into a
production app's git history).
