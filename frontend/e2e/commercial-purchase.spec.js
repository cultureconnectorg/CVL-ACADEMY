const { test, expect } = require("@playwright/test");
const {
  mockAuthenticatedSession,
  FIXTURE_FORMATION_DETAIL,
} = require("./fixtures/auth-fixture");

const FORMATION = {
  ...FIXTURE_FORMATION_DETAIL,
  code: "FMS-01",
  modules: [
    {
      code: "FMS-01-M01",
      name: "Fixture Commercial Module",
      duration_h: 2,
      stade: "graine",
      deliverable: "Fixture deliverable",
      status: "available",
      is_unlocked: true,
      course_progress_pct: 0,
    },
  ],
};

test("Wallet payment activates entitlement and unlocks the module CTA", async ({ page }) => {
  await mockAuthenticatedSession(page, { formationDetail: FORMATION });

  await page.route("**/api/legal/requirements", (route) =>
    route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify({ accepted: true }),
    })
  );
  await page.route("**/api/commercial/offers/FMS-01**", (route) =>
    route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify({
        economy_code: "FMS-01",
        requirement_id: "ACA-ECO-E2E",
        offer_kind: "path",
        amount_eur: 990,
        currency: "EUR",
        source_sheet: "Mapping_812",
      }),
    })
  );
  await page.route("**/api/commercial/entitlements/mine", (route) =>
    route.fulfill({
      status: 200,
      contentType: "application/json",
      body: "[]",
    })
  );
  await page.route("**/api/commercial/orders", async (route) => {
    expect(route.request().method()).toBe("POST");
    const payload = route.request().postDataJSON();
    expect(payload).toEqual({ economy_code: "FMS-01", offer_kind: "path" });
    await route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify({
        order_id: "ord_e2e_1",
        economy_code: "FMS-01",
        status: "PENDING_PAYMENT",
      }),
    });
  });
  await page.route("**/api/commercial/orders/ord_e2e_1/pay-wallet", async (route) => {
    expect(route.request().method()).toBe("POST");
    await route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify({ order_id: "ord_e2e_1", status: "PAID" }),
    });
  });

  await page.goto("/formations/FMS-01");

  await expect(page.getByTestId("commercial-purchase-card")).toBeVisible();
  await expect(page.getByTestId("module-locked-FMS-01-M01")).toBeVisible();
  await expect(page.getByTestId("module-open-FMS-01-M01")).toHaveCount(0);

  await page.getByTestId("commercial-pay-wallet").click();

  await expect(page.getByTestId("commercial-access-active")).toBeVisible();
  await expect(page.getByTestId("module-open-FMS-01-M01")).toBeVisible();
  await expect(page.getByTestId("module-locked-FMS-01-M01")).toHaveCount(0);
});
