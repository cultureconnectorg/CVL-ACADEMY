import { useEffect, useRef } from "react";
import { useLocation } from "react-router-dom";
import { createAutofocusGuard } from "@/lib/spatial/attention";
import { routeToTopologyNode } from "@/lib/spatial/routeTopologyMap";
import { readRouteDepth, writeRouteDepth } from "@/lib/depthMemory";

function findByToken(snapshot) {
  if (!snapshot || typeof document === "undefined") return null;
  if (snapshot.focusId) {
    const byId = document.getElementById(snapshot.focusId);
    if (byId) return byId;
  }
  if (snapshot.focusTestId) {
    return Array.from(document.querySelectorAll("[data-testid]")).find(
      (node) => node.getAttribute("data-testid") === snapshot.focusTestId
    ) || null;
  }
  return null;
}

function waitForTarget(resolveTarget, timeoutMs = 1800) {
  return new Promise((resolve) => {
    const immediate = resolveTarget();
    if (immediate) {
      resolve(immediate);
      return;
    }
    let settled = false;
    let timer = null;
    const finish = (value) => {
      if (settled) return;
      settled = true;
      observer.disconnect();
      if (timer) window.clearTimeout(timer);
      resolve(value);
    };
    const observer = new MutationObserver(() => {
      const target = resolveTarget();
      if (target) finish(target);
    });
    observer.observe(document.documentElement, { childList: true, subtree: true });
    timer = window.setTimeout(() => finish(null), timeoutMs);
  });
}

function recommendedFormationTarget() {
  if (typeof document === "undefined") return null;
  const next = document.querySelector('[data-testid="next-action-cta"]');
  const href = next?.getAttribute?.("href");
  const match = href?.match(/^\/formations\/([^/]+)\/modules\//);
  if (!match) return null;
  return document.querySelector(`[data-testid="formation-${match[1]}"]`);
}

function snapshotCurrentRoute(pathname) {
  if (!pathname || typeof window === "undefined" || typeof document === "undefined") return;
  const active = document.activeElement;
  writeRouteDepth(pathname, {
    x: window.scrollX || 0,
    y: window.scrollY || 0,
    focusTestId: active?.getAttribute?.("data-testid") || null,
    focusId: active?.id || null,
    capturedAt: Date.now(),
  });
}

/**
 * Production integration of H0.8 focus memory/autofocus:
 * restored explicit focus wins, then a real learner recommendation on
 * /formations, then no forced fallback. Any explicit pointer/keyboard/touch
 * intent that lands while an async target is resolving cancels autofocus.
 */
export default function SpatialFocusManager() {
  const location = useLocation();
  const guardRef = useRef(null);
  const pathRef = useRef(location.pathname);
  if (!guardRef.current) guardRef.current = createAutofocusGuard();

  useEffect(() => {
    const note = () => guardRef.current.noteExplicitIntent();
    window.addEventListener("pointerdown", note, true);
    window.addEventListener("keydown", note, true);
    window.addEventListener("touchstart", note, true);
    return () => {
      window.removeEventListener("pointerdown", note, true);
      window.removeEventListener("keydown", note, true);
      window.removeEventListener("touchstart", note, true);
    };
  }, []);

  useEffect(() => {
    const previous = pathRef.current;
    if (previous && previous !== location.pathname && routeToTopologyNode(previous)) {
      snapshotCurrentRoute(previous);
    }
    pathRef.current = location.pathname;

    if (!routeToTopologyNode(location.pathname)) return undefined;
    let cancelled = false;
    const saved = readRouteDepth(location.pathname);
    const request = guardRef.current.request(() => {});

    const applyTarget = (target, snapshot = null) => {
      if (cancelled || !target) return;
      // Resolve through the guard only after the async target exists. Replacing
      // the no-op apply here keeps stale requests from ever stealing focus.
      const guarded = guardRef.current.request(() => {
        if (snapshot) window.scrollTo?.(snapshot.x || 0, snapshot.y || 0);
        target.focus?.({ preventScroll: true });
      });
      guarded.resolve();
    };

    if (saved?.focusTestId || saved?.focusId) {
      waitForTarget(() => findByToken(saved)).then((target) => applyTarget(target, saved));
    } else if (location.pathname === "/formations") {
      waitForTarget(recommendedFormationTarget).then((target) => applyTarget(target));
    }

    // Resolve the placeholder request immediately; its sole purpose is to
    // advance the request sequence before async lookup begins.
    request.resolve();

    return () => {
      cancelled = true;
      snapshotCurrentRoute(location.pathname);
    };
  }, [location.pathname]);

  return null;
}
