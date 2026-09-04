/**
 * ACA-0006 — thin client for the canonical FMS runtime API
 * (`/api/canonical/...`). Kept separate from `lib/api.js`'s own concerns
 * so the legacy learning API surface stays untouched — this file only
 * adds new calls, it changes nothing existing.
 */
import { api } from "@/lib/api";

export function listCanonicalFormations() {
  return api.get("/canonical/formations").then((r) => r.data);
}

export function getCanonicalFormation(formationCode) {
  return api.get(`/canonical/formations/${formationCode}`).then((r) => r.data);
}

export function listCanonicalModules(formationCode) {
  return api.get(`/canonical/formations/${formationCode}/modules`).then((r) => r.data);
}

export function getCanonicalModule(formationCode, moduleCode) {
  return api
    .get(`/canonical/formations/${formationCode}/modules/${moduleCode}`)
    .then((r) => r.data);
}

export function markCanonicalContentViewed(formationCode, moduleCode) {
  return api
    .post(`/canonical/formations/${formationCode}/modules/${moduleCode}/viewed`)
    .then((r) => r.data);
}

export function getMyCanonicalProgress(formationCode) {
  return api
    .get("/canonical/progress/mine", { params: formationCode ? { formation_code: formationCode } : {} })
    .then((r) => r.data);
}
