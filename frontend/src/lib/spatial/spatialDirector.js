import { experienceStateForNode } from "@/lib/spatial/experienceState";

/**
 * Spatial Director
 *
 * Translates product/learning state into perceptual controls. Routing remains
 * authoritative in routeTopologyMap/worldSceneMap; this layer only decides how
 * strongly the world should respond to the current state.
 */
export function directSpatialExperience({ node, scene, reducedMotion = false }) {
  const experience = experienceStateForNode(node);
  const motionIntensity = reducedMotion ? 0 : experience.intensity;
  const focusStrength = experience.attention;

  return {
    ...experience,
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
    pointerRangeX: 4 + motionIntensity * 16,
    pointerRangeY: 3 + motionIntensity * 11,
    springResponse: 0.025 + motionIntensity * 0.045,
    atmosphereOpacity: 0.14 + motionIntensity * 0.42,
    worldBreath: node === "MODULE" ? 0.08 : 0.34 + motionIntensity * 0.36,
  };
}
