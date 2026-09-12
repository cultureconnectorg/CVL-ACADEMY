import { directSpatialExperience } from "./spatialDirector";
import { SPATIAL_SIGNAL_TYPES } from "./spatialLearningSignals";
import { WORLD_SCENES } from "./worldSceneMap";

describe("spatialDirector", () => {
  test("module baseline is calm and focused", () => {
    const result = directSpatialExperience({ node: "MODULE", scene: WORLD_SCENES.MODULE });
    expect(result.learningState).toBe("DEEP_FOCUS");
    expect(result.motionIntensity).toBe(0.18);
    expect(result.focusStrength).toBe(0.96);
    expect(result.signalType).toBeNull();
  });

  test("trusted learning signal temporarily overrides perception only", () => {
    const result = directSpatialExperience({ node: "MODULE", scene: WORLD_SCENES.MODULE, signal: { type: SPATIAL_SIGNAL_TYPES.MODULE_VALIDATED } });
    expect(result.signalType).toBe(SPATIAL_SIGNAL_TYPES.MODULE_VALIDATED);
    expect(result.learningState).toBe("ACHIEVEMENT");
    expect(result.motionIntensity).toBe(0.72);
    expect(result.camera).toBe(WORLD_SCENES.MODULE.camera);
    expect(result.depth).toBe(WORLD_SCENES.MODULE.depth);
  });

  test("reduced motion always wins over transient signal", () => {
    const result = directSpatialExperience({ node: "MODULE", scene: WORLD_SCENES.MODULE, reducedMotion: true, signal: { type: SPATIAL_SIGNAL_TYPES.MODULE_VALIDATED } });
    expect(result.motionIntensity).toBe(0);
    expect(result.pointerRangeX).toBe(0);
    expect(result.pointerRangeY).toBe(0);
    expect(result.worldBreath).toBe(0);
  });
});
