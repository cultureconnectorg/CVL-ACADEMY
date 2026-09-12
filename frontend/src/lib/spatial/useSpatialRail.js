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

/** Fractional item index under the viewport center — used by H0.10 attention. */
export function interpolateRailPosition(viewportCenter, itemCenters) {
  if (!Number.isFinite(viewportCenter) || !Array.isArray(itemCenters) || itemCenters.length === 0) return 0;
  const centers = itemCenters.map(Number).filter(Number.isFinite);
  if (centers.length === 0) return 0;
  if (viewportCenter <= centers[0]) return 0;
  const last = centers.length - 1;
  if (viewportCenter >= centers[last]) return last;

  for (let i = 0; i < last; i += 1) {
    const a = centers[i];
    const b = centers[i + 1];
    if (viewportCenter >= a && viewportCenter <= b) {
      if (b === a) return i;
      return i + (viewportCenter - a) / (b - a);
    }
  }
  return last;
}

function itemSelector(index) {
  return `[data-spatial-rail-index="${index}"]`;
}

/**
 * H0.10/H0.6 rail runtime: roving tabindex, rapid-input retargeting,
 * 1:1 pointer drag, nearest-item settle and continuous attention position.
 * It never activates domain actions; callers decide what Enter/Space means.
 */
export function useSpatialRail({ railRef, itemCount, initialIndex = 0 }) {
  const reduced = useReducedMotion();
  const initial = clampRailIndex(initialIndex, itemCount);
  const [focusedIndex, setFocusedIndex] = useState(initial);
  const [attentionPosition, setAttentionPosition] = useState(initial);
  const dragRef = useRef(null);
  const aliveRef = useRef(true);
  const physicsRef = useRef(null);
  const attentionFrameRef = useRef(null);

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
      if (attentionFrameRef.current && typeof cancelAnimationFrame === "function") {
        cancelAnimationFrame(attentionFrameRef.current);
      }
    };
  }, [railRef]);

  useEffect(() => {
    setFocusedIndex((index) => clampRailIndex(index, itemCount));
    setAttentionPosition((position) => Math.max(0, Math.min(Math.max(itemCount - 1, 0), position)));
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

  const measureAttentionPosition = useCallback(() => {
    const rail = railRef.current;
    if (!rail) return;
    const railRect = rail.getBoundingClientRect();
    const items = Array.from(rail.querySelectorAll("[data-spatial-rail-index]"));
    if (items.length === 0) return;
    const centers = items.map((item) => {
      const rect = item.getBoundingClientRect();
      return rect.left - railRect.left + rail.scrollLeft + rect.width / 2;
    });
    const viewportCenter = rail.scrollLeft + railRect.width / 2;
    setAttentionPosition(interpolateRailPosition(viewportCenter, centers));
  }, [railRef]);

  const scheduleAttentionMeasure = useCallback(() => {
    if (attentionFrameRef.current || typeof requestAnimationFrame !== "function") return;
    attentionFrameRef.current = requestAnimationFrame(() => {
      attentionFrameRef.current = null;
      measureAttentionPosition();
    });
  }, [measureAttentionPosition]);

  const centerIndex = useCallback((index) => {
    const target = targetScrollForIndex(index);
    const rail = railRef.current;
    const physics = physicsRef.current;
    if (target === null || !rail || !physics) return;
    if (reduced) {
      physics.jump(target);
      scheduleAttentionMeasure();
      return;
    }
    // Pointer drag / depth-memory restoration can move the real DOM scroll
    // independently of the spring. Synchronize only while the spring is idle,
    // then retarget from the true visual position instead of snapping from 0.
    if (!physics.running && Math.abs(physics.position - rail.scrollLeft) > 0.5) {
      physics.jump(rail.scrollLeft);
    }
    physics.setTarget(target);
  }, [railRef, reduced, scheduleAttentionMeasure, targetScrollForIndex]);

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
    scheduleAttentionMeasure();
  }, [railRef, scheduleAttentionMeasure]);

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
    attentionPosition,
    focusIndex,
    centerIndex,
    itemProps,
    railProps: {
      "data-spatial-rail": "true",
      onPointerDown,
      onPointerMove,
      onPointerUp: endDrag,
      onPointerCancel: endDrag,
      onScrollCapture: scheduleAttentionMeasure,
      style: { touchAction: "pan-y" },
    },
  };
}
