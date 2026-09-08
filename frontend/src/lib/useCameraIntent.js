import { useCallback, useEffect, useRef, useState } from "react";
import {
  CAMERA_STATES,
  computeFlightKeyframes,
  createCameraToken,
} from "@/lib/spatial/cameraFollow";
import { waitForElement } from "@/lib/spatial/mountGuard";
import { useReducedMotion } from "@/lib/useReducedMotion";

/**
 * RAIL 4 ("continue les H", 2026-09-07) — the one production caller of
 * `lib/spatial/cameraFollow.js`.
 *
 * **ACA-0015 update (2026-09-08)** — the two prerequisites that file's
 * own docstring named for the full cross-route CROSSING/REVEALING
 * handoff are both now real: (a) `Layout` is a genuine Outlet-based
 * layout route (ACA-0015/ACA-0016's routing restructure), and (b) a
 * real mount-detection race guard (`lib/spatial/mountGuard.js`'s
 * `waitForElement`) resolves the destination anchor the instant it
 * actually mounts, instead of assuming a same-frame handoff. `fly()`
 * therefore gains an optional third argument: when a caller supplies
 * `destinationSelector`, the flight continues past FOLLOWING into a
 * real CROSSING → REVEALING → SETTLING sequence once the destination
 * page's own real anchor element appears; a caller that omits it keeps
 * the exact prior INTENT → LOCKING → FOLLOWING → IDLE behavior,
 * byte-identical.
 *
 * `destinationSelector` is a real, load-bearing accessibility hazard if
 * chosen carelessly — a caller must pass a selector for an element the
 * destination page genuinely renders as its own most relevant anchor
 * (e.g. `[aria-current="true"]` on Roadmap's own current-stage card),
 * never an invented one. If the anchor doesn't appear within
 * `mountGuard`'s timeout (empty data, slow fetch, or the caller passed
 * a selector that never matches on this destination), the flight
 * degrades gracefully straight to IDLE — never blocks navigation,
 * never leaves a stray clone on screen.
 *
 * `reduced` bypasses the flight entirely and navigates instantly — the
 * prototype's own reduced-motion branch does the same
 * (`cameraFollowTransition`'s first check); CROSSING/REVEALING/SETTLING
 * never run either, same as the rest of the flight.
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
   * @param {{ destinationSelector?: string }} [opts] optional — see
   *   this hook's own docstring for the CROSSING/REVEALING contract.
   */
  const fly = useCallback(
    (sourceEl, onNavigate, opts = {}) => {
      const { destinationSelector } = opts;
      if (reduced || !sourceEl) {
        setStateIfMounted(CAMERA_STATES.IDLE);
        onNavigate();
        return;
      }
      const myToken = tokenRef.current.next();
      setStateIfMounted(CAMERA_STATES.INTENT);

      const rect = sourceEl.getBoundingClientRect();
      const cs = window.getComputedStyle(sourceEl);
      const cloneCss = [
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
      const clone = document.createElement("div");
      clone.textContent = sourceEl.textContent;
      clone.setAttribute("aria-hidden", "true");
      clone.setAttribute("data-testid", "camera-intent-clone");
      clone.style.cssText = cloneCss;
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
        if (!tokenRef.current.isCurrent(myToken)) return; // superseded meanwhile

        if (!destinationSelector) {
          setStateIfMounted(CAMERA_STATES.IDLE);
          return;
        }

        // CROSSING: the destination route has been requested but its
        // real anchor may not exist in the DOM yet (data fetch,
        // component mount) — this is exactly the race
        // cameraFollow.js's own docstring named as unresolved before
        // mountGuard.js existed.
        setStateIfMounted(CAMERA_STATES.CROSSING);
        waitForElement(destinationSelector).then((destEl) => {
          if (!tokenRef.current.isCurrent(myToken)) return; // retargeted/cancelled while waiting
          if (!destEl) {
            // Graceful degrade — same doctrine as an unsupported audio/
            // haptics API: never block navigation, never fabricate a
            // handoff to an anchor that never appeared.
            setStateIfMounted(CAMERA_STATES.IDLE);
            return;
          }

          setStateIfMounted(CAMERA_STATES.REVEALING);
          const destRect = destEl.getBoundingClientRect();
          const { dx, dy, scale } = computeFlightKeyframes(rect, destRect);
          const revealClone = document.createElement("div");
          revealClone.setAttribute("aria-hidden", "true");
          revealClone.setAttribute("data-testid", "camera-reveal-clone");
          revealClone.style.cssText = cloneCss;
          document.body.appendChild(revealClone);

          const revealAnim = revealClone.animate(
            [
              { transform: "translate(0,0) scale(1)", opacity: 0.85 },
              {
                transform: `translate(${dx}px, ${dy}px) scale(${scale})`,
                opacity: 0,
              },
            ],
            { duration: 320, easing: "cubic-bezier(.16,1,.3,1)", fill: "forwards" }
          );
          revealAnim.onfinish = () => {
            revealClone.remove();
            if (!tokenRef.current.isCurrent(myToken)) return;
            setStateIfMounted(CAMERA_STATES.SETTLING);
            // SETTLING is a brief named beat (the destination's own real
            // content is already visible under the clone by now) before
            // returning to IDLE — no further DOM change of its own.
            setTimeout(() => {
              if (tokenRef.current.isCurrent(myToken)) setStateIfMounted(CAMERA_STATES.IDLE);
            }, 120);
          };
        });
      };
    },
    [reduced, setStateIfMounted]
  );

  return { fly, cameraState };
}
