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
const path = require("path");

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
        // Pinned local Chromium (see repo/sandbox docs) rather than a
        // Playwright-managed download — this sandbox pre-installs Chrome
        // for Testing under PLAYWRIGHT_BROWSERS_PATH and forbids
        // `playwright install` re-fetching a different revision.
        launchOptions: {
          executablePath:
            process.env.PLAYWRIGHT_CHROMIUM_PATH || "/opt/pw-browsers/chromium",
        },
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
