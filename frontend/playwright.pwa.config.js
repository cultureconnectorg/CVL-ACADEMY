const path = require("path");

module.exports = {
  testDir: "./e2e",
  testMatch: "pwa-offline.spec.js",
  timeout: 30_000,
  expect: { timeout: 15_000 },
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 1 : 0,
  reporter: [["list"]],
  use: {
    baseURL: "http://127.0.0.1:4180",
    trace: "retain-on-failure",
  },
  projects: [{ name: "chromium", use: {} }],
  webServer: {
    command: "node scripts/serve-build.js",
    cwd: path.resolve(__dirname),
    url: "http://127.0.0.1:4180",
    reuseExistingServer: false,
    timeout: 60_000,
    env: { PORT: "4180" },
  },
};
