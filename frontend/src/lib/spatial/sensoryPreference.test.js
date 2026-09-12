import {
  readSpatialSensoryOptIn,
  writeSpatialSensoryOptIn,
  SPATIAL_SENSORY_STORAGE_KEY,
} from "./sensoryPreference";

function memoryStorage(initial = {}) {
  const map = new Map(Object.entries(initial));
  return {
    getItem: (key) => map.get(key) ?? null,
    setItem: (key, value) => map.set(key, String(value)),
  };
}

describe("Spatial sensory preference", () => {
  test("defaults to opt-out when no explicit consent exists", () => {
    expect(readSpatialSensoryOptIn(memoryStorage())).toBe(false);
  });

  test("persists only an explicit boolean opt-in", () => {
    const storage = memoryStorage();
    expect(writeSpatialSensoryOptIn(true, storage)).toBe(true);
    expect(storage.getItem(SPATIAL_SENSORY_STORAGE_KEY)).toBe("true");
    expect(readSpatialSensoryOptIn(storage)).toBe(true);

    expect(writeSpatialSensoryOptIn(false, storage)).toBe(false);
    expect(storage.getItem(SPATIAL_SENSORY_STORAGE_KEY)).toBe("false");
    expect(readSpatialSensoryOptIn(storage)).toBe(false);
  });

  test("blocked storage fails closed", () => {
    const blocked = {
      getItem() { throw new Error("blocked"); },
      setItem() { throw new Error("blocked"); },
    };
    expect(readSpatialSensoryOptIn(blocked)).toBe(false);
    expect(writeSpatialSensoryOptIn(true, blocked)).toBe(true);
  });
});
