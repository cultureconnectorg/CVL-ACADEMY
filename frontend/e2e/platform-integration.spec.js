const { test, expect } = require("@playwright/test");

const backendUrl = process.env.E2E_BACKEND_URL || "http://127.0.0.1:4174";

test("browser can reach the real Academy backend and Mongo-backed readiness", async ({ page }) => {
  await page.goto("/");

  const result = await page.evaluate(async (url) => {
    const response = await fetch(`${url}/api/health/ready`);
    const body = await response.json();
    return { status: response.status, body };
  }, backendUrl);

  expect(result.status).toBe(200);
  expect(result.body.status).toBe("ready");
  expect(result.body.startup_ready).toBe(true);
  expect(result.body.mongo_ready).toBe(true);
});
