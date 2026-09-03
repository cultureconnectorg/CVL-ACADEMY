# ACA-0003 — FMS Canonical Delta Matrix

```
MODE = ANALYSIS_ONLY. No mutation performed: db.formations, db.progress,
module codes, and the FMS corpus in production are all untouched.
Founder authorization for this pass: DEC-002 (FMS_Chantier_Complet_
20260822.zip = CANONICAL_FOR_NOW), G1 = PASSED_FOR_ANALYSIS_ONLY,
G2 = NOT_AUTHORIZED, G3 = NOT_AUTHORIZED.
STOP_AFTER_DELIVERY = TRUE.
```

## Method

The canonical archive (`FMS_Chantier_Complet_20260822.zip`, 223 Markdown
files) was extracted and read in full: every `00_INDEX.md` status line,
every `Master_Module_Map.md` (all 6 métiers), every registry/rubric/
infrastructure file that exists, and representative module content
(`08_FMS01_Master_Learning_Map.md`, `09_FMS01_Master_Module_Map.md`,
`01_FMS-A_Referentiel_Artist_Development.md`). This was cross-checked
against the repo's own prior validation of this exact archive
(`docs/FMS_IMPORT_VALIDATION_REPORT.md` — 223/223 files parsed, 0 errors,
26 real types) and against what the repo actually serves today:
`backend/seed_data.py` (30-formation catalogue, `FORMATIONS[...]`),
`backend/seed_modules.py` (module content for the "coming_soon"
formations), `backend/models.py` (`ModuleProgress`), `backend/fms_import/`
(parser/module_map/importer/indexer), `backend/skills/models.py`,
`backend/certification/models.py`.

**Canonical source confirmed by its own index as final**: the last
"État d'avancement global" block in `00_INDEX.md` reads *"CHANTIER DES
6 MÉTIERS COMPLET"* — all six packages (FMS-01 V1.0, FMS-02 V1.1, FMS-03
through FMS-06 V1.0) marked 🔒 locked and individually audited (a
documented 5-question lock audit per métier, with real defects found and
corrected in the archive itself — see §"Data-quality notes" below). Next
step stated by the archive's own authors: *"Intégration des six métiers
dans CVLN Academy."* That integration is exactly what `G2`/`G3` gate and
remain `NOT_AUTHORIZED` this pass.

---

## 1. Delta exact par métier FMS-01 → FMS-06

| Métier | Canonical status (per `00_INDEX.md`) | Canonical modules | Canonical doc types present | Repo-served formation | Repo-served modules | Repo module code format |
|---|---|---|---|---|---|---|
| FMS-01 Artist Development | 🔒 Package V1.0 verrouillé | **15** (M01–M15) + A01 | Full 21-type set (see §3) | `FMS-01` in `seed_data.py`, inline | **12** (M01–M12) | `FMS-01-M01` |
| FMS-02 Music Business | 🔒 Package V1.1 verrouillé | **16** (M01–M16) + A02 | Full 21-type set | `FMS-02` in `seed_data.py`, inline | **10** (M01–M10) | `FMS-02-M01` |
| FMS-03 Music Production | 🔒 Package V1.0 verrouillé | **16** (M01–M16) + A03 | Full 21-type set | `FMS-03` in `seed_data.py`, inline | **8** (M01–M08) | `FMS-03-M01` |
| FMS-04 Artist Branding | 🔒 Package V1.0 verrouillé | **16** (M01–M16) + A04 | 18-type set — **no** `Evidence_Registry`/`Skill_IDs_Registry`/`Rubric_Master`, **has** `Infrastructure.md` (see §3) | `FMS-04` in `seed_data.py`; modules injected from `seed_modules.py` | **8** (M01–M08) | `FMS-04-M01` |
| FMS-05 Artist Management | 🔒 Package V1.0 verrouillé | **16** (M01–M16) + A05 | Same 18-type set as FMS-04 | `FMS-05` in `seed_data.py`; modules from `seed_modules.py` | **8** (M01–M08) | `FMS-05-M01` |
| FMS-06 Executive/Cultural Production | 🔒 Package V1.0 COMPLET | **16** (M01–M16) + A06 | Same 18-type set as FMS-04 | `FMS-06` in `seed_data.py`; modules from `seed_modules.py` | **7** (M01–M07) | `FMS-06-M01` |
| **Total** | — | **95 modules** | — | — | **53 modules** | — |

