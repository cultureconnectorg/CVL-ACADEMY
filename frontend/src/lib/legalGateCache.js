import { api } from "./api";

// LegalGuard (see App.js) used to call GET /legal/requirements from scratch on
// every single client-side navigation between protected routes, because it is
// mounted per-<Route> and React Router unmounts/remounts it on every path
// change. That meant a real network round trip -- and a render that returns
// null while it's in flight -- before *any* protected page could paint, on
// every click. This module makes that check session-cached instead, while
// keeping the guarantee the backend fix (see e2e "legal gate backend failure
// stays technical instead of faking legal acceptance") relies on: a failed or
// unknown check is NEVER treated as accepted, and is never cached.
//
// Trade-off, spelled out: within TTL_MS, a repeat navigation trusts the last
// server answer instead of re-asking. That is intentionally not "check on
// every click" -- the previous behaviour was not a deliberate security
// control, it was an accidental side effect of the guard living inside the
// route tree. A ~5 minute freshness window is the accepted norm for this kind
// of session-scoped legal gate (comparable to a cookie-consent or ToS gate):
// the server is still the sole source of truth, callers must still route
// through a real GET /legal/requirements at least every TTL_MS, and every
// action that can actually change the answer forces a fresh check by calling
// invalidateLegalAcceptance() below rather than assuming the new state:
//   - a successful POST /legal/accept (LegalAcceptance.jsx)
//   - logout (auth.jsx) -- so a different account on the same tab never
//     inherits a stale verdict
// Rules unchanged from before this cache existed: a 401 still surfaces as
// "session expired", any other failure still surfaces as "service
// unavailable" (GateFailure), and neither is ever cached as "accepted".

const TTL_MS = 5 * 60 * 1000;

let cache = null; // { userId, accepted, checkedAt } | null
let inflight = null; // { userId, promise } | null

function isFresh(entry) {
  return Boolean(entry) && Date.now() - entry.checkedAt < TTL_MS;
}

/** Synchronous, no network: the last known-good answer for this user, if still fresh. */
export function peekLegalAcceptance(userId) {
  if (cache && cache.userId === userId && isFresh(cache)) {
    return { accepted: cache.accepted };
  }
  return null;
}

/** Resolves to { accepted }. Dedupes concurrent callers; never caches a rejection. */
export function fetchLegalAcceptance(userId) {
  const cached = peekLegalAcceptance(userId);
  if (cached) return Promise.resolve(cached);

  if (inflight && inflight.userId === userId) return inflight.promise;

  const promise = api
    .get("/legal/requirements")
    .then(({ data }) => {
      const result = { accepted: Boolean(data.accepted) };
      cache = { userId, accepted: result.accepted, checkedAt: Date.now() };
      inflight = null;
      return result;
    })
    .catch((error) => {
      inflight = null;
      cache = null;
      throw error;
    });

  inflight = { userId, promise };
  return promise;
}

/** Force the next check back to the network. Call after /legal/accept succeeds, and on logout. */
export function invalidateLegalAcceptance() {
  cache = null;
  inflight = null;
}
