const { test, expect } = require("@playwright/test");
const { mockAuthenticatedSession } = require("./fixtures/auth-fixture");

// ACA-0023 (scroll slice) — a real browser back/forward restores where
// the user was scrolled to; a fresh navigation always lands at the top.
// A short viewport forces every route to be scrollable regardless of
// how much fixture content it renders.
test.use({ viewport: { width: 1280, height: 400 } });

test.describe("scroll restoration (ACA-0023)", () => {
  test("browser back restores the exact scroll position; forward navigation starts at the top", async ({
    page,
  }) => {
    await mockAuthenticatedSession(page);
    await page.goto("/dashboard");
    await page.waitForSelector('[data-testid="app-layout"]');

    await page.evaluate(() => window.scrollTo(0, 260));
    await expect.poll(() => page.evaluate(() => window.scrollY)).toBe(260);

    // A real forward navigation (Link click, PUSH) — must start at top,
    // never inherit the previous page's scroll position.
    await page.getByTestId("nav-formations").click();
    await expect(page).toHaveURL(/\/formations$/);
    await expect.poll(() => page.evaluate(() => window.scrollY)).toBe(0);

    await page.evaluate(() => window.scrollTo(0, 90));
    await expect.poll(() => page.evaluate(() => window.scrollY)).toBe(90);

    // Real browser back (POP) to /dashboard — must restore the exact
    // position scrolled to before leaving, not reset to 0.
    await page.goBack();
    await expect(page).toHaveURL(/\/dashboard$/);
    await expect.poll(() => page.evaluate(() => window.scrollY)).toBe(260);

    // Real browser forward (POP) back to /formations — must restore
    // that page's own remembered position too.
    await page.goForward();
    await expect(page).toHaveURL(/\/formations$/);
    await expect.poll(() => page.evaluate(() => window.scrollY)).toBe(90);
  });

  test("a fresh deep link to a route never previously scrolled starts at the top", async ({
    page,
  }) => {
    await mockAuthenticatedSession(page);
    await page.goto("/dashboard");
    await page.waitForSelector('[data-testid="app-layout"]');
    await expect.poll(() => page.evaluate(() => window.scrollY)).toBe(0);
  });
});
