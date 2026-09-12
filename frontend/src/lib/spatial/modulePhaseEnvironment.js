export const MODULE_PHASE_ENVIRONMENT = Object.freeze({
  hook: Object.freeze({ activity: 0.72, focus: 0.62, depth: 0.58, warmth: 0.9 }),
  objectives: Object.freeze({ activity: 0.58, focus: 0.76, depth: 0.68, warmth: 0.92 }),
  course: Object.freeze({ activity: 0.22, focus: 0.98, depth: 0.86, warmth: 0.78 }),
  workshop: Object.freeze({ activity: 0.48, focus: 0.88, depth: 0.76, warmth: 0.94 }),
  deliverable: Object.freeze({ activity: 0.36, focus: 0.94, depth: 0.82, warmth: 0.9 }),
  quiz: Object.freeze({ activity: 0.14, focus: 1, depth: 0.9, warmth: 0.74 }),
  mini_mission: Object.freeze({ activity: 0.52, focus: 0.9, depth: 0.8, warmth: 1 }),
});

export function environmentForModulePhase(phase) {
  return MODULE_PHASE_ENVIRONMENT[phase] || null;
}
