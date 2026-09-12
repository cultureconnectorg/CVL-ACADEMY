import { useCallback, useEffect, useRef, useState } from "react";
import { makeRailPhysics } from "./physics";
import { useReducedMotion } from "@/lib/useReducedMotion";

export function clampRailIndex(index, count) {
  if (!Number.isFinite(index) || count <= 0) return 0;
  return Math.max(0, Math.min(count - 1, Math.round(index)));
}

export function nearestRailIndex(railRect, itemRects) {
  if (!railRect || !Array.isArray(itemRects) || itemRects.length === 0) return 0;
  const center = railRect.left + railRect.width / 2;
  let bestIndex = 0;
  let bestDistance = Infinity;
  itemRects.forEach((rect, index) => {
    if (!rect) return;
    const itemCenter = rect.left + rect.width / 2;
    const distance = Math.abs(itemCenter - center);
    if (distance < bestDistance) {
      bestDistance = distance;
      bestIndex = index;
    }
  });
  return bestIndex;
}

function itemSelector(index) {
  return `[data-spatial-rail-index="${index}"]`;
}

/**
 * H0.10/H0.6 rail runtime: roving tabindex, rapid-input retargeting,
 * 1:1 pointer drag and nearest-item settle. It never activates domain
 * actions; callers decide what Enter/Space means beyond focus movement.
 */
export function useSpatialRail({ railRef, itemCount, initialIndex = 0 }) {
  const reduced = useReducedMotion();
  const [focusedIndex, setFocusedIndex] = useState(() => clampRailIndex(initialIndex, itemCount));
  const dragRef = useRef(null);
  const aliveRef = useRef(true);
  const physicsRef = useRef(null);

  useEffect(() => {
    aliveRef.current = true;
    const physics = makeRailPhysics((position) => {
      const rail = railRef.current;
      if (!aliveRef.current || !rail) return;
      rail.scrollLeft = Math.max(0, position);
    });
    physicsRef.current = physics;
    return () => {
      aliveRef.current = false;
      physicsRef.current = null;
    };
  }, [railRef]);

  useEffect(() => {
    setFocusedIndex((index) => clampRailIndex(index, itemCount));
  }, [itemCount]);

  const targetScrollForIndex = useCallback((index) => {
    const rail = railRef.current;
    if (!rail) return null;
    const item = rail.querySelector(itemSelector(clampRailIndex(index, itemCount)));
    if (!item) return null;
    const railRect = rail.getBoundingClientRect();
    const itemRect = item.getBoundingClientRect();
    const delta = itemRect.left + itemRect.width / 2 - (railRect.left + railRect.width / 2);
    return Math.max(0, rail.scrollLeft + delta);
  }, [itemCount, railRef]);

  const centerIndex = useCallback((index) => {
    const target = targetScrollForIndex(index);
    const rail = railRef.current;
    const physics = physicsRef.current;
    if (target === null || !rail || !physics) return;
    if (reduced) {
      physics.jump(target);
      return;
    }
    // Pointer drag / depth-memory restoration can move the real DOM scroll
    // independently of the spring. Synchronize only while the spring is idle,
    // then retarget from the true visual position instead of snapping from 0.
    if (!physics.running && Math.abs(physics.position - rail.scrollLeft) > 0.5) {
      physics.jump(rail.scrollLeft);
    }
    physics.setTarget(target);
  }, [railRef, reduced, targetScrollForIndex]);

  const focusIndex = useCallback((index, { focus = true, center = true } = {}) => {
    const next = clampRailIndex(index, itemCount);
    setFocusedIndex(next);
    const rail = railRef.current;
    if (focus && rail) {
      rail.querySelector(itemSelector(next))?.focus?.({ preventScroll: true });
    }
    if (center) centerIndex(next);
  }, [centerIndex, itemCount, railRef]);

  const itemProps = useCallback((index) => ({
    tabIndex: index === focusedIndex ? 0 : -1,
    "data-spatial-rail-index": index,
    onFocus: () => setFocusedIndex(index),
    onKeyDown: (event) => {
      if (event.key === "ArrowRight") {
        event.preventDefault();
        focusIndex(focusedIndex + 1);
      } else if (event.key === "ArrowLeft") {
        event.preventDefault();
        focusIndex(focusedIndex - 1);
      } else if (event.key === "Home") {
        event.preventDefault();
        focusIndex(0);
      } else if (event.key === "End") {
        event.preventDefault();
        focusIndex(itemCount - 1);
      }
    },
  }), [focusIndex, focusedIndex, itemCount]);

  const onPointerDown = useCallback((event) => {
    if (event.button !== 0 || !railRef.current) return;
    dragRef.current = {
      pointerId: event.pointerId,
      startX: event.clientX,
      startScroll: railRef.current.scrollLeft,
    };
    railRef.current.setPointerCapture?.(event.pointerId);
  }, [railRef]);

  const onPointerMove = useCallback((event) => {
    const drag = dragRef.current;
    const rail = railRef.current;
    if (!drag || !rail || drag.pointerId !== event.pointerId) return;
    const delta = event.clientX - drag.startX;
    rail.scrollLeft = Math.max(0, drag.startScroll - delta);
  }, [railRef]);

  const settleFromCurrentScroll = useCallback(() => {
    const rail = railRef.current;
    if (!rail) return;
    const items = Array.from(rail.querySelectorAll("[data-spatial-rail-index]"));
    const index = nearestRailIndex(
      rail.getBoundingClientRect(),
      items.map((item) => item.getBoundingClientRect())
    );
    focusIndex(index, { focus: false, center: true });
  }, [focusIndex, railRef]);

  const endDrag = useCallback((event) => {
    const drag = dragRef.current;
    if (!drag || drag.pointerId !== event.pointerId) return;
    railRef.current?.releasePointerCapture?.(event.pointerId);
    dragRef.current = null;
    settleFromCurrentScroll();
  }, [railRef, settleFromCurrentScroll]);

  return {
    focusedIndex,
    focusIndex,
    centerIndex,
    itemProps,
    railProps: {
      "data-spatial-rail": "true",
      onPointerDown,
      onPointerMove,
      onPointerUp: endDrag,
      onPointerCancel: endDrag,
      style: { touchAction: "pan-y" },
    },
  };
}
