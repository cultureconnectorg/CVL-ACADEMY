import axios from "axios";
import { emitSpatialSignalFromResponse } from "@/lib/spatial/spatialLearningSignals";

/**
 * Build one canonical API base from whatever was entered in
 * REACT_APP_BACKEND_URL.
 *
 * Accepted examples all resolve to the same result:
 * - https://cvl-academy.onrender.com
 * - https://cvl-academy.onrender.com/
 * - https://cvl-academy.onrender.com/api
 * - https://cvl-academy.onrender.com/api/auth/register
 *
 * This prevents malformed requests such as
 * /api/auth/register/api/auth/register when the environment variable was
 * accidentally configured with a full endpoint instead of the backend root.
 */
export function normalizeBackendApiBase(rawValue = "") {
  const value = String(rawValue || "").trim().replace(/\/+$/, "");
  if (!value) return "/api";

  // Strip an existing /api segment and anything after it, then append exactly
  // one canonical /api suffix. Matching is case-insensitive and only applies
  // to a real path segment, so hostnames containing the letters "api" are safe.
  const backendRoot = value.replace(/\/api(?:\/.*)?$/i, "");
  return `${backendRoot}/api`;
}

const rawBackendUrl = process.env.REACT_APP_BACKEND_URL || "";
export const API_BASE = normalizeBackendApiBase(rawBackendUrl);

const TOKEN_KEY = "cvln_token";
const REFRESH_KEY = "cvln_refresh_token";

export function getToken() {
  return localStorage.getItem(TOKEN_KEY);
}

export function setSession({ token, refresh_token }) {
  if (token) localStorage.setItem(TOKEN_KEY, token);
  if (refresh_token) localStorage.setItem(REFRESH_KEY, refresh_token);
}

export function clearSession() {
  localStorage.removeItem(TOKEN_KEY);
  localStorage.removeItem(REFRESH_KEY);
}

export const api = axios.create({ baseURL: API_BASE });

api.interceptors.request.use((config) => {
  const t = getToken();
  if (t) config.headers.Authorization = `Bearer ${t}`;
  return config;
});

// The access token is short-lived (2h) by design — a 401 triggers one
// silent refresh-token exchange + retry before falling back to logout, so
// users aren't kicked out mid-session just because the access token aged out.
let refreshInFlight = null;

async function refreshAccessToken() {
  const refreshToken = localStorage.getItem(REFRESH_KEY);
  if (!refreshToken) return null;
  if (!refreshInFlight) {
    refreshInFlight = axios
      .post(`${API_BASE}/auth/refresh`, { refresh_token: refreshToken })
      .then(({ data }) => {
        setSession(data);
        return data.token;
      })
      .catch(() => {
        clearSession();
        return null;
      })
      .finally(() => {
        refreshInFlight = null;
      });
  }
  return refreshInFlight;
}

api.interceptors.response.use(
  (response) => {
    // Spatial is a perceptual subscriber only. A failed visual signal must
    // never block, mutate, or change the backend-owned business response.
    emitSpatialSignalFromResponse(response);
    return response;
  },
  async (err) => {
    const original = err?.config;
    if (err?.response?.status === 401 && original && !original._retried) {
      original._retried = true;
      const newToken = await refreshAccessToken();
      if (newToken) {
        original.headers.Authorization = `Bearer ${newToken}`;
        return api(original);
      }
      clearSession();
    }
    return Promise.reject(err);
  }
);
