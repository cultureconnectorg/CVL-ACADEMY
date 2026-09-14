import * as THREE from "three";
import { EffectComposer } from "three/examples/jsm/postprocessing/EffectComposer.js";
import { RenderPass } from "three/examples/jsm/postprocessing/RenderPass.js";
import { UnrealBloomPass } from "three/examples/jsm/postprocessing/UnrealBloomPass.js";
import { SPATIAL_QUALITY } from "./devicePerformancePolicy";

const CAMERA_FOV = 50;
const CAMERA_Z = 6;
const FAR_Z = 0;
const NEAR_Z = 2.1;
const NEAR_BAND = 0.4;
const OVERSCAN_FAR = 1.08;
const OVERSCAN_NEAR = 1.38;
const CROSSFADE_MS = 900;
const POINTER_RANGE = 0.34;
const TOUCH_RANGE = 0.22;
const POINTER_LERP = 0.06;
const SCROLL_RANGE = 0.22;
const IDLE_DRIFT_AMPLITUDE = 0.05;
const IDLE_DRIFT_PERIOD_MS = 26000;
const EXPOSURE_BASE = 1.0;
const SIGNAL_DECAY_MS = 2200;

function planeSize(camera, distance) {
  const vFov = (camera.fov * Math.PI) / 180;
  const height = 2 * Math.tan(vFov / 2) * distance;
  const width = height * camera.aspect;
  return { width, height };
}

