import { experienceStateForNode } from "@/lib/spatial/experienceState";
import { spatialSignalProfile } from "@/lib/spatial/spatialLearningSignals";

/**
 * Spatial Director
 *
 * DOMAIN_STATE != SPATIAL_STATE. Backend/domain state remains authoritative.
 * This director translates trusted route state plus short-lived learning
 * signals into perceptual controls. H0.10 physics/attention stay authoritative
 * for motion mechanics; this file does not create a second physics engine.
 */
export function directSpatialExperience({ node, scene, reducedMotion = false, signal = null }) {
  const baseline = experienceStateForNode(node);
  const transient = spatialSignalProfile(signal?.type);
  const experience = transient
    ? {
        ...baseline,
        intent: transient.intent,
        learningState: transient.learningState,
        intensity: transient.intensity,
        attention: transient.attention,
      }
    : baseline;

  const motionIntensity = reducedMotion ? 0 : experience.intensity;
  const focusStrength = experience.attention;

  return {
    ...experience,
    signalType: transient?.type || null,
    signalTtlMs: transient?.ttlMs || 0,
    motionIntensity,
    focusStrength,
    camera: scene.camera,
    depth: scene.depth,
    scale: scene.scale,
    light: scene.light,
    warmth: scene.warmth,
    vignette: scene.vignette,
    focusX: scene.focusX,
    focusY: scene.focusY,
    pointerRangeX: reducedMotion ? 0 : 4 + motionIntensity * 16,
    pointerRangeY: reducedMotion ? 0 : 3 + motionIntensity * 11,
    atmosphereOpacity: transient?.atmosphereOpacity ?? 0.14 + motionIntensity * 0.42,
    worldBreath: reducedMotion ? 0 : transient?.worldBreath ?? (node === "MODULE" ? 0.08 : 0.34 + motionIntensity * 0.36),
  };
}
