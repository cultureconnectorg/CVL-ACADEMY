import Landing from "@/pages/Landing";
import SpatialBackground from "@/components/spatial/SpatialBackground.jsx";

/**
 * Visual-only enhancement wrapper.
 * Landing remains the source of truth for auth, routing and content.
 */
export default function LandingSpatial() {
  return (
    <div className="relative min-h-screen overflow-hidden bg-transparent" data-testid="landing-spatial-shell">
      <SpatialBackground />
      <div className="relative z-10">
        <Landing />
      </div>
    </div>
  );
}
