export const CAMERA_PHASES = Object.freeze({
  IDLE: "IDLE",
  INTENT: "INTENT",
  LOCKING: "LOCKING",
  FOLLOWING: "FOLLOWING",
  CROSSING: "CROSSING",
  REVEALING: "REVEALING",
  SETTLING: "SETTLING",
  RETURNING: "RETURNING",
});

const PHASE_ORDER = Object.freeze([
  CAMERA_PHASES.INTENT,
  CAMERA_PHASES.LOCKING,
  CAMERA_PHASES.FOLLOWING,
  CAMERA_PHASES.CROSSING,
  CAMERA_PHASES.REVEALING,
  CAMERA_PHASES.SETTLING,
]);

function finite(value, fallback = 0) {
  return Number.isFinite(value) ? value : fallback;
}

export function rectSnapshot(rect) {
  if (!rect) return null;
  return Object.freeze({
    x: finite(rect.x ?? rect.left),
    y: finite(rect.y ?? rect.top),
    width: Math.max(0, finite(rect.width)),
    height: Math.max(0, finite(rect.height)),
  });
}

function cameraPoint(value, fallback = { x: 50, y: 50 }) {
  if (!value) return Object.freeze({ ...fallback });
  return Object.freeze({ x: finite(value.x, fallback.x), y: finite(value.y, fallback.y) });
}

/** H0.8 Camera Anchor Contract, productionized as immutable plain data. */
export function makeAnchorContract({
  anchorId,
  sourceRoute,
  destinationRoute,
  sourceRect = null,
  destinationRect = null,
  cameraFrom,
  cameraTarget,
  cameraOriginFrom,
  cameraOriginTarget,
  depthFrom = 0,
  depthTarget = 0,
  entryPath = "forward",
  returnPath = "exact-return",
  reducedMotionFallback = "crossfade",
} = {}) {
  if (!anchorId || !sourceRoute || !destinationRoute) return null;
  return Object.freeze({
    anchorId: String(anchorId),
    sourceRoute: String(sourceRoute),
    destinationRoute: String(destinationRoute),
    sourceRect: rectSnapshot(sourceRect),
    destinationRect: rectSnapshot(destinationRect),
    cameraFrom: cameraPoint(cameraFrom),
    cameraTarget: cameraPoint(cameraTarget),
    cameraOriginFrom: cameraPoint(cameraOriginFrom),
    cameraOriginTarget: cameraPoint(cameraOriginTarget),
    depthFrom: finite(depthFrom),
    depthTarget: finite(depthTarget),
    entryPath,
    returnPath,
    reducedMotionFallback,
  });
}

export function anchorSelector(anchorId, role) {
  if (!anchorId) return null;
  const escaped = String(anchorId).replace(/\\/g, "\\\\").replace(/"/g, '\\"');
  const roleClause = role ? `[data-spatial-anchor-role="${role}"]` : "";
  return `[data-spatial-anchor="${escaped}"]${roleClause}`;
}

export function cameraOriginFromRect(rect, viewport = {}) {
  const snap = rectSnapshot(rect);
  if (!snap) return { x: 50, y: 50 };
  const width = Math.max(1, finite(viewport.width, typeof window !== "undefined" ? window.innerWidth : 1));
  const height = Math.max(1, finite(viewport.height, typeof window !== "undefined" ? window.innerHeight : 1));
  return {
    x: Math.max(0, Math.min(100, ((snap.x + snap.width / 2) / width) * 100)),
    y: Math.max(0, Math.min(100, ((snap.y + snap.height / 2) / height) * 100)),
  };
}

/** Latest user intent wins. Older tokens become inert immediately. */
export function createCameraIntentController() {
  let token = 0;
  let phase = CAMERA_PHASES.IDLE;
  return {
    begin({ returning = false } = {}) {
      token += 1;
      phase = returning ? CAMERA_PHASES.RETURNING : CAMERA_PHASES.INTENT;
      return token;
    },
    isCurrent(candidate) {
      return candidate === token;
    },
    setPhase(candidate, nextPhase) {
      if (candidate !== token) return false;
      phase = nextPhase;
      return true;
    },
    cancel() {
      token += 1;
      phase = CAMERA_PHASES.IDLE;
    },
    get token() {
      return token;
    },
    get phase() {
      return phase;
    },
  };
}

export function nextCameraPhase(phase, { returning = false } = {}) {
  if (returning && phase === CAMERA_PHASES.RETURNING) return CAMERA_PHASES.LOCKING;
  const index = PHASE_ORDER.indexOf(phase);
  if (index < 0) return CAMERA_PHASES.IDLE;
  return PHASE_ORDER[index + 1] || CAMERA_PHASES.IDLE;
}
