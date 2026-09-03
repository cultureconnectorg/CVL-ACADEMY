import { FEATURE_FLAGS, readFeatureFlag } from "./featureFlags";

const FLAG_NAMES = [
  "SPATIAL_ENGINE",
  "SPATIAL_ROUTE_TRANSITIONS",
  "SPATIAL_ENVIRONMENT",
  "SPATIAL_AUDIO",
  "SPATIAL_HAPTICS",
  "SPATIAL_DEBUG",
  "LIFECYCLE_RUNTIME",
];

describe("featureFlags.js", () => {
  const originalEnv = { ...process.env };
  afterEach(() => {
    process.env = { ...originalEnv };
  });

  test("every flag defaults to false when unset — OFF = current production behavior", () => {
    FLAG_NAMES.forEach((name) => {
      delete process.env[`REACT_APP_ACADEMY_${name}`];
    });
    FLAG_NAMES.forEach((name) => {
      expect(FEATURE_FLAGS[name]).toBe(false);
    });
  });

  test("an unrecognized/garbage value reads as false, never throws", () => {
    process.env.REACT_APP_ACADEMY_SPATIAL_ENGINE = "yes-please";
    expect(FEATURE_FLAGS.SPATIAL_ENGINE).toBe(false);
  });

  test("'true' or '1' turns a flag on, read live (not cached at import time)", () => {
    process.env.REACT_APP_ACADEMY_SPATIAL_ENGINE = "true";
    expect(FEATURE_FLAGS.SPATIAL_ENGINE).toBe(true);
    process.env.REACT_APP_ACADEMY_SPATIAL_ENGINE = "false";
    expect(FEATURE_FLAGS.SPATIAL_ENGINE).toBe(false);
    process.env.REACT_APP_ACADEMY_SPATIAL_ENGINE = "1";
    expect(FEATURE_FLAGS.SPATIAL_ENGINE).toBe(true);
  });

  test("readFeatureFlag matches the FEATURE_FLAGS getter for the same name", () => {
    process.env.REACT_APP_ACADEMY_SPATIAL_DEBUG = "true";
    expect(readFeatureFlag("SPATIAL_DEBUG")).toBe(true);
    expect(readFeatureFlag("SPATIAL_DEBUG")).toBe(FEATURE_FLAGS.SPATIAL_DEBUG);
  });

  test("flags are independent — enabling one never enables another", () => {
    process.env.REACT_APP_ACADEMY_SPATIAL_AUDIO = "true";
    expect(FEATURE_FLAGS.SPATIAL_AUDIO).toBe(true);
    expect(FEATURE_FLAGS.SPATIAL_HAPTICS).toBe(false);
    expect(FEATURE_FLAGS.SPATIAL_ENGINE).toBe(false);
  });
});