function makeLayer(texture, { distanceFromCamera, band, overscan }) {
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
  return { mesh, material, geometry, distanceFromCamera, overscan };
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

function clamp(value, min, max) {
  return Math.max(min, Math.min(max, value));
}

export function createSpatialWorldEngine({ canvas, quality, reducedMotion }) {
  const full = quality === SPATIAL_QUALITY.FULL;
  const balanced = quality === SPATIAL_QUALITY.BALANCED;
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
  let baseExposure = EXPOSURE_BASE;
  let stageGrowth = 0;

  const pointer = { x: 0, y: 0 };
  const pointerTarget = { x: 0, y: 0 };
  const pan = { x: 0, y: 0 };
  const panTarget = { x: 0, y: 0 };
  let scrollTarget = 0;
  let scrollCurrent = 0;
  let contextActive = false;
  let touchStart = null;
  let signalStart = 0;
  let signalIntensity = 0;
  let signalBreath = 0;

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
    [currentSet, incomingSet].forEach((set) => set?.layers.forEach((layer) => resizeLayer(layer, camera)));
    requestFrame();
  }

  function buildLayerSet(url) {
    return new Promise((resolve, reject) => {
      textureLoader.load(
        url,
        (texture) => {
          texture.colorSpace = THREE.SRGBColorSpace;
          texture.anisotropy = full ? Math.min(4, renderer.capabilities.getMaxAnisotropy()) : 1;
          const layers = [
            makeLayer(texture, { distanceFromCamera: CAMERA_Z - FAR_Z, band: null, overscan: OVERSCAN_FAR }),
          ];
          // BALANCED now keeps one inexpensive foreground plane too. This is
          // what makes mobile feel spatial instead of like a static wallpaper.
          if (full || balanced) {
            const nearTexture = texture.clone();
            nearTexture.needsUpdate = true;
            layers.push(makeLayer(nearTexture, {
              distanceFromCamera: CAMERA_Z - NEAR_Z,
              band: NEAR_BAND,
              overscan: OVERSCAN_NEAR,
            }));
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

  function applyEnvironment(scene0, environment) {
    if (scene0) {
      baseExposure = EXPOSURE_BASE * (scene0.light ?? 1);
      panTarget.x = ((scene0.focusX ?? 50) - 50) / 100;
      panTarget.y = -((scene0.focusY ?? 50) - 50) / 100;
    }
    stageGrowth = clamp(environment?.growth ?? environment?.worldGrowth ?? 0, 0, 1);
    renderer.toneMappingExposure = baseExposure * (1 + stageGrowth * 0.035);
  }

  async function transitionTo({ url, scene: scene0, environment }) {
    if (disposed || !url) return;
    applyEnvironment(scene0, environment);
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
    incomingSet.layers.forEach((layer) => { layer.material.opacity = 0; });
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

  function onLearningSignal(profile) {
    if (!profile || reduced) return;
    signalStart = performance.now();
    signalIntensity = clamp(profile.intensity ?? 0.2, 0, 1);
    signalBreath = clamp(profile.worldBreath ?? 0.1, 0, 1);
    requestFrame();
  }

  function onPointerMove(event) {
    if (reduced) return;
    pointerTarget.x = (event.clientX / Math.max(window.innerWidth, 1) - 0.5) * POINTER_RANGE;
    pointerTarget.y = -(event.clientY / Math.max(window.innerHeight, 1) - 0.5) * POINTER_RANGE;
    requestFrame();
  }

  function onTouchStart(event) {
    if (reduced || !event.touches?.[0]) return;
    touchStart = { x: event.touches[0].clientX, y: event.touches[0].clientY };
  }

  function onTouchMove(event) {
    if (reduced || !touchStart || !event.touches?.[0]) return;
    const touch = event.touches[0];
    const dx = clamp((touch.clientX - touchStart.x) / Math.max(window.innerWidth, 1), -1, 1);
    const dy = clamp((touch.clientY - touchStart.y) / Math.max(window.innerHeight, 1), -1, 1);
    pointerTarget.x = dx * TOUCH_RANGE;
    pointerTarget.y = -dy * TOUCH_RANGE;
    requestFrame();
  }

  function onTouchEnd() {
    touchStart = null;
    pointerTarget.x *= 0.35;
    pointerTarget.y *= 0.35;
    requestFrame();
  }

  function onScroll() {
    if (reduced) return;
    const maxScroll = Math.max(document.documentElement.scrollHeight - window.innerHeight, 1);
    const progress = clamp(window.scrollY / maxScroll, 0, 1);
    scrollTarget = (progress - 0.5) * 2 * SCROLL_RANGE;
    requestFrame();
  }

  function onPointerLeave() {
    pointerTarget.x = 0;
    pointerTarget.y = 0;
    requestFrame();
  }

  if (typeof window !== "undefined") {
    window.addEventListener("pointermove", onPointerMove, { passive: true });
    window.addEventListener("touchstart", onTouchStart, { passive: true });
    window.addEventListener("touchmove", onTouchMove, { passive: true });
    window.addEventListener("touchend", onTouchEnd, { passive: true });
    window.addEventListener("scroll", onScroll, { passive: true });
    document.documentElement.addEventListener("mouseleave", onPointerLeave, { passive: true });
  }

  let rafId = null;
  let lastRenderedX = null;
  let lastRenderedY = null;
  let lastRenderedZ = null;
  let idleFrames = 0;
  const IDLE_STOP_AFTER = 8;
  const STILL_EPSILON = 0.0004;

  function requestFrame() {
    if (rafId === null && !disposed) rafId = requestAnimationFrame(frame);
  }

  const resizeObserver = typeof ResizeObserver !== "undefined" ? new ResizeObserver(() => resize()) : null;
  resizeObserver?.observe(canvas.parentElement || canvas);
  window.addEventListener("resize", resize);
  resize();
  onScroll();

  function frame(t) {
    if (disposed) return;

    pointer.x += (pointerTarget.x - pointer.x) * POINTER_LERP;
    pointer.y += (pointerTarget.y - pointer.y) * POINTER_LERP;
    pan.x += (panTarget.x - pan.x) * 0.045;
    pan.y += (panTarget.y - pan.y) * 0.045;
    scrollCurrent += (scrollTarget - scrollCurrent) * 0.055;

    let driftX = 0;
    let driftY = 0;
    if (!reduced && full) {
      const phase = (t % IDLE_DRIFT_PERIOD_MS) / IDLE_DRIFT_PERIOD_MS;
      driftX = Math.sin(phase * Math.PI * 2) * IDLE_DRIFT_AMPLITUDE;
      driftY = Math.cos(phase * Math.PI * 2) * IDLE_DRIFT_AMPLITUDE * 0.6;
    }

    let signal = 0;
    if (!reduced && signalStart > 0) {
      const elapsed = t - signalStart;
      if (elapsed < SIGNAL_DECAY_MS) {
        const normalized = 1 - elapsed / SIGNAL_DECAY_MS;
        signal = Math.sin(normalized * Math.PI) * signalIntensity;
      } else {
        signalStart = 0;
      }
    }

    const contextScale = contextActive ? 0.3 : 1;
    camera.position.x = (pointer.x + pan.x * 0.62 + driftX) * contextScale;
    camera.position.y = (pointer.y + pan.y * 0.62 + driftY + scrollCurrent * 0.52) * contextScale;
    camera.position.z = CAMERA_Z - signal * (0.16 + signalBreath * 0.22);
    camera.lookAt(camera.position.x * 0.35, camera.position.y * 0.35, FAR_Z);

    renderer.toneMappingExposure = baseExposure * (1 + stageGrowth * 0.035 + signal * 0.08);
    if (bloomPass) bloomPass.strength = 0.55 + signal * 0.38;

    // Different layer speeds make scroll/touch/camera motion perceptually real.
    [currentSet, incomingSet].forEach((set) => {
      if (!set) return;
      const near = set.layers[1];
      if (near) {
        near.mesh.position.x = -camera.position.x * 0.12;
        near.mesh.position.y = -camera.position.y * 0.16 - scrollCurrent * 0.13;
        near.mesh.scale.z = 1;
      }
    });

    const crossfading = Boolean(incomingSet);
    if (crossfading) {
      const p = Math.min(1, (t - crossfadeStart) / CROSSFADE_MS);
      incomingSet.layers.forEach((layer) => { layer.material.opacity = p; });
      currentSet?.layers.forEach((layer) => { layer.material.opacity = 1 - p; });
      if (p >= 1) {
        disposeLayerSet(currentSet);
        currentSet = incomingSet;
        incomingSet = null;
      }
    }

    if (composer) composer.render();
    else renderer.render(scene, camera);

    const settled =
      !full && !crossfading && signalStart === 0 &&
      lastRenderedX !== null &&
      Math.abs(camera.position.x - lastRenderedX) < STILL_EPSILON &&
      Math.abs(camera.position.y - lastRenderedY) < STILL_EPSILON &&
      Math.abs(camera.position.z - lastRenderedZ) < STILL_EPSILON;
    lastRenderedX = camera.position.x;
    lastRenderedY = camera.position.y;
    lastRenderedZ = camera.position.z;
    idleFrames = settled ? idleFrames + 1 : 0;

    if (idleFrames >= IDLE_STOP_AFTER) rafId = null;
    else rafId = requestAnimationFrame(frame);
  }

  function handleVisibility() {
    if (document.hidden) {
      if (rafId) cancelAnimationFrame(rafId);
      rafId = null;
    } else if (!disposed) requestFrame();
  }
  document.addEventListener("visibilitychange", handleVisibility);

  return {
    transitionTo,
    onCameraEvent,
    onLearningSignal,
    setContextActive(active) {
      contextActive = Boolean(active);
      requestFrame();
    },
    setReducedMotion(value) {
      reduced = Boolean(value);
      if (reduced) {
        pointerTarget.x = 0;
        pointerTarget.y = 0;
        scrollTarget = 0;
        signalStart = 0;
      }
      requestFrame();
    },
    dispose() {
      disposed = true;
      if (rafId) cancelAnimationFrame(rafId);
      window.removeEventListener("pointermove", onPointerMove);
      window.removeEventListener("touchstart", onTouchStart);
      window.removeEventListener("touchmove", onTouchMove);
      window.removeEventListener("touchend", onTouchEnd);
      window.removeEventListener("scroll", onScroll);
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
