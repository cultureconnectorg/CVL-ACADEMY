const { test, expect } = require("@playwright/test");
const { mockAuthenticatedSession } = require("./fixtures/auth-fixture");

test.describe("Spatial H0.8 focus memory", () => {
  test("formations autofocuses the real recommended formation without inventing state", async ({ page }) => {
    await mockAuthenticatedSession(page);
    await page.goto("/formations");
    await expect(page.getByTestId("formations-page")).toBeVisible();

    const nextHref = await page.getByTestId("next-action-cta").getAttribute("href");
    const match = nextHref.match(/^\/formations\/([^/]+)\/modules\//);
    expect(match).not.toBeNull();
    await expect(page.getByTestId(`formation-${match[1]}`)).toBeFocused();
  });

  test("browser Back restores the exact formation card that invoked navigation", async ({ page }) => {
    await mockAuthenticatedSession(page);
    await page.goto("/formations");
    const card = page.getByTestId("formation-FMS-01");
    await expect(card).toBeVisible();
    await card.focus();
    await expect(card).toBeFocused();
    await card.click();
    await expect(page.getByTestId("formation-detail")).toBeVisible();

    await page.goBack();
    await expect(page.getByTestId("formations-page")).toBeVisible();
    await expect(page.getByTestId("formation-FMS-01")).toBeFocused();
  });
});
