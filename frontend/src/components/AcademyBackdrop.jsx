import { usePedagogicalGraph } from "@/lib/usePedagogicalGraph";
import { FEATURE_FLAGS } from "@/lib/featureFlags";

/**
 * RAIL 3 ("Finir Spatial Learning", 2026-09-07) — the environmental
 * signature named in `docs/ACADEMY_SPATIAL_END_TO_END_ARCHITECTURE.md`
 * §2: a real, data-driven tint behind the app shell, keyed to the
 * learner's real current intention (`graph.intentionPole`'s real pole
 * color, read off `/user/learning-path` — never invented, never a
 * per-page hand-picked color).
 *
 * **Disclosed limitation, not silently worked around**: the
 * architecture doc's own target is a backdrop that survives route
 * changes without resetting (`ENVIRONMENT_RESET_PER_ROUTE = FORBIDDEN`).
 * Achieving that requires promoting `Layout` to a React Router layout
 * route (`<Outlet/>`) so it mounts once for the whole authenticated
 * shell instead of once per `<Route element={<Protected>...}>` — a real
 * `App.js` routing restructure. The H1 integration plan's own
 * authorization for this pass requires "existing `<Routes>`... stay
 * byte-identical," so that restructure is deliberately not done here —
 * same posture as the plan's own two REPLACE-BLOCKED items, needing its
 * own separate go-ahead. This component is mounted per-`Layout`
 * instance instead: the tint is still real and still correct for
 * whatever page is showing, it just re-establishes on each navigation
 * rather than persisting seamlessly across it.
 *
 * Pointer-events-none, low z-index, purely decorative — removing it
 * changes zero functional behavior, and it renders nothing at all
 * unless `SPATIAL_ENVIRONMENT` is on (default off).
 */
export default function AcademyBackdrop() {
  const enabled = FEATURE_FLAGS.SPATIAL_ENVIRONMENT;
  const { graph } = usePedagogicalGraph({ enabled });

  if (!enabled) return null;

  const intentionNode = graph.formationNodes.find((n) => n.pole === graph.intentionPole);
  const tint = intentionNode?.poleColor || "#E05A33"; // CVLN orange — the app's own real default accent, never an arbitrary invented color

  return (
    <div
      aria-hidden="true"
      data-testid="academy-backdrop"
      className="fixed inset-0 pointer-events-none transition-[background] duration-700 ease-out"
      style={{
        zIndex: 0,
        background: `radial-gradient(1200px 800px at 15% -10%, ${tint}14, transparent 60%)`,
      }}
    />
  );
}
