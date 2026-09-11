// Playwright config — W1-E regression baseline + portable CI browser.
const path = require("path");

const chromiumPath = process.env.PLAYWRIGHT_CHROMIUM_PATH;

module.exports = {
  testDir: "./e2e",
  timeout: 30_000,
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 1 : 0,
  reporter: [["list"]],
  use: {
    baseURL: "http://127.0.0.1:4173",
    trace: "retain-on-failure",
  },
  projects: [
    {
      name: "chromium",
      use: {
        // Local sandbox can keep using its preinstalled executable through
        // PLAYWRIGHT_CHROMIUM_PATH. GitHub Actions leaves this unset and uses
        // the browser installed by `npx playwright install chromium`.
        launchOptions: chromiumPath ? { executablePath: chromiumPath } : {},
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
      REACT_APP_BACKEND_URL: "http://127.0.0.1:4174",
    },
  },
};
