# ACA-0011 — Identity/FREK-ID Entry, Implementation Report

```
STATUS: implemented, flag-gated OFF by default
(REACT_APP_ACADEMY_SPATIAL_IDENTITY_ENTRY). Landing.js's register flow
renders exactly today's production behavior (toast + instant redirect)
until this flag is deliberately turned on.
```

## What this closes

No prior research doc exists for ACA-0011 specifically (unlike
ACA-0010's `ACADEMY_HERO_ENTRY_RESEARCH.md`); this pass grounds it in
the same sourced mechanism the Hero research already established and
cited as directly transferable — NFS/Autolog's lesson (research §1,
matrix row `SELECTION_CHANGES_THE_WORLD`): **a real action should
visibly change what the world says back**, not silently update a
database row behind a toast that can be missed and an instant redirect
that races it off-screen.

Today: `register()` succeeds → `toast.success(...)` fires → `nav(
"/onboarding")` fires in the same tick. The FREK-ID — the one durable,
real artifact this moment produces — is mentioned only inside a toast
string a visitor may not read before the page has already changed.

## What was built

`frontend/src/pages/Landing.js`:

- On a successful register, when `SPATIAL_IDENTITY_ENTRY` is on and
  reduced-motion is off: `newIdentity` state holds `{ frek_id }`, the
  auth card's `<Enter>`/form block is replaced by a `Confirm`-wrapped
  identity reveal (brand line → "FREK-ID generated" heading → the real
  `frek_id`, `mono`, at primary visual weight), then `nav("/onboarding")`
  fires after `IDENTITY_CONFIRM_BEAT` (900ms — restrained, MOT-008
  "calm by default," never a celebratory/blocking pause).
- The toast is kept, not replaced — the in-context reveal is the
  primary acknowledgment (research's "world talks back" mechanism);
  the toast remains a redundant, accessible fallback (screen readers,
  and any moment the visitor's attention was elsewhere).
- Off (flag disabled), reduced motion on, or the login path (re-entry,
  not a new identity — no such event to acknowledge): behavior is
  byte-identical to before — toast then immediate `nav`.
- `data-testid="identity-confirm"` / `"identity-frek-id"` added for
  future e2e coverage once this runs against a real backend.

## What was deliberately not built here

- No Camera Anchor Contract on this transition (`cameraFollow.js`,
  Rail 4) — that engine is scoped to same-page `SpatialHub` activation
  only today; wiring a real cross-component camera intent into this
  moment is ACA-0015 territory (porting camera-follow to real routes),
  not this task.
- No change to the login path — re-entering an existing identity is
  not the "new identity" event this research mechanism addresses.
- No backend change — `frek_id` is already real, already returned by
  `register()`; this pass only changes how it's surfaced.

## Verification

- `CI=true yarn build` — compiled successfully, zero new warnings.
- `npx eslint src/pages/Landing.js src/lib/featureFlags.js` — clean.
- Full relevant Playwright suite (31 tests) — **31/31 passed** at the
  flag's default (off), proving zero regression to auth usability,
  keyboard flow, and routing.
- The flag-on register-success path is not covered by a new e2e test:
  this sandbox has no backend (`register()` requires one), so the
  success branch was never reachable by the existing suite either,
  before or after this change — same disclosed limitation as
  `e2e/README.md` already states for every authenticated journey.

## Never claim

Not `FULLY_COMPLETE`. ACA-0012 (Onboarding spatialization), ACA-0015
(camera-follow ported to real routes), and this flag's own eventual
production activation with real e2e coverage against a live backend
all remain open, separate backlog items.
