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
 *
 * Each photograph also has a "-mobile" sibling (900px-wide source, same
 * WebP q78 pipeline; ~38% of the desktop file's weight, see
 * scripts/backgrounds/ generation note in the perf commit that added
 * these) generated alongside it. A narrow viewport never benefits from the
 * full 1570px-wide source -- it's downscaled by the browser/GPU on decode
 * regardless -- so backgroundForNode() below picks the smaller file for it
 * automatically. This does not touch renderer quality (antialiasing/DPR/
 * anisotropy, see webglEngine.js) at all; it is a separate, additive win on
 * the network payload every scene transition has to download first.
 */

const BASE = "/spatial/backgrounds";
const MOBILE_MAX_VIEWPORT = 900; // px, matches the -mobile asset's generation width

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

/**
 * @param {string} node
 * @param {{ viewportWidth?: number }} [options] viewportWidth in CSS px; when
 *   given and <= MOBILE_MAX_VIEWPORT, returns the lighter "-mobile" asset.
 */
export function backgroundForNode(node, { viewportWidth } = {}) {
  if (!node) return null;
  const desktopUrl = BACKGROUND_BY_SCENE[node] || null;
  if (!desktopUrl) return null;
  if (typeof viewportWidth === "number" && viewportWidth > 0 && viewportWidth <= MOBILE_MAX_VIEWPORT) {
    return desktopUrl.replace(/\.webp$/, "-mobile.webp");
  }
  return desktopUrl;
}
