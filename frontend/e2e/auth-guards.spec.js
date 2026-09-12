const { test, expect } = require("@playwright/test");

// Internal-only paths must still redirect anonymous visitors to the landing page.
const PROTECTED_PATHS = [
  "/dashboard",
  "/formations/FMS-01/modules/FMS-01-M01",
  "/trainer",
  "/jury",
  "/admin",
  "/admin/stakeholders",
  "/partner",
  "/institution",
  "/stakeholder/claim/example-code",
];

// Hybrid discovery paths intentionally remain addressable without authentication.
const PUBLIC_DISCOVERY_PATHS = [
  "/roadmap",
  "/formations",
  "/formations/FMS-01",
  "/missions",
  "/badges",
  "/frek-profile",
  "/wallet",
  "/skills",
  "/certifications",
];

test.describe("auth guards (W1-E)", () => {
  for (const path of PROTECTED_PATHS) {
    test(`unauthenticated deep link to ${path} redirects to /`, async ({ page }) => {
      await page.goto(path);
      await expect(page).toHaveURL(/\/$/);
      await expect(page.getByTestId("landing-page")).toBeVisible();
    });
  }

  for (const path of PUBLIC_DISCOVERY_PATHS) {
    test(`unauthenticated deep link to ${path} remains on public discovery URL`, async ({ page }) => {
      await page.goto(path);
      await expect(page).toHaveURL(new RegExp(`${path.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")}$`));
      await expect(page.getByTestId("public-discovery-layout")).toBeVisible();
    });
  }
});
