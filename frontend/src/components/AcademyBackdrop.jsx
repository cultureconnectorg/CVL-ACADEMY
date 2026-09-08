import { usePedagogicalGraph } from "@/lib/usePedagogicalGraph";
import { FEATURE_FLAGS } from "@/lib/featureFlags";
import { useAuth } from "@/lib/auth.jsx";

// consumer->learner->...->FORÊT stade order the rest of the app already
// uses (Roadmap.js's own STAGE_CODES) — reused verbatim here to derive
// a real botanical density (1..6), never a fabricated separate scale.
const STAGE_CODES = ["graine", "pousse", "racine", "branches", "arbre", "foret"];

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
 * **Visual redesign pass (2026-09-08)** — replaces the single flat
 * radial gradient with the layered env-base/env-light/veg-blob
 * treatment from the validated H0.10 prototype (index.css's own
 * "Spatial shell — visual language" block documents the full mapping).
 * Still real data driving it: the formation-signature tint is the same
 * `intentionNode.poleColor` as before; the botanical layer's density
 * (1-6 blobs shown) is the learner's real stade index on
 * Roadmap.js's own GRAINE->FORÊT scale — not a decorative random count.
 *
 * Pointer-events-none, low z-index, purely decorative — removing it
 * changes zero functional behavior, and it renders nothing at all
 * unless `SPATIAL_ENVIRONMENT` is on (default off).
 */
export default function AcademyBackdrop() {
  const enabled = FEATURE_FLAGS.SPATIAL_ENVIRONMENT;
  const { graph } = usePedagogicalGraph({ enabled });
  const { user } = useAuth();

  if (!enabled) return null;

  const intentionNode = graph.formationNodes.find((n) => n.pole === graph.intentionPole);
  const tint = intentionNode?.poleColor || "#E05A33"; // CVLN orange — the app's own real default accent, never an arbitrary invented color
  const stadeIdx = STAGE_CODES.indexOf(user?.stade);
  const density = Math.max(1, Math.min(6, stadeIdx + 1 || 1));

  return (
    <div
      aria-hidden="true"
      data-testid="academy-backdrop"
      className="spatial-backdrop"
      style={{ "--env-glow-1": tint, "--formation-signature": tint }}
    >
      <div className="env-base" />
      <div className="env-light" />
      {Array.from({ length: density }).map((_, i) => (
        <div
          key={i}
          // The last-rendered blob (regardless of density) always
          // carries the real formation signature — same "one node
          // whose hue morphs, never resets" continuity the prototype
          // established, ported here onto whichever blob is currently
          // visible at this density rather than a fixed index.
          className={`veg-blob${i === density - 1 ? " veg-signature" : ""}`}
          style={{
            width: 160 + (i % 3) * 40,
            height: 140 + (i % 3) * 35,
            left: `${8 + i * 15}%`,
            top: `${12 + (i % 4) * 20}%`,
            opacity: i === density - 1 ? undefined : 0.5,
            background:
              i === density - 1
                ? undefined
                : `radial-gradient(circle, color-mix(in srgb, var(--st-${STAGE_CODES[i] || "graine"}) 10%, transparent), transparent 70%)`,
          }}
        />
      ))}
    </div>
  );
}
