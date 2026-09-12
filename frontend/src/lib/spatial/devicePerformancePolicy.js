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

export function detectSpatialQuality(nav = typeof navigator !== "undefined" ? navigator : null) {
  if (!nav) return SPATIAL_QUALITY.FULL;
  return spatialQualityFromCapabilities({
    deviceMemory: nav.deviceMemory,
    hardwareConcurrency: nav.hardwareConcurrency,
    saveData: Boolean(nav.connection?.saveData),
  });
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
