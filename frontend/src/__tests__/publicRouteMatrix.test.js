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
    expect(appSource).toMatch(new RegExp(`path=\\"${escaped}\\"[^>]*element=\\{<PublicOrMember>`));
  });

  test.each(protectedRoutes)("%s remains protected", (route) => {
    const escaped = route.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
    expect(appSource).toMatch(new RegExp(`path=\\"${escaped}\\"[^>]*element=\\{<Protected`));
  });

  test("module content route is not public", () => {
    expect(appSource).not.toMatch(/path=\"\/formations\/:fc\/modules\/:mc\"[^>]*PublicOrMember/);
  });

  test("public auth routes exist", () => {
    expect(appSource).toContain('path="/login"');
    expect(appSource).toContain('path="/register"');
  });
});
