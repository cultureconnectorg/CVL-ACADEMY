import { sceneForPathname } from "@/lib/spatial/worldSceneMap";

describe("worldSceneMap", () => {
  test("maps the core learning journey to increasing depth", () => {
    const landing = sceneForPathname("/");
    const onboarding = sceneForPathname("/onboarding");
    const dashboard = sceneForPathname("/dashboard");
    const formations = sceneForPathname("/formations");
    const formation = sceneForPathname("/formations/MUSIC-BUSINESS");
    const module = sceneForPathname("/formations/MUSIC-BUSINESS/modules/M01");

    expect(landing.node).toBe("LANDING");
    expect(onboarding.node).toBe("ONBOARDING");
    expect(dashboard.node).toBe("DASHBOARD");
    expect(formations.node).toBe("FORMATIONS");
    expect(formation.node).toBe("FORMATION");
    expect(module.node).toBe("MODULE");

    expect(onboarding.scene.depth).toBeGreaterThan(landing.scene.depth);
    expect(formation.scene.depth).toBeGreaterThan(formations.scene.depth);
    expect(module.scene.depth).toBeGreaterThan(formation.scene.depth);
  });

  test("preserves lateral destinations at hub depth", () => {
    const dashboardDepth = sceneForPathname("/dashboard").scene.depth;
    expect(sceneForPathname("/roadmap").scene.depth).toBe(dashboardDepth);
    expect(sceneForPathname("/missions").scene.depth).toBe(dashboardDepth);
    expect(sceneForPathname("/badges").scene.depth).toBe(dashboardDepth);
    expect(sceneForPathname("/wallet").scene.depth).toBe(dashboardDepth);
  });

  test("fails safe for routes outside the Spatial topology", () => {
    const legal = sceneForPathname("/legal/privacy");
    expect(legal.node).toBeNull();
    expect(legal.scene.camera).toBe("static");
    expect(legal.scene.zone).toBe("neutral");
  });
});
