const fs = require("fs");
const path = require("path");

const appSource = fs.readFileSync(path.resolve(__dirname, "../App.js"), "utf8");

const hybridRoutes = [
  "/roadmap",
  "/formations",
  "/formations/:code",
  "/missions",
  "/badges",
  "/frek-profile",
  "/wallet",
  "/skills",
  "/certifications",
];

const protectedRoutes = [
  "/dashboard",
  "/formations/:fc/modules/:mc",
  "/trainer",
  "/jury",
  "/admin",
  "/admin/stakeholders",
];

describe("public/internal/hybrid route matrix", () => {
  test.each(hybridRoutes)("%s is wired through PublicOrMember", (route) => {
    const escaped = route.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
    expect(appSource).toMatch(new RegExp(`path="${escaped}"\\s*element=\\{<PublicOrMember>`));
  });

  test.each(protectedRoutes)("%s remains protected", (route) => {
    const escaped = route.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
    expect(appSource).toMatch(new RegExp(`path="${escaped}"\\s*element=\\{\\s*<Protected`));
  });

  test("module content route is not public", () => {
    // RECONCILE-2 Groupe 4 (2026-09-14): the original `[\s\S]*?` here matched
    // "PublicOrMember" ANYWHERE later in the file, not just on this route's
    // own declaration — since several genuinely-hybrid routes (missions,
    // badges, ...) legitimately follow this one, the assertion was already
    // failing against main's own unmodified App.js before this group ever
    // touched it (confirmed against the pre-reconciliation file). Narrowed
    // to check only this route's own `element={...}`, matching the same
    // adjacency style as the `protectedRoutes` check above (which already
    // covers this exact route against `<Protected`, so this test is now a
    // non-redundant, narrower negative check on the same declaration).
    expect(appSource).not.toMatch(
      /path="\/formations\/:fc\/modules\/:mc"\s*element=\{<PublicOrMember/
    );
  });

  test("public auth routes exist", () => {
    expect(appSource).toContain('path="/login"');
    expect(appSource).toContain('path="/register"');
  });
});
