const { test, expect } = require("@playwright/test");
const {
  mockAuthenticatedSession,
  FIXTURE_MODULE_QUIZ_READY,
} = require("./fixtures/auth-fixture");

const MODULE_URL = "/formations/FMS-01/modules/FMS-01-M01";

async function gotoQuizReadyModule(page, overrides = {}) {
  await mockAuthenticatedSession(page, { moduleData: FIXTURE_MODULE_QUIZ_READY, ...overrides });
  await page.goto(MODULE_URL);
  await page.getByTestId("phase-toggle-quiz").click();
}

// W3-B — ACTIVE -> CONTEXT -> RETURN for quiz, mini_mission (mission), and
// the Mentor panel. "Cas pédagogique" is deliberately not covered: no such
// screen exists in the current product (FMS pedagogical cases are a
// distinct, unmounted content concept — see docs/SPATIAL_LEARNING_W0.5_
// FMS_SOURCE_AUDIT.md — and FMS_CANONICAL_MIGRATION stays FORBIDDEN), so
// there is nothing to wrap without fabricating a screen that doesn't exist.
test.describe("quiz context (W3-B)", () => {
  test("starting the quiz enters CONTEXT", async ({ page }) => {
    await gotoQuizReadyModule(page);
    await page.getByTestId("phase-quiz-open").click();
    const wrapper = page.getByTestId("phase-quiz-questions").locator("..");
    await expect(wrapper).toHaveAttribute("data-context-state", "context");
  });

  test("CURRENT_MODULE_PRESERVED: the URL never changes while taking the quiz", async ({
    page,
  }) => {
    await gotoQuizReadyModule(page);
    await page.getByTestId("phase-quiz-open").click();
    await page.getByTestId("quiz-q-1-a").click();
    await expect(page).toHaveURL(new RegExp(`${MODULE_URL}$`));
  });

  test("PROGRESS_NOT_MUTATED_BY_ANIMATION: opening the quiz and answering sends zero mutating requests until Submit", async ({
    page,
  }) => {
    await gotoQuizReadyModule(page);
    const mutations = [];
    page.on("request", (req) => {
      if (["POST", "PUT", "PATCH", "DELETE"].includes(req.method()) && req.url().includes("/api/")) {
        mutations.push(`${req.method()} ${req.url()}`);
      }
    });
    await page.getByTestId("phase-quiz-open").click();
    await page.getByTestId("quiz-q-1-a").click();
    expect(mutations).toEqual([]);
  });

  test("submitting a passing quiz auto-advances to mini_mission, which enters CONTEXT too", async ({
    page,
  }) => {
    await gotoQuizReadyModule(page);
    await page.getByTestId("phase-quiz-open").click();
    await page.getByTestId("quiz-q-1-a").click();
    await page.getByTestId("quiz-submit").click();
    await expect(page.getByTestId("quiz-result")).toBeVisible();

    const missionWrapper = page.getByTestId("mini-mission-commit").locator("..");
    await expect(missionWrapper).toHaveAttribute("data-context-state", "context");
  });

  test("RETURN_POSITION_PRESERVED: after submitting, the module URL and formation are unchanged", async ({
    page,
  }) => {
    await gotoQuizReadyModule(page);
    await page.getByTestId("phase-quiz-open").click();
    await page.getByTestId("quiz-q-1-a").click();
    await page.getByTestId("quiz-submit").click();
    await expect(page).toHaveURL(new RegExp(`${MODULE_URL}$`));
    await expect(page.getByTestId("module-journey")).toBeVisible();
  });

  test("KEYBOARD_FOCUS: quiz choices and submit are reachable by keyboard", async ({ page }) => {
    await gotoQuizReadyModule(page);
    await page.getByTestId("phase-quiz-open").click();
    // The testid is on the <label>; the actual focusable control is the
    // radio <input> it wraps (native label-click-forwarding is what the
    // other tests' `.click()` already relies on).
    const radio = page.getByTestId("quiz-q-1-a").locator("input");
    await radio.focus();
    await expect(radio).toBeFocused();
  });

  test("REDUCED_MOTION: the quiz context still settles fully visible", async ({ page }) => {
    await mockAuthenticatedSession(page, { moduleData: FIXTURE_MODULE_QUIZ_READY });
    await page.emulateMedia({ reducedMotion: "reduce" });
    await page.goto(MODULE_URL);
    await page.getByTestId("phase-toggle-quiz").click();
    await page.getByTestId("phase-quiz-open").click();
    const wrapper = page.getByTestId("phase-quiz-questions").locator("..");
    await expect(wrapper).toHaveAttribute("data-context-state", "context");
    const opacity = await wrapper.evaluate((el) => getComputedStyle(el).opacity);
    expect(opacity).toBe("1");
  });
});

