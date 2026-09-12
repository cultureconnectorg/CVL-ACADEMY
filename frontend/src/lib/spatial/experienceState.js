export const EXPERIENCE_INTENTS = Object.freeze({
  DISCOVER: "DISCOVER",
  ORIENT: "ORIENT",
  COMMIT: "COMMIT",
  LEARN: "LEARN",
  PRACTICE: "PRACTICE",
  PROVE: "PROVE",
  MONETIZE: "MONETIZE",
  RETURN: "RETURN",
});

export const LEARNING_STATES = Object.freeze({
  DISCOVERY: "DISCOVERY",
  ORIENTATION: "ORIENTATION",
  ACTIVE_PATH: "ACTIVE_PATH",
  DEEP_FOCUS: "DEEP_FOCUS",
  ACTION: "ACTION",
  ACHIEVEMENT: "ACHIEVEMENT",
  VALUE: "VALUE",
  IDENTITY: "IDENTITY",
});

const NODE_STATE = Object.freeze({
  LANDING: { intent: EXPERIENCE_INTENTS.DISCOVER, learningState: LEARNING_STATES.DISCOVERY, intensity: 0.78, attention: 0.45 },
  ONBOARDING: { intent: EXPERIENCE_INTENTS.ORIENT, learningState: LEARNING_STATES.ORIENTATION, intensity: 0.72, attention: 0.58 },
  DASHBOARD: { intent: EXPERIENCE_INTENTS.ORIENT, learningState: LEARNING_STATES.ACTIVE_PATH, intensity: 0.62, attention: 0.68 },
  FORMATIONS: { intent: EXPERIENCE_INTENTS.DISCOVER, learningState: LEARNING_STATES.ACTIVE_PATH, intensity: 0.66, attention: 0.62 },
  FORMATION: { intent: EXPERIENCE_INTENTS.COMMIT, learningState: LEARNING_STATES.ACTIVE_PATH, intensity: 0.58, attention: 0.78 },
  MODULE: { intent: EXPERIENCE_INTENTS.LEARN, learningState: LEARNING_STATES.DEEP_FOCUS, intensity: 0.18, attention: 0.96 },
  ROADMAP: { intent: EXPERIENCE_INTENTS.ORIENT, learningState: LEARNING_STATES.ACTIVE_PATH, intensity: 0.54, attention: 0.66 },
  MISSIONS_LIST: { intent: EXPERIENCE_INTENTS.PRACTICE, learningState: LEARNING_STATES.ACTION, intensity: 0.7, attention: 0.74 },
  BADGES: { intent: EXPERIENCE_INTENTS.PROVE, learningState: LEARNING_STATES.ACHIEVEMENT, intensity: 0.6, attention: 0.72 },
  SKILLS: { intent: EXPERIENCE_INTENTS.PROVE, learningState: LEARNING_STATES.ACHIEVEMENT, intensity: 0.48, attention: 0.8 },
  CERTIFICATIONS: { intent: EXPERIENCE_INTENTS.PROVE, learningState: LEARNING_STATES.ACHIEVEMENT, intensity: 0.5, attention: 0.82 },
  WALLET: { intent: EXPERIENCE_INTENTS.MONETIZE, learningState: LEARNING_STATES.VALUE, intensity: 0.42, attention: 0.82 },
  FREK_PROFILE: { intent: EXPERIENCE_INTENTS.RETURN, learningState: LEARNING_STATES.IDENTITY, intensity: 0.36, attention: 0.88 },
});

export function experienceStateForNode(node) {
  return NODE_STATE[node] || {
    intent: EXPERIENCE_INTENTS.ORIENT,
    learningState: LEARNING_STATES.ORIENTATION,
    intensity: 0.3,
    attention: 0.7,
  };
}
