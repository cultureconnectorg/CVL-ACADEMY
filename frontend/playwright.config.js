// Playwright config — W1-E regression baseline.
//
// Scope, honestly stated: this sandbox has no running MongoDB and no
// backend process available (confirmed: no `mongod`/`docker` daemon, see
// the W1-E tranche report). So these specs cover only the journeys that
// are provably correct against the frontend alone — unauthenticated
// routing/auth-guard/keyboard/reduced-motion behavior, which is exactly
// what AuthProvider (frontend/src/lib/auth.jsx) resolves synchronously
// from `localStorage` with zero network call when no token is present.
// Authenticated journeys (login, ModuleJourney, quiz, certification —
// anything needing the backend + MongoDB) are out of reach in this
// sandbox and are NOT claimed as tested here; see e2e/README.md.
//
// `webServer` boots the existing CRA/craco dev server (no new tooling
// dependency beyond @playwright/test itself) on a dedicated port so it
// never collides with a developer's own `yarn start` on 3000.
const fs = require("fs");
const path = require("path");

// ACA-0031 — the pinned sandbox path below is real for the dev sandbox
// this config was originally written in (Chrome for Testing pre-
// installed under PLAYWRIGHT_BROWSERS_PATH, `playwright install`
// forbidden from re-fetching a different revision there) but does NOT
// exist on a GitHub Actions runner, where the new `e2e` CI job (see
// .github/workflows/ci.yml) instead runs `npx playwright install
// --with-deps chromium` to fetch Playwright's own managed browser.
// Hardcoding the sandbox path unconditionally broke that job outright
// ("Failed to launch chromium because executable doesn't exist at
// /opt/pw-browsers/chromium" — every one of the 86 specs failed the
// same way, confirmed via the job's own logs). Only pin the explicit
// path when it's real on this machine; otherwise leave
// `executablePath` undefined so Playwright resolves its own installed
// browser, exactly what `playwright install` puts there.
const SANDBOX_CHROMIUM_PATH = "/opt/pw-browsers/chromium";
const explicitChromiumPath =
  process.env.PLAYWRIGHT_CHROMIUM_PATH ||
  (fs.existsSync(SANDBOX_CHROMIUM_PATH) ? SANDBOX_CHROMIUM_PATH : undefined);

module.exports = {
  testDir: "./e2e",
  timeout: 30_000,
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: 0,
  reporter: [["list"]],
  use: {
    baseURL: "http://127.0.0.1:4173",
    trace: "retain-on-failure",
  },
  projects: [
    {
      name: "chromium",
      use: {
        launchOptions: explicitChromiumPath
          ? { executablePath: explicitChromiumPath }
          : {},
      },
    },
  ],
  webServer: {
    command: "npx craco start",
    cwd: path.resolve(__dirname),
    url: "http://127.0.0.1:4173",
    reuseExistingServer: !process.env.CI,
    timeout: 120_000,
    env: {
      PORT: "4173",
      BROWSER: "none",
      // Deliberately unreachable — no backend is available in this
      // sandbox. Every API call the app makes on these unauthenticated
      // pages fails fast and is already caught (see auth.jsx / api.js),
      // so the pages under test still render deterministically without
      // one; pointing at a real nothing-here port instead of leaving
      // this unset keeps that failure fast and explicit.
      REACT_APP_BACKEND_URL: "http://127.0.0.1:4174",
    },
  },
};
