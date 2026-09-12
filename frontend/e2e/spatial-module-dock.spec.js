const { test, expect } = require("@playwright/test");
const { mockAuthenticatedSession } = require("./fixtures/auth-fixture");

const MODULE_URL = "/formations/FMS-01/modules/FMS-01-M01";

test.describe("Spatial contextual module dock", () => {
  test("projects the existing current phase and navigates only through existing toggles", async ({ page }) => {
    await mockAuthenticatedSession(page);
    await page.goto(MODULE_URL);

    const dock = page.getByTestId("spatial-module-dock");
    await expect(dock).toBeVisible();
    await expect(dock).toHaveAttribute("data-spatial-current-phase", "hook");

    await expect(page.getByTestId("spatial-module-dock-prev")).toBeDisabled();
    await expect(page.getByTestId("spatial-module-dock-next")).toBeEnabled();
    await page.getByTestId("spatial-module-dock-next").click();

    await expect(page.getByTestId("phase-objectives").locator("..")).toHaveAttribute("data-journey-role", "current");
    await expect(dock).toHaveAttribute("data-spatial-current-phase", "objectives");
  });

  test("dock navigation is perceptual only and sends no domain mutation", async ({ page }) => {
    await mockAuthenticatedSession(page);
    const mutations = [];
    page.on("request", (req) => {
      if (["POST", "PUT", "PATCH", "DELETE"].includes(req.method()) && req.url().includes("/api/")) {
        mutations.push(`${req.method()} ${req.url()}`);
      }
    });
    await page.goto(MODULE_URL);
    await page.getByTestId("spatial-module-dock-next").click();
    expect(mutations).toEqual([]);
  });

  test("recomposition gives current phase foreground depth while reduced motion removes travel", async ({ page }) => {
    await mockAuthenticatedSession(page);
    await page.goto(MODULE_URL);
    const currentCard = page.getByTestId("phase-hook");
    const transform = await currentCard.evaluate((el) => getComputedStyle(el).transform);
    expect(transform).not.toBe("none");

    await page.emulateMedia({ reducedMotion: "reduce" });
    await page.reload();
    const reducedTransform = await page.getByTestId("phase-hook").evaluate((el) => getComputedStyle(el).transform);
    expect(reducedTransform).toBe("none");
  });

  test("current phase retargets the persistent world instead of swapping environments", async ({ page }) => {
    await mockAuthenticatedSession(page);
    await page.goto(MODULE_URL);
    const world = page.getByTestId("spatial-background");
    await expect(world).toHaveAttribute("data-spatial-module-phase", "hook");
    const worldNodeBefore = await world.getAttribute("data-spatial-node");

    await page.getByTestId("spatial-module-dock-next").click();
    await expect(world).toHaveAttribute("data-spatial-module-phase", "objectives");
    await expect(world).toHaveAttribute("data-spatial-node", worldNodeBefore);
  });

  test("dock never mounts outside a module route and phase environment is cleared", async ({ page }) => {
    await mockAuthenticatedSession(page);
    await page.goto(MODULE_URL);
    await expect(page.getByTestId("spatial-background")).toHaveAttribute("data-spatial-module-phase", "hook");

    await page.goto("/formations");
    await expect(page.getByTestId("spatial-module-dock")).toHaveCount(0);
    await expect(page.getByTestId("spatial-background")).not.toHaveAttribute("data-spatial-module-phase", /.+/);
  });
});
