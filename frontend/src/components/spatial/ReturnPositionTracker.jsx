import { useEffect, useMemo } from "react";
import { useLocation } from "react-router-dom";
import { useAuth } from "@/lib/auth.jsx";
import { sceneForPathname } from "@/lib/spatial/worldSceneMap";
import {
  consumeReturnPositionRestore,
  isRestorablePath,
  loadReturnPosition,
  returnPositionUserKey,
  saveReturnPosition,
} from "@/lib/returnPosition";

function focusToken() {
  if (typeof document === "undefined") return null;
  const el = document.activeElement;
  if (!el || el === document.body) return null;
  return el.id || el.getAttribute?.("data-testid") || el.getAttribute?.("data-spatial-focus-id") || null;
}

function railOffset() {
  if (typeof document === "undefined") return null;
  const rail = document.querySelector("[data-spatial-rail]");
  return rail && Number.isFinite(rail.scrollLeft) ? rail.scrollLeft : null;
}

function restoreFocus(token) {
  if (!token || typeof document === "undefined") return;
  const byId = document.getElementById(token);
  const candidates = byId
    ? [byId]
    : Array.from(document.querySelectorAll("[data-testid], [data-spatial-focus-id]")).filter(
        (node) => node.getAttribute("data-testid") === token || node.getAttribute("data-spatial-focus-id") === token
      );
  const target = candidates[0];
  if (target && typeof target.focus === "function") target.focus({ preventScroll: true });
}

export default function ReturnPositionTracker() {
  const location = useLocation();
  const { user } = useAuth();
  const userKey = returnPositionUserKey(user);
  const scene = useMemo(() => sceneForPathname(location.pathname), [location.pathname]);

  useEffect(() => {
    if (!userKey || !isRestorablePath(location.pathname) || typeof window === "undefined") return undefined;

    const saved = loadReturnPosition(userKey);
    if (
      saved?.pathname === location.pathname &&
      consumeReturnPositionRestore(userKey)
    ) {
      let first = null;
      let second = null;
      first = window.requestAnimationFrame(() => {
        second = window.requestAnimationFrame(() => {
          window.scrollTo({ top: saved.scrollY || 0, left: 0, behavior: "auto" });
          const rail = document.querySelector("[data-spatial-rail]");
          if (rail && Number.isFinite(saved.railOffset)) rail.scrollLeft = saved.railOffset;
          restoreFocus(saved.focusId);
        });
      });
      return () => {
        if (first) window.cancelAnimationFrame(first);
        if (second) window.cancelAnimationFrame(second);
      };
    }
    return undefined;
  }, [location.pathname, userKey]);

  useEffect(() => {
    if (!userKey || !isRestorablePath(location.pathname) || typeof window === "undefined") return undefined;

    let frame = null;
    const persist = () => {
      saveReturnPosition(userKey, {
        pathname: location.pathname,
        search: location.search,
        scrollY: window.scrollY || 0,
        focusId: focusToken(),
        railOffset: railOffset(),
        camera: {
          node: scene.node || null,
          camera: scene.scene.camera,
          depth: scene.scene.depth,
          zone: scene.scene.zone,
        },
      });
    };
    const schedulePersist = () => {
      if (frame) return;
      frame = window.requestAnimationFrame(() => {
        frame = null;
        persist();
      });
    };

    window.addEventListener("scroll", schedulePersist, { passive: true });
    window.addEventListener("pagehide", persist);
    document.addEventListener("focusin", schedulePersist);
    persist();

    return () => {
      window.removeEventListener("scroll", schedulePersist);
      window.removeEventListener("pagehide", persist);
      document.removeEventListener("focusin", schedulePersist);
      if (frame) window.cancelAnimationFrame(frame);
      persist();
    };
  }, [location.pathname, location.search, scene, userKey]);

  return null;
}
