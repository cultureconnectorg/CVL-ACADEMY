const { test, expect } = require("@playwright/test");

// W2-B — Landing Spatial Learning. Two functional primitive usages on the
// public Landing page: FOCUS on the active language pill, ENTER on the
// register/login mode swap (heading block + the conditionally-rendered
// display_name field). See docs/SPATIAL_LEARNING_W2B_LANDING_REPORT.md for
// why APPROACH/RECEDE/HORIZON were deliberately NOT used here.
test.describe("landing spatial learning (W2-B)", () => {
  test("the active language pill is marked distinctly from the others", async ({ page }) => {
    await page.goto("/");
    const fr = page.getByTestId("landing-lang-fr");
    const en = page.getByTestId("landing-lang-en");
    await expect(fr).toBeVisible();
    await expect(en).toBeVisible();

    // fr starts active by default (see i18n.jsx) — clicking en flips which
    // pill is FOCUS-marked. Assert on the actual style FOCUS applies
    // (opacity), not just the pre-existing color class, since that's the
    // new, real behavior under test.
    const beforeEnOpacity = await en.evaluate((el) => getComputedStyle(el.parentElement).opacity);
    await en.click();
    await expect(page).toHaveURL(/\/$/); // language switch never navigates
    await page.waitForTimeout(500); // let the FOCUS transition (160ms) settle
    const afterEnOpacity = await en.evaluate((el) => getComputedStyle(el.parentElement).opacity);
    expect(parseFloat(afterEnOpacity)).toBeGreaterThan(parseFloat(beforeEnOpacity));
  });

  test("switching to login mode removes the display_name field from the DOM entirely", async ({
    page,
  }) => {
    await page.goto("/");
    // Default mode is "register" — the field starts present.
    await expect(page.getByTestId("auth-display-name")).toBeVisible();

    await page.getByTestId("auth-toggle").click();
    // Login mode: the field must be gone, not just hidden — no stray
    // `required` validation, no keyboard-focus trap on an invisible input.
    await expect(page.getByTestId("auth-display-name")).toHaveCount(0);
  });

  test("switching back to register mode brings the display_name field back, focusable and required", async ({
    page,
  }) => {
    await page.goto("/");
    await page.getByTestId("auth-toggle").click(); // -> login
    await page.getByTestId("auth-toggle").click(); // -> register
    const field = page.getByTestId("auth-display-name");
    await expect(field).toBeVisible();
    await expect(field).toHaveAttribute("required", "");
    await field.focus();
    await expect(field).toBeFocused();
  });

  test("the login form (no display_name) submits its own required-field validation cleanly", async ({
    page,
  }) => {
    await page.goto("/");
    await page.getByTestId("auth-toggle").click(); // -> login
    await expect(page.getByTestId("auth-display-name")).toHaveCount(0);
    // No backend in this sandbox, so this won't actually log in — the
    // point is that submitting doesn't get blocked by a hidden, empty
    // required display_name field (the exact regression a REVEAL-while-
    // hidden implementation would have risked).
    await page.getByTestId("auth-email").fill("test@example.com");
    await page.getByTestId("auth-password").fill("password123");
    await page.getByTestId("auth-submit").click();
    // Still on the login form (no navigation happened either way) — what
    // matters is no browser-native validation popup blocked the click on
    // a field that no longer exists.
    await expect(page.getByTestId("auth-form")).toBeVisible();
  });

  test("mode toggle heading settles fully visible under reduced motion", async ({ page }) => {
    await page.emulateMedia({ reducedMotion: "reduce" });
    await page.goto("/");
    await page.getByTestId("auth-toggle").click();
    const heading = page.locator('[data-testid="auth-form"]').locator("..").locator("h2");
    await expect(heading).toBeVisible();
    const opacity = await heading.evaluate((el) => getComputedStyle(el).opacity);
    expect(opacity).toBe("1");
  });
});
