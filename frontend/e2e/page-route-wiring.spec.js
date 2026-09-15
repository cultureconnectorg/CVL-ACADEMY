const { test, expect } = require("@playwright/test");
const {
  mockAuthenticatedSession,
  FIXTURE_USER,
} = require("./fixtures/auth-fixture");

async function jsonRoute(page, pattern, body) {
  await page.route(pattern, (route) =>
    route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify(body),
    })
  );
}

async function prepareStudent(page, overrides = {}) {
  await mockAuthenticatedSession(page, overrides);
  await jsonRoute(page, "**/api/frek/profile", {
    stade_progress_pct: 0,
    stade_next_at: 10,
    recent_signals: [],
  });
  await jsonRoute(page, "**/api/progression/summary", {
    completed_modules: 0,
    total_modules: 0,
    global_pct: 0,
  });
  await jsonRoute(page, "**/api/missions/mine", []);
  await jsonRoute(page, "**/api/badges", []);
  await jsonRoute(page, "**/api/wallet/me", {
    account: { jcc_balance: 0, token_balance: 0, badges: [] },
    recent_transactions: [],
  });
  await jsonRoute(page, "**/api/skills/mine", []);
  await jsonRoute(page, "**/api/certifications/attempts/mine", []);
  await jsonRoute(page, "**/api/certifications/rubrics", []);
}

test.describe("authenticated page route wiring", () => {
  const studentPages = [
    ["/dashboard", "dashboard-page"],
    ["/roadmap", "roadmap-page"],
    ["/formations", "formations-page"],
    ["/formations/FMS-01", "formation-detail"],
    ["/formations/FMS-01/modules/FMS-01-M01", "module-journey"],
    ["/missions", "missions-page"],
    ["/badges", "badges-page"],
    ["/frek-profile", "frek-profile-page"],
    ["/wallet", "wallet-page"],
    ["/skills", "skills-page"],
    ["/certifications", "certifications-page"],
  ];

  for (const [path, testId] of studentPages) {
    test(`${path} resolves to its wired page`, async ({ page }) => {
      await prepareStudent(page);
      await page.goto(path);
      await expect(page).toHaveURL(new RegExp(`${path.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")}$`));
      await expect(page.getByTestId(testId)).toBeVisible();
    });
  }

  test("/onboarding resolves for an authenticated learner who is not onboarded", async ({ page }) => {
    await mockAuthenticatedSession(page, {
      user: { ...FIXTURE_USER, onboarding_completed: false },
    });
    await jsonRoute(page, "**/api/onboarding/options", {
      metiers: [],
      territoires: [],
      langs: ["fr"],
    });
    await page.goto("/onboarding");
    await expect(page).toHaveURL(/\/onboarding$/);
    await expect(page.getByTestId("onboarding-page")).toBeVisible();
  });

  test("legal gate backend failure stays technical instead of faking legal acceptance", async ({ page }) => {
    await mockAuthenticatedSession(page, {
      user: { ...FIXTURE_USER, onboarding_completed: false },
    });
    await page.route("**/api/legal/requirements", (route) =>
      route.fulfill({
        status: 503,
        contentType: "application/json",
        body: JSON.stringify({ detail: "temporarily unavailable" }),
      })
    );

    await page.goto("/onboarding");

    await expect(page).toHaveURL(/\/onboarding$/);
    await expect(page.getByTestId("legal-gate-error")).toBeVisible();
    await expect(page).not.toHaveURL(/\/legal\/accept$/);
  });

  test("/trainer resolves for trainer role with an organisation", async ({ page }) => {
    await prepareStudent(page, {
      user: { ...FIXTURE_USER, role: "trainer", org_id: "org-fixture-1" },
    });
    await jsonRoute(page, "**/api/orgs/org-fixture-1/cohorts", []);
    // TrainerDashboard.js's loadPhysicalSessions() unconditionally fetches
    // these two alongside the cohorts list above; real backend contracts
    // (backend/api/physical_sessions.py, backend/api/certification.py) are
    // both `List[...]`. Without these, they fell through to the generic
    // "{}" fallback and `pending.filter(...)` (backend/api/certification.py's
    // GET /attempts/pending consumer) threw "pending.filter is not a
    // function", crashing the whole TrainerDashboard tree before
    // "trainer-dashboard-page" could ever be found.
    await jsonRoute(page, "**/api/physical-sessions/assigned", []);
    await jsonRoute(page, "**/api/certifications/attempts/pending", []);
    await page.goto("/trainer");
    await expect(page).toHaveURL(/\/trainer$/);
    await expect(page.getByTestId("trainer-dashboard-page")).toBeVisible();
    await expect(page.getByTestId("cohorts-panel")).toBeVisible();
    await expect(page.getByTestId("create-cohort-form")).toBeVisible();
  });

  for (const role of ["jury", "corrector"]) {
    test(`/jury resolves for ${role} role`, async ({ page }) => {
      await prepareStudent(page, {
        user: { ...FIXTURE_USER, role },
      });
      await jsonRoute(page, "**/api/certifications/attempts/pending", []);
      await page.goto("/jury");
      await expect(page).toHaveURL(/\/jury$/);
      await expect(page.getByTestId("jury-dashboard-page")).toBeVisible();
    });
  }

  test("/admin resolves for admin role and its panels receive array contracts", async ({ page }) => {
    await prepareStudent(page, {
      user: { ...FIXTURE_USER, role: "admin" },
    });
    await jsonRoute(page, "**/api/fms/imports", []);
    await jsonRoute(page, "**/api/integrations", []);
    await jsonRoute(page, "**/api/orgs", []);
    await jsonRoute(page, "**/api/formations", []);
    await jsonRoute(page, "**/api/institutional/connectors", []);
    // RubricImportPanel (frontend/src/pages/admin/AdminDashboard.js's
    // RUBRIC_DOMAINS) unconditionally fetches all three canonical-formation
    // list routes on mount. Real backend contracts (backend/api/canonical.py,
    // klt_canonical.py, kor_canonical.py) are all `List[...]`. Without these
    // mocks they fell through to the generic "{}" fallback, and
    // `(formationsByDomain[d.key] || []).map(...)` threw "... .map is not a
    // function" (since `{}` is truthy, `|| []` never kicks in), crashing the
    // whole AdminDashboard tree shortly after its first render -- late enough
    // for "admin-dashboard-page" to be briefly visible but "fms-import-panel"
    // to already be gone by the next assertion.
    await jsonRoute(page, "**/api/canonical/formations", []);
    await jsonRoute(page, "**/api/klt-canonical/formations", []);
    await jsonRoute(page, "**/api/kor-canonical/formations", []);
    await page.goto("/admin");
    await expect(page).toHaveURL(/\/admin$/);
    await expect(page.getByTestId("admin-dashboard-page")).toBeVisible();
    await expect(page.getByTestId("fms-import-panel")).toBeVisible();
    await expect(page.getByTestId("integrations-panel")).toBeVisible();
    await expect(page.getByTestId("orgs-panel")).toBeVisible();
    await expect(page.getByTestId("catalogue-panel")).toBeVisible();
    await expect(page.getByTestId("institutional-bridge-panel")).toBeVisible();
  });
});
