const { test, expect } = require("@playwright/test");

// Every `<Protected>`-wrapped path in src/App.js. An unauthenticated
// visitor deep-linking any of these must land back on "/" — this is the
// exact behavior `Protected` implements (`if (!user) return <Navigate
// to="/" replace />`), and this suite proves it holds for each route
// individually rather than trusting the shared wrapper by inspection alone.
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
  "/trainer", // also role-gated (TRAINER_ROLES) — unauthenticated fails the earlier !user check first
  "/jury", // also role-gated (JURY_ROLES)
  "/admin", // also role-gated (ADMIN_ROLES)
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
