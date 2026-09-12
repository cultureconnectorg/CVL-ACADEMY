import { signalForApiResponse, SPATIAL_SIGNAL_TYPES } from "./spatialLearningSignals";

describe("spatialLearningSignals", () => {
  test("maps module phase progress", () => {
    expect(signalForApiResponse({ config: { method: "post", url: "/modules/FMS/M01/phase" }, data: {} })?.type).toBe(SPATIAL_SIGNAL_TYPES.LEARNING_PROGRESS);
  });

  test("maps quiz pass and retry without punitive semantics", () => {
    expect(signalForApiResponse({ config: { method: "post", url: "/formations/FMS/modules/M01/quiz/submit" }, data: { passed: true } })?.type).toBe(SPATIAL_SIGNAL_TYPES.ASSESSMENT_PASSED);
    expect(signalForApiResponse({ config: { method: "post", url: "/formations/FMS/modules/M01/quiz/submit" }, data: { passed: false } })?.type).toBe(SPATIAL_SIGNAL_TYPES.ASSESSMENT_RETRY);
  });

  test("maps mission completion", () => {
    expect(signalForApiResponse({ config: { method: "post", url: "/missions/STUDIO-01/submit" }, data: {} })?.type).toBe(SPATIAL_SIGNAL_TYPES.MISSION_COMPLETED);
  });

  test("ignores unrelated API responses", () => {
    expect(signalForApiResponse({ config: { method: "get", url: "/health/ready" }, data: {} })).toBeNull();
  });
});
