# ACA-0031 — Continuous End-to-End Regression Gate

```
STATUS: EXECUTED (2026-09-08). The frontend's real Playwright e2e
suite (86 specs) now runs in CI on every push/PR, alongside the
existing backend flake8+pytest and frontend build jobs. Its one
long-standing failure was root-caused and fixed — not worked around —
and the full suite is now genuinely 86/86.
```

## What this closes

Every prior report in this session's history — going back through W1-E,
every Rail/H1 report, ACA-0013 through ACA-0020 — carried the same
disclosed limitation: *"Playwright/e2e is not part of this repo's GitHub
Actions CI gate (only `backend` flake8+pytest and `frontend` build run
there)."* That was true and honestly stated at the time, but it meant a
real regression in routing, auth guards, keyboard behavior, or the
spatial engine's structural wiring could land on `main` with CI green.
`.github/workflows/ci.yml` now runs the full e2e suite as a third job.

## The real root cause behind the "pre-existing flake" (not worked around)

Every one of those same reports also carried a second disclosure:
`module-journey-navigation.spec.js`'s `BACK_FORWARD` test "fails
identically on the base commit... a confirmed pre-existing, unrelated
flake." That framing was wrong, and this pass proved it wrong rather
than repeating it: run in isolation with `--repeat-each=3`, the test
failed **3/3 times, deterministically** — not a flake at all.

The actual cause: `e2e/fixtures/auth-fixture.js`'s generic
`**/api/**` catch-all fulfills every unmocked request with `{}`. Four
real endpoints `FormationDetail.js` → `PhysicalSessionsPanel.js` calls
on mount (`/formations/{code}/physical-sessions`, `/physical-locations`,
`/physical-sessions/mine`, `/certifications/rubrics`,
`/certifications/attempts/mine`) were never given their own specific
mock — so `PhysicalSessionsPanel` received `{}` where the **real**
backend (`api/physical_sessions.py`, `api/certification.py` —
confirmed by reading their `response_model=List[...]` declarations)
always returns an array. `sessions.map is not a function` threw inside
that component; React's own error boundary caught it by unmounting the
entire `FormationDetail` tree — which is exactly why
`getByTestId("formation-detail")` (and, on the next step,
`module-journey`) never appeared. A real, deterministic fixture gap,
confirmed by direct DOM/console inspection against a live dev server
(`page.on("pageerror")` captured the exact `TypeError` and component
stack), not an ambient timing issue.

## What was built

### `frontend/e2e/fixtures/auth-fixture.js`
Five new specific routes added (mirroring the exact discipline the file
already uses for `/missions` and `/badges/mine` — "must be arrays, not
the generic `{}` fallback"): `**/api/formations/*/physical-sessions`,
`**/api/physical-locations`, `**/api/physical-sessions/mine`,
`**/api/certifications/rubrics`, `**/api/certifications/attempts/mine`
— all `[]`. No production code changed: `PhysicalSessionsPanel.js`
was already correct to assume an array, because that's the real
backend's own guaranteed contract; the fixture was the thing out of
sync with it.

### `.github/workflows/ci.yml`
New `e2e` job: checks out, installs deps (`yarn install
--frozen-lockfile`), installs Playwright's Chromium
(`npx playwright install --with-deps chromium` — GitHub's runner has no
pre-installed browser, unlike this sandbox), then `npx playwright test`
(which itself boots the `craco start` dev server per
`playwright.config.js`'s own `webServer` config — no new tooling
introduced). Runs alongside `backend`/`frontend`, not nested inside
either.

## Verification

- `npx playwright test e2e/module-journey-navigation.spec.js
  --repeat-each=3` — **12/12 passed** (was 0/3 on the BACK_FORWARD test
  before the fix, confirmed via a dedicated debug run capturing the
  exact `pageerror`).
- Full suite: `npx playwright test e2e/` — **86/86 passed.** This is
  the first 100% green run of this repo's entire e2e suite this
  session — every prior run carried the one now-fixed failure.
- `npx eslint e2e/fixtures/auth-fixture.js` — clean.
- `CI=true yarn build` — clean (unaffected by an e2e-fixture-only
  change, re-run for completeness).
- `python3 -c "import yaml; yaml.safe_load(open('.github/workflows/ci.yml'))"`
  — valid YAML (no GitHub Actions runner available in this sandbox to
  execute the workflow directly; the job's steps are the same
  `yarn install`/`npx playwright test` commands already verified to
  work locally, plus the standard `playwright install --with-deps`
  step from Playwright's own CI documentation).

## What remains open

- **Branch protection** ("Require status checks to pass before
  merging", naming `backend`/`frontend`/`e2e`) is a repository
  **Settings** change outside what a commit can do — same disclosed
  limitation `ci.yml`'s own original REL-01 comment already carried for
  the first two jobs, now extended to `e2e`. Flagged for the
  Founder/an org admin.
- **`backend_test.py`** stays excluded from the `pytest` CI step
  (`--ignore=tests/backend_test.py`, pre-existing, unrelated to this
  pass) — not investigated here.
- The `e2e` job's actual runtime on GitHub's shared runners (network/
  CPU characteristics differ from this sandbox) is unverified — the
  workflow is correct and each step independently proven, but the full
  job has not been observed to complete in Actions yet as of this
  report; the next CI run against this branch will be the first real
  signal.
