# W3-D — Spatial Progression — REPORT

```
GRAINE -> POUSSE -> RACINE -> BRANCHES -> ARBRE -> FORÊT: already the
  existing progression system (STAGE_CODES in Roadmap.js, `stade` on
  the user, STADE_EMOJI throughout) — this tranche did not invent it.
Exposed: XP = NO, levels = REMOVED (found live, fixed), quests = NO,
  player = NO, skill tree = NO.
```

## What was actually found and fixed

A grep sweep for `xp|level|quest|player|skill.?tree` across
`src/pages`/`src/components`/`src/lib` turned up one real, live
violation: `Roadmap.js` rendered `{t("roadmap_p.level_word")} {s.level}`
— literally **"Level 1", "Level 2", … "Level 6"** — on every stage card,
in **all four shipped languages** (`level_word` translated to "Niveau"
/ "Level" / "Nivo" / "Nivel"). This predates W3 entirely; W3-D is the
first tranche whose scope covers progression display, so it's fixed
here rather than left standing.

Nothing else matched: `Dashboard.js`'s stage section, `FrekProfile.js`,
`Missions.js`, and `FormationDetail.js` were already clean (stage name +
emoji + percentage-toward-next-stage, no numeric level/XP language).

## REQ_ID table

| REQ_ID | BEFORE | CHANGE | FILES | RUNTIME_PROOF | TEST | PERF | A11Y | REGRESSION | STATUS |
|---|---|---|---|---|---|---|---|---|---|
| SL-PROGRESS-01 (remove exposed "Level N") | `{t("roadmap_p.level_word")} {s.level} · {s.cc}+ CC` rendered "Level 1 · 0+ CC" etc., in fr/en/ht/es | Line removed; `level_word` key deleted from all 4 language blocks (only consumer was this one line, grep-confirmed); the card now reads just `{s.cc}+ CC` | `frontend/src/pages/Roadmap.js`, `frontend/src/lib/i18n.jsx` | Rendered body text on `/roadmap` contains no match for `/\blevel\b/i`, `/\bniveau\b/i`, or `/\bnivel\b/i` (the 3 translated forms actually shipped) | `roadmap-progression.spec.js` "no gamification language … is exposed" | — | No change to any label a screen reader announces beyond the removed word itself | None — `level`/`level_word` had exactly one consumer each (grep-confirmed before deleting) | VERIFIED |
| SL-PROGRESS-02 (felt, not counted) | Current stage marked only by a static `border-2 border-[--cvln-orange]` class, no depth/motion at all | Every stage card wrapped in `FocusFieldItem` (W2-C, reused as-is — no new primitive built), `focusedId` = the user's real `stade` (domain data, not a click) — current stage becomes TARGET (APPROACH), every other stage SECONDARY (RECEDE) | `Roadmap.js` | Current stage card → `data-focus-role="target"`; every other stage → `"secondary"`, confirmed for a stage other than the very first (so it's the real current-stage value driving it, not an accidental default) | `roadmap-progression.spec.js` "current stage … is spatially foregrounded, others recede" | Negligible — opacity/transform on 6 cards | No change — existing `active`/`done` classes and `data-testid`s untouched, `FocusFieldItem` is purely additive | None | VERIFIED |
| SL-PROGRESS-03 (reduced motion) | — | `FocusFieldItem` already consults `useReducedMotion()` (W2-C) | — | Foregrounded stage still applies a non-`none` transform under emulated reduced motion | `roadmap-progression.spec.js` "REDUCED_MOTION" | — | — | None | VERIFIED |
| SL-PROGRESS-04 (CC credits preserved) | `s.cc}+ CC` shown alongside the removed "Level" text | Unchanged — CC (crédits compétences) is a real academic credit unit already used identically elsewhere (`FormationDetail.js`'s `{f.cc} CC`, `Dashboard.js`'s CC balance), not gamification currency, so it stays | `Roadmap.js` | `stage-racine` still shows "50+ CC" | `roadmap-progression.spec.js` "CC thresholds are still shown" | — | — | None | VERIFIED |

## Test run (this tranche)

- `npx eslint src e2e playwright.config.js` → clean.
- `CI=true npx craco test --watchAll=false` → 28/28 Jest unit tests unaffected (no new pure logic this tranche — reused W2-C's already-tested `deriveFocusRole`).
- `CI=true yarn build` → compiled successfully. `main.js` gzip: 168.59 kB → 168.56 kB (−27 B, the trimmed i18n strings; `Roadmap.js` itself is a separate lazy chunk).
- `npx playwright test` → **69/69 passing** (65 pre-existing specs re-run unmodified + 4 new in `roadmap-progression.spec.js`).
- Backend regression (unchanged): `black --check`, `flake8` clean; `pytest tests/ -n 0 --ignore=tests/backend_test.py` → 40/40 passing.

## Regression check

`git status --porcelain` before commit showed exactly 3 files:
`Roadmap.js`, `i18n.jsx` (both modified), and 1 new file
(`roadmap-progression.spec.js`). No backend file, no
`db.formations`/`db.progress`/module-code/FMS-corpus file touched.
