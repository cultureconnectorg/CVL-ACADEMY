import React from "react";
import { renderToStaticMarkup } from "react-dom/server";
import SpatialBackground from "./SpatialBackground";

const FLAG_NAMES = ["SPATIAL_ENGINE", "SPATIAL_ENVIRONMENT"];

describe("SpatialBackground production defaults", () => {
  const originalEnv = { ...process.env };

  afterEach(() => {
    process.env = { ...originalEnv };
  });

  test("renders the approved Spatial engine ON when deployment env does not override it", () => {
    FLAG_NAMES.forEach((name) => delete process.env[`REACT_APP_ACADEMY_${name}`]);
    const html = renderToStaticMarkup(<SpatialBackground pathname="/" />);
    expect(html).toContain('data-spatial-engine="on"');
    expect(html).toContain('data-spatial-motion="full"');
    expect(html).toContain('/spatial/cvln-academy-spatial-world.svg');
  });

  test("an explicit deployment kill-switch still forces the static fallback", () => {
    process.env.REACT_APP_ACADEMY_SPATIAL_ENGINE = "false";
    const html = renderToStaticMarkup(<SpatialBackground pathname="/" />);
    expect(html).toContain('data-spatial-engine="off"');
  });
});
