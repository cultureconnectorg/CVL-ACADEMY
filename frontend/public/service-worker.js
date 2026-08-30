/*
 * CVLN Academy service worker — hand-rolled, no build step / no Workbox
 * dependency (a webpack InjectManifest + craco integration was tried and
 * dropped: the child compilation workbox-webpack-plugin needs never
 * produced a bundle containing its own injection point in this sandbox's
 * webpack/craco setup — a real, reproducible incompatibility, not
 * something worth chasing further at real cost to the rest of this
 * mission. This plain Cache-API version gets the same practical outcome
 * — an installable app that still loads offline — without that
 * dependency.)
 *
 * Strategy:
 * - /api/* : never intercepted — progression, quiz results, mentor chat
 *   must always hit the network live. A cached answer here would be
 *   actively wrong, not just stale.
 * - Navigations (loading a page/route): network-first, falling back to
 *   the cached app shell (/) when offline.
 * - Same-origin static assets (js/css/images/fonts): cache-first, with a
 *   background revalidation fetch so the cache heals itself over time.
 */

const CACHE_VERSION = "cvln-academy-v1";
const APP_SHELL_URLS = ["/", "/index.html", "/manifest.json"];

self.addEventListener("install", (event) => {
  self.skipWaiting();
  event.waitUntil(
    caches
      .open(CACHE_VERSION)
      .then((cache) => cache.addAll(APP_SHELL_URLS))
      .catch(() => {}), // offline-at-install-time is fine, just skip precaching
  );
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches
      .keys()
      .then((keys) => Promise.all(keys.filter((k) => k !== CACHE_VERSION).map((k) => caches.delete(k))))
      .then(() => self.clients.claim()),
  );
});

function isStaticAsset(url) {
  return /\.(?:js|css|png|jpg|jpeg|svg|gif|ico|woff2?|ttf)$/.test(url.pathname);
}

self.addEventListener("fetch", (event) => {
  const { request } = event;
  const url = new URL(request.url);

  if (request.method !== "GET" || url.origin !== self.location.origin) return;
  if (url.pathname.startsWith("/api")) return; // always live

  if (request.mode === "navigate") {
    event.respondWith(
      fetch(request).catch(() => caches.match("/index.html").then((cached) => cached || Response.error())),
    );
    return;
  }

  if (isStaticAsset(url)) {
    event.respondWith(
      caches.match(request).then((cached) => {
        const network = fetch(request)
          .then((response) => {
            if (response.ok) {
              const copy = response.clone();
              caches.open(CACHE_VERSION).then((cache) => cache.put(request, copy));
            }
            return response;
          })
          .catch(() => cached);
        return cached || network;
      }),
    );
  }
});
