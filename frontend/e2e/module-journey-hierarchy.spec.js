const { test, expect } = require("@playwright/test");
const { mockAuthenticatedSession } = require("./fixtures/auth-fixture");

// W3-A — ModuleJourney spatial shell. The fixture module has a mixed
// state (hook: done + default-open, objectives: done, course: reachable
// frontier, workshop/deliverable/quiz/mini_mission: not yet reachable) so
// all four JourneyHierarchy roles are exercised in a single render — see
// e2e/fixtures/auth-fixture.js's FIXTURE_MODULE comment for the exact
// derivation.
test.describe("ModuleJourney spatial hierarchy (W3-A)", () => {
  test("AUTHENTICATED_ROUTE: the fixture session reaches the real module journey, not a redirect", async ({
    page,
  }) => {
    await mockAuthenticatedSession(page);
    await page.goto("/formations/FMS-01/modules/FMS-01-M01");
    await expect(page).toHaveURL(/\/formations\/FMS-01\/modules\/FMS-01-M01$/);
    await expect(page.getByTestId("module-journey")).toBeVisible();
  });

  test("hook is done AND the default open phase -> CURRENT wins over ACQUIRED", async ({
    page,
  }) => {
    await mockAuthenticatedSession(page);
    await page.goto("/formations/FMS-01/modules/FMS-01-M01");
    const hookWrapper = page.locator('[data-testid="phase-hook"]').locator("..");
    await expect(hookWrapper).toHaveAttribute("data-journey-role", "current");
  });

  test("objectives is done, not open -> ACQUIRED", async ({ page }) => {
    await mockAuthenticatedSession(page);
    await page.goto("/formations/FMS-01/modules/FMS-01-M01");
    const wrapper = page.locator('[data-testid="phase-objectives"]').locator("..");
    await expect(wrapper).toHaveAttribute("data-journey-role", "acquired");
  });

  test("course is the reachable frontier, not yet entered -> NEXT", async ({ page }) => {
    await mockAuthenticatedSession(page);
    await page.goto("/formations/FMS-01/modules/FMS-01-M01");
    const wrapper = page.locator('[data-testid="phase-course"]').locator("..");
    await expect(wrapper).toHaveAttribute("data-journey-role", "next");
  });

  test("workshop/deliverable/quiz/mini_mission are not yet reachable -> LOCKED", async ({
    page,
  }) => {
    await mockAuthenticatedSession(page);
    await page.goto("/formations/FMS-01/modules/FMS-01-M01");
    for (const key of ["workshop", "deliverable", "quiz", "mini_mission"]) {
      const wrapper = page.locator(`[data-testid="phase-${key}"]`).locator("..");
      await expect(wrapper).toHaveAttribute("data-journey-role", "locked");
    }
  });

  test("opening a different reachable phase re-derives roles live: course becomes CURRENT, hook becomes ACQUIRED", async ({
    page,
  }) => {
    await mockAuthenticatedSession(page);
    await page.goto("/formations/FMS-01/modules/FMS-01-M01");
    await page.getByTestId("phase-toggle-course").click();

    const courseWrapper = page.locator('[data-testid="phase-course"]').locator("..");
    const hookWrapper = page.locator('[data-testid="phase-hook"]').locator("..");
    await expect(courseWrapper).toHaveAttribute("data-journey-role", "current");
    await expect(hookWrapper).toHaveAttribute("data-journey-role", "acquired");
  });

  test("LOCKED phases stay disabled — hierarchy is visual only, the unlock rule is untouched", async ({
    page,
  }) => {
    await mockAuthenticatedSession(page);
    await page.goto("/formations/FMS-01/modules/FMS-01-M01");
    await expect(page.getByTestId("phase-toggle-workshop")).toBeDisabled();
  });

  test("REDUCED_MOTION: the CURRENT phase still settles at its foreground scale", async ({
    page,
  }) => {
    await mockAuthenticatedSession(page);
    await page.emulateMedia({ reducedMotion: "reduce" });
    await page.goto("/formations/FMS-01/modules/FMS-01-M01");
    const hookWrapper = page.locator('[data-testid="phase-hook"]').locator("..");
    await expect(hookWrapper).toHaveAttribute("data-journey-role", "current");
    const transform = await hookWrapper.evaluate((el) => getComputedStyle(el).transform);
    // CURRENT's scale (1.01) still applies a real transform, just settled
    // near-instantly under reduced motion.
    expect(transform).not.toBe("none");
  });

  test("PROGRESS_NOT_MUTATED_BY_ANIMATION: viewing the hierarchy sends zero mutating requests", async ({
    page,
  }) => {
    await mockAuthenticatedSession(page);
    const mutations = [];
    page.on("request", (req) => {
      if (["POST", "PUT", "PATCH", "DELETE"].includes(req.method()) && req.url().includes("/api/")) {
        mutations.push(`${req.method()} ${req.url()}`);
      }
    });
    await page.goto("/formations/FMS-01/modules/FMS-01-M01");
    await page.getByTestId("phase-toggle-course").click();
    await page.getByTestId("phase-toggle-objectives").click();
    expect(mutations).toEqual([]);
  });
});
