import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import { buildPedagogicalGraph } from "@/lib/pedagogicalGraph";

/**
 * RAIL 3 — the one fetching entry point for the pedagogical graph.
 * Reuses exactly the endpoints `Dashboard.js` already calls
 * (`/user/learning-path`, `/missions`, `/badges/mine`), extended with
 * two Rail 2 additions (`/skills/mine`, `/qualifications/mine`) —
 * never a new backend contract invented for spatial's sake. A network
 * failure on any one call degrades that slice to empty rather than
 * failing the whole graph (a learner with e.g. zero qualifications
 * issued yet is a normal, common state, not an error).
 *
 * `signals` is exposed alongside `graph` so a caller that also needs
 * `lifecycleState.js`'s own signals shape (which reuses several of the
 * same responses) doesn't have to fetch twice — see `Dashboard.js`.
 */
export function usePedagogicalGraph({ enabled = true } = {}) {
  const [state, setState] = useState({ graph: buildPedagogicalGraph(), signals: {}, loading: enabled });

  useEffect(() => {
    if (!enabled) return;
    let cancelled = false;

    (async () => {
      const results = await Promise.allSettled([
        api.get("/user/learning-path").then((r) => r.data),
        api.get("/missions").then((r) => r.data),
        api.get("/badges/mine").then((r) => r.data),
        api.get("/skills/mine").then((r) => r.data),
        api.get("/qualifications/mine").then((r) => r.data),
      ]);
      const [learningPath, missions, badges, skills, qualifications] = results.map((r) =>
        r.status === "fulfilled" ? r.value : null
      );
      const signals = { learningPath, missions, badges, skills, qualifications };
      if (!cancelled) {
        setState({ graph: buildPedagogicalGraph(signals), signals, loading: false });
      }
    })();

    return () => {
      cancelled = true;
    };
  }, [enabled]);

  return state;
}
