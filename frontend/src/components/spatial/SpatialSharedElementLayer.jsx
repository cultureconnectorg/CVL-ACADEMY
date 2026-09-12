import { useEffect, useRef } from "react";
import { FEATURE_FLAGS } from "@/lib/featureFlags";
import { useReducedMotion } from "@/lib/useReducedMotion";
import { SPATIAL_CAMERA_EVENT } from "@/lib/spatial/cameraRuntime";
import "./spatial-shared-element.css";

function px(value) {
  return typeof value === "number" ? `${value}px` : value || undefined;
}

function createClone(snapshot) {
  if (!snapshot?.rect || !snapshot.text || typeof document === "undefined") return null;
  const node = document.createElement("div");
  node.className = "spatial-shared-element-clone";
  node.textContent = snapshot.text;
  node.setAttribute("aria-hidden", "true");
  Object.assign(node.style, {
    left: px(snapshot.rect.left),
    top: px(snapshot.rect.top),
    width: px(snapshot.rect.width),
    height: px(snapshot.rect.height),
    color: snapshot.color || undefined,
    backgroundColor: snapshot.backgroundColor || "transparent",
    fontFamily: snapshot.fontFamily || undefined,
    fontSize: snapshot.fontSize || undefined,
    fontWeight: snapshot.fontWeight || undefined,
    lineHeight: snapshot.lineHeight || undefined,
    letterSpacing: snapshot.letterSpacing || undefined,
    borderRadius: snapshot.borderRadius || undefined,
    textAlign: snapshot.textAlign || undefined,
  });
  return node;
}

function animateSharedElement(from, to, root, destinationNode = null) {
  if (!from?.rect || !to?.rect || !root) return null;
  const clone = createClone(from);
  if (!clone) return null;

  const previousVisibility = destinationNode?.style?.visibility;
  if (destinationNode?.style) destinationNode.style.visibility = "hidden";
  root.appendChild(clone);

  const dx = to.rect.left - from.rect.left;
  const dy = to.rect.top - from.rect.top;
  const sx = from.rect.width > 0 ? to.rect.width / from.rect.width : 1;
  const sy = from.rect.height > 0 ? to.rect.height / from.rect.height : 1;

  const animation = clone.animate(
    [
      { transform: "translate3d(0,0,0) scale(1,1)", opacity: 1 },
      {
        transform: `translate3d(${dx}px, ${dy}px, 0) scale(${sx}, ${sy})`,
        opacity: 1,
        color: to.color || from.color || undefined,
        backgroundColor: to.backgroundColor || from.backgroundColor || "transparent",
      },
    ],
    {
      duration: 420,
      easing: "cubic-bezier(0.16, 1, 0.3, 1)",
      fill: "forwards",
    },
  );

  let cleaned = false;
  const cleanup = () => {
    if (cleaned) return;
    cleaned = true;
    clone.remove();
    if (destinationNode?.style) destinationNode.style.visibility = previousVisibility || "";
  };
  animation.addEventListener?.("finish", cleanup, { once: true });
  animation.addEventListener?.("cancel", cleanup, { once: true });
  return () => {
    try { animation.cancel(); } catch { cleanup(); }
    cleanup();
  };
}

function destinationSelectorFor(detail) {
  if (detail.kind === "RETURN_FOLLOW") return detail.sharedSourceSelector || detail.sourceSelector;
  return detail.sharedDestinationSelector || detail.destinationSelector;
}

/**
 * A route-independent visual handoff layer. It never owns navigation and only
 * animates geometry already confirmed by the camera contract. Reduced motion
 * and the route-transition kill switch disable the clone entirely.
 */
export default function SpatialSharedElementLayer() {
  const rootRef = useRef(null);
  const cleanupRef = useRef(null);
  const reduced = useReducedMotion();

  useEffect(() => {
    if (!FEATURE_FLAGS.SPATIAL_ROUTE_TRANSITIONS || reduced || typeof window === "undefined") {
      return undefined;
    }
    const onCamera = (event) => {
      const detail = event?.detail;
      if (!detail || (detail.kind !== "FOLLOW" && detail.kind !== "RETURN_FOLLOW")) return;
      if (!detail.sharedSource?.rect || !detail.sharedDestination?.rect) return;
      cleanupRef.current?.();
      const selector = destinationSelectorFor(detail);
      const destinationNode = selector ? document.querySelector(selector) : null;
      cleanupRef.current = animateSharedElement(
        detail.sharedSource,
        detail.sharedDestination,
        rootRef.current,
        destinationNode,
      );
    };
    window.addEventListener(SPATIAL_CAMERA_EVENT, onCamera);
    return () => {
      window.removeEventListener(SPATIAL_CAMERA_EVENT, onCamera);
      cleanupRef.current?.();
      cleanupRef.current = null;
    };
  }, [reduced]);

  return <div ref={rootRef} className="spatial-shared-element-layer" aria-hidden="true" />;
}
