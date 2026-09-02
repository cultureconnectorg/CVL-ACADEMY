const { test, expect } = require("@playwright/test");

test.describe("routing safety (W1-E)", () => {
  test("canonical root URL renders the landing page", async ({ page }) => {
    await page.goto("/");
    await expect(page).toHaveURL(/\/$/);
    await expect(page.getByTestId("landing-page")).toBeVisible();
  });

  test("an unknown deep link redirects to / (catch-all route)", async ({ page }) => {
    await page.goto("/this-route-does-not-exist");
    await expect(page).toHaveURL(/\/$/);
    await expect(page.getByTestId("landing-page")).toBeVisible();
  });

  test("a hard refresh on / re-renders the same page, no crash", async ({ page }) => {
    await page.goto("/");
    await expect(page.getByTestId("landing-page")).toBeVisible();
    await page.reload();
    await expect(page.getByTestId("landing-page")).toBeVisible();
  });

  test("browser back returns to the previous canonical URL", async ({ page }) => {
    await page.goto("/");
    await page.goto("/this-route-does-not-exist"); // redirects to / but pushes its own history entry first
    await expect(page).toHaveURL(/\/$/);
    await page.goBack();
    // Both entries resolve to "/" content-wise (redirect target), but the
    // navigation itself must not throw / leave the app in a blank state.
    await expect(page.getByTestId("landing-page")).toBeVisible();
  });
});
