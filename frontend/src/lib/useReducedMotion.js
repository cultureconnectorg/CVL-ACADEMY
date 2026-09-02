import { useEffect, useState } from "react";
import { prefersReducedMotion } from "@/lib/motion-tokens";

/**
 * Live-updating version of `prefersReducedMotion()` for components that
 * need to re-render if the OS preference changes while the page is open
 * (e.g. a user toggling it in system settings without reloading).
 *
 * W1-B foundation only — not imported by any page yet.
 */
export function useReducedMotion() {
  const [reduced, setReduced] = useState(() => prefersReducedMotion());

  useEffect(() => {
    if (typeof window === "undefined" || !window.matchMedia) return undefined;
    const mql = window.matchMedia("(prefers-reduced-motion: reduce)");
    const onChange = () => setReduced(mql.matches);
    mql.addEventListener("change", onChange);
    return () => mql.removeEventListener("change", onChange);
  }, []);

  return reduced;
}
