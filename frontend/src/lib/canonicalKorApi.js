/**
 * RAIL 2 — "Master -> Runtime Academy" (Founder, 2026-09-06) — thin
 * client for the canonical KORA runtime API (`/api/kor-canonical/...`).
 * Mirrors `lib/canonicalKltApi.js` exactly; kept as its own file so the
 * FMS/Kiltikonet canonical surfaces stay untouched.
 */
import { api } from "@/lib/api";

export function listCanonicalKorFormations() {
  return api.get("/kor-canonical/formations").then((r) => r.data);
}

export function getCanonicalKorFormation(formationCode) {
  return api.get(`/kor-canonical/formations/${formationCode}`).then((r) => r.data);
}

export function listCanonicalKorModules(formationCode) {
  return api
    .get(`/kor-canonical/formations/${formationCode}/modules`)
    .then((r) => r.data);
}

export function getCanonicalKorModule(formationCode, moduleCode) {
  return api
    .get(`/kor-canonical/formations/${formationCode}/modules/${moduleCode}`)
    .then((r) => r.data);
}

export function listCanonicalKorSkills(formationCode) {
  return api
    .get(`/kor-canonical/formations/${formationCode}/skills`)
    .then((r) => r.data);
}

export function markCanonicalKorContentViewed(formationCode, moduleCode) {
  return api
    .post(`/kor-canonical/formations/${formationCode}/modules/${moduleCode}/viewed`)
    .then((r) => r.data);
}

export function getMyCanonicalKorProgress(formationCode) {
  return api
    .get("/kor-canonical/progress/mine", {
      params: formationCode ? { formation_code: formationCode } : {},
    })
    .then((r) => r.data);
}
