import React from "react";
import ReactDOM from "react-dom/client";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import "@/index.css";
import App from "@/App";
import * as serviceWorkerRegistration from "@/serviceWorkerRegistration";

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 60_000,
      refetchOnWindowFocus: false,
    },
  },
});

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  <React.StrictMode>
    <QueryClientProvider client={queryClient}>
      <App />
    </QueryClientProvider>
  </React.StrictMode>,
);

// Registers the precaching service worker in production builds only —
// see src/service-worker.js / src/serviceWorkerRegistration.js.
//
// onUpdate fires once a new service worker has already installed,
// activated and claimed this tab (service-worker.js calls skipWaiting()
// unconditionally, so there is no "waiting" worker to unblock here) — the
// tab's already-loaded JS/HTML is still the previous deploy's until it
// reloads. A guarded one-time reload closes that gap automatically
// instead of leaving a user stuck on stale UI until they notice and
// refresh themselves.
const SW_RELOAD_GUARD_KEY = "cvln_sw_update_reload_attempted";
serviceWorkerRegistration.register({
  onUpdate: () => {
    let alreadyReloaded = false;
    try {
      alreadyReloaded = sessionStorage.getItem(SW_RELOAD_GUARD_KEY) === "1";
      if (!alreadyReloaded) sessionStorage.setItem(SW_RELOAD_GUARD_KEY, "1");
    } catch {
      alreadyReloaded = true;
    }
    if (!alreadyReloaded) window.location.reload();
  },
});
