export const SPATIAL_QUALITY = Object.freeze({
  FULL: "full",
  BALANCED: "balanced",
  LITE: "lite",
});

function finitePositive(value) {
  return Number.isFinite(value) && value > 0 ? value : null;
}

/**
 * Conservative client capability policy. Unknown browser hints never degrade
 * quality. Data Saver is treated as an explicit resource preference, while
 * deviceMemory/hardwareConcurrency only lower ambient visual work — never
 * navigation, content, focus, unlock rules, or domain state.
 */
export function spatialQualityFromCapabilities({
  deviceMemory = null,
  hardwareConcurrency = null,
  saveData = false,
} = {}) {
  const memory = finitePositive(deviceMemory);
  const cores = finitePositive(hardwareConcurrency);

  if (saveData || (memory !== null && memory <= 2) || (cores !== null && cores <= 2)) {
    return SPATIAL_QUALITY.LITE;
  }
  if ((memory !== null && memory <= 4) || (cores !== null && cores <= 4)) {
    return SPATIAL_QUALITY.BALANCED;
  }
  return SPATIAL_QUALITY.FULL;
}

function pointerIsCoarse(win) {
  try {
    return Boolean(win?.matchMedia?.("(pointer: coarse)")?.matches);
  } catch {
    return false;
  }
}

/**
 * Browser hints such as navigator.deviceMemory are missing on iOS Safari.
 * Without a fallback, phones can therefore be misclassified as FULL and pay
 * for every ambient animation/filter. Viewport + coarse-pointer detection is
 * used only as a rendering-cost fallback; application behavior is unchanged.
 */
export function detectSpatialQuality(
  nav = typeof navigator !== "undefined" ? navigator : null,
  win = typeof window !== "undefined" ? window : null
) {
  const capabilityQuality = spatialQualityFromCapabilities({
    deviceMemory: nav?.deviceMemory,
    hardwareConcurrency: nav?.hardwareConcurrency,
    saveData: Boolean(nav?.connection?.saveData),
  });

  if (capabilityQuality === SPATIAL_QUALITY.LITE) return capabilityQuality;

  const width = finitePositive(win?.innerWidth);
  const coarse = pointerIsCoarse(win);

  if (coarse && width !== null && width <= 900) return SPATIAL_QUALITY.LITE;
  if (coarse || (width !== null && width <= 768)) return SPATIAL_QUALITY.BALANCED;

  return capabilityQuality;
}

/**
 * WebGL-specific tier (frontend/src/lib/spatial/webglEngine.js). Unlike
 * detectSpatialQuality — which the CSS/SVG world's ambient-animation cost
 * model conservatively forces to LITE for ANY narrow touch device
 * regardless of real capability, the fix for the mobile freeze (2ae1282)
 * — a single textured WebGL plane with no bloom/near-layer is cheap
 * enough that a genuinely capable phone should not be excluded outright.
 * Real capability (deviceMemory/hardwareConcurrency/saveData) still gates
 * LITE here exactly as it does above: weak hardware never gets WebGL,
 * full stop. A capable device on a coarse (touch) pointer is capped at
 * BALANCED, never FULL — webglEngine.js only builds the near-layer
 * parallax plane and enables UnrealBloomPass at FULL, so this keeps
 * every touch device unconditionally on the cheap single-plane,
 * no-bloom path regardless of how capable it is. Viewport width is
 * deliberately not consulted here (unlike detectSpatialQuality): a
 * narrow *desktop* browser window with a mouse is not battery/thermal
 * constrained, so it keeps its real capability tier.
 */
export function detectWebglQuality(
  nav = typeof navigator !== "undefined" ? navigator : null,
  win = typeof window !== "undefined" ? window : null
) {
  const capabilityQuality = spatialQualityFromCapabilities({
    deviceMemory: nav?.deviceMemory,
    hardwareConcurrency: nav?.hardwareConcurrency,
    saveData: Boolean(nav?.connection?.saveData),
  });

  if (capabilityQuality === SPATIAL_QUALITY.LITE) return capabilityQuality;
  if (pointerIsCoarse(win)) return SPATIAL_QUALITY.BALANCED;
  return capabilityQuality;
}

export function spatialQualityProfile(quality) {
  if (quality === SPATIAL_QUALITY.LITE) {
    return Object.freeze({ motionScale: 0.38, pointerScale: 0.32, atmosphereScale: 0.72, breathScale: 0.34 });
  }
  if (quality === SPATIAL_QUALITY.BALANCED) {
    return Object.freeze({ motionScale: 0.72, pointerScale: 0.68, atmosphereScale: 0.88, breathScale: 0.7 });
  }
  return Object.freeze({ motionScale: 1, pointerScale: 1, atmosphereScale: 1, breathScale: 1 });
}
