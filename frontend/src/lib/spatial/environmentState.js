export const STADE_ENVIRONMENT = Object.freeze({
  graine: { density: 0.18, growth: 0.12, glow: 0.78, horizon: 0.9 },
  pousse: { density: 0.32, growth: 0.28, glow: 0.86, horizon: 0.94 },
  racine: { density: 0.48, growth: 0.44, glow: 0.94, horizon: 0.98 },
  branches: { density: 0.64, growth: 0.62, glow: 1.02, horizon: 1.02 },
  arbre: { density: 0.82, growth: 0.8, glow: 1.1, horizon: 1.06 },
  foret: { density: 1, growth: 1, glow: 1.18, horizon: 1.1 },
});

const FALLBACK = Object.freeze({
  stade: "graine",
  ...STADE_ENVIRONMENT.graine,
});

/**
 * Converts the real domain stade into perceptual environment controls.
 * It never mutates progression and never guesses an unknown stade.
 */
export function environmentForStade(stade) {
  if (!stade || !STADE_ENVIRONMENT[stade]) return FALLBACK;
  return Object.freeze({ stade, ...STADE_ENVIRONMENT[stade] });
}
