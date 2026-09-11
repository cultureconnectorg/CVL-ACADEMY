import {
  captureElementDepth,
  captureRouteDepth,
  readContextDepth,
  readElementDepth,
  readRouteDepth,
  restoreElementDepth,
  restoreRouteDepth,
  writeContextDepth,
} from "@/lib/depthMemory";

describe("Spatial DepthMemory", () => {
  beforeEach(() => {
    sessionStorage.clear();
    document.body.innerHTML = "";
    window.scrollTo = jest.fn();
    window.requestAnimationFrame = (cb) => cb();
    Object.defineProperty(window, "scrollX", { configurable: true, value: 12 });
    Object.defineProperty(window, "scrollY", { configurable: true, value: 345 });
  });

  test("captures and restores exact route scroll plus focused control", () => {
    const button = document.createElement("button");
    button.setAttribute("data-testid", "formation-FMS-01");
    document.body.appendChild(button);
    button.focus();

    const captured = captureRouteDepth("/formations");
    expect(captured).toMatchObject({ x: 12, y: 345, focusTestId: "formation-FMS-01" });
    expect(readRouteDepth("/formations")).toMatchObject({ x: 12, y: 345 });

    button.blur();
    expect(restoreRouteDepth("/formations")).toBe(true);
    expect(window.scrollTo).toHaveBeenCalledWith(12, 345);
    expect(document.activeElement).toBe(button);
  });

  test("captures and restores horizontal rail position", () => {
    const rail = document.createElement("div");
    Object.defineProperty(rail, "scrollLeft", { writable: true, value: 420 });
    Object.defineProperty(rail, "scrollTop", { writable: true, value: 7 });
    rail.scrollTo = jest.fn();

    captureElementDepth("/roadmap", "stage-rail", rail);
    expect(readElementDepth("/roadmap", "stage-rail")).toMatchObject({ left: 420, top: 7 });

    expect(restoreElementDepth("/roadmap", "stage-rail", rail)).toBe(true);
    expect(rail.scrollTo).toHaveBeenCalledWith({ left: 420, top: 7, behavior: "auto" });
  });

  test("persists route-local contextual state without touching backend truth", () => {
    expect(writeContextDepth("formations:pole", "FMS")).toBe(true);
    expect(readContextDepth("formations:pole", "ALL")).toBe("FMS");
    expect(readContextDepth("missing", "ALL")).toBe("ALL");
  });
});
