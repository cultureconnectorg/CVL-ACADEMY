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

    await expect(racine).toHaveAttribute("aria-current", "step");
    await expect(branches).not.toHaveAttribute("aria-current", "step");
  });

  test("continuous attention has exactly one primary plane and follows the retargeted rail", async ({ page }) => {
    await setup(page);

    const primaryVisuals = page.locator('[data-testid^="stage-visual-"][data-attention-tier="PRIMARY_ATTENTION"]');
    await expect(primaryVisuals).toHaveCount(1);
    await expect(page.getByTestId("stage-visual-racine")).toHaveAttribute("data-attention-tier", "PRIMARY_ATTENTION");

    const racine = page.getByTestId("stage-racine");
    await racine.focus();
    await page.keyboard.press("ArrowRight");

    await expect.poll(async () => Number(
      await page.getByTestId("roadmap-scroll").getAttribute("data-attention-position")
    )).toBeGreaterThan(2.5);
    await expect(page.getByTestId("stage-visual-branches")).toHaveAttribute("data-attention-tier", "PRIMARY_ATTENTION");
    await expect(primaryVisuals).toHaveCount(1);

    const primaryBlur = await page.getByTestId("stage-visual-branches").evaluate((el) => getComputedStyle(el).filter);
    const farBlur = await page.getByTestId("stage-visual-graine").evaluate((el) => getComputedStyle(el).filter);
    expect(primaryBlur).toContain("blur(0px)");
    expect(farBlur).not.toContain("blur(0px)");
  });

  test("progressive horizon is bound to real domain distance, not perceptual focus", async ({ page }) => {
    await setup(page);

    await expect(page.getByTestId("stage-racine")).toHaveAttribute("data-domain-stage-state", "CURRENT");
    await expect(page.getByTestId("stage-branches")).toHaveAttribute("data-domain-stage-state", "HORIZON");
    await expect(page.getByTestId("stage-arbre")).toHaveAttribute("data-domain-stage-state", "HORIZON");
    await expect(page.getByTestId("stage-foret")).toHaveAttribute("data-domain-stage-state", "HORIZON");
    await expect(page.getByTestId("horizon-branches")).toHaveAttribute("data-horizon-distance", "1");
    await expect(page.getByTestId("horizon-arbre")).toHaveAttribute("data-horizon-distance", "2");
    await expect(page.getByTestId("horizon-foret")).toHaveAttribute("data-horizon-distance", "3");

    const nearOpacity = await page.getByTestId("horizon-branches").evaluate((el) => Number(getComputedStyle(el).opacity));
    const farOpacity = await page.getByTestId("horizon-foret").evaluate((el) => Number(getComputedStyle(el).opacity));
    expect(nearOpacity).toBeGreaterThan(farOpacity);

    const racine = page.getByTestId("stage-racine");
    await racine.focus();
    await page.keyboard.press("End");
    await expect(page.getByTestId("stage-foret")).toBeFocused();
    await expect.poll(async () => page.getByTestId("stage-visual-foret").getAttribute("data-attention-tier")).toBe("PRIMARY_ATTENTION");
    await expect(page.getByTestId("stage-foret")).toHaveAttribute("data-domain-stage-state", "HORIZON");
    await expect(page.getByTestId("stage-racine")).toHaveAttribute("aria-current", "step");
  });

  test("latent context is removed from the accessibility tree but current/focused domain context is never hidden", async ({ page }) => {
    await setup(page);
    const racine = page.getByTestId("stage-racine");
    await racine.focus();
    await page.keyboard.press("End");
    await expect(page.getByTestId("stage-foret")).toBeFocused();

    await expect.poll(async () => page.getByTestId("stage-graine").getAttribute("data-attention-tier")).toBe("LATENT_CONTEXT");
    await expect(page.getByTestId("stage-graine")).toHaveAttribute("aria-hidden", "true");
    await expect(page.getByTestId("stage-racine")).not.toHaveAttribute("aria-hidden", "true");
    await expect(page.getByTestId("stage-foret")).not.toHaveAttribute("aria-hidden", "true");
  });

  test("repeated directional cadence predicts only one perceptual step ahead then expires", async ({ page }) => {
    await setup(page);
    const rail = page.getByTestId("roadmap-scroll");
    const racine = page.getByTestId("stage-racine");
    await racine.focus();

    await page.keyboard.press("ArrowRight");
    await page.keyboard.press("ArrowRight");

    await expect(page.getByTestId("stage-arbre")).toBeFocused();
    await expect(rail).toHaveAttribute("data-spatial-cadence", /REPEATED|FAST_REPEAT/);
    await expect(rail).toHaveAttribute("data-spatial-predicted-index", "5");
    await expect(page.getByTestId("stage-foret")).toHaveAttribute("data-spatial-predicted", "true");

    // Prediction never becomes domain truth or DOM focus.
    await expect(page.getByTestId("stage-foret")).not.toBeFocused();
    await expect(page.getByTestId("stage-foret")).toHaveAttribute("data-domain-stage-state", "HORIZON");
    await expect(page.getByTestId("stage-racine")).toHaveAttribute("aria-current", "step");

    await expect.poll(async () => rail.getAttribute("data-spatial-predicted-index"), { timeout: 1200 }).toBe("-1");
    await expect(rail).toHaveAttribute("data-spatial-cadence", "STOPPED");
  });

  test("direction reversal cancels prediction instead of fighting explicit intent", async ({ page }) => {
    await setup(page);
    const rail = page.getByTestId("roadmap-scroll");
    await page.getByTestId("stage-racine").focus();
    await page.keyboard.press("ArrowRight");
    await page.keyboard.press("ArrowRight");
    await expect(rail).toHaveAttribute("data-spatial-predicted-index", "5");

    await page.keyboard.press("ArrowLeft");
    await expect(page.getByTestId("stage-branches")).toBeFocused();
    await expect(rail).toHaveAttribute("data-spatial-cadence", "REVERSAL");
    await expect(rail).toHaveAttribute("data-spatial-predicted-index", "-1");
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
    await expect(rail).toHaveAttribute("data-spatial-predicted-index", "-1");
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
    await expect(page.getByTestId("stage-visual-branches")).toHaveAttribute("data-attention-tier", "PRIMARY_ATTENTION");
    await expect(page.getByTestId("spatial-background")).toHaveAttribute("data-spatial-motion", "reduced");
  });
});
