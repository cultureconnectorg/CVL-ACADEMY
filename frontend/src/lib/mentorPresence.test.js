import { isPedagogicalContext } from "@/lib/mentorPresence";

describe("mentor contextual presence (W3-C)", () => {
  test("true inside a module (ModuleJourney)", () => {
    expect(isPedagogicalContext("/formations/FMS-01/modules/FMS-01-M01")).toBe(true);
  });

  test("true with a trailing slash", () => {
    expect(isPedagogicalContext("/formations/FMS-01/modules/FMS-01-M01/")).toBe(true);
  });

  test("false on formation discovery/detail — browsing is not mid-lesson", () => {
    expect(isPedagogicalContext("/formations")).toBe(false);
    expect(isPedagogicalContext("/formations/FMS-01")).toBe(false);
  });

  test("false on dashboard, missions, badges, wallet, frek-profile, roadmap", () => {
    ["/dashboard", "/missions", "/badges", "/wallet", "/frek-profile", "/roadmap", "/skills", "/certifications"].forEach(
      (path) => expect(isPedagogicalContext(path)).toBe(false)
    );
  });

  test("false on staff screens", () => {
    ["/trainer", "/jury", "/admin"].forEach((path) => expect(isPedagogicalContext(path)).toBe(false));
  });

  test("false on the public landing and onboarding", () => {
    expect(isPedagogicalContext("/")).toBe(false);
    expect(isPedagogicalContext("/onboarding")).toBe(false);
  });

  test("does not false-positive on a path that merely contains the words", () => {
    expect(isPedagogicalContext("/formations/modules-are-great/details")).toBe(false);
  });
});
