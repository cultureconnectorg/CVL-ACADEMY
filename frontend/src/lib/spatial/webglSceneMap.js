/**
 * Maps a WORLD_SCENES key (frontend/src/lib/spatial/worldSceneMap.js) to a
 * real background photograph for the WebGL world (ADR W4 WEBGL DECISION
 * superseded — see docs/ADR_W5_WEBGL_REOPENED.md).
 *
 * Assets live at frontend/public/spatial/backgrounds/*.webp — sourced from
 * the Founder's own reference art, converted from PNG (~2.3MB each) to
 * WebP q82 (~200-320KB each) for real production delivery. Several
 * WORLD_SCENES keys deliberately share one image because they already
 * share a `zone` in worldSceneMap.js (SKILLS/BADGES/CERTIFICATIONS all use
 * "achievement") — one photograph per *zone*, not per route, matching the
 * existing "one continuous world" doctrine
 * (docs/ACADEMY_SPATIAL_END_TO_END_ARCHITECTURE.md §1).
 *
 * FREK_PROFILE has no dedicated reference image yet (no "identity" panel
 * was produced) — it borrows the Community photograph as the closest
 * thematic match (professional/social identity). Replace
 * BACKGROUND_BY_SCENE.FREK_PROFILE when a real one exists.
 */

const BASE = "/spatial/backgrounds";

export const BACKGROUND_BY_SCENE = Object.freeze({
  LANDING: `${BASE}/01_Landing.webp`,
  ONBOARDING: `${BASE}/02_Onboarding.webp`,
  DASHBOARD: `${BASE}/03_Dashboard.webp`,
  FORMATIONS: `${BASE}/04_Formations.webp`,
  FORMATION: `${BASE}/05_Detail_Formation.webp`,
  MODULE: `${BASE}/06_Module.webp`,
  ROADMAP: `${BASE}/10_Roadmap.webp`,
  MISSIONS_LIST: `${BASE}/07_Missions.webp`,
  BADGES: `${BASE}/08_Skills_Community.webp`,
  SKILLS: `${BASE}/08_Skills_Community.webp`,
  CERTIFICATIONS: `${BASE}/08_Skills_Community.webp`,
  WALLET: `${BASE}/09_Wallet.webp`,
  FREK_PROFILE: `${BASE}/11_Community.webp`,
});

/** Assets ready for surfaces not yet spatialized (no WORLD_SCENES entry today). */
export const RESERVED_BACKGROUNDS = Object.freeze({
  COMMUNITY: `${BASE}/11_Community.webp`,
  ADMIN: `${BASE}/12_Admin_Institutions_Partners.webp`,
});

export function backgroundForNode(node) {
  if (!node) return null;
  return BACKGROUND_BY_SCENE[node] || null;
}
