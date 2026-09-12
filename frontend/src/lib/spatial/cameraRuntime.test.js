import { consumePendingCameraIntent, readPendingCameraIntent } from "./cameraRuntime";

function memoryStorage(initial = {}) {
  const map = new Map(Object.entries(initial));
  return {
    getItem: (key) => map.get(key) ?? null,
    setItem: (key, value) => map.set(key, String(value)),
    removeItem: (key) => map.delete(key),
  };
}

describe("cameraRuntime pending intent", () => {
  test("reads only a valid camera intent", () => {
    const storage = memoryStorage({
      "cvln:spatial-camera-intent:v1": JSON.stringify({
        anchorId: "module-M01",
        sourceRoute: "/dashboard",
        destinationRoute: "/formations/FMS-01/modules/M01",
      }),
    });
    expect(readPendingCameraIntent(storage)).toMatchObject({ anchorId: "module-M01" });
  });

  test("consume is one-shot", () => {
    const storage = memoryStorage({
      "cvln:spatial-camera-intent:v1": JSON.stringify({
        anchorId: "module-M01",
        sourceRoute: "/dashboard",
        destinationRoute: "/formations/FMS-01/modules/M01",
      }),
    });
    expect(consumePendingCameraIntent(storage)?.anchorId).toBe("module-M01");
    expect(readPendingCameraIntent(storage)).toBeNull();
  });

  test("invalid storage never fabricates an intent", () => {
    const storage = memoryStorage({ "cvln:spatial-camera-intent:v1": "{}" });
    expect(readPendingCameraIntent(storage)).toBeNull();
  });
});
