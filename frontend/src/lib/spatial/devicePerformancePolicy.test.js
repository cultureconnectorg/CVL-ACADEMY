import {
  SPATIAL_QUALITY,
  detectSpatialQuality,
  spatialQualityFromCapabilities,
  spatialQualityProfile,
} from "./devicePerformancePolicy";

describe("devicePerformancePolicy", () => {
  test("unknown capability hints fail open to full fidelity", () => {
    expect(spatialQualityFromCapabilities()).toBe(SPATIAL_QUALITY.FULL);
  });

  test("explicit data saver selects lite ambient work", () => {
    expect(spatialQualityFromCapabilities({ saveData: true, deviceMemory: 8, hardwareConcurrency: 8 }))
      .toBe(SPATIAL_QUALITY.LITE);
  });

  test("low memory or low core count selects lite", () => {
    expect(spatialQualityFromCapabilities({ deviceMemory: 2, hardwareConcurrency: 8 }))
      .toBe(SPATIAL_QUALITY.LITE);
    expect(spatialQualityFromCapabilities({ deviceMemory: 8, hardwareConcurrency: 2 }))
      .toBe(SPATIAL_QUALITY.LITE);
  });

  test("mid-range devices keep balanced spatial motion", () => {
    expect(spatialQualityFromCapabilities({ deviceMemory: 4, hardwareConcurrency: 8 }))
      .toBe(SPATIAL_QUALITY.BALANCED);
    expect(spatialQualityFromCapabilities({ deviceMemory: 8, hardwareConcurrency: 4 }))
      .toBe(SPATIAL_QUALITY.BALANCED);
  });

  test("coarse small-screen devices select lite even when browser memory hints are missing", () => {
    const nav = { hardwareConcurrency: 6 };
    const win = {
      innerWidth: 390,
      matchMedia: () => ({ matches: true }),
    };
    expect(detectSpatialQuality(nav, win)).toBe(SPATIAL_QUALITY.LITE);
  });

  test("coarse large-screen devices keep balanced rendering", () => {
    const nav = { hardwareConcurrency: 8 };
    const win = {
      innerWidth: 1024,
      matchMedia: () => ({ matches: true }),
    };
    expect(detectSpatialQuality(nav, win)).toBe(SPATIAL_QUALITY.BALANCED);
  });

  test("desktop-class clients retain full rendering", () => {
    const nav = { deviceMemory: 8, hardwareConcurrency: 8 };
    const win = {
      innerWidth: 1440,
      matchMedia: () => ({ matches: false }),
    };
    expect(detectSpatialQuality(nav, win)).toBe(SPATIAL_QUALITY.FULL);
  });

  test("quality profiles only scale perception, never domain semantics", () => {
    expect(spatialQualityProfile(SPATIAL_QUALITY.LITE)).toMatchObject({
      motionScale: 0.38,
      pointerScale: 0.32,
    });
    expect(spatialQualityProfile(SPATIAL_QUALITY.FULL).motionScale).toBe(1);
  });
});
