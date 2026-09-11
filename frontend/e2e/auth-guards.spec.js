const { test, expect } = require("@playwright/test");

// Every authenticated/protected path in src/App.js. An unauthenticated
// visitor deep-linking any of these must land back on "/".
const PROTECTED_PATHS = [
  "/dashboard",
  "/roadmap",
  "/formations",
  "/formations/FMS-01",
  "/formations/FMS-01/modules/FMS-01-M01",
  "/missions",
  "/badges",
  "/frek-profile",
  "/wallet",
  "/skills",
  "/certifications",
  "/trainer",
  "/jury",
  "/admin",
  "/admin/stakeholders",
  "/partner",
  "/institution",
  "/stakeholder/claim/example-code",
];

test.describe("auth guards (W1-E)", () => {
  for (const path of PROTECTED_PATHS) {
    test(`unauthenticated deep link to ${path} redirects to /`, async ({ page }) => {
      await page.goto(path);
      await expect(page).toHaveURL(/\/$/);
      await expect(page.getByTestId("landing-page")).toBeVisible();
    });
  }
});
