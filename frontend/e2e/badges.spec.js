const { test, expect } = require("@playwright/test");
const { mockAuthenticatedSession } = require("./fixtures/auth-fixture");

// Real content coverage for /badges — previously missing entirely.
// mobile-nav.spec.js's "a sheet link navigates" test reaches this
// route but only asserts on the URL, never on the page actually
// rendering; that gap let a 100%-reproducible crash
// (`all.findIndex is not a function`, from the catalogue fetch
// falling through to auth-fixture.js's generic `{}` mock) go
// undetected by all 92 other e2e specs. Found by manually driving the
// real dev server, not by an existing test — this file closes that
// gap for real, not just the one fixture mock that fixed it.
test.describe("badges (ACA-0014/ACA-0017 spatial depth cards)", () => {
  test("AUTHENTICATED_ROUTE: the real catalogue + earned badges render, not a redirect or a crash", async ({
    page,
  }) => {
    await mockAuthenticatedSession(page);
    await page.goto("/badges");
    await expect(page).toHaveURL(/\/badges$/);
    await expect(page.getByTestId("badges-page")).toBeVisible();
    await expect(page.getByTestId("badge-B10")).toBeVisible();
    await expect(page.getByTestId("badge-B50")).toBeVisible();
  });

  test("an earned badge shows the obtained marker; an unearned one does not", async ({
    page,
  }) => {
    await mockAuthenticatedSession(page);
    await page.route("**/api/badges/mine", (route) =>
      route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify([
          { code: "B10", name: "Première étincelle", earned_at: "2026-01-01T00:00:00Z" },
        ]),
      })
    );
    await page.goto("/badges");
    await expect(page.getByTestId("badge-B10")).toContainText("Obtenu");
    await expect(page.getByTestId("badge-B50")).not.toContainText("Obtenu");
  });

  test("PROGRESS_NOT_MUTATED_BY_ANIMATION: viewing the catalogue sends zero mutating requests", async ({
    page,
  }) => {
    await mockAuthenticatedSession(page);
    const mutations = [];
    page.on("request", (req) => {
      if (["POST", "PUT", "PATCH", "DELETE"].includes(req.method()) && req.url().includes("/api/")) {
        mutations.push(`${req.method()} ${req.url()}`);
      }
    });
    await page.goto("/badges");
    await expect(page.getByTestId("badges-page")).toBeVisible();
    expect(mutations).toEqual([]);
  });

  test("REDUCED_MOTION: an earned badge still settles at full opacity", async ({ page }) => {
    // Deliberately mocks B10 as earned here -- an *unearned* badge is
    // correctly dimmed to 0.7 opacity by design (locked/not-yet-earned
    // is a real signal, independent of reduced-motion), so asserting
    // full opacity only makes sense against an earned one.
    await mockAuthenticatedSession(page);
    await page.route("**/api/badges/mine", (route) =>
      route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify([
          { code: "B10", name: "Première étincelle", earned_at: "2026-01-01T00:00:00Z" },
        ]),
      })
    );
    await page.emulateMedia({ reducedMotion: "reduce" });
    await page.goto("/badges");
    await expect(page.getByTestId("badge-B10")).toBeVisible();
    const opacity = await page
      .getByTestId("badge-B10")
      .evaluate((el) => getComputedStyle(el).opacity);
    expect(opacity).toBe("1");
  });
});
