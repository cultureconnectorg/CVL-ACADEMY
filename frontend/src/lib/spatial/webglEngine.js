import * as THREE from "three";
import { EffectComposer } from "three/examples/jsm/postprocessing/EffectComposer.js";
import { RenderPass } from "three/examples/jsm/postprocessing/RenderPass.js";
import { UnrealBloomPass } from "three/examples/jsm/postprocessing/UnrealBloomPass.js";
import { SPATIAL_QUALITY } from "./devicePerformancePolicy";

/**
 * Vanilla three.js world engine (no react-three-fiber — matches the rest
 * of frontend/src/lib/spatial/*: plain functions/classes the React layer
 * calls into, same shape as makeRailPhysics/cameraFollow). Dynamically
 * imported by SpatialWebGLBackground.jsx so `three` never lands in the
 * main bundle for a session that never enables SPATIAL_WEBGL or that
 * falls back to the CSS world (LITE tier, no WebGL, reduced-motion-off
 * path is unaffected — reduced motion still renders this engine, just
 * with drift/parallax disabled, see setReducedMotion).
 *
 * Two textured planes per scene — the full photograph on a far plane,
 * and the same photograph's bottom band (water/rock/foliage in every
 * supplied reference image) UV-cropped onto a nearer plane — is a real,
 * long-established single-photo parallax technique (side-scroller
 * background layering, extended to a full photograph). Because both
 * planes sit at different distances from a real perspective camera,
 * pointer/idle camera movement produces genuine differential
 * parallax — not a CSS translate3d approximation.
 */

const CAMERA_FOV = 50;
const CAMERA_Z = 6;
const FAR_Z = 0;
const NEAR_Z = 2.1;
const NEAR_BAND = 0.4; // bottom 40% of each photograph
const OVERSCAN_FAR = 1.06;
const OVERSCAN_NEAR = 1.32;
const CROSSFADE_MS = 900;
const POINTER_RANGE = 0.34;
const POINTER_LERP = 0.06;
const IDLE_DRIFT_AMPLITUDE = 0.05;
const IDLE_DRIFT_PERIOD_MS = 26000;
const EXPOSURE_BASE = 1.0;

function planeSize(camera, distance) {
  const vFov = (camera.fov * Math.PI) / 180;
  const height = 2 * Math.tan(vFov / 2) * distance;
  const width = height * camera.aspect;
  return { width, height };
}

function makeLayer(texture, { distanceFromCamera, band, overscan }) {
  const size = { width: 1, height: 1 };
  const geometry = new THREE.PlaneGeometry(1, 1);
  const material = new THREE.MeshBasicMaterial({
    map: texture,
    transparent: true,
    opacity: 0,
    depthWrite: false,
    toneMapped: true,
  });
  const mesh = new THREE.Mesh(geometry, material);
  mesh.position.z = CAMERA_Z - distanceFromCamera;
  if (band) {
    texture.wrapS = THREE.ClampToEdgeWrapping;
    texture.wrapT = THREE.ClampToEdgeWrapping;
    texture.repeat.set(1, band);
    texture.offset.set(0, 0);
  }
  return { mesh, material, geometry, distanceFromCamera, overscan, size };
}

function resizeLayer(layer, camera) {
  const { width, height } = planeSize(camera, layer.distanceFromCamera);
  layer.mesh.scale.set(width * layer.overscan, height * layer.overscan, 1);
}

function disposeLayerSet(set) {
  if (!set) return;
  set.layers.forEach((layer) => {
    layer.geometry.dispose();
    layer.material.dispose();
    layer.material.map?.dispose?.();
    layer.mesh.parent?.remove(layer.mesh);
  });
}

