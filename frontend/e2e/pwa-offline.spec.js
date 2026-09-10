const { test, expect } = require("@playwright/test");

// RG-07 / LRN-008 — real production-build PWA smoke. This is not run by
// the normal dev-server E2E pass because service-worker registration is
// intentionally production-only. `playwright.pwa.config.js` serves the
// actual `build/` directory so this test exercises the shipped worker.
test("installed production shell reloads while offline and never fabricates API data", async ({
  page,
  context,
}) => {
  await page.goto("/");
  await expect(page.locator("body")).toBeVisible();

  const registrationState = await page.evaluate(async () => {
    if (!("serviceWorker" in navigator)) return "unsupported";
    const registration = await navigator.serviceWorker.ready;
    return registration.active?.state || "missing";
  });
  expect(registrationState).toBe("activated");

  // One controlled reload ensures the active worker is actually in the
  // navigation path before connectivity is removed.
  await page.reload();
  await expect.poll(() => page.evaluate(() => Boolean(navigator.serviceWorker.controller))).toBe(true);

  await context.setOffline(true);
  await page.reload({ waitUntil: "domcontentloaded" });

  // The cached SPA shell must still render instead of Chromium's offline
  // error page. We intentionally don't claim authenticated content can
  // progress offline: /api is excluded from the service worker by design.
  await expect(page.locator("#root")).toBeAttached();
  await expect(page.locator("body")).not.toContainText("ERR_INTERNET_DISCONNECTED");

  const apiResult = await page.evaluate(async () => {
    try {
      await fetch("/api/__pwa_probe__");
      return "unexpected-response";
    } catch {
      return "network-failed";
    }
  });
  expect(apiResult).toBe("network-failed");

  await context.setOffline(false);
});
