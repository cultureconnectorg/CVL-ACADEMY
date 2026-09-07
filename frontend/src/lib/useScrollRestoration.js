/**
 * ACA-0023 (scroll slice) — Exact return-to-position, scroll axis.
 *
 * React Router v6 + lazy-loaded routes means the browser's own
 * `history.scrollRestoration = "auto"` can't be trusted: by the time it
 * fires, the async route content often hasn't painted its real height
 * yet, so it restores against the wrong layout. This hook takes manual
 * control instead — the standard SPA pattern.
 *
 * Scope, deliberately: the browser-history scroll axis of ACA-0023
 * only. The camera/rail/focus axes are a real, separate decision tied
 * to whether the spatial engine is actually mounted in production
 * (ACA-0014, still flag-gated off) — nothing here assumes or depends
 * on it, and nothing here claims to restore camera/rail/focus state.
 */

import { useEffect, useRef } from "react";
import { useLocation, useNavigationType } from "react-router-dom";
import { getPosition, savePosition } from "@/lib/scrollRestoration";

const RESTORE_ATTEMPTS = 5;

export function useScrollRestoration() {
  const location = useLocation();
  const navType = useNavigationType();
  const currentKeyRef = useRef(location.key);

  // Take manual control once — the browser's own "auto" restoration
  // would otherwise race this hook on the very next back/forward.
  useEffect(() => {
    if (typeof window === "undefined" || !window.history) return;
    const previous = window.history.scrollRestoration;
    try {
      window.history.scrollRestoration = "manual";
    } catch {
      // Some embedders/browsers disallow setting this — restoration
      // below still runs, just alongside whatever the browser also does.
    }
    return () => {
      try {
        window.history.scrollRestoration = previous;
      } catch {
        /* noop */
      }
    };
  }, []);

  // Continuously remember the scroll position of whichever location is
  // current — no "about to leave" event to miss, no timing race with
  // whatever unmounts first.
  useEffect(() => {
    currentKeyRef.current = location.key;
    const onScroll = () => savePosition(currentKeyRef.current, window.scrollY);
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
  }, [location.key]);

  // On arrival: a real browser back/forward (POP) with a remembered
  // position restores it; everything else (a Link click, a redirect,
  // or a POP to a history entry never scrolled on) lands at the top —
  // the standard SPA default a user expects from a fresh navigation.
  useEffect(() => {
    const saved = navType === "POP" ? getPosition(location.key) : undefined;
    if (typeof saved !== "number") {
      window.scrollTo(0, 0);
      return;
    }
    // Lazy-loaded route content may not have its real height on the
    // very first frame after mount — retry across a few rAFs rather
    // than assuming layout is already settled.
    let attempts = 0;
    let frame = requestAnimationFrame(function tryScroll() {
      window.scrollTo(0, saved);
      attempts += 1;
      if (attempts < RESTORE_ATTEMPTS) {
        frame = requestAnimationFrame(tryScroll);
      }
    });
    return () => cancelAnimationFrame(frame);
  }, [location.key, navType]);
}
