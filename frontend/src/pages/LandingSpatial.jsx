import Landing from "@/pages/Landing";

/**
 * Public landing entry point.
 * SpatialWorldFrame is mounted once at the application root and owns the
 * background/camera runtime for every route, including `/`, `/login`, and
 * `/register`. Keeping this wrapper visual-only avoids double-mounting
 * SpatialBackground on landing.
 */
export default function LandingSpatial({ authMode }) {
  return <Landing initialMode={authMode} />;
}
