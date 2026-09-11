const { test, expect } = require("@playwright/test");
const { mockAuthenticatedSession } = require("./fixtures/auth-fixture");

// ACA-0023 — exact client-side return context. A real browser POP must
// restore document scroll, named spatial rail position and the last
// stable focused Academy control for that history entry. A fresh
// PUSH/deep-link remains fresh. Rail assertions always use the browser-achieved
// position because scrollLeft is clamped to the element's real maximum.
test.use({ viewport: { width: 1280, height: 400 } });

test.describe("scroll, rail and focus restoration (ACA-0023)", () => {
  test("browser back restores the exact scroll position; forward navigation starts at the top", async ({
    page,
  }) => {
    await mockAuthenticatedSession(page);
    await page.goto("/dashboard");
    await page.waitForSelector('[data-testid="app-layout"]');

    await page.evaluate(() => window.scrollTo(0, 260));
    await expect.poll(() => page.evaluate(() => window.scrollY)).toBe(260);

    await page.getByTestId("nav-formations").click();
    await expect(page).toHaveURL(/\/formations$/);
    await expect.poll(() => page.evaluate(() => window.scrollY)).toBe(0);

    await page.evaluate(() => window.scrollTo(0, 90));
    await expect.poll(() => page.evaluate(() => window.scrollY)).toBe(90);

    await page.goBack();
    await expect(page).toHaveURL(/\/dashboard$/);
    await expect.poll(() => page.evaluate(() => window.scrollY)).toBe(260);

    await page.goForward();
    await expect(page).toHaveURL(/\/formations$/);
    await expect.poll(() => page.evaluate(() => window.scrollY)).toBe(90);
  });

  test("browser back restores the exact formation card that had focus before entering it", async ({
    page,
  }) => {
    await mockAuthenticatedSession(page);
    await page.goto("/formations");
    const card = page.getByTestId("formation-FMS-01");
    await expect(card).toBeVisible();
    await card.focus();
    await expect(card).toBeFocused();

    await card.click();
    await expect(page).toHaveURL(/\/formations\/FMS-01$/);

    await page.goBack();
    await expect(page).toHaveURL(/\/formations$/);
    await expect(page.getByTestId("formation-FMS-01")).toBeFocused();
  });

  test("browser back restores the roadmap spatial rail position", async ({ page }) => {
    await mockAuthenticatedSession(page, { user: { stade: "pousse" } });
    await page.goto("/roadmap");
    const rail = page.getByTestId("roadmap-scroll");
    await expect(rail).toBeVisible();

    const targetScrollLeft = await rail.evaluate((element) => {
      const maxScrollLeft = Math.max(0, element.scrollWidth - element.clientWidth);
      const target = Math.min(320, maxScrollLeft);
      element.scrollLeft = target;
      element.dispatchEvent(new Event("scroll", { bubbles: false }));
      return element.scrollLeft;
    });
    expect(targetScrollLeft).toBeGreaterThan(0);
    await expect.poll(() => rail.evaluate((element) => element.scrollLeft)).toBe(targetScrollLeft);

    await page.getByTestId("nav-formations").click();
    await expect(page).toHaveURL(/\/formations$/);

    await page.goBack();
    await expect(page).toHaveURL(/\/roadmap$/);
    await expect.poll(() => page.getByTestId("roadmap-scroll").evaluate((element) => element.scrollLeft)).toBe(targetScrollLeft);
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