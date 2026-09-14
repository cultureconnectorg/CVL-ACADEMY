const { test, expect } = require("@playwright/test");
const { mockAuthenticatedSession } = require("./fixtures/auth-fixture");

// ACA-0019 — the real formation-level learner resources (cas fil rouge,
// student templates, candidate guide) that read_model.py now actually
// returns are reachable and readable on the canonical formation page,
// closed by default so a long body is never dumped unrequested.
test.describe("canonical learner resources (ACA-0019)", () => {
  const FIXTURE_FORMATION = {
    canonical_formation_code: "FMS-01",
    metier_number: "01",
    metier_name: "Artist Development",
    canonical_version: "FMS_20260822_V1",
    pedagogical_source: "CANONICAL",
    module_codes_in_order: [],
    module_count: 0,
    pedagogical_case_title: "Anaïs Solaine",
    has_dedicated_skill_registry: true,
    has_infrastructure_doc: false,
    learner_resources: [
      {
        resource_type: "cas_fil_rouge",
        title: "Cas Fil Rouge — Anaïs Solaine",
        content_markdown: "Le cas Anaïs Solaine accompagne l'apprenant tout au long du parcours.",
        source_file: "10_FMS01_Cas_Fil_Rouge_Anais_Solaine.md",
      },
      {
        resource_type: "templates_etudiants",
        title: "Templates étudiants",
        content_markdown: "Gabarit vierge que l'apprenant remplit pour son diagnostic.",
        source_file: "60_FMS01_Templates_Etudiants.md",
      },
      {
        resource_type: "guide_candidat",
        title: "Guide Candidat",
        content_markdown: "Orientation pour le candidat avant l'entrée en formation.",
        source_file: "61_FMS01_Guide_Candidat.md",
      },
    ],
  };

  async function mockCanonicalFormation(page) {
    await mockAuthenticatedSession(page);
    await page.route("**/api/canonical/formations/FMS-01/modules", (route) =>
      route.fulfill({ status: 200, contentType: "application/json", body: "[]" })
    );
    await page.route("**/api/canonical/formations/FMS-01", (route) =>
      route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify(FIXTURE_FORMATION),
      })
    );
  }

  test("all 3 real learner resources render, collapsed by default", async ({ page }) => {
    await mockCanonicalFormation(page);
    await page.goto("/canonical/FMS-01");

    await expect(page.getByTestId("canonical-learner-resources")).toBeVisible();
    for (const type of ["cas_fil_rouge", "templates_etudiants", "guide_candidat"]) {
      await expect(page.getByTestId(`canonical-learner-resource-${type}`)).toBeVisible();
      await expect(
        page.getByTestId(`canonical-learner-resource-content-${type}`)
      ).toBeHidden();
    }
  });

  test("toggling one resource reveals its real content, others stay closed", async ({
    page,
  }) => {
    await mockCanonicalFormation(page);
    await page.goto("/canonical/FMS-01");

    await page.getByTestId("canonical-learner-resource-toggle-cas_fil_rouge").click();
    await expect(
      page.getByTestId("canonical-learner-resource-content-cas_fil_rouge")
    ).toContainText("Anaïs Solaine");
    await expect(
      page.getByTestId("canonical-learner-resource-content-templates_etudiants")
    ).toBeHidden();

    // Toggling closed again hides it.
    await page.getByTestId("canonical-learner-resource-toggle-cas_fil_rouge").click();
    await expect(
      page.getByTestId("canonical-learner-resource-content-cas_fil_rouge")
    ).toBeHidden();
  });
});
