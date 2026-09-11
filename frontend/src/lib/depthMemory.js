const PREFIX = "cvln:spatial-depth:";

function storage() {
  try {
    return window.sessionStorage;
  } catch {
    return null;
  }
}

function safeParse(raw, fallback = null) {
  if (!raw) return fallback;
  try {
    return JSON.parse(raw);
  } catch {
    return fallback;
  }
}

export function routeDepthKey(pathname) {
  return `${PREFIX}route:${pathname}`;
}

export function elementDepthKey(pathname, id) {
  return `${PREFIX}element:${pathname}:${id}`;
}

export function writeRouteDepth(pathname, snapshot) {
  const store = storage();
  if (!store || !pathname) return false;
  try {
    store.setItem(routeDepthKey(pathname), JSON.stringify(snapshot));
    return true;
  } catch {
    return false;
  }
}

export function readRouteDepth(pathname) {
  const store = storage();
  if (!store || !pathname) return null;
  return safeParse(store.getItem(routeDepthKey(pathname)));
}

export function captureRouteDepth(pathname) {
  if (typeof window === "undefined" || typeof document === "undefined") return null;
  const active = document.activeElement;
  const focusTestId = active?.getAttribute?.("data-testid") || null;
  const focusId = active?.id || null;
  const snapshot = {
    x: window.scrollX || 0,
    y: window.scrollY || 0,
    focusTestId,
    focusId,
    capturedAt: Date.now(),
  };
  writeRouteDepth(pathname, snapshot);
  return snapshot;
}

export function restoreRouteDepth(pathname) {
  if (typeof window === "undefined" || typeof document === "undefined") return false;
  const snapshot = readRouteDepth(pathname);
  if (!snapshot) return false;

  const restore = () => {
    window.scrollTo?.(snapshot.x || 0, snapshot.y || 0);
    let target = null;
    if (snapshot.focusTestId) {
      target = document.querySelector(`[data-testid="${CSS.escape(snapshot.focusTestId)}"]`);
    }
    if (!target && snapshot.focusId) {
      target = document.getElementById(snapshot.focusId);
    }
    target?.focus?.({ preventScroll: true });
  };

  if (typeof window.requestAnimationFrame === "function") {
    window.requestAnimationFrame(() => window.requestAnimationFrame(restore));
  } else {
    restore();
  }
  return true;
}

export function writeElementDepth(pathname, id, snapshot) {
  const store = storage();
  if (!store || !pathname || !id) return false;
  try {
    store.setItem(elementDepthKey(pathname, id), JSON.stringify(snapshot));
    return true;
  } catch {
    return false;
  }
}

export function readElementDepth(pathname, id) {
  const store = storage();
  if (!store || !pathname || !id) return null;
  return safeParse(store.getItem(elementDepthKey(pathname, id)));
}

export function captureElementDepth(pathname, id, element) {
  if (!element) return null;
  const snapshot = {
    left: element.scrollLeft || 0,
    top: element.scrollTop || 0,
    capturedAt: Date.now(),
  };
  writeElementDepth(pathname, id, snapshot);
  return snapshot;
}

export function restoreElementDepth(pathname, id, element) {
  if (!element) return false;
  const snapshot = readElementDepth(pathname, id);
  if (!snapshot) return false;
  if (typeof element.scrollTo === "function") {
    element.scrollTo({ left: snapshot.left || 0, top: snapshot.top || 0, behavior: "auto" });
  } else {
    element.scrollLeft = snapshot.left || 0;
    element.scrollTop = snapshot.top || 0;
  }
  return true;
}

export function writeContextDepth(key, value) {
  const store = storage();
  if (!store || !key) return false;
  try {
    store.setItem(`${PREFIX}context:${key}`, JSON.stringify(value));
    return true;
  } catch {
    return false;
  }
}

export function readContextDepth(key, fallback = null) {
  const store = storage();
  if (!store || !key) return fallback;
  return safeParse(store.getItem(`${PREFIX}context:${key}`), fallback);
}
