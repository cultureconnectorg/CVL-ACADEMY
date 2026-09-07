import { useCallback, useEffect, useRef, useState } from "react";
import { CAMERA_STATES, createCameraToken } from "@/lib/spatial/cameraFollow";
import { useReducedMotion } from "@/lib/useReducedMotion";

/**
 * RAIL 4 ("continue les H", 2026-09-07) — the one production caller of
 * `lib/spatial/cameraFollow.js`. Scope, stated plainly (see that file's
 * own docstring for why): a same-page INTENT->LOCKING->FOLLOWING flight
 * on the element the learner just activated, then a real navigate() —
 * never the full cross-route REVEALING handoff to a destination anchor,
 * which stays NOT_AUTHORIZED until the App.js Outlet restructure this
 * doctrine already deferred once (`AcademyBackdrop.jsx`'s own gap).
 *
 * `reduced` bypasses the flight entirely and navigates instantly — the
 * prototype's own reduced-motion branch does the same
 * (`cameraFollowTransition`'s first check).
 */
export function useCameraIntent() {
  const reduced = useReducedMotion();
  const tokenRef = useRef(null);
  if (!tokenRef.current) tokenRef.current = createCameraToken();
  const mountedRef = useRef(true);
  const [cameraState, setCameraState] = useState(CAMERA_STATES.IDLE);

  useEffect(() => {
    mountedRef.current = true;
    return () => {
      mountedRef.current = false;
    };
  }, []);

  const setStateIfMounted = useCallback((s) => {
    if (mountedRef.current) setCameraState(s);
  }, []);

  /**
   * @param {HTMLElement|null} sourceEl the real activated node
   * @param {() => void} onNavigate the real navigation callback — called
   *   mid-flight (FOLLOWING), matching the prototype's own timing:
   *   `goto()` fires before the clone's flight animation finishes.
   */
  const fly = useCallback(
    (sourceEl, onNavigate) => {
      if (reduced || !sourceEl) {
        setStateIfMounted(CAMERA_STATES.IDLE);
        onNavigate();
        return;
      }
      const myToken = tokenRef.current.next();
      setStateIfMounted(CAMERA_STATES.INTENT);

      const rect = sourceEl.getBoundingClientRect();
      const cs = window.getComputedStyle(sourceEl);
      const clone = document.createElement("div");
      clone.textContent = sourceEl.textContent;
      clone.setAttribute("aria-hidden", "true");
      clone.setAttribute("data-testid", "camera-intent-clone");
      clone.style.cssText = [
        "position:fixed",
        `left:${rect.left}px`,
        `top:${rect.top}px`,
        `width:${rect.width}px`,
        `font-family:${cs.fontFamily}`,
        `font-weight:${cs.fontWeight}`,
        `font-size:${cs.fontSize}`,
        `color:${cs.color}`,
        "z-index:9999",
        "pointer-events:none",
        "margin:0",
      ].join(";");
      document.body.appendChild(clone);
      setStateIfMounted(CAMERA_STATES.LOCKING);

      const anim = clone.animate(
        [
          { transform: "translate(0,0) scale(1)", opacity: 1 },
          { transform: "scale(1.22)", opacity: 0 },
        ],
        { duration: 260, easing: "cubic-bezier(.16,1,.3,1)", fill: "forwards" }
      );
      setStateIfMounted(CAMERA_STATES.FOLLOWING);
      // Navigate mid-flight — the clone keeps animating over whatever
      // renders next, same as the prototype calling goto() before its
      // own clone.animate().onfinish resolves.
      onNavigate();

      anim.onfinish = () => {
        clone.remove();
        if (tokenRef.current.isCurrent(myToken)) setStateIfMounted(CAMERA_STATES.IDLE);
      };
    },
    [reduced, setStateIfMounted]
  );

  return { fly, cameraState };
}
