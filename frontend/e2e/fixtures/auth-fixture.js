// Deterministic test-only auth + formations-discovery fixture (W2-D).
//
// Required per the human authorization before touching any authenticated
// surface: a mock/test fixture "permis uniquement dans l'environnement de
// test" — FAKE_PRODUCTION_DATA is forbidden. Nothing here reaches a real
// database or a real user: every value is intercepted at the network
// layer inside a single Playwright browser context and discarded when
// the test ends. No file under this directory is imported by the app
// itself (grep-checkable: only e2e/*.spec.js require() it).
//
// Field shapes mirror exactly what frontend/src/lib/auth.jsx and
// frontend/src/pages/Formations.js already consume from the real API —
// this fixture stands in for the backend response, it does not invent a
// different contract.

const FIXTURE_USER = {
  id: "e2e-fixture-user",
  email: "e2e-fixture@example.invalid",
  display_name: "E2E Fixture",
  frek_id: "E2E-FIXTURE-0001",
  role: "student",
  onboarding_completed: true,
  lang: "fr",
};

const FIXTURE_POLES = [
  { code: "FMS", name: "Formation & Savoirs", color: "#D9631E" },
  { code: "MKT", name: "Marketing Culturel", color: "#1E6B4F" },
];

const FIXTURE_LEARNING_PATH = {
  metier_vise: "Développement Artistique",
  own_pole: [
    {
      code: "FMS-01",
      name: "Fixture Formation One",
      pole: "FMS",
      pole_color: "#D9631E",
      duration_h: 12,
      cc: 4,
      modules_count: 6,
      validated_count: 2,
      progress_pct: 33,
      is_unlocked: true,
      is_recommended: true,
      lock_reason: "",
    },
    {
      code: "FMS-02",
      name: "Fixture Formation Two",
      pole: "FMS",
      pole_color: "#D9631E",
      duration_h: 8,
      cc: 3,
      modules_count: 5,
      validated_count: 0,
      progress_pct: 0,
      is_unlocked: false,
      is_recommended: true,
      lock_reason: "Termine Fixture Formation One pour débloquer.",
    },
  ],
  other_poles: [
    {
      code: "MKT-01",
      name: "Fixture Formation Three",
      pole: "MKT",
      pole_color: "#1E6B4F",
      duration_h: 10,
      cc: 3,
      modules_count: 4,
      validated_count: 0,
      progress_pct: 0,
      is_unlocked: false,
      is_recommended: false,
      lock_reason: "Se débloque en progressant.",
    },
  ],
  next_action: {
    pole_color: "#D9631E",
    module_name: "Fixture Module 3",
    formation_name: "Fixture Formation One",
    formation_code: "FMS-01",
    module_code: "FMS-01-M03",
  },
};

const FIXTURE_MODULE = {
  formation: { code: "FMS-01", name: "Fixture Formation One", pole_color: "#D9631E", pole_name: "FMS" },
  module: {
    code: "FMS-01-M01",
    name: "Fixture Module One",
    duration_h: 2,
    stade: "pousse",
    course_progress_pct: 0,
    phases: {
      hook: { narrative: "Fixture hook narrative." },
      objectives: { items: ["Fixture objective 1", "Fixture objective 2"] },
      course: {
        content_md: "## Fixture course\nSome fixture reading content.",
        reading_min: 5,
        video_placeholder: { duration_min: 10 },
      },
      workshop: {
        estimated_min: 15,
        steps: [{ n: 1, action: "Fixture step", detail: "Fixture detail" }],
      },
      deliverable: { spec_md: "Fixture deliverable spec.", min_chars: 20 },
      mini_mission: { brief: "Fixture mini-mission brief." },
    },
  },
  is_unlocked: true,
  lock_reason: "",
  status: "in_progress",
  phase_flags: {
    hook: true,
    objectives: true,
    course: false,
    workshop: false,
    deliverable: false,
    quiz: false,
    mini_mission: false,
  },
  progress: { course_progress_pct: 0 },
};

const FIXTURE_MODULE_QUIZ_READY = {
  ...FIXTURE_MODULE,
  phase_flags: {
    hook: true,
    objectives: true,
    course: true,
    workshop: true,
    deliverable: true,
    quiz: false,
    mini_mission: false,
  },
};

const FIXTURE_QUIZ = {
  quiz: [
    {
      n: 1,
      type: "qcm",
      question: "Fixture question one?",
      choices: [
        { id: "a", text: "Fixture choice A" },
        { id: "b", text: "Fixture choice B" },
      ],
    },
  ],
};

const FIXTURE_QUIZ_RESULT_PASSED = {
  passed: true,
  score: 1,
  correct: 1,
  total: 1,
  cc_earned: 5,
  signal_emitted: "FMS-01-M01-QUIZ",
};

