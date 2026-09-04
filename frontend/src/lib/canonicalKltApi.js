/**
 * "Branchage complet de Kiltikonet" (Founder, 2026-09-04) — thin client
 * for the canonical Kiltikonet runtime API (`/api/klt-canonical/...`).
 * Mirrors `lib/canonicalApi.js` exactly; kept as its own file so the FMS
 * canonical surface stays untouched.
 */
import { api } from "@/lib/api";

export function listCanonicalKltFormations() {
  return api.get("/klt-canonical/formations").then((r) => r.data);
}

export function getCanonicalKltFormation(formationCode) {
  return api.get(`/klt-canonical/formations/${formationCode}`).then((r) => r.data);
}

export function listCanonicalKltModules(formationCode) {
  return api
    .get(`/klt-canonical/formations/${formationCode}/modules`)
    .then((r) => r.data);
}

export function getCanonicalKltModule(formationCode, moduleCode) {
  return api
    .get(`/klt-canonical/formations/${formationCode}/modules/${moduleCode}`)
    .then((r) => r.data);
}

export function listCanonicalKltSkills(formationCode) {
  return api
    .get(`/klt-canonical/formations/${formationCode}/skills`)
    .then((r) => r.data);
}

export function markCanonicalKltContentViewed(formationCode, moduleCode) {
  return api
    .post(`/klt-canonical/formations/${formationCode}/modules/${moduleCode}/viewed`)
    .then((r) => r.data);
}

export function getMyCanonicalKltProgress(formationCode) {
  return api
    .get("/klt-canonical/progress/mine", {
      params: formationCode ? { formation_code: formationCode } : {},
    })
    .then((r) => r.data);
}
