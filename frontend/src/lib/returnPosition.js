const STORAGE_PREFIX = "cvln:return-position:v1";
const RESUME_PREFIX = "cvln:return-resume:v1";

const RESTORABLE_ROUTE = /^\/(dashboard|roadmap|formations(?:\/[^/]+(?:\/modules\/[^/]+)?)?|missions|badges|skills|certifications|wallet|frek-profile)$/;

function storageAvailable(storage) {
  return Boolean(storage && typeof storage.getItem === "function" && typeof storage.setItem === "function");
}

export function returnPositionUserKey(user) {
  return user?.id || user?.frek_id || null;
}

export function isRestorablePath(pathname) {
  return typeof pathname === "string" && RESTORABLE_ROUTE.test(pathname);
}

function keyFor(prefix, userKey) {
  return userKey ? `${prefix}:${String(userKey)}` : null;
}

export function saveReturnPosition(userKey, snapshot, storage = globalThis?.localStorage) {
  const key = keyFor(STORAGE_PREFIX, userKey);
  if (!key || !isRestorablePath(snapshot?.pathname) || !storageAvailable(storage)) return false;

  const payload = {
    pathname: snapshot.pathname,
    search: typeof snapshot.search === "string" ? snapshot.search : "",
    scrollY: Number.isFinite(snapshot.scrollY) ? Math.max(0, snapshot.scrollY) : 0,
    focusId: snapshot.focusId || null,
    railOffset: Number.isFinite(snapshot.railOffset) ? Math.max(0, snapshot.railOffset) : null,
    camera: snapshot.camera || null,
    savedAt: new Date().toISOString(),
  };

  try {
    storage.setItem(key, JSON.stringify(payload));
    return true;
  } catch {
    return false;
  }
}

export function loadReturnPosition(userKey, storage = globalThis?.localStorage) {
  const key = keyFor(STORAGE_PREFIX, userKey);
  if (!key || !storageAvailable(storage)) return null;
  try {
    const parsed = JSON.parse(storage.getItem(key) || "null");
    if (!parsed || !isRestorablePath(parsed.pathname)) return null;
    return parsed;
  } catch {
    return null;
  }
}

export function clearReturnPosition(userKey, storage = globalThis?.localStorage) {
  const key = keyFor(STORAGE_PREFIX, userKey);
  if (!key || !storage || typeof storage.removeItem !== "function") return;
  try {
    storage.removeItem(key);
  } catch {
    // localStorage may be blocked; return-position is progressive enhancement.
  }
}

export function armReturnPositionRestore(userKey, storage = globalThis?.sessionStorage) {
  const key = keyFor(RESUME_PREFIX, userKey);
  if (!key || !storageAvailable(storage)) return false;
  try {
    storage.setItem(key, "1");
    return true;
  } catch {
    return false;
  }
}

export function consumeReturnPositionRestore(userKey, storage = globalThis?.sessionStorage) {
  const key = keyFor(RESUME_PREFIX, userKey);
  if (!key || !storageAvailable(storage)) return false;
  try {
    const armed = storage.getItem(key) === "1";
    if (armed && typeof storage.removeItem === "function") storage.removeItem(key);
    return armed;
  } catch {
    return false;
  }
}

export function resumeHref(snapshot) {
  if (!snapshot || !isRestorablePath(snapshot.pathname)) return null;
  return `${snapshot.pathname}${snapshot.search || ""}`;
}
