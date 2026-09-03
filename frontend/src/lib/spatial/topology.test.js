import { TOPOLOGY_NODES, resolveEdge, hasDeclaredEdge } from "./topology";

describe("topology.js", () => {
  test("every declared node is a real mission §7 concept, route is either a string or explicitly null", () => {
    Object.values(TOPOLOGY_NODES).forEach((node) => {
      expect(node.route === null || typeof node.route === "string").toBe(true);
    });
  });

  test("a valid, explicitly declared forward edge resolves with real metadata", () => {
    const edge = resolveEdge("LANDING", "SIGNUP");
    expect(edge.declared).toBe(true);
    expect(edge.direction).toBe("forward");
    expect(edge.spatialDirection).toBe("lateral");
  });

  test("a declared deeper edge inverts to shallower on the return direction", () => {
    const forward = resolveEdge("ONBOARDING", "ACTIVATION");
    expect(forward.spatialDirection).toBe("deeper");
    const back = resolveEdge("ACTIVATION", "ONBOARDING");
    expect(back.declared).toBe(true);
    expect(back.direction).toBe("return");
    expect(back.spatialDirection).toBe("shallower");
    // depth/entry roles swap too, consistent with reversing direction
    expect(back.sourceDepth).toBe(forward.destinationDepth);
    expect(back.destinationDepth).toBe(forward.sourceDepth);
  });

  test("a lateral edge's inverse is still lateral", () => {
    const forward = resolveEdge("DASHBOARD", "SKILLS");
    expect(forward.spatialDirection).toBe("lateral");
    const back = resolveEdge("SKILLS", "DASHBOARD");
    expect(back.spatialDirection).toBe("lateral");
  });

  test("an undeclared pair fails safe: lateral, no shared-object policy, never throws", () => {
    expect(() => resolveEdge("WALLET", "QUIZ")).not.toThrow();
    const edge = resolveEdge("WALLET", "QUIZ");
    expect(edge.declared).toBe(false);
    expect(edge.spatialDirection).toBe("lateral");
    expect(edge.sharedObjectPolicy).toBe("none");
  });

  test("hasDeclaredEdge is true for either direction of a real edge, false for an undeclared pair", () => {
    expect(hasDeclaredEdge("MODULE", "QUIZ")).toBe(true);
    expect(hasDeclaredEdge("QUIZ", "MODULE")).toBe(true); // inverse also counts
    expect(hasDeclaredEdge("WALLET", "QUIZ")).toBe(false);
  });

  test("context-overlay edges (Quiz/Mission/Mentor from Module) carry sharedObjectPolicy metadata", () => {
    const edge = resolveEdge("MODULE", "QUIZ");
    expect(edge.sharedObjectPolicy).toBe("context-overlay");
  });

  test("no route string was invented for a node explicitly marked as a lifecycle-only concept", () => {
    expect(TOPOLOGY_NODES.ACTIVATION.route).toBeNull();
    expect(TOPOLOGY_NODES.EXPANSION.route).toBeNull();
    expect(TOPOLOGY_NODES.ECOSYSTEM.route).toBeNull();
  });
});
