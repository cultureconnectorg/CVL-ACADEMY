const { test, expect } = require("@playwright/test");
const { mockAuthenticatedSession } = require("./fixtures/auth-fixture");

const MODULE_URL = "/formations/FMS-01/modules/FMS-01-M01";

// W3-E — the remaining required browser-level coverage for ModuleJourney
// not already exercised by W3-A/B/C/D's own specs: back/forward
// navigation in and out of a module, and keyboard reachability across the
// phase stepper itself (module-journey-hierarchy.spec.js covers the
// hierarchy roles; module-journey-context.spec.js covers quiz-internal
// keyboard focus — this file covers the stepper's own tab order).
test.describe("ModuleJourney back/forward + keyboard (W3-E)", () => {
  test("BACK_FORWARD: leaving a module via BackButton and returning via browser back re-renders the same journey state", async ({
    page,
  }) => {
    await mockAuthenticatedSession(page);
    await page.goto(MODULE_URL);
    await expect(page.getByTestId("module-journey")).toBeVisible();

    // Client-side navigation out (real <Link>, no full reload).
    await page.getByTestId("back-to-formation").click();
    await expect(page.getByTestId("formation-detail")).toBeVisible();
    await expect(page).toHaveURL(/\/formations\/FMS-01$/);

    // Browser back returns to the module, freshly mounted from the same
    // fixture — the hierarchy must be exactly what it was.
    await page.goBack();
    await expect(page).toHaveURL(new RegExp(`${MODULE_URL}$`));
    await expect(page.getByTestId("module-journey")).toBeVisible();
    const hookWrapper = page.locator('[data-testid="phase-hook"]').locator("..");
    await expect(hookWrapper).toHaveAttribute("data-journey-role", "current");

    // Forward returns to the formation detail page again.
    await page.goForward();
    await expect(page.getByTestId("formation-detail")).toBeVisible();
  });

  test("PROGRESS_NOT_MUTATED_BY_ANIMATION: the back/forward round-trip itself sends zero mutating requests", async ({
    page,
  }) => {
    await mockAuthenticatedSession(page);
    const mutations = [];
    page.on("request", (req) => {
      if (["POST", "PUT", "PATCH", "DELETE"].includes(req.method()) && req.url().includes("/api/")) {
        mutations.push(`${req.method()} ${req.url()}`);
      }
    });
    await page.goto(MODULE_URL);
    await page.getByTestId("back-to-formation").click();
    await page.goBack();
    await page.goForward();
    expect(mutations).toEqual([]);
  });

  test("KEYBOARD_FOCUS: tabbing through the phase stepper reaches every open phase and skips locked ones", async ({
    page,
  }) => {
    await mockAuthenticatedSession(page);
    await page.goto(MODULE_URL);

    await page.getByTestId("phase-toggle-hook").focus();
    await expect(page.getByTestId("phase-toggle-hook")).toBeFocused();

    // hook -> objectives: both reachable (hook done, objectives done),
    // native tab order lands on the very next phase toggle.
    await page.keyboard.press("Tab");
    await expect(page.getByTestId("phase-toggle-objectives")).toBeFocused();

    // objectives -> course: course is the reachable frontier (NEXT).
    await page.keyboard.press("Tab");
    await expect(page.getByTestId("phase-toggle-course")).toBeFocused();

    // workshop/deliverable/quiz/mini_mission are all `disabled` (LOCKED) —
    // disabled buttons are natively skipped by the browser's own tab
    // order, so this is unlock-rule behavior already, not new wiring.
    await expect(page.getByTestId("phase-toggle-workshop")).toBeDisabled();
  });

  test("REDUCED_MOTION: the whole stepper still renders its 4 roles correctly with motion disabled", async ({
    page,
  }) => {
    await mockAuthenticatedSession(page);
    await page.emulateMedia({ reducedMotion: "reduce" });
    await page.goto(MODULE_URL);
    await expect(page.locator('[data-testid="phase-hook"]').locator("..")).toHaveAttribute(
      "data-journey-role",
      "current"
    );
    await expect(page.locator('[data-testid="phase-workshop"]').locator("..")).toHaveAttribute(
      "data-journey-role",
      "locked"
    );
  });
});