export function createSpatialWorldEngine({ canvas, quality, reducedMotion }) {
  const full = quality === SPATIAL_QUALITY.FULL;
  // MSAA and a >1x pixel ratio both multiply fragment-shader work — real
  // cost on any GPU, more so on a phone's. BALANCED (the only tier touch
  // devices reach — see detectWebglQuality) skips both: at typical mobile
  // viewing distance a single un-antialiased 1x-DPR photograph reads as
  // sharp, and the saved fragment work is exactly what a phone GPU is
  // tightest on.
  const renderer = new THREE.WebGLRenderer({
    canvas,
    antialias: full,
    powerPreference: "high-performance",
    alpha: false,
  });
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = EXPOSURE_BASE;
  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, full ? 2 : 1));

  const scene = new THREE.Scene();
  scene.background = new THREE.Color(0x04101e);
  const camera = new THREE.PerspectiveCamera(CAMERA_FOV, 1, 0.1, 50);
  camera.position.set(0, 0, CAMERA_Z);

  const textureLoader = new THREE.TextureLoader();
  const root = new THREE.Group();
  scene.add(root);

  let currentSet = null;
  let incomingSet = null;
  let crossfadeStart = 0;
  let disposed = false;
  let reduced = Boolean(reducedMotion);

  const pointer = { x: 0, y: 0 };
  const pointerTarget = { x: 0, y: 0 };
  const panTarget = { x: 0, y: 0 };
  let contextActive = false;

  let composer = null;
  let bloomPass = null;
  if (full) {
    composer = new EffectComposer(renderer);
    composer.addPass(new RenderPass(scene, camera));
    bloomPass = new UnrealBloomPass(new THREE.Vector2(1, 1), 0.55, 0.6, 0.82);
    composer.addPass(bloomPass);
  }

  function resize() {
    const parent = canvas.parentElement;
    if (!parent) return;
    const width = parent.clientWidth || window.innerWidth;
    const height = parent.clientHeight || window.innerHeight;
    camera.aspect = width / Math.max(height, 1);
    camera.updateProjectionMatrix();
    renderer.setSize(width, height, false);
    composer?.setSize(width, height);
    [currentSet, incomingSet].forEach((set) => {
      set?.layers.forEach((layer) => resizeLayer(layer, camera));
    });
    requestFrame();
  }

  function buildLayerSet(url) {
    return new Promise((resolve, reject) => {
      textureLoader.load(
        url,
        (texture) => {
          texture.colorSpace = THREE.SRGBColorSpace;
          // Anisotropic filtering only pays for itself at a grazing viewing
          // angle; this photograph is viewed near head-on. Real sampling
          // cost, so BALANCED skips it same as antialiasing/DPR above.
          texture.anisotropy = full ? Math.min(4, renderer.capabilities.getMaxAnisotropy()) : 1;
          const layers = [
            makeLayer(texture, { distanceFromCamera: CAMERA_Z - FAR_Z, band: null, overscan: OVERSCAN_FAR }),
          ];
          if (full) {
            const nearTexture = texture.clone();
            nearTexture.needsUpdate = true;
            layers.push(
              makeLayer(nearTexture, {
                distanceFromCamera: CAMERA_Z - NEAR_Z,
                band: NEAR_BAND,
                overscan: OVERSCAN_NEAR,
              })
            );
          }
          layers.forEach((layer) => {
            resizeLayer(layer, camera);
            root.add(layer.mesh);
          });
          resolve({ layers });
        },
        undefined,
        reject
      );
    });
  }

  function applyEnvironment(scene0) {
    if (!scene0) return;
    renderer.toneMappingExposure = EXPOSURE_BASE * (scene0.light ?? 1);
    panTarget.x = ((scene0.focusX ?? 50) - 50) / 100;
    panTarget.y = -((scene0.focusY ?? 50) - 50) / 100;
  }

  async function transitionTo({ url, scene: scene0 }) {
    if (disposed || !url) return;
    applyEnvironment(scene0);
    let built;
    try {
      built = await buildLayerSet(url);
    } catch {
      return;
    }
    if (disposed) {
      disposeLayerSet(built);
      return;
    }
    if (incomingSet) disposeLayerSet(incomingSet);
    incomingSet = built;
    incomingSet.layers.forEach((layer) => {
      layer.material.opacity = 0;
    });
    crossfadeStart = performance.now();
    requestFrame();
  }

  function onCameraEvent(detail) {
    if (!detail?.kind) return;
    if (detail.cameraOriginFrom && (detail.kind === "LOCK" || detail.kind === "RETURN_LOCK")) {
      panTarget.x = (detail.cameraOriginFrom.x - 50) / 100;
      panTarget.y = -(detail.cameraOriginFrom.y - 50) / 100;
    } else if (detail.cameraOriginTarget && (detail.kind === "FOLLOW" || detail.kind === "RETURN_FOLLOW")) {
      panTarget.x = (detail.cameraOriginTarget.x - 50) / 100;
      panTarget.y = -(detail.cameraOriginTarget.y - 50) / 100;
    } else if (detail.kind === "CANCEL") {
      panTarget.x = 0;
      panTarget.y = 0;
    }
    requestFrame();
  }

  function onPointerMove(event) {
    if (reduced) return;
    pointerTarget.x = (event.clientX / Math.max(window.innerWidth, 1) - 0.5) * POINTER_RANGE;
    pointerTarget.y = -(event.clientY / Math.max(window.innerHeight, 1) - 0.5) * POINTER_RANGE;
    requestFrame();
  }
  function onPointerLeave() {
    pointerTarget.x = 0;
    pointerTarget.y = 0;
    requestFrame();
  }

  if (typeof window !== "undefined") {
    window.addEventListener("pointermove", onPointerMove, { passive: true });
    document.documentElement.addEventListener("mouseleave", onPointerLeave, { passive: true });
  }

  let rafId = null;
  let lastT = performance.now();
  // Idle-stop: once the scene has fully settled (no pending crossfade, camera
  // not meaningfully moving), rendering the exact same pixels forever wastes
  // GPU/CPU and — on a phone — battery/thermal headroom for zero visible
  // benefit. Touch devices never fire pointermove without an active drag, so
  // on BALANCED (the only tier touch reaches, see detectWebglQuality) this
  // routinely settles within a handful of frames after any scene/camera
  // change and goes fully dormant until the next real trigger (see
  // requestFrame(), called from every event handler below that can move the
  // camera or swap the photograph). FULL keeps its continuous idle drift —
  // desktop is untouched.
  let lastRenderedX = null;
  let lastRenderedY = null;
  let idleFrames = 0;
  const IDLE_STOP_AFTER = 6;
  const STILL_EPSILON = 0.0004;

  function requestFrame() {
    if (rafId === null && !disposed) {
      lastT = performance.now();
      rafId = requestAnimationFrame(frame);
    }
  }

  const resizeObserver =
    typeof ResizeObserver !== "undefined" ? new ResizeObserver(() => resize()) : null;
  resizeObserver?.observe(canvas.parentElement || canvas);
  window.addEventListener("resize", resize);
  resize();

  function frame(t) {
    if (disposed) return;
    lastT = t;

    pointer.x += (pointerTarget.x - pointer.x) * POINTER_LERP;
    pointer.y += (pointerTarget.y - pointer.y) * POINTER_LERP;

    let driftX = 0;
    let driftY = 0;
    if (!reduced && full) {
      const phase = (t % IDLE_DRIFT_PERIOD_MS) / IDLE_DRIFT_PERIOD_MS;
      driftX = Math.sin(phase * Math.PI * 2) * IDLE_DRIFT_AMPLITUDE;
      driftY = Math.cos(phase * Math.PI * 2) * IDLE_DRIFT_AMPLITUDE * 0.6;
    }

    const contextScale = contextActive ? 0.3 : 1;
    camera.position.x = (pointer.x + panTarget.x * 0.6 + driftX) * contextScale;
    camera.position.y = (pointer.y + panTarget.y * 0.6 + driftY) * contextScale;
    camera.lookAt(camera.position.x * 0.4, camera.position.y * 0.4, FAR_Z);

    const crossfading = Boolean(incomingSet);
    if (crossfading) {
      const elapsed = t - crossfadeStart;
      const p = Math.min(1, elapsed / CROSSFADE_MS);
      incomingSet.layers.forEach((layer) => {
        layer.material.opacity = p;
      });
      currentSet?.layers.forEach((layer) => {
        layer.material.opacity = 1 - p;
      });
      if (p >= 1) {
        disposeLayerSet(currentSet);
        currentSet = incomingSet;
        incomingSet = null;
      }
    }

    if (composer) composer.render();
    else renderer.render(scene, camera);

    const settled =
      !full &&
      !crossfading &&
      lastRenderedX !== null &&
      Math.abs(camera.position.x - lastRenderedX) < STILL_EPSILON &&
      Math.abs(camera.position.y - lastRenderedY) < STILL_EPSILON;
    lastRenderedX = camera.position.x;
    lastRenderedY = camera.position.y;

    if (settled) {
      idleFrames += 1;
    } else {
      idleFrames = 0;
    }

    if (idleFrames >= IDLE_STOP_AFTER) {
      rafId = null; // dormant — requestFrame() wakes it back up on demand
    } else {
      rafId = requestAnimationFrame(frame);
    }
  }
  // The loop is already running: the initial resize() call above (before
  // frame() existed textually, but function declarations hoist) already
  // called requestFrame() and scheduled the first frame.

  function handleVisibility() {
    if (document.hidden) {
      if (rafId) cancelAnimationFrame(rafId);
      rafId = null;
    } else if (!disposed) {
      requestFrame();
    }
  }
  document.addEventListener("visibilitychange", handleVisibility);

  return {
    transitionTo,
    onCameraEvent,
    setContextActive(active) {
      contextActive = Boolean(active);
      requestFrame();
    },
    setReducedMotion(value) {
      reduced = Boolean(value);
      if (reduced) {
        pointerTarget.x = 0;
        pointerTarget.y = 0;
      }
      requestFrame();
    },
    dispose() {
      disposed = true;
      if (rafId) cancelAnimationFrame(rafId);
      window.removeEventListener("pointermove", onPointerMove);
      document.documentElement.removeEventListener("mouseleave", onPointerLeave);
      window.removeEventListener("resize", resize);
      document.removeEventListener("visibilitychange", handleVisibility);
      resizeObserver?.disconnect();
      disposeLayerSet(currentSet);
      disposeLayerSet(incomingSet);
      composer?.dispose?.();
      renderer.dispose();
    },
  };
}
