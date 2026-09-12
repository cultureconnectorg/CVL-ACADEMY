const { test, expect } = require("@playwright/test");
const {
  mockAuthenticatedSession,
  FIXTURE_FORMATION_DETAIL,
} = require("./fixtures/auth-fixture");

const FORMATION = {
  ...FIXTURE_FORMATION_DETAIL,
  code: "FMS-01",
  modules: [],
};

const INVOICE_INTENT = {
  billing_document_id: "bill_e2e_1",
  document_type: "INVOICE",
  status: "INVOICE_INTENT",
  legal_invoice_number: null,
  order_id: "ord_billing_e2e_1",
  economy_code: "FMS-01",
  amount_eur: 990,
  currency: "EUR",
};

test("paid learner can issue and download the Factur-X invoice after reconnect", async ({ page }) => {
  await mockAuthenticatedSession(page, { formationDetail: FORMATION });

  await page.route("**/api/legal/requirements", (route) =>
    route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify({ accepted: true }) })
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
      }),
    })
  );
  await page.route("**/api/commercial/entitlements/mine", (route) =>
    route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify([
        { economy_code: "FMS-01", status: "ACTIVE", source: "CVLN_WALLET" },
      ]),
    })
  );
  await page.route("**/api/billing/invoices/mine**", (route) =>
    route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify([INVOICE_INTENT]),
    })
  );
  await page.route("**/api/billing/profile", async (route) => {
    if (route.request().method() === "GET") {
      return route.fulfill({
        status: 404,
        contentType: "application/json",
        body: JSON.stringify({ detail: "BILLING_PROFILE_NOT_FOUND" }),
      });
    }
    expect(route.request().method()).toBe("PUT");
    const payload = route.request().postDataJSON();
    expect(payload).toMatchObject({
      legal_name: "Client Test",
      address_line1: "2 rue Client",
      postal_code: "69001",
      city: "Lyon",
      country: "FR",
    });
    return route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify(payload),
    });
  });
  await page.route("**/api/billing/orders/ord_billing_e2e_1/issue", (route) =>
    route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify({
        ...INVOICE_INTENT,
        status: "ISSUED",
        legal_invoice_number: "ACA-2026-000001",
        einvoice_format: "FACTUR-X_EN16931",
        einvoice_validation: "PASS",
      }),
    })
  );
  await page.route("**/api/billing/orders/ord_billing_e2e_1/invoice/pdf", (route) =>
    route.fulfill({ status: 200, contentType: "application/pdf", body: "%PDF-E2E" })
  );
  await page.route("**/api/billing/orders/ord_billing_e2e_1/invoice/xml", (route) =>
    route.fulfill({
      status: 200,
      contentType: "application/xml",
      body: "<CrossIndustryInvoice />",
    })
  );

  await page.goto("/formations/FMS-01");
  await expect(page.getByTestId("commercial-access-active")).toBeVisible();
  await expect(page.getByTestId("billing-invoice-panel")).toBeVisible();

  await page.getByTestId("billing-legal-name").fill("Client Test");
  await page.getByTestId("billing-address").fill("2 rue Client");
  await page.getByTestId("billing-postal-code").fill("69001");
  await page.getByTestId("billing-city").fill("Lyon");
  await page.getByTestId("billing-country").fill("FR");
  await page.getByTestId("billing-issue-invoice").click();

  await expect(page.getByTestId("billing-issued-card")).toBeVisible();
  await expect(page.getByTestId("billing-invoice-number")).toHaveText("ACA-2026-000001");
  await expect(page.getByTestId("billing-download-pdf")).toBeVisible();
  await expect(page.getByTestId("billing-download-xml")).toBeVisible();
});
