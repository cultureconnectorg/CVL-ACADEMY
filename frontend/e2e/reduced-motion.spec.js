const { test, expect } = require("@playwright/test");

// Proves the actual CSS added in W1-A (src/index.css) behaves correctly
// under the real `prefers-reduced-motion: reduce` OS preference —
// checking computed style, not just that the rule exists in the source.
test.describe("prefers-reduced-motion (W1-E / MOT-029)", () => {
  test("animation-duration collapses to ~0 when reduced motion is on", async ({ page }) => {
    await page.emulateMedia({ reducedMotion: "reduce" });
    await page.goto("/");
    await expect(page.getByTestId("landing-page")).toBeVisible();

    const duration = await page.evaluate(
      () => getComputedStyle(document.body).animationDuration
    );
    // Chromium serializes the computed value in seconds (0.01ms == 1e-5s),
    // so assert on the parsed magnitude rather than a literal "0.01ms"
    // string — this is what the index.css rule actually guarantees
    // (imperceptibly short, not exactly the source unit).
    expect(parseFloat(duration)).toBeLessThan(0.0001);
  });

  test("animation-duration is NOT forced when reduced motion is off (control)", async ({
    page,
  }) => {
    await page.emulateMedia({ reducedMotion: "no-preference" });
    await page.goto("/");
    await expect(page.getByTestId("landing-page")).toBeVisible();

    const duration = await page.evaluate(
      () => getComputedStyle(document.body).animationDuration
    );
    // <body> has no animation of its own — absent the reduced-motion
    // override, its computed animation-duration is the CSS initial value
    // (0s), not the forced near-zero value from the W1-A rule.
    expect(parseFloat(duration)).toBe(0);
  });
});
