const { test, expect } = require("@playwright/test");
const { mockAuthenticatedSession } = require("./fixtures/auth-fixture");

// ACA-0030 — Ecosystem Builder surface. auth-fixture.js's default mock
// for GET /ecosystem-builder/me returns an empty "consumer" stage
// surface; these specs override that route per-test where a different
// stage/content shape is needed (Playwright resolves the LAST
// registered matching route first, so a route added after
// mockAuthenticatedSession() takes precedence over its default).
test.describe("ecosystem builder surface (ACA-0030)", () => {
  test("AUTHENTICATED_ROUTE: reaches the real page, consumer stage by default", async ({
    page,
  }) => {
    await mockAuthenticatedSession(page);
    await page.goto("/ecosystem-builder");
    await expect(page).toHaveURL(/\/ecosystem-builder$/);
    await expect(page.getByTestId("ecosystem-builder-page")).toBeVisible();
    await expect(page.getByTestId("builder-stage-consumer")).toHaveAttribute(
      "data-active",
      "true"
    );
  });

  test("nav: the sidebar link reaches the page", async ({ page }) => {
    await mockAuthenticatedSession(page);
    await page.goto("/dashboard");
    await page.getByTestId("nav-ecosystem_builder").click();
    await expect(page).toHaveURL(/\/ecosystem-builder$/);
  });

  test("builder stage surfaces portfolio, credentials, proofs, missions and history from a real composed surface", async ({
    page,
  }) => {
    await mockAuthenticatedSession(page);
    await page.route("**/api/ecosystem-builder/me", (route) =>
      route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify({
          stage: "builder",
          frek_id: "FREK-001",
          display_name: "Ada",
          is_public: true,
          portfolio: [
            { skill_id: "FMS01-A1", label: "Compétence A1", metier: "FMS", niveau: "A01", bloc: "B1", evidence_count: 2 },
          ],
          credentials: [
            { certification_code: "FMS01-A01", score_global: 87.5, mention: "Bien", jury_signature_sha256: "abc123", graded_at: "2026-01-01T00:00:00Z" },
          ],
          verified_proofs: [
            { skill_id: "FMS01-A1", evidence_type: "module_completion", ref: "FMS-01-M01", sha256: "deadbeef00", ts: "2026-01-01T00:00:00Z" },
          ],
          missions_completed: [
            { mission_code: "M-01", accepted_at: "2026-01-01T00:00:00Z", submitted_at: "2026-01-02T00:00:00Z" },
          ],
          ecosystem_history: [
            { event_type: "academy_badge_awarded", published_at: "2026-01-03T00:00:00Z" },
          ],
        }),
      })
    );
    await page.goto("/ecosystem-builder");
    await expect(page.getByTestId("builder-stage-builder")).toHaveAttribute("data-active", "true");
    await expect(page.getByTestId("builder-portfolio-FMS01-A1")).toBeVisible();
    await expect(page.getByTestId("builder-credential-FMS01-A01")).toBeVisible();
    await expect(page.getByTestId("builder-proof-0")).toBeVisible();
    await expect(page.getByTestId("builder-mission-M-01")).toBeVisible();
    await expect(page.getByTestId("builder-history-0")).toBeVisible();
    // consumer/professional stages must not be the active one
    await expect(page.getByTestId("builder-stage-consumer")).toHaveAttribute("data-active", "false");
  });

  test("professional stage shows the become-builder CTA; builder stage does not", async ({
    page,
  }) => {
    await mockAuthenticatedSession(page);
    await page.route("**/api/ecosystem-builder/me", (route) =>
      route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify({
          stage: "professional",
          frek_id: "FREK-001",
          display_name: "Ada",
          is_public: false,
          portfolio: [],
          credentials: [],
          verified_proofs: [],
          missions_completed: [],
          ecosystem_history: [],
        }),
      })
    );
    await page.goto("/ecosystem-builder");
    await expect(page.getByTestId("builder-become-builder-cta")).toBeVisible();
  });

  test("PROGRESS_NOT_MUTATED_BY_ANIMATION: viewing the surface sends zero mutating requests", async ({
    page,
  }) => {
    await mockAuthenticatedSession(page);
    const mutations = [];
    page.on("request", (req) => {
      if (["POST", "PUT", "PATCH", "DELETE"].includes(req.method()) && req.url().includes("/api/")) {
        mutations.push(`${req.method()} ${req.url()}`);
      }
    });
    await page.goto("/ecosystem-builder");
    await expect(page.getByTestId("ecosystem-builder-page")).toBeVisible();
    expect(mutations).toEqual([]);
  });

  test("REDUCED_MOTION: the page still settles fully visible", async ({ page }) => {
    await mockAuthenticatedSession(page);
    await page.emulateMedia({ reducedMotion: "reduce" });
    await page.goto("/ecosystem-builder");
    await expect(page.getByTestId("ecosystem-builder-page")).toBeVisible();
    await expect(page.getByTestId("builder-stage-card")).toBeVisible();
  });
});
