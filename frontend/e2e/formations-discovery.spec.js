const { test, expect } = require("@playwright/test");
const { mockAuthenticatedSession } = require("./fixtures/auth-fixture");

// W2-D — Formation discovery, and the deterministic authenticated-surface
// test coverage the human authorization required before touching any
// authenticated screen: AUTHENTICATED_ROUTE, KEYBOARD_FOCUS,
// REDUCED_MOTION, RETURN_POSITION, PROGRESS_NOT_MUTATED. All requests are
// intercepted via e2e/fixtures/auth-fixture.js — nothing here touches a
// real backend or database, and no production code path is altered to
// make this possible (see the fixture file's own header comment).
test.describe("formations discovery — authenticated (W2-D)", () => {
  test("AUTHENTICATED_ROUTE: the fixture session reaches the real formations page, not a redirect", async ({
    page,
  }) => {
    await mockAuthenticatedSession(page);
    await page.goto("/formations");
    await expect(page).toHaveURL(/\/formations$/);
    await expect(page.getByTestId("formations-page")).toBeVisible();
    await expect(page.getByTestId("formation-FMS-01")).toBeVisible();
  });

  test("pole filter: selecting a pole marks it TARGET (FocusFieldItem role), never via hover", async ({
    page,
  }) => {
    await mockAuthenticatedSession(page);
    await page.goto("/formations");
    const allPole = page.locator('[data-testid="pole-ALL"]').locator("..");
    const fmsPole = page.locator('[data-testid="pole-FMS"]').locator("..");

    await expect(allPole).toHaveAttribute("data-focus-role", "target");
    await expect(fmsPole).toHaveAttribute("data-focus-role", "secondary");

    // Hovering must NOT change the role — NO_GENERIC_SCALE_HOVER.
    await fmsPole.hover();
    await page.waitForTimeout(200);
    await expect(fmsPole).toHaveAttribute("data-focus-role", "secondary");

    await page.getByTestId("pole-FMS").click();
    await expect(fmsPole).toHaveAttribute("data-focus-role", "target");
    await expect(allPole).toHaveAttribute("data-focus-role", "secondary");
  });

  test("KEYBOARD_FOCUS: tabbing to a formation card marks it TARGET and others RECEDE", async ({
    page,
  }) => {
    await mockAuthenticatedSession(page);
    await page.goto("/formations");
    const card1 = page.getByTestId("formation-FMS-01");
    const card2 = page.getByTestId("formation-MKT-01");

    await card1.focus();
    await expect(card1).toBeFocused();
    const wrapper1 = card1.locator("..");
    const wrapper2 = card2.locator("..");
    await expect(wrapper1).toHaveAttribute("data-focus-role", "target");
    await expect(wrapper2).toHaveAttribute("data-focus-role", "secondary");

    await card1.blur();
    await page.waitForTimeout(200);
    await expect(wrapper1).toHaveAttribute("data-focus-role", "idle");
    await expect(wrapper2).toHaveAttribute("data-focus-role", "idle");
  });

  test("REDUCED_MOTION: focusing a card still settles at its target scale under reduced motion", async ({
    page,
  }) => {
    await mockAuthenticatedSession(page);
    await page.emulateMedia({ reducedMotion: "reduce" });
    await page.goto("/formations");
    const card = page.getByTestId("formation-FMS-01");
    await card.focus();
    const wrapper = card.locator("..");
    await expect(wrapper).toHaveAttribute("data-focus-role", "target");
    // Reduced motion collapses the transition to ~1ms, not zero movement —
    // the end state (APPROACH's scale) must still be reached.
    const transform = await wrapper.evaluate((el) => getComputedStyle(el).transform);
    expect(transform).not.toBe("none");
  });

  test("RETURN_POSITION: leaving and returning to /formations resets the pole filter to its default (documented, not silently changed)", async ({
    page,
  }) => {
    await mockAuthenticatedSession(page);
    await page.goto("/formations");
    await page.getByTestId("pole-FMS").click();
    await expect(page.locator('[data-testid="pole-FMS"]').locator("..")).toHaveAttribute(
      "data-focus-role",
      "target"
    );

    // Navigate away (client-side) and back via a fresh deep link — this
    // documents Formations.js's actual, pre-existing behavior (local
    // `useState` is not persisted across unmount) rather than silently
    // introducing or claiming a persistence feature nobody asked for.
    await page.goto("/dashboard");
    await page.goto("/formations");
    await expect(page.getByTestId("formations-page")).toBeVisible();
    await expect(page.locator('[data-testid="pole-ALL"]').locator("..")).toHaveAttribute(
      "data-focus-role",
      "target"
    );
  });

  test("PROGRESS_NOT_MUTATED: browsing the catalogue sends zero mutating requests", async ({
    page,
  }) => {
    await mockAuthenticatedSession(page);
    const mutations = [];
    page.on("request", (req) => {
      if (["POST", "PUT", "PATCH", "DELETE"].includes(req.method()) && req.url().includes("/api/")) {
        mutations.push(`${req.method()} ${req.url()}`);
      }
    });

    await page.goto("/formations");
    await page.getByTestId("pole-FMS").click();
    await page.getByTestId("formation-FMS-01").focus();
    await page.getByTestId("pole-ALL").click();

    expect(mutations).toEqual([]);
  });
});
