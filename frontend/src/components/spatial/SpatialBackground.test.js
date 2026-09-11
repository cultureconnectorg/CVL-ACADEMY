import { render, screen, cleanup } from "@testing-library/react";
import SpatialBackground from "./SpatialBackground";

describe("SpatialBackground integration contract", () => {
  const engineKey = "REACT_APP_ACADEMY_SPATIAL_ENGINE";
  const envKey = "REACT_APP_ACADEMY_SPATIAL_ENVIRONMENT";

  afterEach(() => {
    delete process.env[engineKey];
    delete process.env[envKey];
    cleanup();
  });

  test("keeps a static safe fallback when Spatial flags are off", () => {
    render(<SpatialBackground />);
    const world = screen.getByTestId("spatial-background");
    expect(world).toHaveAttribute("data-spatial-engine", "off");
    expect(world).toHaveAttribute("data-spatial-motion", "static");
    expect(world).toHaveAttribute("aria-hidden", "true");
  });

  test("uses the existing Spatial flags to enable the living environment", () => {
    process.env[engineKey] = "true";
    process.env[envKey] = "true";
    render(<SpatialBackground />);
    const world = screen.getByTestId("spatial-background");
    expect(world).toHaveAttribute("data-spatial-engine", "on");
    expect(world).toHaveAttribute("data-spatial-motion", "full");
  });
});
