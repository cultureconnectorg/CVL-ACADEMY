/**
 * "raccorder ces corpus au même runtime/funnel Academy" (Founder,
 * 2026-09-07) — thin client for the canonical FREK runtime API
 * (`/api/frk-canonical/...`). Mirrors `lib/canonicalKorApi.js` exactly
 * (minus the skills endpoint — FRK's real corpus carries no skill
 * registry, see `frk_canonical/models.py`'s own docstring); kept as
 * its own file so the FMS/Kiltikonet/KORA canonical surfaces stay
 * untouched.
 */
import { api } from "@/lib/api";

export function listCanonicalFrkFormations() {
  return api.get("/frk-canonical/formations").then((r) => r.data);
}

export function getCanonicalFrkFormation(formationCode) {
  return api.get(`/frk-canonical/formations/${formationCode}`).then((r) => r.data);
}

export function listCanonicalFrkModules(formationCode) {
  return api
    .get(`/frk-canonical/formations/${formationCode}/modules`)
    .then((r) => r.data);
}

export function getCanonicalFrkModule(formationCode, moduleCode) {
  return api
    .get(`/frk-canonical/formations/${formationCode}/modules/${moduleCode}`)
    .then((r) => r.data);
}

export function markCanonicalFrkContentViewed(formationCode, moduleCode) {
  return api
    .post(`/frk-canonical/formations/${formationCode}/modules/${moduleCode}/viewed`)
    .then((r) => r.data);
}

export function getMyCanonicalFrkProgress(formationCode) {
  return api
    .get("/frk-canonical/progress/mine", {
      params: formationCode ? { formation_code: formationCode } : {},
    })
    .then((r) => r.data);
}
