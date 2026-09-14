const { test, expect } = require("@playwright/test");
const { mockAuthenticatedSession } = require("./fixtures/auth-fixture");

async function mockWorkspace(page) {
  await page.route("**/api/governance/cases", (route) =>
    route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify([
        {
          id: "CASE-1",
          title: "Privacy review",
          domain: "PRIVACY",
          sensitivity: "INTERNAL",
          status: "OPEN",
        },
      ]),
    })
  );
  await page.route("**/api/governance/experts", (route) =>
    route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify([
        { id: "EXP-1", display_name: "External Reviewer", domains: ["PRIVACY"] },
      ]),
    })
  );
  await page.route("**/api/assurance/security/release-gate", (route) =>
    route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify({ pass: false, blocking_count: 1, blocking_findings: [] }),
    })
  );
  await page.route("**/api/assurance/risks/critical-gate", (route) =>
    route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify({ pass: true, blocking_count: 0, blocking_risks: [] }),
    })
  );
}

test.describe("professional governance workspace", () => {
  test("admin can render real workspace sections and release gates", async ({ page }) => {
    await mockAuthenticatedSession(page, { user: { role: "admin" } });
    await mockWorkspace(page);
    await page.goto("/admin/professional-workspace");

    await expect(page.getByTestId("professional-workspace-page")).toBeVisible();
    await expect(page.getByTestId("workspace-cases")).toContainText("Privacy review");
    await expect(page.getByTestId("workspace-experts")).toContainText("External Reviewer");
    await expect(page.getByTestId("gate-security-gate")).toContainText("BLOCKED");
    await expect(page.getByTestId("gate-critical-risk-gate")).toContainText("PASS");
  });

  test("student cannot enter admin professional workspace", async ({ page }) => {
    await mockAuthenticatedSession(page, { user: { role: "student" } });
    await page.goto("/admin/professional-workspace");
    await expect(page).toHaveURL(/\/dashboard$/);
    await expect(page.getByTestId("professional-workspace-page")).toHaveCount(0);
  });
});
