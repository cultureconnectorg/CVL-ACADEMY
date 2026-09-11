export const REQUIREMENT_IDS = `GOV-001,GOV-002,GOV-003,GOV-004,GOV-005,GOV-006,GOV-007,GOV-008,GOV-009,GOV-010,GOV-011,GOV-012,GOV-013,GOV-014,GOV-015,PRD-001,PRD-002,PRD-003,PRD-004,PRD-005,PRD-006,PRD-007,PRD-008,PRD-009,PRD-010,PRD-011,PRD-012,PRD-013,PRD-014,PRD-015,MOT-001,MOT-002,MOT-003,MOT-004,MOT-005,MOT-006,MOT-007,MOT-008,MOT-009,MOT-010,MOT-011,MOT-012,MOT-013,MOT-014,MOT-015,MOT-016,MOT-017,MOT-018,MOT-019,MOT-020,LND-001,LND-002,LND-003,LND-004,LND-005,LND-006,LND-007,LND-008,LND-009,LND-010,NAV-001,NAV-002,NAV-003,NAV-004,NAV-005,NAV-006,NAV-007,NAV-008,PRO-001,PRO-002,PRO-003,PRO-004,PRO-005,PRO-006,PRO-007,PRO-008,FMS-001,FMS-002,FMS-003,FMS-004,FMS-005,FMS-006,FMS-007,FMS-008,FMS-009,FMS-010,FMS-011,FMS-012,FMS-013,LRN-001,LRN-002,LRN-003,LRN-004,LRN-005,LRN-006,LRN-007,LRN-008,ECO-001,ECO-002,ECO-003,ECO-004,ECO-005,ECO-006,TEC-001,TEC-002,TEC-003,TEC-004,TEC-005,TEC-006,TEC-007,TEC-008,TEC-009,TEC-010,TEC-011,TEC-012,TEC-013,TEC-014,CLD-001,CLD-002,CLD-003,CLD-004,CLD-005,CLD-006,CLD-007,CLD-008,CLD-009,CLD-010,INT-001,INT-002,INT-003,INT-004,INT-005,INT-006,INT-007,INT-008,INT-009,INT-010`.split(",");

export const EVIDENCE_BY_PREFIX = {
  GOV: {
    implementation: ["INTEGRATION_CONTRACT.md", "docs/SPATIAL_LEARNING_W0_AUDIT.md"],
    runtime: ["frontend/src/App.js", "backend/server.py"],
    tests: ["frontend/e2e/routing.spec.js", "backend/tests/test_lifecycle.py"],
  },
  PRD: {
    implementation: ["docs/ACADEMY_SPATIAL_END_TO_END_ARCHITECTURE.md", "frontend/src/lib/spatial-state.js"],
    runtime: ["frontend/src/pages/Landing.js", "frontend/src/pages/ModuleJourney.js", "frontend/src/pages/Roadmap.js"],
    tests: ["frontend/e2e/landing-spatial.spec.js", "frontend/e2e/module-journey-hierarchy.spec.js", "frontend/e2e/roadmap-progression.spec.js"],
  },
  MOT: {
    implementation: ["frontend/src/lib/motion-tokens.js", "frontend/src/lib/motion-primitives.jsx", "frontend/src/lib/spatial-state.js"],
    runtime: ["frontend/src/lib/RouteTransition.jsx", "frontend/src/lib/ContextFrame.jsx", "frontend/src/pages/Roadmap.js"],
    tests: ["frontend/src/lib/spatial-state.test.js", "frontend/e2e/reduced-motion.spec.js", "frontend/e2e/route-transition.spec.js"],
  },
  LND: {
    implementation: ["frontend/src/pages/Landing.js", "frontend/src/lib/CvlnFocusField.jsx"],
    runtime: ["frontend/src/pages/Landing.js", "frontend/src/App.js"],
    tests: ["frontend/e2e/landing-spatial.spec.js", "frontend/e2e/keyboard-focus.spec.js"],
  },
  NAV: {
    implementation: ["frontend/src/App.js", "frontend/src/lib/RouteTransition.jsx", "frontend/src/lib/depthMemory.js"],
    runtime: ["frontend/src/components/Layout.js", "frontend/src/lib/depthMemory.js"],
    tests: ["frontend/e2e/routing.spec.js", "frontend/e2e/module-journey-navigation.spec.js", "frontend/src/lib/depthMemory.test.js"],
  },
  PRO: {
    implementation: ["backend/api/progression.py", "backend/skills/progression.py", "frontend/src/pages/Roadmap.js"],
    runtime: ["frontend/src/pages/Roadmap.js", "backend/api/progression.py"],
    tests: ["frontend/e2e/roadmap-progression.spec.js", "backend/tests/backend_test.py", "frontend/src/lib/depthMemory.test.js"],
  },
  FMS: {
    implementation: ["backend/fms_lineage/initial_matrix.py", "backend/fms_import/module_map.py", "frontend/src/pages/Formations.js"],
    runtime: ["backend/api/fms.py", "backend/api/fms_lineage.py", "frontend/src/pages/Formations.js"],
    tests: ["backend/tests/test_fms_import.py", "backend/tests/test_fms_lineage.py", "frontend/e2e/formations-discovery.spec.js"],
  },
  LRN: {
    implementation: ["backend/api/learning.py", "frontend/src/pages/ModuleJourney.js", "frontend/src/components/MentorPanel.js"],
    runtime: ["frontend/src/pages/ModuleJourney.js", "backend/api/learning.py"],
    tests: ["frontend/e2e/module-journey-context.spec.js", "frontend/e2e/module-journey-navigation.spec.js", "backend/tests/backend_test.py"],
  },
  ECO: {
    implementation: ["backend/services/integrations/registry.py", "backend/services/frek_core.py", "backend/api/wallet.py"],
    runtime: ["backend/api/integrations.py", "frontend/src/pages/FrekProfile.js", "frontend/src/pages/Wallet.js"],
    tests: ["backend/tests/backend_test.py", "docs/INTEGRATIONS_REPORT.md"],
  },
  TEC: {
    implementation: ["frontend/package.json", "frontend/playwright.config.js", "backend/pytest.ini", "frontend/public/service-worker.js"],
    runtime: ["frontend/src/serviceWorkerRegistration.js", "backend/server.py"],
    tests: ["frontend/e2e/reduced-motion.spec.js", "frontend/e2e/keyboard-focus.spec.js", "backend/tests/backend_test.py"],
  },
  CLD: {
    implementation: ["docs/SPATIAL_LEARNING_W0_AUDIT.md", "docs/SPATIAL_LEARNING_W3E_RUNTIME_PROOF_REPORT.md"],
    runtime: ["docs/SPATIAL_LEARNING_W3E_RUNTIME_PROOF_REPORT.md"],
    tests: ["scripts/spatial-requirements.test.mjs"],
  },
  INT: {
    implementation: ["frontend/src/lib/CvlnFocusField.jsx", "frontend/src/lib/ContextFrame.jsx", "frontend/src/lib/depthMemory.js"],
    runtime: ["frontend/src/pages/Formations.js", "frontend/src/pages/ModuleJourney.js", "frontend/src/components/Layout.js"],
    tests: ["frontend/e2e/keyboard-focus.spec.js", "frontend/e2e/module-journey-context.spec.js", "frontend/src/lib/depthMemory.test.js"],
  },
};

export function prefixFor(id) {
  return id.split("-")[0];
}

export function evidenceFor(id) {
  return EVIDENCE_BY_PREFIX[prefixFor(id)] || null;
}
