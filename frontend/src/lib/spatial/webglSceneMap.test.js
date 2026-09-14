import fs from "fs";
import path from "path";
import { BACKGROUND_BY_SCENE, RESERVED_BACKGROUNDS, backgroundForNode } from "./webglSceneMap";

describe("backgroundForNode", () => {
  test("returns null for an unknown or missing node", () => {
    expect(backgroundForNode(null)).toBeNull();
    expect(backgroundForNode("NOT_A_SCENE")).toBeNull();
  });

  test("without a viewport width, returns the full-resolution desktop asset", () => {
    expect(backgroundForNode("DASHBOARD")).toBe("/spatial/backgrounds/03_Dashboard.webp");
  });

  test("a wide viewport still gets the desktop asset", () => {
    expect(backgroundForNode("DASHBOARD", { viewportWidth: 1440 })).toBe(
      "/spatial/backgrounds/03_Dashboard.webp"
    );
  });

  test("a narrow (mobile) viewport gets the lighter -mobile asset", () => {
    expect(backgroundForNode("DASHBOARD", { viewportWidth: 390 })).toBe(
      "/spatial/backgrounds/03_Dashboard-mobile.webp"
    );
  });

  test("exactly at the breakpoint still counts as mobile", () => {
    expect(backgroundForNode("DASHBOARD", { viewportWidth: 900 })).toBe(
      "/spatial/backgrounds/03_Dashboard-mobile.webp"
    );
  });

  test("an invalid viewportWidth falls back to the desktop asset", () => {
    expect(backgroundForNode("DASHBOARD", { viewportWidth: 0 })).toBe(
      "/spatial/backgrounds/03_Dashboard.webp"
    );
    expect(backgroundForNode("DASHBOARD", { viewportWidth: NaN })).toBe(
      "/spatial/backgrounds/03_Dashboard.webp"
    );
  });

  // Guards the assumption every call site relies on: a "-mobile" sibling
  // actually ships in public/ for every desktop asset this map can return.
  test("every mapped photograph has a real -mobile sibling on disk", () => {
    const publicDir = path.join(__dirname, "..", "..", "..", "public");
    const allUrls = [...Object.values(BACKGROUND_BY_SCENE), ...Object.values(RESERVED_BACKGROUNDS)];
    const uniqueUrls = [...new Set(allUrls)];
    expect(uniqueUrls.length).toBeGreaterThan(0);
    for (const url of uniqueUrls) {
      const desktopPath = path.join(publicDir, url);
      const mobilePath = path.join(publicDir, url.replace(/\.webp$/, "-mobile.webp"));
      expect(fs.existsSync(desktopPath)).toBe(true);
      expect(fs.existsSync(mobilePath)).toBe(true);
    }
  });
});
