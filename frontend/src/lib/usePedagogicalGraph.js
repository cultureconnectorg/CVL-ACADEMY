import { useCallback, useEffect, useRef, useState } from "react";
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
 *
 * RAIL 3 remediation (2026-09-07): also refetches on window `focus` and
 * exposes `refetch`. Real progression can happen while this tab isn't
 * the active one (another tab, another device, a mission completed
 * earlier) — without this, `graph` would only ever reflect the instant
 * of mount, and `useDepthPhysics`'s spring would have no honest
 * real-world retarget to ever animate (a static distance for the whole
 * mount is a spring that only ever jumps once and sits still).
 */
export function usePedagogicalGraph({ enabled = true } = {}) {
  const [state, setState] = useState({ graph: buildPedagogicalGraph(), signals: {}, loading: enabled });
  const requestIdRef = useRef(0);
  const mountedRef = useRef(true);

  const fetchGraph = useCallback(async () => {
    if (!enabled) return;
    const myId = ++requestIdRef.current;
    const results = await Promise.allSettled([
      api.get("/user/learning-path").then((r) => r.data),
      api.get("/missions").then((r) => r.data),
      api.get("/badges/mine").then((r) => r.data),
      api.get("/skills/mine").then((r) => r.data),
      api.get("/qualifications/mine").then((r) => r.data),
    ]);
    // Superseded by a newer fetch (e.g. two focus events in quick
    // succession) — never let a stale response overwrite a fresher one.
    if (myId !== requestIdRef.current || !mountedRef.current) return;
    const [learningPath, missions, badges, skills, qualifications] = results.map((r) =>
      r.status === "fulfilled" ? r.value : null
    );
    const signals = { learningPath, missions, badges, skills, qualifications };
    setState({ graph: buildPedagogicalGraph(signals), signals, loading: false });
  }, [enabled]);

  useEffect(() => {
    mountedRef.current = true;
    return () => {
      mountedRef.current = false;
    };
  }, []);

  useEffect(() => {
    fetchGraph();
  }, [fetchGraph]);

  useEffect(() => {
    if (!enabled) return undefined;
    function onFocus() {
      fetchGraph();
    }
    window.addEventListener("focus", onFocus);
    return () => window.removeEventListener("focus", onFocus);
  }, [enabled, fetchGraph]);

  return { ...state, refetch: fetchGraph };
}
