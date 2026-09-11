import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import { REQUIREMENT_IDS, evidenceFor } from "./spatial-requirements.mjs";

const ROOT = process.cwd();
const read = (p) => fs.readFileSync(path.join(ROOT, p), "utf8");
const exists = (p) => fs.existsSync(path.join(ROOT, p));

const EXPECTED_COUNTS = {
  GOV: 15, PRD: 15, MOT: 20, LND: 10, NAV: 8, PRO: 8,
  FMS: 13, LRN: 8, ECO: 6, TEC: 14, CLD: 10, INT: 10,
};

const CONTENT_ASSERTIONS = {
  "GOV-002": () => assert.ok(exists("backend/server.py") && exists("frontend/src/App.js"), "existing stack must remain present"),
  "GOV-008": () => assert.match(read("frontend/package.json"), /framer-motion/),
  "GOV-009": () => assert.match(read("frontend/src/lib/depthMemory.js"), /sessionStorage/),
  "GOV-010": () => assert.doesNotMatch(read("frontend/src/lib/depthMemory.js"), /api\.|axios|fetch\(/),
  "GOV-014": () => assert.match(read("docs/ACADEMY_HERO_ENTRY_RESEARCH.md"), /PlayStation|Sony/i),
  "PRD-004": () => assert.match(read("frontend/src/lib/motion-primitives.jsx"), /useReducedMotion/),
  "PRD-006": () => assert.ok(exists("frontend/src/lib/RouteTransition.jsx")),
  "PRD-008": () => assert.ok(exists("frontend/src/lib/ContextFrame.jsx")),
  "PRD-009": () => assert.match(read("frontend/src/pages/Roadmap.js"), /future[\s\S]*<Horizon/),
  "PRD-010": () => assert.match(read("frontend/src/components/Layout.js"), /restoreRouteDepth/),
  "MOT-002": () => ["Focus", "Approach", "Enter", "Recede", "Reveal", "Return", "Confirm", "Horizon"].forEach((name) => assert.match(read("frontend/src/lib/motion-primitives.jsx"), new RegExp(`function ${name}\\b`))),
  "MOT-003": () => assert.ok(exists("frontend/src/lib/spatial-state.js")),
  "MOT-004": () => assert.ok(exists("frontend/src/lib/motion-tokens.js")),
  "MOT-009": () => assert.doesNotMatch(read("frontend/src/lib/depthMemory.js"), /preventDefault\(\).*scroll/s),
  "MOT-010": () => assert.ok(exists("frontend/src/lib/RouteTransition.jsx")),
  "MOT-013": () => assert.match(read("frontend/src/pages/Formations.js"), /never hover|NO_GENERIC_SCALE_HOVER/),
  "MOT-017": () => assert.ok(exists("frontend/e2e/reduced-motion.spec.js")),
  "MOT-019": () => assert.ok(exists("docs/ADR_W4_WEBGL_DECISION.md")),
  "LND-002": () => assert.match(read("frontend/src/pages/Landing.js"), /cvln-orange|cvln-forest/),
  "LND-010": () => assert.ok(exists("frontend/src/App.js")),
  "NAV-002": () => assert.ok(exists("frontend/e2e/routing.spec.js")),
  "NAV-003": () => assert.ok(exists("frontend/e2e/module-journey-navigation.spec.js")),
  "NAV-004": () => assert.ok(exists("frontend/e2e/keyboard-focus.spec.js")),
  "NAV-006": () => assert.match(read("frontend/src/lib/depthMemory.js"), /captureRouteDepth[\s\S]*restoreRouteDepth/),
  "NAV-007": () => assert.ok(exists("frontend/e2e/keyboard-focus.spec.js")),
  "PRO-001": () => ["graine", "pousse", "racine", "branches", "arbre", "foret"].forEach((stage) => assert.match(read("frontend/src/pages/Roadmap.js"), new RegExp(stage))),
  "PRO-003": () => assert.match(read("frontend/src/pages/Roadmap.js"), /future[\s\S]*<Horizon/),
  "PRO-005": () => assert.doesNotMatch(read("frontend/src/pages/Roadmap.js"), /Level\s+[0-9N]/i),
  "PRO-006": () => assert.ok(exists("backend/badges_engine.py")),
  "PRO-007": () => assert.ok(exists("backend/skills/progression.py")),
  "FMS-001": () => assert.ok(exists("backend/fms_lineage/initial_matrix.py")),
  "FMS-010": () => assert.ok(exists("backend/seed_modules.py")),
  "LRN-001": () => assert.match(read("frontend/src/components/Layout.js"), /mentorAvailable/),
  "LRN-002": () => assert.match(read("frontend/src/components/Layout.js"), /isPedagogicalContext/),
  "LRN-005": () => assert.ok(exists("backend/api/learning.py")),
  "LRN-007": () => assert.ok(exists("frontend/src/lib/depthMemory.js")),
  "LRN-008": () => assert.ok(exists("frontend/public/service-worker.js") && exists("frontend/src/serviceWorkerRegistration.js")),
  "ECO-001": () => assert.ok(exists("backend/services/frek_core.py")),
  "ECO-002": () => assert.ok(exists("backend/api/wallet.py")),
  "ECO-006": () => assert.ok(exists("backend/services/integrations/registry.py")),
  "TEC-005": () => assert.match(read("frontend/src/components/Layout.js"), /<main|<nav|<aside/),
  "TEC-008": () => assert.ok(exists("frontend/e2e/reduced-motion.spec.js")),
  "TEC-010": () => assert.ok(exists("frontend/e2e/routing.spec.js") && exists("backend/tests/backend_test.py")),
  "TEC-011": () => ["route-transition.spec.js", "reduced-motion.spec.js", "keyboard-focus.spec.js", "module-journey-navigation.spec.js"].forEach((f) => assert.ok(exists(`frontend/e2e/${f}`))),
  "TEC-013": () => assert.doesNotMatch(read("frontend/.env.example"), /sk-[A-Za-z0-9]|BEGIN PRIVATE KEY|mongodb\+srv:\/\/[^<]/),
  "CLD-001": () => assert.ok(exists("docs/SPATIAL_LEARNING_W0_AUDIT.md")),
  "CLD-008": () => assert.ok(exists("scripts/spatial-requirements.mjs")),
  "INT-005": () => assert.ok(exists("backend/api/quizzes.py")),
  "INT-006": () => assert.match(read("frontend/src/lib/depthMemory.js"), /scrollTo/),
  "INT-007": () => assert.ok(exists("frontend/e2e/reduced-motion.spec.js")),
  "INT-008": () => assert.ok(exists("frontend/e2e/keyboard-focus.spec.js")),
  "INT-010": () => assert.ok(exists("frontend/e2e/module-journey-context.spec.js")),
};

test("Spatial Excel master has exactly 137 unique requirement lines", () => {
  assert.equal(REQUIREMENT_IDS.length, 137);
  assert.equal(new Set(REQUIREMENT_IDS).size, 137);
  const actual = Object.fromEntries(Object.keys(EXPECTED_COUNTS).map((p) => [p, REQUIREMENT_IDS.filter((id) => id.startsWith(`${p}-`)).length]));
  assert.deepEqual(actual, EXPECTED_COUNTS);
});

for (const id of REQUIREMENT_IDS) {
  test(`${id} — implementation + runtime + test evidence is registered`, () => {
    const evidence = evidenceFor(id);
    assert.ok(evidence, `${id}: missing evidence group`);
    for (const kind of ["implementation", "runtime", "tests"]) {
      assert.ok(Array.isArray(evidence[kind]) && evidence[kind].length > 0, `${id}: ${kind} evidence missing`);
      for (const file of evidence[kind]) assert.ok(exists(file), `${id}: evidence path missing: ${file}`);
    }
    CONTENT_ASSERTIONS[id]?.();
  });
}
