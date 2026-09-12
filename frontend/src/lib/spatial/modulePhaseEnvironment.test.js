import { environmentForModulePhase } from "./modulePhaseEnvironment";

describe("module phase environment", () => {
  test("deep learning phases calm the world more than action phases", () => {
    const course = environmentForModulePhase("course");
    const quiz = environmentForModulePhase("quiz");
    const workshop = environmentForModulePhase("workshop");
    expect(course.activity).toBeLessThan(workshop.activity);
    expect(quiz.activity).toBeLessThan(workshop.activity);
    expect(quiz.focus).toBeGreaterThan(workshop.focus);
  });

  test("unknown phases never fabricate an environment", () => {
    expect(environmentForModulePhase("unknown")).toBeNull();
    expect(environmentForModulePhase(null)).toBeNull();
  });
});
