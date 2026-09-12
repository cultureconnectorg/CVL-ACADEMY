const { test, expect } = require("@playwright/test");
const { mockAuthenticatedSession } = require("./fixtures/auth-fixture");

async function setup(page) {
  await mockAuthenticatedSession(page, { user: { stade: "racine" } });
  await page.goto("/roadmap");
  await expect(page.getByTestId("roadmap-page")).toBeVisible();
}

test.describe("Spatial roadmap rail runtime", () => {
  test("current domain stage starts as the roving keyboard focus and arrows retarget spatial focus", async ({ page }) => {
    await setup(page);

    const racine = page.getByTestId("stage-racine");
    const branches = page.getByTestId("stage-branches");
    await expect(racine).toHaveAttribute("aria-current", "step");
    await expect(racine).toHaveAttribute("tabindex", "0");
    await expect(branches).toHaveAttribute("tabindex", "-1");

    await racine.focus();
    await page.keyboard.press("ArrowRight");
    await expect(branches).toBeFocused();
    await expect(branches).toHaveAttribute("aria-selected", "true");
    await expect(racine).toHaveAttribute("aria-current", "step");

    // Moving perceptual focus must never change the real learner stage.
    await expect(racine).toHaveAttribute("aria-current", "step");
    await expect(branches).not.toHaveAttribute("aria-current", "step");
  });

  test("Home and End provide deterministic rail navigation", async ({ page }) => {
    await setup(page);
    const racine = page.getByTestId("stage-racine");
    await racine.focus();

    await page.keyboard.press("End");
    await expect(page.getByTestId("stage-foret")).toBeFocused();

    await page.keyboard.press("Home");
    await expect(page.getByTestId("stage-graine")).toBeFocused();
  });

  test("pointer drag follows 1:1 and settles without a domain mutation", async ({ page }) => {
    await setup(page);
    const mutations = [];
    page.on("request", (req) => {
      if (["POST", "PUT", "PATCH", "DELETE"].includes(req.method()) && req.url().includes("/api/")) {
        mutations.push(`${req.method()} ${req.url()}`);
      }
    });

    const rail = page.getByTestId("roadmap-scroll");
    const box = await rail.boundingBox();
    expect(box).not.toBeNull();
    const before = await rail.evaluate((el) => el.scrollLeft);

    await page.mouse.move(box.x + box.width * 0.75, box.y + box.height * 0.5);
    await page.mouse.down();
    await page.mouse.move(box.x + box.width * 0.25, box.y + box.height * 0.5, { steps: 6 });
    await page.mouse.up();

    await expect.poll(async () => rail.evaluate((el) => el.scrollLeft)).toBeGreaterThan(before);
    expect(mutations).toEqual([]);
  });

  test("reduced motion keeps full keyboard semantics without animated settling", async ({ page }) => {
    await mockAuthenticatedSession(page, { user: { stade: "racine" } });
    await page.emulateMedia({ reducedMotion: "reduce" });
    await page.goto("/roadmap");

    const racine = page.getByTestId("stage-racine");
    await racine.focus();
    await page.keyboard.press("ArrowRight");
    await expect(page.getByTestId("stage-branches")).toBeFocused();
    await expect(page.getByTestId("spatial-background")).toHaveAttribute("data-spatial-motion", "reduced");
  });
});
