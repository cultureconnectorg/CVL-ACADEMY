const { test, expect } = require("@playwright/test");
const { mockAuthenticatedSession } = require("./fixtures/auth-fixture");

// W3-D — spatial progression. The GRAINE -> POUSSE -> RACINE -> BRANCHES
// -> ARBRE -> FORÊT stage system already existed as an environmental
// metaphor; this tranche removes the one place it leaked gamification
// language ("Level N") and makes the current stage read as spatially
// foregrounded (CvlnFocusField, W2-C) instead of numbered.
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
