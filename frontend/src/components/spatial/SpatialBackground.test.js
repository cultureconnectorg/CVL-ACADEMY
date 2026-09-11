import { renderToStaticMarkup } from "react-dom/server";
import SpatialBackground from "./SpatialBackground";

describe("SpatialBackground integration contract", () => {
  const engineKey = "REACT_APP_ACADEMY_SPATIAL_ENGINE";
  const envKey = "REACT_APP_ACADEMY_SPATIAL_ENVIRONMENT";

  afterEach(() => {
    delete process.env[engineKey];
    delete process.env[envKey];
  });

  test("keeps a static safe fallback when Spatial flags are explicitly off", () => {
    process.env[engineKey] = "false";
    process.env[envKey] = "false";
    const html = renderToStaticMarkup(<SpatialBackground />);
    expect(html).toContain('data-testid="spatial-background"');
    expect(html).toContain('data-spatial-engine="off"');
    expect(html).toContain('data-spatial-motion="static"');
    expect(html).toContain('aria-hidden="true"');
  });

  test("uses the approved production defaults to enable the living environment", () => {
    const html = renderToStaticMarkup(<SpatialBackground />);
    expect(html).toContain('data-spatial-engine="on"');
    expect(html).toContain('data-spatial-motion="full"');
  });

  test("explicit true deployment overrides also keep the living environment on", () => {
    process.env[engineKey] = "true";
    process.env[envKey] = "true";
    const html = renderToStaticMarkup(<SpatialBackground />);
    expect(html).toContain('data-spatial-engine="on"');
    expect(html).toContain('data-spatial-motion="full"');
  });
});
