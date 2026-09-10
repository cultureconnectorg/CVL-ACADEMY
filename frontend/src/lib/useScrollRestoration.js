/**
 * ACA-0023 — Exact return-to-position, scroll + rail + focus axes.
 *
 * React Router v6 + lazy-loaded routes means browser-native restoration
 * cannot be trusted to run after async route content reaches its final
 * layout. This hook owns restoration for client-side history entries.
 *
 * Document scroll, named spatial rails and the last stable focus target
 * are remembered independently. Focus restoration is deliberately
 * conservative: only stable `id` or `data-testid` targets are stored.
 */

import { useEffect, useRef } from "react";
import { useLocation, useNavigationType } from "react-router-dom";
import {
  getElementPositions,
  getFocusTarget,
  getPosition,
  saveElementPosition,
  saveFocusTarget,
  savePosition,
} from "@/lib/scrollRestoration";

const RESTORE_ATTEMPTS = 5;
const ELEMENT_MEMORY_ATTR = "data-scroll-memory";

function focusDescriptor(element) {
  if (!element || element === document.body || element === document.documentElement) return null;
  if (element.id) return { kind: "id", value: element.id };
  const testId = element.getAttribute?.("data-testid");
  if (testId) return { kind: "testid", value: testId };
  return null;
}

function resolveFocusTarget(target) {
  if (!target) return null;
  if (target.kind === "id") return document.getElementById(target.value);
  if (target.kind === "testid") {
    return Array.from(document.querySelectorAll("[data-testid]")).find(
      (element) => element.getAttribute("data-testid") === target.value
    );
  }
  return null;
}

function canRestoreFocus(element) {
  if (!element || typeof element.focus !== "function") return false;
  if (element.matches?.(":disabled, [aria-disabled='true']")) return false;
  return true;
}

function findMemoryElement(memoryKey) {
  return Array.from(document.querySelectorAll(`[${ELEMENT_MEMORY_ATTR}]`)).find(
    (element) => element.getAttribute(ELEMENT_MEMORY_ATTR) === memoryKey
  );
}

export function useScrollRestoration() {
  const location = useLocation();
  const navType = useNavigationType();
  const currentKeyRef = useRef(location.key);

  useEffect(() => {
    if (typeof window === "undefined" || !window.history) return;
    const previous = window.history.scrollRestoration;
    try {
      window.history.scrollRestoration = "manual";
    } catch {
      // Some embedders disallow changing it. Our own restoration still runs.
    }
    return () => {
      try {
        window.history.scrollRestoration = previous;
      } catch {
        /* noop */
      }
    };
  }, []);

  useEffect(() => {
    currentKeyRef.current = location.key;
    const onWindowScroll = () => savePosition(currentKeyRef.current, window.scrollY);
    const onElementScroll = (event) => {
      const element = event.target;
      const memoryKey = element?.getAttribute?.(ELEMENT_MEMORY_ATTR);
      if (!memoryKey) return;
      saveElementPosition(currentKeyRef.current, memoryKey, {
        left: element.scrollLeft,
        top: element.scrollTop,
      });
    };
    const onFocusIn = (event) => {
      const target = focusDescriptor(event.target);
      if (target) saveFocusTarget(currentKeyRef.current, target);
    };

    window.addEventListener("scroll", onWindowScroll, { passive: true });
    document.addEventListener("scroll", onElementScroll, true);
    document.addEventListener("focusin", onFocusIn);
    return () => {
      window.removeEventListener("scroll", onWindowScroll);
      document.removeEventListener("scroll", onElementScroll, true);
      document.removeEventListener("focusin", onFocusIn);
    };
  }, [location.key]);

  useEffect(() => {
    const savedScroll = navType === "POP" ? getPosition(location.key) : undefined;
    const savedElements = navType === "POP" ? getElementPositions(location.key) : {};
    const savedFocus = navType === "POP" ? getFocusTarget(location.key) : undefined;

    if (typeof savedScroll !== "number") window.scrollTo(0, 0);

    let attempts = 0;
    let frame = requestAnimationFrame(function restoreContext() {
      if (typeof savedScroll === "number") window.scrollTo(0, savedScroll);

      Object.entries(savedElements).forEach(([memoryKey, position]) => {
        const element = findMemoryElement(memoryKey);
        if (element) {
          element.scrollLeft = position.left;
          element.scrollTop = position.top;
        }
      });

      const focusTarget = resolveFocusTarget(savedFocus);
      if (canRestoreFocus(focusTarget)) {
        focusTarget.focus({ preventScroll: true });
      }

      attempts += 1;
      if (attempts < RESTORE_ATTEMPTS) {
        frame = requestAnimationFrame(restoreContext);
      }
    });
    return () => cancelAnimationFrame(frame);
  }, [location.key, navType]);
}
