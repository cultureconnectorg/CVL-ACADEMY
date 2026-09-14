const { test, expect } = require("@playwright/test");
const { mockAuthenticatedSession } = require("./fixtures/auth-fixture");

const spatialEnabled =
  process.env.REACT_APP_ACADEMY_SPATIAL_HUB_ENABLED === "true" &&
  process.env.REACT_APP_ACADEMY_SPATIAL_MODULE_DEPTH === "true";

test.describe("H0.10 production spatial closure", () => {
  test.skip(!spatialEnabled, "Runs only in the dedicated spatial-enabled CI pass");

  test.beforeEach(async ({ page }) => {
    await mockAuthenticatedSession(page, {
      user: { stade: "pousse", cc_credits: 15 },
    });
  });

  test("Roadmap uses the real depth engine and finished stage-card language", async ({ page }) => {
    await page.goto("/roadmap");
    await expect(page.getByTestId("roadmap-page")).toBeVisible();
    const current = page.getByTestId("stage-pousse");
    await expect(current).toHaveClass(/spatial-stage-card/);
    await expect(current).toHaveAttribute("aria-current", "true");
    await expect(current).toHaveAttribute("data-tier", /.+/);
    await expect(page.getByTestId("roadmap-scroll")).toHaveClass(/spatial-stage-rail/);
  });

  test("Roadmap keeps acquired stages accessible and marks future stages as horizon, never completed", async ({ page }) => {
    await page.goto("/roadmap");

    const acquired = page.getByTestId("stage-graine");
    const current = page.getByTestId("stage-pousse");
    const future = page.getByTestId("stage-racine");

    await expect(acquired).toHaveAttribute("data-progression-state", "acquired");
    await expect(acquired).toContainText("✓");
    await expect(current).toHaveAttribute("data-progression-state", "current");
    await expect(future).toHaveAttribute("data-progression-state", "future");
    await expect(future).toHaveAttribute("aria-disabled", "true");
    await expect(future).toContainText(/Verrouill|Locked|Bloquead|Bloke/i);
    await expect(future).not.toContainText("✓");
  });

  test("Formations uses the finished focus-card language without changing routing", async ({ page }) => {
    await page.goto("/formations");
    await expect(page.getByTestId("formations-page")).toBeVisible();
    const card = page.getByTestId("formation-FMS-01");
    await expect(card).toHaveClass(/spatial-formation-card/);
    await expect(card).toHaveAttribute("data-focus-state", "calm");
    await card.focus();
    await expect(card).toHaveAttribute("data-focus-state", "target");
    await expect(card).toHaveAttribute("href", /\/formations\/FMS-01$/);
  });

  test("Badges uses the glanceable depth cluster and a real next target", async ({ page }) => {
    await page.goto("/badges");
    await expect(page.getByTestId("badges-page")).toBeVisible();
    const next = page.getByTestId("badge-B10");
    await expect(next).toHaveClass(/spatial-badge-card/);
    await expect(next).toHaveAttribute("data-tier", "PRIMARY_ATTENTION");
    await expect(next).toHaveAttribute("data-reachable", "true");
  });

  test("ModuleJourney uses the finished physics phase shell and keeps domain roles", async ({ page }) => {
    await page.goto("/formations/FMS-01/modules/FMS-01-M01");
    await expect(page.getByTestId("module-journey")).toBeVisible();
    const phase = page.getByTestId("phase-hook");
    const shell = phase.locator("..");
    await expect(shell).toHaveClass(/spatial-phase-shell/);
    await expect(shell).toHaveAttribute("data-journey-role", "current");
    await expect(shell).toHaveAttribute("data-tier", /.+/);
  });

  test("environmental layer is mounted with spatial environment enabled", async ({ page }) => {
    await page.goto("/dashboard");
    await expect(page.getByTestId("app-layout")).toBeVisible();
    await expect(page.getByTestId("academy-backdrop")).toBeAttached();
    await expect(page.getByTestId("sidebar")).toBeVisible();
  });
});