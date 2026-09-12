const fs = require("fs");
const path = require("path");

function read(name) {
  return fs.readFileSync(path.resolve(__dirname, `../pages/${name}`), "utf8");
}

describe("public discovery data boundary", () => {
  test("wallet/me is only loaded from authenticated branch", () => {
    const source = read("Wallet.js");
    expect(source).toContain('if (!user)');
    expect(source).toMatch(/api\s*\.\s*get\("\/wallet\/me"\)/);
    expect(source).toContain('data-public="true"');
  });

  test("FREK personal profile is not loaded for anonymous visitors", () => {
    const source = read("FrekProfile.js");
    expect(source).toContain('if (!user)');
    expect(source).toContain('api.get("/frek/profile")');
    expect(source).toContain('data-public="true"');
  });

  test("missions mine/actions remain member-only in the UI", () => {
    const source = read("Missions.js");
    expect(source).toContain('api.get("/missions")');
    expect(source).toContain('api.get("/missions/mine")');
    expect(source).toContain('if (!user) return;');
  });

  test("certification attempts remain member-only while rubrics stay public", () => {
    const source = read("Certifications.js");
    expect(source).toContain('api.get("/certifications/rubrics")');
    expect(source).toContain('api.get("/certifications/attempts/mine")');
    expect(source).toContain('if (!user) return;');
  });

  test("skills switch between public registry and member progression", () => {
    const source = read("Skills.js");
    expect(source).toContain('user ? "/skills/mine" : "/skills"');
  });

  test("anonymous formation modules lead to registration, not module content", () => {
    const source = read("FormationDetail.js");
    expect(source).toContain('data-testid={`module-preview-${m.code}`}');
    expect(source).toContain('to="/register"');
    expect(source).toContain('to={`/formations/${code}/modules/${m.code}`}');
  });
});
