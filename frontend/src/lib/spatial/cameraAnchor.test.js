import {
  CAMERA_PHASES,
  anchorSelector,
  cameraOriginFromRect,
  createCameraIntentController,
  makeAnchorContract,
  nextCameraPhase,
} from "./cameraAnchor";

describe("cameraAnchor", () => {
  test("builds an immutable H0.8 camera contract", () => {
    const contract = makeAnchorContract({
      anchorId: "module-current",
      sourceRoute: "/roadmap",
      destinationRoute: "/formations/FMS-01/modules/M01",
      sourceRect: { left: 20, top: 40, width: 200, height: 80 },
      depthFrom: 2,
      depthTarget: 4,
    });
    expect(contract).toMatchObject({
      anchorId: "module-current",
      sourceRoute: "/roadmap",
      destinationRoute: "/formations/FMS-01/modules/M01",
      depthFrom: 2,
      depthTarget: 4,
      returnPath: "exact-return",
      reducedMotionFallback: "crossfade",
    });
    expect(Object.isFrozen(contract)).toBe(true);
  });

  test("fails safe when required route identity is missing", () => {
    expect(makeAnchorContract({ anchorId: "x", sourceRoute: "/roadmap" })).toBeNull();
  });

  test("computes camera origin from a real anchor rectangle", () => {
    expect(
      cameraOriginFromRect(
        { left: 400, top: 300, width: 200, height: 100 },
        { width: 1000, height: 800 }
      )
    ).toEqual({ x: 50, y: 43.75 });
  });

  test("latest intent wins and stale camera work is discarded", () => {
    const camera = createCameraIntentController();
    const first = camera.begin();
    const second = camera.begin();
    expect(camera.isCurrent(first)).toBe(false);
    expect(camera.isCurrent(second)).toBe(true);
    expect(camera.setPhase(first, CAMERA_PHASES.FOLLOWING)).toBe(false);
    expect(camera.setPhase(second, CAMERA_PHASES.LOCKING)).toBe(true);
    expect(camera.phase).toBe(CAMERA_PHASES.LOCKING);
  });

  test("preserves the H0.8 forward phase ordering", () => {
    expect(nextCameraPhase(CAMERA_PHASES.INTENT)).toBe(CAMERA_PHASES.LOCKING);
    expect(nextCameraPhase(CAMERA_PHASES.LOCKING)).toBe(CAMERA_PHASES.FOLLOWING);
    expect(nextCameraPhase(CAMERA_PHASES.FOLLOWING)).toBe(CAMERA_PHASES.CROSSING);
    expect(nextCameraPhase(CAMERA_PHASES.CROSSING)).toBe(CAMERA_PHASES.REVEALING);
    expect(nextCameraPhase(CAMERA_PHASES.REVEALING)).toBe(CAMERA_PHASES.SETTLING);
    expect(nextCameraPhase(CAMERA_PHASES.SETTLING)).toBe(CAMERA_PHASES.IDLE);
  });

  test("creates stable DOM selectors for source/destination anchors", () => {
    expect(anchorSelector("module-current", "source")).toBe(
      '[data-spatial-anchor="module-current"][data-spatial-anchor-role="source"]'
    );
  });
});
