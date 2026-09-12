const { test, expect } = require("@playwright/test");
const { mockAuthenticatedSession, FIXTURE_FORMATION_DETAIL } = require("./fixtures/auth-fixture");

const FORMATION_URL = "/formations/FMS-01";
const MODULE_URL = "/formations/FMS-01/modules/FMS-01-M01";
const FORMATION_WITH_MODULE = {
  ...FIXTURE_FORMATION_DETAIL,
  modules: [
    {
      code: "FMS-01-M01",
      name: "Fixture Module One",
      duration_h: 2,
      stade: "pousse",
      deliverable: "Fixture deliverable",
      status: "in_progress",
      is_unlocked: true,
      course_progress_pct: 20,
    },
  ],
};

async function setup(page) {
  await mockAuthenticatedSession(page, { formationDetail: FORMATION_WITH_MODULE });

  // FormationDetail includes the real commercial entitlement gate. This test
  // exercises camera navigation, not checkout, so make that independent
  // contract explicit: no Economy mapping means no commercial lock. Without
  // this route the generic fixture fallback returns `{}`; CommercialPurchaseCard
  // expects an entitlement array, correctly treats the malformed response as
  // commercial failure and replaces the module link with a lock after first
  // render. That produced a locator which could appear and then detach.
  await page.route("**/api/commercial/offers/FMS-01**", (route) =>
    route.fulfill({
      status: 404,
      contentType: "application/json",
      body: JSON.stringify({ detail: "NO_ECONOMY_MAPPING" }),
    })
  );
}

test.describe("Spatial camera follow H0.8 production bridge", () => {
  test("formation module link creates a real forward camera contract", async ({ page }) => {
    await setup(page);
    await page.goto(FORMATION_URL);
    const open = page.getByTestId("module-open-FMS-01-M01");
    await expect(open).toBeVisible();
    await open.click();

    await expect(page).toHaveURL(new RegExp(`${MODULE_URL}$`));
    await expect(page.getByTestId("module-journey")).toBeVisible();

    await expect.poll(async () => page.evaluate(() => {
      const raw = sessionStorage.getItem("cvln:spatial-camera-return:v1");
      if (!raw) return null;
      const value = JSON.parse(raw);
      return {
        anchorId: value.anchorId,
        sourceRoute: value.sourceRoute,
        destinationRoute: value.destinationRoute,
        hasDestinationRect: Boolean(value.destinationRect),
        hasTarget: Boolean(value.cameraOriginTarget),
      };
    })).toEqual({
      anchorId: "module:FMS-01:FMS-01-M01",
      sourceRoute: FORMATION_URL,
      destinationRoute: MODULE_URL,
      hasDestinationRect: true,
      hasTarget: true,
    });
  });

  test("browser Back follows the inverse path and restores source focus", async ({ page }) => {
    await setup(page);
    await page.goto(FORMATION_URL);
    const open = page.getByTestId("module-open-FMS-01-M01");
    await open.click();
    await expect(page.getByTestId("module-journey")).toBeVisible();

    await expect.poll(async () => page.evaluate(() => Boolean(
      sessionStorage.getItem("cvln:spatial-camera-return:v1")
    ))).toBe(true);

    await page.goBack();
    await expect(page).toHaveURL(new RegExp(`${FORMATION_URL}$`));
    await expect(page.getByTestId("formation-detail")).toBeVisible();
    await expect(page.getByTestId("module-open-FMS-01-M01")).toBeFocused();

    await expect.poll(async () => page.evaluate(() => ({
      armed: sessionStorage.getItem("cvln:spatial-camera-return-armed:v1"),
      contract: sessionStorage.getItem("cvln:spatial-camera-return:v1"),
    }))).toEqual({ armed: null, contract: null });
  });

  test("reduced motion keeps navigation semantic and skips camera persistence", async ({ page }) => {
    await setup(page);
    await page.emulateMedia({ reducedMotion: "reduce" });
    await page.goto(FORMATION_URL);
    await page.getByTestId("module-open-FMS-01-M01").click();
    await expect(page.getByTestId("module-journey")).toBeVisible();
    const stored = await page.evaluate(() => sessionStorage.getItem("cvln:spatial-camera-return:v1"));
    expect(stored).toBeNull();
    await expect(page.getByTestId("spatial-background")).toHaveAttribute("data-spatial-motion", "reduced");
  });
});
