const { test, expect } = require("@playwright/test");

test.describe("external expert workspace", () => {
  test("opens only the assigned case with expert key", async ({ page }) => {
    await page.route("**/api/governance-advanced/expert-workspace/CASE-1", async (route) => {
      const headers = route.request().headers();
      expect(headers["x-cvln-expert-key"]).toBe("cvln_exp_test");
      await route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify({
          workspace_type: "PROFESSIONAL_CASE_SCOPED",
          domain: "LEGAL",
          case: { id: "CASE-1", title: "Legal review", description: "Assigned case" },
          expert: { id: "EXP-1", display_name: "Counsel" },
          assignment: { authority_level: "A3_EXTERNAL_EXPERT", scope: ["case:read"] },
          queues: { documents: [{ id: "DOC-1" }], decisions: [{ id: "DEC-1" }], audit: [] },
          global_browse: false,
          cross_case_access: false,
        }),
      });
    });

    await page.goto("/expert");
    await expect(page.getByTestId("expert-login-shell")).toBeVisible();
    await page.getByLabel("Dossier").fill("CASE-1");
    await page.getByLabel("Clé expert").fill("cvln_exp_test");
    await page.getByRole("button", { name: "Ouvrir mon dossier" }).click();
    await expect(page.getByTestId("expert-workspace")).toContainText("Legal review");
    await expect(page.getByTestId("expert-workspace")).toContainText("Counsel");
    await expect(page.getByTestId("expert-workspace")).toContainText("case:read");
  });

  test("does not retain invalid key as a workspace", async ({ page }) => {
    await page.route("**/api/governance-advanced/expert-workspace/CASE-X", (route) =>
      route.fulfill({
        status: 403,
        contentType: "application/json",
        body: JSON.stringify({ detail: "credential is not assigned to this case" }),
      }),
    );
    await page.goto("/expert");
    await page.getByLabel("Dossier").fill("CASE-X");
    await page.getByLabel("Clé expert").fill("bad");
    await page.getByRole("button", { name: "Ouvrir mon dossier" }).click();
    await expect(page.getByTestId("expert-login-shell")).toContainText(
      "credential is not assigned to this case",
    );
    await expect(page.getByTestId("expert-workspace")).toHaveCount(0);
  });
});
