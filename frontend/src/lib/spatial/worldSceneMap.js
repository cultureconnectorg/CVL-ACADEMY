import { routeToTopologyNode } from "@/lib/spatial/routeTopologyMap";

/**
 * Visual environment states for the existing Spatial topology.
 *
 * This file does not define navigation. App.js + routeTopologyMap.js + topology.js
 * remain authoritative. It only translates an already-known topology node into
 * restrained world/camera variables consumed by the visual background.
 */
export const WORLD_SCENES = Object.freeze({
  LANDING: {
    zone: "world",
    camera: "horizon",
    depth: 0,
    scale: 1,
    x: 0,
    y: 0,
    light: 1,
  },
  ONBOARDING: {
    zone: "gateway",
    camera: "approach",
    depth: 1,
    scale: 1.06,
    x: -2,
    y: 1,
    light: 1.04,
  },
  DASHBOARD: {
    zone: "hub",
    camera: "active",
    depth: 2,
    scale: 1.1,
    x: 1,
    y: 0,
    light: 1,
  },
  FORMATIONS: {
    zone: "learning-district",
    camera: "horizon",
    depth: 2,
    scale: 1.12,
    x: 4,
    y: -1,
    light: 1.03,
  },
  FORMATION: {
    zone: "learning-destination",
    camera: "focus",
    depth: 3,
    scale: 1.18,
    x: 7,
    y: -2,
    light: 1.08,
  },
  MODULE: {
    zone: "learning-interior",
    camera: "enter",
    depth: 4,
    scale: 1.25,
    x: 10,
    y: -3,
    light: 0.94,
  },
  ROADMAP: {
    zone: "horizon-path",
    camera: "horizon",
    depth: 2,
    scale: 1.1,
    x: -5,
    y: -2,
    light: 1.12,
  },
  MISSIONS_LIST: {
    zone: "action-district",
    camera: "active",
    depth: 2,
    scale: 1.12,
    x: -3,
    y: 2,
    light: 0.98,
  },
  BADGES: {
    zone: "achievement",
    camera: "reveal",
    depth: 2,
    scale: 1.1,
    x: 3,
    y: 2,
    light: 1.12,
  },
  SKILLS: {
    zone: "achievement",
    camera: "focus",
    depth: 2,
    scale: 1.12,
    x: 2,
    y: 2,
    light: 1.06,
  },
  CERTIFICATIONS: {
    zone: "achievement",
    camera: "confirm",
    depth: 2,
    scale: 1.1,
    x: 4,
    y: 1,
    light: 1.14,
  },
  WALLET: {
    zone: "value",
    camera: "active",
    depth: 2,
    scale: 1.08,
    x: -4,
    y: 1,
    light: 0.96,
  },
  FREK_PROFILE: {
    zone: "identity",
    camera: "focus",
    depth: 2,
    scale: 1.1,
    x: -2,
    y: 0,
    light: 1,
  },
});

export const STATIC_SCENE = Object.freeze({
  zone: "neutral",
  camera: "static",
  depth: 0,
  scale: 1,
  x: 0,
  y: 0,
  light: 1,
});

export function sceneForPathname(pathname) {
  const node = routeToTopologyNode(pathname);
  return {
    node,
    scene: (node && WORLD_SCENES[node]) || STATIC_SCENE,
  };
}
