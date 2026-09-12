import {
  armReturnPositionRestore,
  consumeReturnPositionRestore,
  isRestorablePath,
  loadReturnPosition,
  resumeHref,
  returnPositionUserKey,
  saveReturnPosition,
} from "./returnPosition";

function memoryStorage() {
  const map = new Map();
  return {
    getItem: (key) => map.get(key) ?? null,
    setItem: (key, value) => map.set(key, String(value)),
    removeItem: (key) => map.delete(key),
  };
}

describe("returnPosition", () => {
  test("scopes memory to a real user identity", () => {
    expect(returnPositionUserKey({ id: "u1", frek_id: "f1" })).toBe("u1");
    expect(returnPositionUserKey({ frek_id: "f1" })).toBe("f1");
    expect(returnPositionUserKey(null)).toBeNull();
  });

  test("accepts learner routes and rejects legal/admin surfaces", () => {
    expect(isRestorablePath("/formations/FMS-01/modules/M01")).toBe(true);
    expect(isRestorablePath("/roadmap")).toBe(true);
    expect(isRestorablePath("/legal/privacy")).toBe(false);
    expect(isRestorablePath("/admin")).toBe(false);
  });

  test("round-trips scroll, focus, rail and camera context", () => {
    const storage = memoryStorage();
    const snapshot = {
      pathname: "/formations/FMS-01/modules/M01",
      search: "?phase=2",
      scrollY: 734,
      focusId: "phase-deliverable",
      railOffset: 288,
      camera: { node: "MODULE", camera: "enter", depth: 4 },
    };

    expect(saveReturnPosition("u1", snapshot, storage)).toBe(true);
    const loaded = loadReturnPosition("u1", storage);
    expect(loaded).toMatchObject(snapshot);
    expect(resumeHref(loaded)).toBe("/formations/FMS-01/modules/M01?phase=2");
  });

  test("resume intent is one-shot", () => {
    const storage = memoryStorage();
    expect(armReturnPositionRestore("u1", storage)).toBe(true);
    expect(consumeReturnPositionRestore("u1", storage)).toBe(true);
    expect(consumeReturnPositionRestore("u1", storage)).toBe(false);
  });

  test("never persists an unknown path", () => {
    const storage = memoryStorage();
    expect(saveReturnPosition("u1", { pathname: "/admin", scrollY: 10 }, storage)).toBe(false);
    expect(loadReturnPosition("u1", storage)).toBeNull();
  });
});
