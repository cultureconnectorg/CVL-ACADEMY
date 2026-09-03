import { routeToTopologyNode } from "./routeTopologyMap";
import { TOPOLOGY_NODES } from "./topology";

describe("routeTopologyMap.js", () => {
  test("every static route it can resolve maps to a real topology.js node", () => {
    ["/", "/onboarding", "/dashboard", "/formations", "/roadmap", "/missions", "/badges", "/skills", "/certifications", "/wallet", "/frek-profile"].forEach(
      (path) => {
        const node = routeToTopologyNode(path);
        expect(node).not.toBeNull();
        expect(TOPOLOGY_NODES).toHaveProperty(node);
      }
    );
  });

  test("dynamic formation route resolves to FORMATION", () => {
    expect(routeToTopologyNode("/formations/FMS-01")).toBe("FORMATION");
  });

  test("dynamic module route resolves to MODULE", () => {
    expect(routeToTopologyNode("/formations/FMS-01/modules/FMS-01-M01")).toBe("MODULE");
  });

  test("an unrecognized pathname resolves to null, never a guess", () => {
    expect(routeToTopologyNode("/some/unknown/path")).toBeNull();
    expect(routeToTopologyNode("/trainer")).toBeNull(); // real route, just not in the funnel topology
  });

  test("null/undefined/empty pathname resolves to null without throwing", () => {
    expect(routeToTopologyNode(null)).toBeNull();
    expect(routeToTopologyNode(undefined)).toBeNull();
    expect(routeToTopologyNode("")).toBeNull();
  });
});