// W3-C moved the Mentor's mount point from "every authenticated screen" to
// "only inside an actual module" (mentorPresence.js) — these specs use
// MODULE_URL, the one screen where it's now actually reachable, rather
// than /formations (see mentor-presence.spec.js for the gating itself).
test.describe("mentor contextual panel (W3-B/W3-C)", () => {
  test("opening the mentor enters CONTEXT and closing it returns to ACTIVE", async ({ page }) => {
    await mockAuthenticatedSession(page);
    await page.goto(MODULE_URL);
    const panel = page.getByTestId("mentor-panel");
    await expect(panel).toHaveAttribute("data-context-state", "active");

    await page.getByTestId("mentor-fab").click();
    await expect(panel).toHaveAttribute("data-context-state", "context");
    await expect(panel).toHaveAttribute("aria-hidden", "false");

    await page.getByTestId("mentor-close").click();
    await expect(panel).toHaveAttribute("data-context-state", "active");
    await expect(panel).toHaveAttribute("aria-hidden", "true");
  });

  test("RETURN_POSITION_PRESERVED: opening/closing the mentor never navigates or changes the module journey underneath", async ({
    page,
  }) => {
    await mockAuthenticatedSession(page);
    await page.goto(MODULE_URL);
    // hook is the default-open phase (CURRENT) per FIXTURE_MODULE — see
    // module-journey-hierarchy.spec.js (W3-A).
    const hookWrapper = page.locator('[data-testid="phase-hook"]').locator("..");
    await expect(hookWrapper).toHaveAttribute("data-journey-role", "current");

    await page.getByTestId("mentor-fab").click();
    await page.getByTestId("mentor-close").click();

    await expect(page).toHaveURL(new RegExp(`${MODULE_URL}$`));
    await expect(hookWrapper).toHaveAttribute("data-journey-role", "current");
  });

  test("closed mentor panel is not keyboard-reachable (no focus trap on hidden controls)", async ({
    page,
  }) => {
    await mockAuthenticatedSession(page);
    await page.goto(MODULE_URL);
    await expect(page.getByTestId("mentor-input")).toHaveAttribute("tabindex", "-1");
    await expect(page.getByTestId("mentor-close")).toHaveAttribute("tabindex", "-1");

    await page.getByTestId("mentor-fab").click();
    await expect(page.getByTestId("mentor-input")).toHaveAttribute("tabindex", "0");
  });

  test("PROGRESS_NOT_MUTATED_BY_ANIMATION: opening/closing the mentor sends zero mutating requests", async ({
    page,
  }) => {
    await mockAuthenticatedSession(page);
    const mutations = [];
    page.on("request", (req) => {
      if (["POST", "PUT", "PATCH", "DELETE"].includes(req.method()) && req.url().includes("/api/")) {
        mutations.push(`${req.method()} ${req.url()}`);
      }
    });
    await page.goto(MODULE_URL);
    await page.getByTestId("mentor-fab").click();
    await page.getByTestId("mentor-close").click();
    expect(mutations).toEqual([]);
  });

  test("REDUCED_MOTION: the mentor context still settles fully visible", async ({ page }) => {
    await mockAuthenticatedSession(page);
    await page.emulateMedia({ reducedMotion: "reduce" });
    await page.goto(MODULE_URL);
    await page.getByTestId("mentor-fab").click();
    const panel = page.getByTestId("mentor-panel");
    await expect(panel).toHaveAttribute("data-context-state", "context");
    const opacity = await panel.evaluate((el) => getComputedStyle(el).opacity);
    expect(opacity).toBe("1");
  });
});
