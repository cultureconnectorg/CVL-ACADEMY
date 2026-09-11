const { test, expect } = require("@playwright/test");
const { mockAuthenticatedSession } = require("./fixtures/auth-fixture");

// W3-D + Excel Spatial master verification — progression must remain
// authoritative while future stages are perceptible as horizon only.
test.describe("roadmap spatial progression (W3-D)", () => {
  test("no gamification language (level/XP/quest/player/skill tree) is exposed", async ({
    page,
  }) => {
    await mockAuthenticatedSession(page, { user: { stade: "pousse" } });
    await page.goto("/roadmap");
    await expect(page.getByTestId("roadmap-page")).toBeVisible();

    const bodyText = await page.locator("body").innerText();
    for (const term of [/\blevel\b/i, /\bniveau\b/i, /\bnivel\b/i, /\bxp\b/i, /\bquest\b/i, /\bplayer\b/i]) {
      expect(bodyText).not.toMatch(term);
    }
  });

  test("the current stage (from real progression data) is spatially foregrounded, others recede", async ({
    page,
  }) => {
    await mockAuthenticatedSession(page, { user: { stade: "pousse" } });
    await page.goto("/roadmap");

    const current = page.getByTestId("stage-pousse");
    const other = page.getByTestId("stage-graine");
    await expect(current).toHaveAttribute("data-focus-role", "target");
    await expect(other).toHaveAttribute("data-focus-role", "secondary");
  });

  test("PRO-003 / PRD-009: future remains visible but subdued through HORIZON without fake unlock", async ({
    page,
  }) => {
    await mockAuthenticatedSession(page, { user: { stade: "pousse" } });
    await page.goto("/roadmap");

    await expect(page.getByTestId("horizon-racine")).toBeVisible();
    await expect(page.getByTestId("horizon-foret")).toBeVisible();
    await expect(page.getByTestId("horizon-label-racine")).toContainText("Horizon");
    await expect(page.getByTestId("horizon-pousse")).toHaveCount(0);
    await expect(page.getByTestId("horizon-graine")).toHaveCount(0);

    const horizonOpacity = await page.getByTestId("horizon-racine").evaluate((el) => Number(getComputedStyle(el).opacity));
    expect(horizonOpacity).toBeLessThan(1);
    await expect(page.getByTestId("horizon-racine").locator("a,button")).toHaveCount(0);
  });

  test("NAV-006 / LRN-007: horizontal route context returns to the exact roadmap rail position", async ({
    page,
  }) => {
    await mockAuthenticatedSession(page, { user: { stade: "pousse" } });
    await page.goto("/roadmap");
    const rail = page.getByTestId("roadmap-scroll");
    await rail.evaluate((el) => { el.scrollLeft = 360; });
    const before = await rail.evaluate((el) => el.scrollLeft);
    expect(before).toBeGreaterThan(0);

    await page.getByTestId("nav-formations").click();
    await expect(page).toHaveURL(/\/formations$/);
    await page.goBack();
    await expect(page).toHaveURL(/\/roadmap$/);
    await expect(page.getByTestId("roadmap-page")).toBeVisible();

    await expect.poll(() => rail.evaluate((el) => el.scrollLeft)).toBe(before);
  });

  test("CC thresholds are still shown — real academic credit units, not gamification", async ({
    page,
  }) => {
    await mockAuthenticatedSession(page, { user: { stade: "graine" } });
    await page.goto("/roadmap");
    await expect(page.getByTestId("stage-racine")).toContainText("50+ CC");
  });

  test("REDUCED_MOTION: the foregrounded stage still settles at its target scale", async ({
    page,
  }) => {
    await mockAuthenticatedSession(page, { user: { stade: "pousse" } });
    await page.emulateMedia({ reducedMotion: "reduce" });
    await page.goto("/roadmap");
    const current = page.getByTestId("stage-pousse");
    await expect(current).toHaveAttribute("data-focus-role", "target");
    const transform = await current.evaluate((el) => getComputedStyle(el).transform);
    expect(transform).not.toBe("none");
  });
});
