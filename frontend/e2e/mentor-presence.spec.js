const { test, expect } = require("@playwright/test");
const { mockAuthenticatedSession } = require("./fixtures/auth-fixture");

const MODULE_URL = "/formations/FMS-01/modules/FMS-01-M01";

// W3-C — MENTOR = CONTEXTUAL_PRESENCE. The FAB/panel must never render on
// every authenticated screen (MENTOR_ALWAYS_VISIBLE = FORBIDDEN) — only
// where mentorPresence.js's isPedagogicalContext() says a pedagogical
// context justifies it (currently: inside a module only, deliberately
// conservative — see that file's own header for the scope decision).
test.describe("mentor contextual presence (W3-C)", () => {
  test("absent on the dashboard", async ({ page }) => {
    await mockAuthenticatedSession(page);
    await page.goto("/dashboard");
    await expect(page.getByTestId("dashboard-page")).toBeVisible();
    await expect(page.getByTestId("mentor-fab")).toHaveCount(0);
    await expect(page.getByTestId("mentor-panel")).toHaveCount(0);
  });

  test("absent on formation discovery (catalogue browsing is not mid-lesson)", async ({
    page,
  }) => {
    await mockAuthenticatedSession(page);
    await page.goto("/formations");
    await expect(page.getByTestId("formations-page")).toBeVisible();
    await expect(page.getByTestId("mentor-fab")).toHaveCount(0);
  });

  test("present inside an actual module", async ({ page }) => {
    await mockAuthenticatedSession(page);
    await page.goto(MODULE_URL);
    await expect(page.getByTestId("module-journey")).toBeVisible();
    await expect(page.getByTestId("mentor-fab")).toBeVisible();
  });

  test("navigating out of a module (client-side) removes the FAB again", async ({ page }) => {
    await mockAuthenticatedSession(page);
    await page.goto(MODULE_URL);
    await expect(page.getByTestId("mentor-fab")).toBeVisible();

    // Back to the formation (client-side <Link>, exercised the same way
    // BackButton does it) — a real in-app navigation, not a fresh goto.
    await page.getByTestId("back-to-formation").click();
    await expect(page.getByTestId("mentor-fab")).toHaveCount(0);
  });

  test("MENTOR_BLOCKS_CONTENT respected: the FAB never obstructs the phase stepper while closed", async ({
    page,
  }) => {
    await mockAuthenticatedSession(page);
    await page.goto(MODULE_URL);
    await expect(page.getByTestId("mentor-fab")).toBeVisible();
    // Every phase's toggle button is still clickable/enabled per its own
    // canOpen rule (hook is always openable) — the FAB's presence in the
    // corner doesn't intercept clicks meant for the stepper.
    await page.getByTestId("phase-toggle-objectives").click();
    await expect(page.getByTestId("phase-objectives")).toHaveClass(/ring-2/);
  });
});
