# W1-E — Regression E2E baseline

Playwright specs proving the W1-A→D changes didn't regress the app.
`npx playwright test` (from `frontend/`) boots the existing CRA/craco dev
server on `:4173` and runs everything headless against the pinned local
Chromium at `/opt/pw-browsers/chromium` (see `playwright.config.js`).

## Honest scope

This sandbox has **no running MongoDB and no backend process** (no
`mongod`, no reachable Docker daemon — verified before writing these
specs). So these specs cover exactly what's provably correct against the
frontend alone:

- `routing.spec.js` — canonical URLs, deep links to an unknown path,
  hard refresh.
- `auth-guards.spec.js` — every `<Protected>` route (see `src/App.js`)
  redirects an unauthenticated visitor to `/`, for a direct deep link.
- `reduced-motion.spec.js` — the `prefers-reduced-motion` CSS rule added
  in W1-A (`src/index.css`) actually collapses `animation-duration` when
  the OS preference is emulated on.
- `keyboard-focus.spec.js` — the public login form's inputs show a
  visible focus ring on keyboard focus (`box-shadow` is not `none`).

This works because `AuthProvider` (`src/lib/auth.jsx`) resolves
`user`/`loading` synchronously from `localStorage` with **zero network
call** when no token is stored — every page under test here renders
deterministically without a backend.

## What is NOT covered here, and why

Authenticated journeys — login, Onboarding, ModuleJourney, quiz,
certifications, the 6 specific inputs W1-A actually patched (they live on
`Onboarding`/`AdminDashboard`/`TrainerDashboard`/`JuryDashboard`/
`ModuleJourney`, all of which require a real logged-in user) — need a
running backend + MongoDB, which this sandbox does not have. Their
correctness for this wave is established by code inspection + the eslint/
build/unit-test proof already reported for W1-A through W1-D, not by an
E2E pass claimed here. Wiring these specs up against a real backend+DB
(e.g. in CI) is the natural next step once that environment exists — this
file is the place to extend from, not a finished, exhaustive suite.
