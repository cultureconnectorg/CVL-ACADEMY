import { useLocation } from "react-router-dom";
import { useAuth } from "@/lib/auth.jsx";
import SpatialBackground from "@/components/spatial/SpatialBackground.jsx";
import ReturnPositionTracker from "@/components/spatial/ReturnPositionTracker.jsx";

/**
 * Mounts the visual world behind the already-existing application routes.
 * It does not own navigation, auth, content, or route transitions.
 */
export default function SpatialWorldFrame({ children }) {
  const location = useLocation();
  const { user } = useAuth();

  return (
    <div className="relative min-h-screen overflow-hidden" data-testid="spatial-world-frame">
      <ReturnPositionTracker />
      <SpatialBackground pathname={location.pathname} stade={user?.stade} />
      <div className="relative z-10 min-h-screen">{children}</div>
    </div>
  );
}
