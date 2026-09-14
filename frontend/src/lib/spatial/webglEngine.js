import * as THREE from "three";
import { EffectComposer } from "three/examples/jsm/postprocessing/EffectComposer.js";
import { RenderPass } from "three/examples/jsm/postprocessing/RenderPass.js";
import { UnrealBloomPass } from "three/examples/jsm/postprocessing/UnrealBloomPass.js";
import { SPATIAL_QUALITY } from "./devicePerformancePolicy";

/**
 * Vanilla three.js world engine. Dynamically imported so `three` never lands
 * in the main bundle for sessions that stay on the CSS world.
 *
 * PERFORMANCE CONTRACT
 * - visual fidelity stays route-compatible with the existing world;
 * - FULL keeps bloom + near-layer parallax;
 * - BALANCED stays single-plane/no-bloom;
 * - the renderer is paced adaptively instead of burning 60fps forever;
 * - hidden tabs stop completely;
 * - route-transition races cannot resurrect stale textures.
 */

const CAMERA_FOV = 50;
const CAMERA_Z = 6;
const FAR_Z = 0;
const NEAR_Z = 2.1;
const NEAR_BAND = 0.4;
const OVERSCAN_FAR = 1.06;
const OVERSCAN_NEAR = 1.32;
const CROSSFADE_MS = 900;
const POINTER_RANGE = 0.34;
const POINTER_LERP = 0.06;
const IDLE_DRIFT_AMPLITUDE = 0.05;
const IDLE_DRIFT_PERIOD_MS = 26000;
const EXPOSURE_BASE = 1.0;
const ACTIVE_WINDOW_MS = 1400;
const ACTIVE_FPS = 60;
const FULL_IDLE_FPS = 30;
const BALANCED_IDLE_FPS = 24;
const FULL_DPR_CAP = 1.5;
const BALANCED_DPR_CAP = 1.25;

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
  const idleFps = full ? FULL_IDLE_FPS : BALANCED_IDLE_FPS;
  const dprCap = full ? FULL_DPR_CAP : BALANCED_DPR_CAP;
  const renderer = new THREE.WebGLRenderer({
    canvas,
    antialias: true,
    powerPreference: "high-performance",
    alpha: false,
  });
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = EXPOSURE_BASE;
  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, dprCap));

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
  let transitionSerial = 0;

  const pointer = { x: 0, y: 0 };
  const pointerTarget = { x: 0, y: 0 };
  const panTarget = { x: 0, y: 0 };
  let contextActive = false;
  let activeUntil = performance.now() + ACTIVE_WINDOW_MS;

  let composer = null;
  let bloomPass = null;
  if (full) {
    composer = new EffectComposer(renderer);
    composer.addPass(new RenderPass(scene, camera));
    bloomPass = new UnrealBloomPass(new THREE.Vector2(1, 1), 0.55, 0.6, 0.82);
    composer.addPass(bloomPass);
  }

  function markActive(duration = ACTIVE_WINDOW_MS) {
    activeUntil = Math.max(activeUntil, performance.now() + duration);
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
    markActive(500);
  }

  function buildLayerSet(url) {
    return new Promise((resolve, reject) => {
      textureLoader.load(
        url,
        (texture) => {
          texture.colorSpace = THREE.SRGBColorSpace;
          texture.anisotropy = Math.min(4, renderer.capabilities.getMaxAnisotropy());
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
    const serial = ++transitionSerial;
    applyEnvironment(scene0);
    markActive(CROSSFADE_MS + 400);
    let built;
    try {
      built = await buildLayerSet(url);
    } catch {
      return;
    }
    if (disposed || serial !== transitionSerial) {
      disposeLayerSet(built);
      return;
    }
    if (incomingSet) disposeLayerSet(incomingSet);
    incomingSet = built;
    incomingSet.layers.forEach((layer) => {
      layer.material.opacity = 0;
    });
    crossfadeStart = performance.now();
  }

  function onCameraEvent(detail) {
    if (!detail?.kind) return;
    markActive();
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
  }

  function onPointerMove(event) {
    if (reduced) return;
    pointerTarget.x = (event.clientX / Math.max(window.innerWidth, 1) - 0.5) * POINTER_RANGE;
    pointerTarget.y = -(event.clientY / Math.max(window.innerHeight, 1) - 0.5) * POINTER_RANGE;
    markActive(500);
  }

  function onPointerLeave() {
    pointerTarget.x = 0;
    pointerTarget.y = 0;
    markActive(500);
  }

  if (typeof window !== "undefined") {
    window.addEventListener("pointermove", onPointerMove, { passive: true });
    document.documentElement.addEventListener("mouseleave", onPointerLeave, { passive: true });
  }

  const resizeObserver =
    typeof ResizeObserver !== "undefined" ? new ResizeObserver(() => resize()) : null;
  resizeObserver?.observe(canvas.parentElement || canvas);
  window.addEventListener("resize", resize);
  resize();

  let rafId = null;
  let lastAnimationT = performance.now();
  let lastRenderT = 0;

  function frame(t) {
    if (disposed) return;

    const targetFps = t < activeUntil || incomingSet ? ACTIVE_FPS : idleFps;
    const minFrameMs = 1000 / targetFps;
    if (t - lastRenderT < minFrameMs) {
      rafId = requestAnimationFrame(frame);
      return;
    }
    lastRenderT = t;

    const dt = Math.min(t - lastAnimationT, 100);
    lastAnimationT = t;

    const lerpScale = Math.max(1, dt / (1000 / 60));
    pointer.x += (pointerTarget.x - pointer.x) * Math.min(1, POINTER_LERP * lerpScale);
    pointer.y += (pointerTarget.y - pointer.y) * Math.min(1, POINTER_LERP * lerpScale);

    let driftX = 0;
    let driftY = 0;
    if (!reduced) {
      const phase = (t % IDLE_DRIFT_PERIOD_MS) / IDLE_DRIFT_PERIOD_MS;
      driftX = Math.sin(phase * Math.PI * 2) * IDLE_DRIFT_AMPLITUDE;
      driftY = Math.cos(phase * Math.PI * 2) * IDLE_DRIFT_AMPLITUDE * 0.6;
    }

    const contextScale = contextActive ? 0.3 : 1;
    camera.position.x = (pointer.x + panTarget.x * 0.6 + driftX) * contextScale;
    camera.position.y = (pointer.y + panTarget.y * 0.6 + driftY) * contextScale;
    camera.lookAt(camera.position.x * 0.4, camera.position.y * 0.4, FAR_Z);

    if (incomingSet) {
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

    rafId = requestAnimationFrame(frame);
  }

  rafId = requestAnimationFrame(frame);

  function handleVisibility() {
    if (document.hidden) {
      if (rafId) cancelAnimationFrame(rafId);
      rafId = null;
    } else if (!rafId && !disposed) {
      lastAnimationT = performance.now();
      lastRenderT = 0;
      markActive(500);
      rafId = requestAnimationFrame(frame);
    }
  }
  document.addEventListener("visibilitychange", handleVisibility);

  return {
    transitionTo,
    onCameraEvent,
    setContextActive(active) {
      contextActive = Boolean(active);
      markActive();
    },
    setReducedMotion(value) {
      reduced = Boolean(value);
      markActive(500);
      if (reduced) {
        pointerTarget.x = 0;
        pointerTarget.y = 0;
      }
    },
    dispose() {
      disposed = true;
      transitionSerial += 1;
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
