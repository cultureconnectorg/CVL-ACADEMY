import { cameraOriginFromRect, rectSnapshot } from "./cameraAnchor";

export const SPATIAL_CAMERA_EVENT = "cvln:spatial-camera";
const STORAGE_KEY = "cvln:spatial-camera-intent:v1";

function storageAvailable(storage) {
  return Boolean(storage && typeof storage.getItem === "function" && typeof storage.setItem === "function");
}

function emit(detail) {
  if (typeof window === "undefined" || typeof CustomEvent !== "function") return;
  window.dispatchEvent(new CustomEvent(SPATIAL_CAMERA_EVENT, { detail }));
}

export function beginCameraIntent({
  anchorId,
  destinationRoute,
  destinationSelector = null,
  element,
  returnRoute,
} = {}) {
  if (!anchorId || !destinationRoute || !element || typeof window === "undefined") return false;
  const sourceRect = rectSnapshot(element.getBoundingClientRect?.());
  if (!sourceRect) return false;
  const sourceRoute = window.location.pathname;
  const origin = cameraOriginFromRect(sourceRect, {
    width: window.innerWidth,
    height: window.innerHeight,
  });
  const intent = {
    version: 1,
    anchorId,
    sourceRoute,
    destinationRoute,
    destinationSelector,
    returnRoute: returnRoute || sourceRoute,
    sourceRect,
    cameraOriginFrom: origin,
    createdAt: Date.now(),
  };
  try {
    if (storageAvailable(window.sessionStorage)) {
      window.sessionStorage.setItem(STORAGE_KEY, JSON.stringify(intent));
    }
  } catch {
    // Camera follow is progressive enhancement; navigation must still proceed.
  }
  emit({ kind: "LOCK", ...intent });
  return true;
}

export function readPendingCameraIntent(storage = globalThis?.sessionStorage) {
  if (!storageAvailable(storage)) return null;
  try {
    const value = JSON.parse(storage.getItem(STORAGE_KEY) || "null");
    if (!value?.anchorId || !value?.sourceRoute || !value?.destinationRoute) return null;
    return value;
  } catch {
    return null;
  }
}

export function consumePendingCameraIntent(storage = globalThis?.sessionStorage) {
  const value = readPendingCameraIntent(storage);
  if (!value || !storage || typeof storage.removeItem !== "function") return value;
  try {
    storage.removeItem(STORAGE_KEY);
  } catch {
    // Ignore blocked storage.
  }
  return value;
}

export function completeCameraIntent(intent, element) {
  if (!intent || !element || typeof window === "undefined") return null;
  const destinationRect = rectSnapshot(element.getBoundingClientRect?.());
  if (!destinationRect) return null;
  const target = cameraOriginFromRect(destinationRect, {
    width: window.innerWidth,
    height: window.innerHeight,
  });
  const completed = {
    ...intent,
    destinationRect,
    cameraOriginTarget: target,
  };
  emit({ kind: "FOLLOW", ...completed });
  return completed;
}

export function cancelCameraIntent() {
  try {
    globalThis?.sessionStorage?.removeItem?.(STORAGE_KEY);
  } catch {
    // Progressive enhancement only.
  }
  emit({ kind: "CANCEL" });
}
