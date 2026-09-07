const { test, expect } = require("@playwright/test");
const { mockAuthenticatedSession } = require("./fixtures/auth-fixture");

// ACA-0022 — mobile global navigation. Below `md` the sidebar is
// `hidden`; before this, a signed-in visitor on a phone had literally
// no navigation besides browser back/forward. Proves the real fix:
// a fixed bottom tab bar for the 4 primary destinations, and a "More"
// sheet reaching every remaining STUDENT_NAV entry.
test.use({ viewport: { width: 390, height: 844 } });

test.describe("mobile navigation (ACA-0022)", () => {
  test("bottom tab bar renders the 4 primary destinations + More, sidebar stays hidden", async ({
    page,
  }) => {
    await mockAuthenticatedSession(page);
    await page.goto("/dashboard");

    await expect(page.getByTestId("sidebar")).toBeHidden();
    await expect(page.getByTestId("mobile-nav-bar")).toBeVisible();
    for (const key of ["dashboard", "roadmap", "formations", "missions"]) {
      await expect(page.getByTestId(`mobile-nav-${key}`)).toBeVisible();
    }
    await expect(page.getByTestId("mobile-nav-more")).toBeVisible();
  });

  test("tapping a primary tab navigates to the real route", async ({ page }) => {
    await mockAuthenticatedSession(page);
    await page.goto("/dashboard");
    await page.getByTestId("mobile-nav-formations").click();
    await expect(page).toHaveURL(/\/formations$/);
    await expect(page.getByTestId("formations-page")).toBeVisible();
  });

  test("More opens a sheet reaching the rest of the nav (badges/skills/certifications/wallet/frek-profile)", async ({
    page,
  }) => {
    await mockAuthenticatedSession(page);
    await page.goto("/dashboard");

    await page.getByTestId("mobile-nav-more").click();
    await expect(page.getByTestId("mobile-nav-sheet")).toBeVisible();
    for (const key of ["badges", "skills", "certifications", "wallet", "frek_profile"]) {
      await expect(page.getByTestId(`mobile-nav-sheet-${key}`)).toBeVisible();
    }
    await expect(page.getByTestId("logout-btn-mobile")).toBeVisible();
  });

  test("Escape closes the More sheet", async ({ page }) => {
    await mockAuthenticatedSession(page);
    await page.goto("/dashboard");
    await page.getByTestId("mobile-nav-more").click();
    await expect(page.getByTestId("mobile-nav-sheet")).toBeVisible();
    await page.keyboard.press("Escape");
    await expect(page.getByTestId("mobile-nav-sheet")).toBeHidden();
  });

  test("backdrop click closes the More sheet without navigating", async ({ page }) => {
    await mockAuthenticatedSession(page);
    await page.goto("/dashboard");
    await page.getByTestId("mobile-nav-more").click();
    await page.getByTestId("mobile-nav-sheet-backdrop").click({ position: { x: 10, y: 10 } });
    await expect(page.getByTestId("mobile-nav-sheet")).toBeHidden();
    await expect(page).toHaveURL(/\/dashboard$/);
  });

  test("a sheet link navigates and the sheet does not survive the navigation", async ({ page }) => {
    await mockAuthenticatedSession(page);
    await page.goto("/dashboard");
    await page.getByTestId("mobile-nav-more").click();
    await page.getByTestId("mobile-nav-sheet-badges").click();
    await expect(page).toHaveURL(/\/badges$/);
    await expect(page.getByTestId("mobile-nav-sheet")).toBeHidden();
  });
});