The 95-module canonical total matches the repo's own prior parse count
exactly (`FMS_IMPORT_VALIDATION_REPORT.md`: "module (contenu complet) |
95"), confirming this delta is read from the same corpus, not a fresh
guess. **The repo currently serves 56% of the canonical module count
(53/95), and every one of those 53 modules is different pedagogy from
its canonical counterpart** — not a subset, a parallel invention (§2).

## 2. Delta modules — titles, not just counts

The repo's legacy modules were written before any real FMS ZIP existed
(confirmed by `FMS_IMPORT_VALIDATION_REPORT.md` §1: *"la convention
documentée avant ce ZIP... ne correspondait à aucun des 223 fichiers
réels"*). Comparing titles directly, FMS-01 M01:

| | Title | Deliverable/evidence model |
|---|---|---|
| **Legacy** `FMS-01-M01` | "Identité artistique et culturelle" | `hook` (blind test), `deliverable` ("Carte identité artistique trilingue + photo"), `frek_signal: FREK-WORK` |
| **Canonical** `FMS01-M01` | "Introduction au métier d'Artist Development" | Bloc "Transversal", N1 QCM (10 questions), exercise ("classer 12 activités dans le bon métier FMS"), no individual deliverable — a contextualization module |

This is not a renamed version of the same module — canonical M01 is an
orientation module about the FMS métier boundaries; legacy M01 is a
portfolio-building exercise that canonical only reaches around M04–M05
("Clarifier un univers artistique", "Positionner un artiste sur le
marché"). **Every one of the 15 canonical FMS-01 titles**:

```
M01 Introduction au métier d'Artist Development
M02 Comprendre le diagnostic artistique
M03 Réaliser un diagnostic artistique encadré
M04 Clarifier un univers artistique
M05 Positionner un artiste sur le marché
M06 Construire le fond narratif
M07 Diagnostic artistique autonome
M08 Univers & Identité : arbitrage de directions concurrentes
M09 Positionnement stratégique différenciant
M10 Storytelling : fond narratif complet
M11 Roadmap & trajectoire de développement
M12 Dossier de présentation complet (pitch, bio, artist statement)
M13 Artist Development multi-projets
M14 Spécialisation Caraïbe & Diaspora
M15 Artist Development dans l'écosystème CVLN (Bridge)
```

follows a Découverte → Initiation → Professionnel → Avancé/optionnel →
Bridge progression built around **one continuous case** (Anaïs Solaine,
M03→M12), a structure the legacy content has no equivalent of. The same
holds for FMS-02 through FMS-06 (full canonical title lists captured
during this pass, available on request — omitted here for length; each
follows the identical Découverte→Initiation→Professionnel→Avancé/
Spécialisation→Bridge shape with its own continuing case, e.g. FMS-03's
"Rasin Nouvo", FMS-06's cross-métier arbitration of the same Anaïs Solaine
case now "arbitrée dans un portefeuille").

## 3. Delta ressources — resource types the repo has never ingested

Real type inventory already established by `FMS_IMPORT_VALIDATION_REPORT.md`
(26 real types across all 223 files). None of the following are
represented anywhere in `seed_data.py`/`seed_modules.py` today — they
exist **only** in the canonical archive and in `backend/fms_import/`'s
parser (which recognizes them but has never written them to a live DB —
§6):

| Resource type | Count (6 métiers) | Repo equivalent |
|---|---|---|
| `module` (contenu complet) | 95 | Partial — 53 legacy modules, different content |
| `blueprint` | 15 (FMS-01 only) | None |
| `master_learning_map` | 6 | None |
| `master_module_map` | 6 | None |
| `cas_fil_rouge` | 6 | None — no continuing-case model exists in the repo at all |
| `case_competency_matrix` | 6 | None |
| `matrice_tracabilite` | 6 | None |
| `evidence_registry` | 3 (FMS-01/02/03 only) | Partial — `backend/skills/models.py`'s `EvidenceType` is a generic enum (`quiz`/`deliverable`/`mini_mission`/`certification`), not the canonical per-métier evidence catalogue |
| `skill_ids_registry` | 3 (FMS-01/02/03 only) | Partial — `Skill.id` format already matches (`FMS01-A1`, per `skills/models.py` docstring), but no skill has actually been registered from this archive |
| `rubric_master` | 3 (FMS-01/02/03 only; FMS-04/05/06 reuse the same 0–4 scale inline in their grilles) | **EXISTS** — `backend/certification/models.py` was already reconciled against `28_FMS01_Rubric_Master.md`/`49_FMS01_A01_Grille_Certificative_V1.md` (0–4 scale, critères éliminatoires, plafonnement de mention) — the one canonical concept the repo's data model already fits without modification |
| `infrastructure` | 3 (FMS-04/05/06 only) | None |
| `grille_certificative` | 7 (1 brouillon + 6 finales) | None loaded; format matches `certification/models.py`'s rubric shape |
| `cas_inedit` / `sujet_officiel` / `guide_jury` | 6 each | None |
| `banque_n1` / `banque_n2` | 6 each | None — no QCM/exercise bank exists in the repo; `quizzes.py` has its own unrelated question set |
| `guide_formateur` / `guide_correcteur` / `guide_candidat` | 6 each | None |
| `templates_etudiants` | 6 | Partial — `backend/template_engine/` is a generic fillable-template engine (workstream #7), not seeded with these specific 42 templates (7 per métier × 6) |
| `gabarit` / `index` / `matrice_pedagogique` / `note_harmonisation` | 1 each | None — these are archive-governance documents, not learner-facing content; no repo equivalent expected |

**Structural asymmetry inside the canonical source itself**:
`Evidence_Registry`/`Skill_IDs_Registry`/`Rubric_Master` exist as
standalone files only for FMS-01/02/03; FMS-04/05/06 fold the same
information inline into their `Infrastructure.md` and grading grilles
instead (confirmed: `grep` finds real `FMS04-*`/`FMS05-*`/`FMS06-*` Skill
ID tokens throughout their module and grille files — the skill IDs exist,
just not centralized in a dedicated registry file). Any future importer
logic must not assume every métier has the same 21 file types; it must
tolerate this real variation, already partly true of
`backend/fms_import/module_map.py`'s two-layout tolerance for Module Maps.

## 4. Delta compétences (Skill IDs)

| Métier | Skill IDs (distinct, canonical) | Éliminatoires (canonical) | Repo Skill registry entries |
|---|---|---|---|
| FMS-01 | 19 (A1–F1) | 3 verrous (per `00_INDEX.md`) | 0 |
| FMS-02 | 16 | 3 (B2/C2/E1) | 0 |
| FMS-03 | 12 (4 Skill IDs covering 3 verrous — D1/E1 jointly one verrou, clarified during lock audit) | 3 verrous / 4 Skill IDs | 0 |
| FMS-04 | 12 | not individually confirmed this pass (grille exists, not read line-by-line) | 0 |
| FMS-05 | 12 | not individually confirmed this pass | 0 |
| FMS-06 | 12 | not individually confirmed this pass | 0 |
| **Total** | **83 distinct Skill IDs** | — | **0** |

`backend/skills/models.py`'s `Skill` model and ID format already fit this
data exactly (workstream #14 aligned it to `FMS01-A1` format) — this is a
schema-ready, zero-content gap, not a schema gap.

## 5. Conflits de codes

**No literal Mongo-key collision exists today**, because the two
conventions differ in exactly one character:

- Legacy (`seed_data.py`/`seed_modules.py`): `FMS-01-M01` (hyphen between
  `FMS` and the métier number).
- Canonical (`fms_import/module_map.py`'s own regex, and every
  `Master_Module_Map.md` `**ID**` field): `FMS01-M01` (no hyphen).

**This is a fragile non-collision, not a safe one.** Three real risks:

1. **Formation-level collision is exact today**: the legacy formation
   code `FMS-01` and every canonical document's own self-reference
   (`# FMS-01 — ARTIST DEVELOPMENT`) use the identical string `FMS-01`.
   If a future migration replaces `db.formations["FMS-01"].modules` with
   canonical content while a learner's `ModuleProgress` rows still carry
   `formation_code="FMS-01"` + the old `module_code="FMS-01-M01"`, those
   rows silently point at a formation whose module list no longer
   contains that code — an orphaned, invisible progress record, not a
   crash.
2. **A well-intentioned normalization would create a real collision.**
   Any future code that strips the extra hyphen (e.g. to "clean up" the
   two conventions) would map legacy `FMS-01-M01` and canonical
   `FMS01-M01` onto the same string — silently overwriting the key for a
   position whose actual pedagogical content is entirely different
   (§2). This is precisely the scenario `BIN-003`
   (`LEGACY_PROGRESS_MUST_NOT_BE_REASSIGNED_SILENTLY`) exists to forbid.
3. **Skill IDs are already canonical-format and collision-free** —
   `Skill.id` (`FMS01-A1`) was built to the real convention from the
   start (workstream #14) and has zero legacy content occupying the same
   keys (§4: 0 registered skills today). No migration risk there, only a
   population gap.

## 6. Contenu legacy sans équivalent canonique

Concepts the current Academy platform models that the canonical FMS
archive does not use at all:

- `hook`, `frek_signal` (`FREK-WORK`/`FREK-SCORE`/`FREK-LINK`/`FREK-CERT`/
  `FREK-CONTRIB`) — Academy-specific engagement/signal wrapper, zero
  occurrences in the canonical corpus.
- `stades` (`graine`/`pousse`/`racine`/`branches`/`arbre`/`foret`) at the
  module/formation level — the canonical corpus uses its own, different
  progression vocabulary (`Découverte → Initiation → Professionnel →
  Avancé/Spécialisation → Bridge`), not the Academy's botanical stage
  names. These are two genuinely different progression models, not a
  naming variant of the same one.
- `badge_name`, `cc` (credits), `economics` (pricing/funding
  placeholders), `contexts`/`audience_levels`/`bridge_entities`/
  `job_truth` (`catalog_cartography.py`'s market-positioning layer) — all
  Academy/business wrapper metadata around a formation, orthogonal to
  the canonical pedagogy itself. None of this needs to disappear; none
  of it is contradicted by canonical content — it simply describes a
  different layer (how Academy markets/prices/credits a formation, not
  what it teaches).
- "Bridge" as a *list of related CVLN entities* (`bridge_entities`,
  `job_truth.bridge`) — the canonical corpus also has a "Bridge" concept
  but models it as **one pedagogical module** per métier (M15 for
  FMS-01, M16 for FMS-02–06, "…dans l'écosystème CVLN"), not a metadata
  list. Same word, two different mechanisms — a real naming collision
  worth flagging so a future migration doesn't conflate them.

## 7. Contenu canonique sans équivalent legacy

The inverse direction — everything in §3 the repo has zero model for,
plus, at the conceptual level:

- **A continuing pedagogical case per métier** (Anaïs Solaine for
  FMS-01/02/03/06, "Rasin Nouvo" for FMS-03's production angle, distinct
  cases for FMS-04/05), explicitly cross-referenced across métiers
  ("diagnostiquée (01), positionnée économiquement (02), produite (03),
  mise en marque (04), pilotée au quotidien (05), et arbitrée dans un
  portefeuille (06)"). The repo's legacy modules are self-contained
  exercises with no case continuity — a real pedagogical mechanism with
  zero repo equivalent.
- **A locked doctrine per métier** (e.g. FMS-01's *"Observer → Distinguer
  → Formuler → Confronter → Arbitrer → Documenter"*, `01_FMS-A_...md`)
  governing every module's professional judgment calls, plus explicit
  "verrous doctrinaux" (doctrinal locks) that are eliminatory in
  certification. No equivalent structure exists in `seed_data.py`.
- **A five-question lock audit per métier**, performed and documented
  inside the archive itself, with real defects found and fixed (see
  "Data-quality notes" below) — a quality process the repo has no
  parallel for its own legacy content.
- **Frontier/boundary matrices between the 6 métiers** (referenced from
  `06_FMS-F_Referentiel_Executive_Cultural_Production.md`: "Master
  Competency Matrix complète (15 compétences × 6 métiers)" and "Matrice
  des frontières (5 zones verrouillées)") — not read in full this pass
  (out of scope for a delta at module level) but flagged as existing and
  unrepresented.

## 8. Risques de progression

- **Today, zero risk is live**: `db.fms_resources` has never been
  populated (`FMS_IMPORT_VALIDATION_REPORT.md` §6 — no MongoDB instance
  was available to run the write path; only the pure parse/validate
  pipeline was exercised). `db.formations`/`db.progress` are driven
  entirely by `seed_data.py`/`seed_modules.py` today, untouched by this
  pass.
- **The risk is entirely in the future migration step** (`ACA-0005`/
  `ACA-0006`, both correctly gated `NOT_AUTHORIZED`/design-only): any
  binding of canonical content into `db.formations` must not silently
  reinterpret an existing `ModuleProgress.module_code`. A learner who
  completed legacy `FMS-01-M01` ("Identité artistique et culturelle")
  has *not* completed canonical `FMS01-M01` ("Introduction au métier") —
  crediting one as the other would misrepresent real learner history in
  either direction, and would give a false certification prerequisite
  signal (only 12 legacy checkpoints exist against 15–16 canonical ones
  per métier).
- **Certification exposure**: `backend/certification/models.py`'s engine
  is already built to canonical criteria (Rubric Master 0–4, critères
  éliminatoires) but has zero real Skill IDs registered (§4) — an
  attempt graded today would be scored against invented criteria, not
  the real 19/16/12-per-métier canonical set. This is a content gap, not
  a runtime bug, but it means **certification is not yet trustworthy
  against the canonical standard**, independent of the module-migration
  question.

## 9. Options de migration avec impact

Three options, matching the shape `docs/FMS_CANONICAL_MIGRATION_WORKSTREAM.md`
(design-only, from an earlier wave) already sketched, refined here with
the concrete numbers from this diff:

| Option | Mechanism | Impact on existing `ModuleProgress` | Impact on module codes | Reversibility |
|---|---|---|---|---|
| **A — Versioning** | Canonical content imported as a new version of each formation (`FMS-01` v2), legacy stays addressable as v1 | Zero rows touched; a learner's legacy progress remains valid against the legacy version | New codes needed to distinguish versions (e.g. keep `FMS01-M01` canonical vs `FMS-01-M01` legacy, formalize the distinction as the version boundary) | High — nothing is deleted or reassigned |
| **B — Legacy namespace** | Canonical content becomes the live `FMS-01`…`FMS-06`; legacy content is renamed into an explicit non-colliding namespace (e.g. `FMS-01-LEGACY-M01`) before the swap | Existing rows re-pointed to the renamed legacy codes — a data migration script, not a silent reassignment | Legacy codes change once, deliberately, with a migration record | Medium — legacy content preserved, but a real one-time data write is required |
| **C — Mapping table** | A `LegacyModuleMapping` collection records `{legacy_code, canonical_code, relationship}` (`SUPERSEDES` / `PARTIAL_OVERLAP` / `NO_EQUIVALENT`) without renaming or moving anything | Zero rows touched; the mapping is read-only reference data queried at display time | No codes change | Highest — purely additive, easiest to undo |

None of these has been chosen — `DEC-003` (FMS migration strategy) is
explicitly `PENDING`, and `ACA-0005`'s gate is `FOUNDER_DECISION`. Given
this diff's finding that legacy and canonical content are pedagogically
unrelated (not approximate versions of each other), **Option C most
directly avoids ever implying legacy progress "was" canonical progress**,
at the cost of the repo carrying both bodies of content side by side
until a further decision retires the legacy one — a trade-off for the
Founder to weigh, not a recommendation this pass is authorized to act on.

## 10. Data-quality notes (from the canonical source itself, not this audit)

Reported here because §"Method" requires citing what was actually read,
not because they are this session's findings — the archive's own
lock-audit process found and fixed these before declaring each métier
locked:

- FMS-01: an arithmetic inconsistency in the Bloc 1 total duration
  (Module Map vs Guide Formateur) — corrected in-archive.
- FMS-02: one Skill ID formatting defect in M13 — corrected.
- FMS-04/05/06: M13's grading grille named only 6 of 12 Skill IDs
  (matching a defect already found once in FMS-02) — corrected to name
  all 12.
- FMS-03: the Skill IDs Registry stated "3 critères éliminatoires" while
  listing 4 Skill IDs — clarified as 3 verrous carried by 4 Skill IDs.
- Documented, not-fabricated open gaps remain (per `00_INDEX.md`'s own
  "Écarts connus"): no specialized second `cas inédit` per métier for
  diaspora-track candidates; single N2 exercise variant for M03–M07
  across all métiers; N1 question bank sized to what was actually
  written, not a fixed target (FMS-01: 96 questions; FMS-03: 32; FMS-04:
  26; FMS-05: 25; FMS-06: 25 — **FMS-02's own index carries an internal
  inconsistency, stating both "43 questions réelles" at its file listing
  and "68" in the later global tally; not resolved by this pass, flagged
  for the Founder/pedagogy team since it is a canonical-source
  discrepancy, not a repo error**).
- Minor archive numbering quirks, inert: file `58` doesn't exist because
  `00_GABARIT_Construction_Metier.md` (extracted generic template) was
  numbered `00` instead of sequentially; files `181`/`182` are absent
  between FMS-05's M16 and its A05 kit with no explanation in the index
  — all FMS-05 content (16 modules + full A05 kit) is otherwise present,
  so this reads as a skipped numbering step, not missing content, but is
  reported rather than silently assumed.

---

## Aucune mutation

Confirmed: this pass extracted the archive to a scratch directory only
(`/tmp/.../scratchpad/fms_canonical/`, outside the repository), read
repository files, and wrote this one new document. `git status` shows
no other change. `db.formations`, `db.progress`, module codes, and the
production FMS corpus are exactly as they were before this pass.

**G1 = PASSED_FOR_ANALYSIS_ONLY. G2 = NOT_AUTHORIZED. G3 = NOT_AUTHORIZED.**

`STOP = TRUE`.
