import {
  consumeArmedCameraReturn,
  consumePendingCameraIntent,
  readArmedCameraReturn,
  readPendingCameraIntent,
  readReturnCameraContract,
  snapshotSharedElement,
} from "./cameraRuntime";

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

  test("return contract is validated separately from pending forward intent", () => {
    const storage = memoryStorage({
      "cvln:spatial-camera-return:v1": JSON.stringify({
        anchorId: "module-M01",
        sourceRoute: "/formations/FMS-01",
        destinationRoute: "/formations/FMS-01/modules/M01",
      }),
    });
    expect(readReturnCameraContract(storage)).toMatchObject({ sourceRoute: "/formations/FMS-01" });
    expect(readPendingCameraIntent(storage)).toBeNull();
  });

  test("armed return is consumed once and clears the stored return contract", () => {
    const contract = {
      anchorId: "module-M01",
      sourceRoute: "/dashboard",
      destinationRoute: "/formations/FMS-01/modules/M01",
    };
    const storage = memoryStorage({
      "cvln:spatial-camera-return:v1": JSON.stringify(contract),
      "cvln:spatial-camera-return-armed:v1": JSON.stringify(contract),
    });
    expect(readArmedCameraReturn(storage)).toMatchObject(contract);
    expect(consumeArmedCameraReturn(storage)).toMatchObject(contract);
    expect(readArmedCameraReturn(storage)).toBeNull();
    expect(readReturnCameraContract(storage)).toBeNull();
  });

  test("shared element snapshot keeps only perceptual geometry and typography", () => {
    const element = document.createElement("h3");
    element.textContent = "Fixture Formation";
    element.style.color = "rgb(10, 20, 30)";
    element.style.fontSize = "20px";
    element.style.fontWeight = "700";
    element.getBoundingClientRect = () => ({
      x: 10, y: 20, left: 10, top: 20, right: 210, bottom: 60,
      width: 200, height: 40,
    });
    document.body.appendChild(element);

    const snapshot = snapshotSharedElement(element);
    expect(snapshot).toMatchObject({
      text: "Fixture Formation",
      rect: { left: 10, top: 20, width: 200, height: 40 },
      color: "rgb(10, 20, 30)",
      fontSize: "20px",
      fontWeight: "700",
    });
    element.remove();
  });
});
