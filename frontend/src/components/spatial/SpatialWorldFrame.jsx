import { useLocation } from "react-router-dom";
import SpatialBackground from "@/components/spatial/SpatialBackground.jsx";

/**
 * Mounts the visual world behind the already-existing application routes.
 * It does not own navigation, auth, content, or route transitions.
 */
export default function SpatialWorldFrame({ children }) {
  const location = useLocation();

  return (
    <div className="relative min-h-screen overflow-hidden" data-testid="spatial-world-frame">
      <SpatialBackground pathname={location.pathname} />
      <div className="relative z-10 min-h-screen">{children}</div>
    </div>
  );
}
