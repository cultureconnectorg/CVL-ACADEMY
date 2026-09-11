import { renderToStaticMarkup } from "react-dom/server";
import SpatialBackground from "./SpatialBackground";

describe("SpatialBackground integration contract", () => {
  const engineKey = "REACT_APP_ACADEMY_SPATIAL_ENGINE";
  const envKey = "REACT_APP_ACADEMY_SPATIAL_ENVIRONMENT";

  afterEach(() => {
    delete process.env[engineKey];
    delete process.env[envKey];
  });

  test("keeps a static safe fallback when Spatial flags are off", () => {
    const html = renderToStaticMarkup(<SpatialBackground />);
    expect(html).toContain('data-testid="spatial-background"');
    expect(html).toContain('data-spatial-engine="off"');
    expect(html).toContain('data-spatial-motion="static"');
    expect(html).toContain('aria-hidden="true"');
  });

  test("uses the existing Spatial flags to enable the living environment", () => {
    process.env[engineKey] = "true";
    process.env[envKey] = "true";
    const html = renderToStaticMarkup(<SpatialBackground />);
    expect(html).toContain('data-spatial-engine="on"');
    expect(html).toContain('data-spatial-motion="full"');
  });
});
