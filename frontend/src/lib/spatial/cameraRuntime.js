import { cameraOriginFromRect, rectSnapshot } from "./cameraAnchor";

export const SPATIAL_CAMERA_EVENT = "cvln:spatial-camera";
const STORAGE_KEY = "cvln:spatial-camera-intent:v1";
const RETURN_KEY = "cvln:spatial-camera-return:v1";
const RETURN_ARMED_KEY = "cvln:spatial-camera-return-armed:v1";

function storageAvailable(storage) {
  return Boolean(storage && typeof storage.getItem === "function" && typeof storage.setItem === "function");
}

function emit(detail) {
  if (typeof window === "undefined" || typeof CustomEvent !== "function") return;
  window.dispatchEvent(new CustomEvent(SPATIAL_CAMERA_EVENT, { detail }));
}

function readJson(key, storage) {
  if (!storageAvailable(storage)) return null;
  try {
    return JSON.parse(storage.getItem(key) || "null");
  } catch {
    return null;
  }
}

function writeJson(key, value, storage) {
  if (!storageAvailable(storage)) return false;
  try {
    storage.setItem(key, JSON.stringify(value));
    return true;
  } catch {
    return false;
  }
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
  const sourceTestId = element.getAttribute?.("data-testid") || null;
  const intent = {
    version: 1,
    anchorId,
    sourceRoute,
    sourceSelector: sourceTestId ? `[data-testid="${sourceTestId}"]` : null,
    destinationRoute,
    destinationSelector,
    returnRoute: returnRoute || sourceRoute,
    sourceRect,
    cameraOriginFrom: origin,
    createdAt: Date.now(),
  };
  writeJson(STORAGE_KEY, intent, window.sessionStorage);
  emit({ kind: "LOCK", ...intent });
  return true;
}

export function readPendingCameraIntent(storage = globalThis?.sessionStorage) {
  const value = readJson(STORAGE_KEY, storage);
  if (!value?.anchorId || !value?.sourceRoute || !value?.destinationRoute) return null;
  return value;
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

export function completeCameraIntent(intent, element, { returning = false } = {}) {
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
  if (!returning) writeJson(RETURN_KEY, completed, window.sessionStorage);
  emit({ kind: returning ? "RETURN_FOLLOW" : "FOLLOW", ...completed });
  return completed;
}

export function readReturnCameraContract(storage = globalThis?.sessionStorage) {
  const value = readJson(RETURN_KEY, storage);
  if (!value?.sourceRoute || !value?.destinationRoute || !value?.anchorId) return null;
  return value;
}

export function armCameraReturn(contract = readReturnCameraContract(), element = null) {
  if (!contract || typeof window === "undefined") return false;
  const node = element || (contract.destinationSelector ? document.querySelector(contract.destinationSelector) : null);
  const rect = node ? rectSnapshot(node.getBoundingClientRect?.()) : contract.destinationRect;
  if (!rect) return false;
  const origin = cameraOriginFromRect(rect, { width: window.innerWidth, height: window.innerHeight });
  writeJson(RETURN_ARMED_KEY, contract, window.sessionStorage);
  emit({ kind: "RETURN_LOCK", ...contract, cameraOriginFrom: origin });
  return true;
}

export function readArmedCameraReturn(storage = globalThis?.sessionStorage) {
  const value = readJson(RETURN_ARMED_KEY, storage);
  if (!value?.sourceRoute || !value?.destinationRoute || !value?.anchorId) return null;
  return value;
}

export function consumeArmedCameraReturn(storage = globalThis?.sessionStorage) {
  const value = readArmedCameraReturn(storage);
  if (!value || !storage || typeof storage.removeItem !== "function") return value;
  try {
    storage.removeItem(RETURN_ARMED_KEY);
    storage.removeItem(RETURN_KEY);
  } catch {
    // Ignore blocked storage.
  }
  return value;
}

export function cancelCameraIntent() {
  try {
    globalThis?.sessionStorage?.removeItem?.(STORAGE_KEY);
  } catch {
    // Progressive enhancement only.
  }
  emit({ kind: "CANCEL" });
}
