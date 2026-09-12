const { test, expect } = require("@playwright/test");
const {
  mockAuthenticatedSession,
  FIXTURE_MODULE_QUIZ_READY,
} = require("./fixtures/auth-fixture");

const MODULE_URL = "/formations/FMS-01/modules/FMS-01-M01";

test.describe("Spatial context depth environment", () => {
  test("quiz context moves foreground content into depth and calms the persistent world", async ({ page }) => {
    await mockAuthenticatedSession(page, { moduleData: FIXTURE_MODULE_QUIZ_READY });
    await page.goto(MODULE_URL);
    await page.getByTestId("phase-toggle-quiz").click();
    await page.getByTestId("phase-quiz-open").click();

    const context = page.getByTestId("phase-quiz-questions").locator("..");
    await expect(context).toHaveAttribute("data-spatial-depth-role", "context-foreground");
    await expect(page.getByTestId("spatial-background")).toHaveAttribute("data-spatial-context", "active");
  });

  test("mentor return restores world, URL and exact invoking control", async ({ page }) => {
    await mockAuthenticatedSession(page);
    await page.goto(MODULE_URL);
    const fab = page.getByTestId("mentor-fab");
    await fab.click();
    await expect(page.getByTestId("spatial-background")).toHaveAttribute("data-spatial-context", "active");

    await page.getByTestId("mentor-close").click();
    await expect(page.getByTestId("spatial-background")).toHaveAttribute("data-spatial-context", "idle");
    await expect(page).toHaveURL(new RegExp(`${MODULE_URL}$`));
    await expect(fab).toBeFocused();
  });

  test("reduced motion preserves semantic context with no meaningful Z travel", async ({ page }) => {
    await mockAuthenticatedSession(page, { moduleData: FIXTURE_MODULE_QUIZ_READY });
    await page.emulateMedia({ reducedMotion: "reduce" });
    await page.goto(MODULE_URL);
    await page.getByTestId("phase-toggle-quiz").click();
    await page.getByTestId("phase-quiz-open").click();

    const context = page.getByTestId("phase-quiz-questions").locator("..");
    await expect(context).toHaveAttribute("data-spatial-depth-role", "context-foreground");
    await expect(page.getByTestId("spatial-background")).toHaveAttribute("data-spatial-motion", "reduced");
  });
});