const FIXTURE_FORMATION_DETAIL = {
  code: "FMS-01",
  name: "Fixture Formation One",
  pole_color: "#D9631E",
  pole_name: "FMS",
  description: "Fixture description.",
  objective_strategic: "Fixture objective.",
  duration_h: 12,
  cc: 4,
  badge_name: "Fixture Badge",
  debouches: "Fixture débouchés.",
  prerequisites: "Fixture prerequisites.",
  stades: ["graine", "pousse"],
  is_unlocked: true,
  lock_reason: "",
  modules: [
    {
      code: "FMS-01-M01",
      name: "Fixture Module One",
      duration_h: 2,
      stade: "pousse",
      deliverable: "Fixture deliverable.",
      status: "in_progress",
      is_unlocked: true,
      course_progress_pct: 0,
    },
  ],
};

/**
 * Installs the fixture for one Playwright `page`: a fake but internally
 * consistent authenticated session, entirely intercepted at the network
 * layer. Protected-route tests represent a learner who has already accepted
 * the current legal bundle and already made a necessary-only cookie choice;
 * legal/cookie-consent behavior itself is tested separately. This keeps those
 * production guards active without letting unrelated modal UI block a feature
 * test's real pointer path.
 *
 * @param {import('@playwright/test').Page} page
 * @param {{ user?, poles?, learningPath? }} overrides
 */
async function mockAuthenticatedSession(page, overrides = {}) {
  const user = { ...FIXTURE_USER, ...(overrides.user || {}) };
  const poles = overrides.poles || FIXTURE_POLES;
  const learningPath = overrides.learningPath || FIXTURE_LEARNING_PATH;
  const moduleData = overrides.moduleData || FIXTURE_MODULE;
  const formationDetail = overrides.formationDetail || FIXTURE_FORMATION_DETAIL;

  await page.addInitScript(
    ([token, refresh, cookiePreference]) => {
      window.localStorage.setItem("cvln_token", token);
      window.localStorage.setItem("cvln_refresh_token", refresh);
      window.localStorage.setItem("cvln_cookie_consent_v1", JSON.stringify(cookiePreference));
    },
    [
      "e2e-fixture-token",
      "e2e-fixture-refresh-token",
      {
        version: 1,
        necessary: true,
        analytics: false,
        marketing: false,
        choice: "necessary",
        decided_at: "2026-01-01T00:00:00.000Z",
      },
    ]
  );

  // Playwright resolves page.route handlers in last-in-first-out order.
  // Register the broad fallback first, then layer specific contracts above it
  // so auth/domain fixtures win deterministically.
  await page.route("**/api/**", (route) => route.fulfill({ status: 200, body: "{}" }));

  await page.route("**/api/auth/me", (route) =>
    route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify(user) })
  );
  await page.route("**/api/legal/requirements", (route) =>
    route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify({ accepted: true, bundle_version: "e2e-current", documents: [] }),
    })
  );
  await page.route("**/api/poles", (route) =>
    route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify(poles) })
  );
  await page.route("**/api/user/learning-path", (route) =>
    route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify(learningPath),
    })
  );
  await page.route("**/api/missions", (route) =>
    route.fulfill({ status: 200, contentType: "application/json", body: "[]" })
  );
  await page.route("**/api/badges/mine", (route) =>
    route.fulfill({ status: 200, contentType: "application/json", body: "[]" })
  );

  let quizJustPassed = false;
  await page.route("**/api/modules/*/*", (route) => {
    if (route.request().method() !== "GET") return route.fallback();
    const body = quizJustPassed
      ? { ...moduleData, phase_flags: { ...moduleData.phase_flags, quiz: true } }
      : moduleData;
    return route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify(body) });
  });

  const quiz = overrides.quiz || FIXTURE_QUIZ;
  const quizResult = overrides.quizResult || FIXTURE_QUIZ_RESULT_PASSED;
  await page.route("**/api/formations/*/modules/*/quiz", (route) =>
    route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify(quiz) })
  );
  await page.route("**/api/formations/*/modules/*/quiz/submit", (route) => {
    if (quizResult.passed) quizJustPassed = true;
    return route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify(quizResult),
    });
  });
  await page.route("**/api/mentor/chat", (route) =>
    route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify({ reply: "Fixture mentor reply." }),
    })
  );
  await page.route("**/api/formations/*", (route) =>
    route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify(formationDetail),
    })
  );

  return { user, poles, learningPath, moduleData, quiz, quizResult, formationDetail };
}

module.exports = {
  mockAuthenticatedSession,
  FIXTURE_USER,
  FIXTURE_POLES,
  FIXTURE_LEARNING_PATH,
  FIXTURE_MODULE,
  FIXTURE_MODULE_QUIZ_READY,
  FIXTURE_QUIZ,
  FIXTURE_QUIZ_RESULT_PASSED,
  FIXTURE_FORMATION_DETAIL,
};