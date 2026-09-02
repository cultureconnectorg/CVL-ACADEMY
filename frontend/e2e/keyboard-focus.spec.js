const { test, expect } = require("@playwright/test");

// The public login form is the one accessibility-relevant surface reachable
// without a backend/DB in this sandbox (see e2e/README.md for why the 6
// inputs W1-A actually patched — Onboarding/AdminDashboard/TrainerDashboard/
// JuryDashboard/ModuleJourney — are all behind an authenticated user and
// out of reach here). This proves keyboard focus is visibly indicated on
// the entry point every unauthenticated user actually lands on.
test.describe("keyboard focus visibility (W1-E)", () => {
  test("the email field shows a visible focus ring on keyboard focus", async ({ page }) => {
    await page.goto("/");
    const email = page.getByTestId("auth-email");
    await email.focus();
    await expect(email).toBeFocused();

    const boxShadow = await email.evaluate((el) => getComputedStyle(el).boxShadow);
    expect(boxShadow).not.toBe("none");
  });

  test("the password field shows a visible focus ring on keyboard focus", async ({ page }) => {
    await page.goto("/");
    const password = page.getByTestId("auth-password");
    await password.focus();
    await expect(password).toBeFocused();

    const boxShadow = await password.evaluate((el) => getComputedStyle(el).boxShadow);
    expect(boxShadow).not.toBe("none");
  });

  test("tabbing through the auth form moves focus forward, never traps it", async ({ page }) => {
    await page.goto("/");
    await page.getByTestId("auth-email").focus();
    await page.keyboard.press("Tab");
    await expect(page.getByTestId("auth-password")).toBeFocused();
    await page.keyboard.press("Tab");
    await expect(page.getByTestId("auth-submit")).toBeFocused();
  });
});
