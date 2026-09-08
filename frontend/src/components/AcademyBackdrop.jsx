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
 * **ACA-0015/ACA-0016 update (2026-09-08)** — the disclosed limitation
 * above is resolved: `Layout` is now a real Outlet-based layout route
 * (`App.js`'s `LayoutRoute`, `SPATIAL_H1_INTEGRATION_PLAN.md`'s own
 * REPLACE-BLOCKED item, unblocked by explicit Founder authorization).
 * This component now mounts exactly once for the whole in-section
 * navigation (dashboard <-> roadmap <-> formations <-> ... — every
 * route `Layout`-wrapped), and only remounts crossing the Landing/
 * Onboarding boundary, where the environment doesn't apply anyway.
 * `ENVIRONMENT_RESET_PER_ROUTE = FORBIDDEN` now genuinely holds — real,
 * DOM-identity-verified proof in
 * `e2e/environmental-continuity.spec.js` (a JS-only marker property
 * stamped on the live node survives an in-section navigation; the same
 * marker does not survive a real boundary crossing, proving the
 * technique is meaningful, not trivially true).
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
