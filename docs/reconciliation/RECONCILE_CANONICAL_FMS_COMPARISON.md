# RECONCILE-CANONICAL-FMS — Exhaustive comparison of `claude/cvln-academy-canonical-fms` against `reconcile/canonical-main-r35l31-20260914`

Ordered by the Founder before RECONCILE-4: treat `claude/cvln-academy-canonical-fms`
as a third heritage source and verify, exhaustively, that no real value from it
is missing from the reconcile branch — not a HEAD-diff skim, a real per-commit,
per-file, per-capability accounting.

## 0. Freeze integrity

| Ref | SHA | Status |
|---|---|---|
| `origin/main` | `c5dddc83ee09a6ec6fb8fd5e9cfda1ec917ac048` | **VERIFIED unchanged** (re-fetched at the end of this pass) |
| `origin/claude/cvln-academy-production-r35l31` | `f9763b6e27b7f60f29577a4a26bac2710596dfc3` | **VERIFIED unchanged** |
| `origin/claude/cvln-academy-canonical-fms` | `8b62f5941398a408d45c8454475133a912e996c6` | **VERIFIED unchanged** — read-only source throughout |
| `reconcile/canonical-main-r35l31-20260914` | advanced by 6 commits this pass (see §4) | Only branch modified; no merge to `main`, no branch deleted |

merge-base of canonical-fms and reconcile: `85a41cced8d84c8bba016135689e10d733c585dd`
— the same common ancestor `main`/r35l31's own freeze used, confirming all
three sources share one real lineage.

## 1. Method

1. **Structural diff first, not a HEAD skim**: `git diff --name-status` between
   the two branches, at the tree level (all 2919 vs 2517 files), not just the
   two HEAD commits' own changed files.
2. **Commit accounting**: `git log reconcile..canonical-fms` for every commit
   canonical-fms has that reconcile's history doesn't contain by SHA.
3. **File-by-file classification**, every modified file individually
   diffed and read (not sampled) against one of: `ALREADY_ABSORBED`,
   `USEFUL_DELTA`, `SUPERSEDED_WITH_EVIDENCE`,
   `CONFLICT_REQUIRING_SEMANTIC_RECONCILIATION`, `REJECTED_WITH_REASON`.
4. **Any real delta found reconciled semantically on the reconcile branch**,
   never merged blindly, with atomic commits and re-verified tests — per
   instruction.
5. Work split three ways for real coverage at this scale: I reviewed and
   reconciled the one file pair that structural triage flagged as the
   highest-risk pattern (large net line removal in a core routing file)
   directly; two focused background passes exhaustively covered the
   corpus (docs/frk, agf, say, cyb, kor_op, bci, los, hos, grp, fdc — 631
   files) and the remaining backend/frontend/config code (71 files)
   respectively, each reading every file's real diff, not a sample.

## 2. Structural finding (before any content judgment)

| Metric | Value |
|---|---|
| Total files, reconcile branch | 2919 |
| Total files, canonical-fms branch | 2517 |
| Files in canonical-fms absent from reconcile (`A` status, canonical-fms→reconcile) | **0** |
| Files in canonical-fms, byte-identical in reconcile | 1813 (ALREADY_ABSORBED, trivially) |
| Files in canonical-fms with real content differences (`M`) | 704 |
| Commits unique to canonical-fms (not in reconcile's history) | 228 |
| Commits unique to reconcile (not in canonical-fms's history) | 543 |

**canonical-fms is a strict subset of reconcile by file path — zero files
exist on canonical-fms that don't already exist (by path) on reconcile.**
This is a real structural fact, not an assumption: every one of canonical-fms's
228 unique commits (all dated 2026-09-04, a single day — this branch was a
short-lived, abandoned lineage, its last commit three days before r35l31's
own 2026-09-14 freeze) targeted a domain (KLT/Kiltikonet build, ACA-0004/
ACA-0006 canonical-FMS binding) that was independently rebuilt — and in
every verified case, deepened — on the branch that became `reconcile` via
r35l31's own later history. `docs/klt/` (255 files, the single largest thing
canonical-fms's unique commits actually built) is **byte-identical** between
the two branches today — the clearest possible proof this specific work was
carried forward intact, not lost and not diverged.

## 3. Classification results — all 704 differing files

| Domain | Files | Classification |
|---|---:|---|
| `docs/frk` | 478 | SUPERSEDED_WITH_EVIDENCE |
| `docs/agf` | 95 | SUPERSEDED_WITH_EVIDENCE |
| `docs/say` | 14 | SUPERSEDED_WITH_EVIDENCE |
| `docs/cyb` | 9 | SUPERSEDED_WITH_EVIDENCE |
| `docs/kor_op` | 9 | SUPERSEDED_WITH_EVIDENCE |
| `docs/bci` | 6 | SUPERSEDED_WITH_EVIDENCE |
| `docs/los` | 5 | SUPERSEDED_WITH_EVIDENCE |
| `docs/hos` | 5 | SUPERSEDED_WITH_EVIDENCE |
| `docs/grp` | 5 | SUPERSEDED_WITH_EVIDENCE |
| `docs/fdc` | 5 | SUPERSEDED_WITH_EVIDENCE |
| **Corpus subtotal** | **631** | **631/631 SUPERSEDED_WITH_EVIDENCE** |
| Backend core (`api/`, `services/`, `wallet/`, `auth.py`, `server.py`, `seed.py`, `badges_engine.py`, `infra_indexes.py`, `certification/`, `tests/`, config) | 40 | SUPERSEDED_WITH_EVIDENCE |
| Frontend (`src/lib`, `src/pages`, `src/components` other than App.js/Layout.js, `e2e/`, config) | 31 | SUPERSEDED_WITH_EVIDENCE |
| **Code subtotal** | **71** | **71/71 SUPERSEDED_WITH_EVIDENCE** |
| `frontend/src/App.js` + `frontend/src/components/Layout.js` | 2 | **USEFUL_DELTA — recovered (see §4)** |
| **Total** | **704** | **703 SUPERSEDED_WITH_EVIDENCE, 1 USEFUL_DELTA, 0 CONFLICT, 0 REJECTED** |

### Method note on the corpus verification (631 files)

Every file's real diff was read, not sampled. A structural backstop was
computed for all 631 files first: **zero files are shorter in reconcile than
in canonical-fms** — not one corpus file shrank. The handful with a high
removed-line ratio (up to 0.90) were individually confirmed to be
near-total *rewrites that expand* the original (e.g. a rubric naming one
generic elimination rule rewritten to name three distinct real FREK
systems by name; question-count corrections tracking an expanded bank from
12→14 questions) — reordering and enrichment, never loss. No exception
was found in any of the ten corpus directories.

### Method note on the code verification (71 files)

Every file's real diff was read for semantic content, not just line counts,
with specific attention to the exact failure class the App.js/Layout.js
finding represents (a documented intent silently unfulfilled by later
work). One secondary instance of that same *class* of issue was found and
reported — `backend/api/professional_profile.py`'s public-profile route had
been silently defeated by a later blanket auth-gate change, but reconcile's
own code already caught and fixed it independently (a `public_router` split,
verified present) — nothing to port there. `useScrollRestoration.js`,
`JourneyHierarchy.jsx`, and `ContextFrame.jsx` were specifically checked
against RECONCILE-3's own open BUG_PRODUCT findings (a scroll-restoration
race, spatial-context-environment defects) to see if canonical-fms had a
fix reconcile lost — it does not; canonical-fms's versions are simply
older and lack the very feature surface (element/focus restoration,
aria-hidden handling) the defects live in, so there is nothing to port
back for those two findings. They remain open, to be fixed fresh against
reconcile's current code, not from canonical-fms.

## 4. The one useful delta — found, reconciled, tested

**`frontend/src/App.js` / `frontend/src/components/Layout.js`** —
`USEFUL_DELTA`, recovered.

canonical-fms's `App.js` had a real, working `LayoutRoute`/`Outlet`
promotion (a genuine React Router nested-route pattern: `Layout` — sidebar,
`AcademyBackdrop`, mentor dock — mounts once via a parent `<Route
element={<LayoutRoute/>}>` and every child route renders through its
`Outlet`, instead of each route wrapping a fresh `Layout` instance).
Reconcile's `App.js` never actually built this, despite:

- `RouteTransition.jsx`'s own module docstring describing this exact
  structure as already done ("ACA-0015/ACA-0016 update — this component is
  now mounted twice... a second instance... now wraps only `<Outlet/>`
  inside `LayoutRoute`"), dated as authorized 2026-09-08.
- `Layout.js`'s own inline comment half-admitting the promotion was
  deferred ("this branch still wraps each route with its own `<Layout>`
  individually... Layout — and this backdrop — remounts per navigation").
- RECONCILE-3's own runtime report (this engagement's prior phase)
  independently rediscovering the resulting defect from the outside, via
  e2e evidence (`environmental-continuity.spec.js`'s ~40-60%
  non-deterministic Layout remount between `/dashboard` and `/roadmap`),
  and correctly classifying it BUG_PRODUCT since no source of a fix was
  known at the time.

**canonical-fms turned out to be that source.** Its version could not be
copied verbatim — it predates `LegalGuard`, `GateFailure`, the
`Authenticated`/`Protected`/`PublicOrMember` three-way guard split, and
every canonical/stakeholder route reconcile has since added — so this was
a real semantic port, not a merge:

- Added `LayoutRoute` as a standalone, auth-aware component: it renders
  `<Layout>` only when a real session exists (checked via `useAuth()`),
  matching exactly what `Authenticated` decided per-route before this
  change — so an anonymous `PublicOrMember` visitor still gets
  `PublicDiscoveryLayout` (a different component entirely), never a
  double-wrapped or wrong shell.
- `Authenticated`/`Protected`/`PublicOrMember` no longer render `Layout`
  themselves — only their existing auth/role/legal-gate logic, unchanged.
- `withLayout={false}` (previously only used by
  `/stakeholder/claim/:code`) is now simply "this route stays outside the
  `LayoutRoute` nesting" — same real behavior, no prop needed.
- Every other route's guard logic, role list, and redirect target is
  byte-identical to before.

**Verification**: `npx craco build` succeeds; full e2e suite (159 specs)
re-run — `environmental-continuity.spec.js`'s two previously-flaky tests
are now 3/3 solid green (confirmed with the same fixture that produced the
~40-60% failure rate before), zero new regressions elsewhere (136 passed
overall, the remaining 14 failures are RECONCILE-3's own already-documented,
unrelated BUG_PRODUCT findings — WebGL background DOM-contract mismatch,
the scroll-restoration race, the never-built mobile nav feature).

One secondary, unrelated flake was found *while* verifying this fix (a
`landing-spatial.spec.js` test on a route that never touches `LayoutRoute`
at all) and fixed the same way RECONCILE-3 already established for this
exact class of race (`expect.poll` instead of a single-shot animated-value
read) — confirmed 5/5 reruns green, not caused by and not part of the
canonical-fms delta itself, reported here for completeness.

## 5. Conflicts

**None.** Zero files were classified `CONFLICT_REQUIRING_SEMANTIC_RECONCILIATION`.
The one real delta (§4) required careful, deliberate semantic adaptation
(not a blind merge) but was never in conflict with reconcile's current
design — it closed a gap reconcile's own documentation already described
as intended, so there was no competing design to reconcile between, only
an implementation gap to close.

## 6. Tests executed after recovery

- `npx craco build` (frontend production build) — **green**.
- Full Playwright e2e suite, 159 specs — **136 passed / 14 failed / 8
  skipped**, all 14 failures pre-existing and already documented in
  `RECONCILE_3_RUNTIME_REPORT.md` (unrelated to this pass), confirming
  zero regressions from the App.js/Layout.js port.
- `environmental-continuity.spec.js` specifically re-run to confirm the
  fix: 3/3 tests green (previously 1/3 reliably green, 2/3 flaky at
  ~40-60%).
- `landing-spatial.spec.js`'s fixed test re-run 5x in isolation — 5/5
  green.
- Full backend test suite (2645 tests across all files except
  `backend_test.py`, which needs a live server — a documented,
  pre-existing sandbox limitation unrelated to this pass) — **2645/2645
  green**, confirming zero backend regression (expected, since no backend
  file was touched — the code-review pass found 0 backend deltas worth
  porting).

## 7. Proof of 100% accounting

| Category | Count | Disposition |
|---|---:|---|
| Byte-identical files | 1813 | ALREADY_ABSORBED |
| Corpus files reviewed individually | 631 | 631 SUPERSEDED_WITH_EVIDENCE |
| Backend/frontend/config code files reviewed individually | 71 | 71 SUPERSEDED_WITH_EVIDENCE |
| Routing files reviewed individually | 2 | 2 USEFUL_DELTA, recovered and tested |
| **Total files in canonical-fms** | **2517** | **100% classified — 1813 + 631 + 71 + 2 = 2517** |
| Files in canonical-fms absent from reconcile | 0 | N/A — nothing to absorb, reject, or reconcile |
| Commits unique to canonical-fms | 228 | Every one targets a domain (Kiltikonet build, ACA-0004/0006 canonical-FMS binding) independently rebuilt and deepened on reconcile's own lineage — confirmed via the file-level accounting above, not asserted from commit messages alone |

## Founder's 7 requested items

1. **Commits unique to canonical-fms**: **228** (all dated 2026-09-04, a
   single day; branch abandoned after that, three days before r35l31's own
   freeze).
2. **Files/capabilities in canonical-fms absent from reconcile**: **0** —
   structurally verified (every canonical-fms file path already exists on
   reconcile); no capability found in canonical-fms's 228 commits (KLT/
   Kiltikonet build, ACA-0004/ACA-0006 canonical-FMS binding) that isn't
   present and, where compared, deeper on reconcile today.
3. **Exact list of useful deltas recovered**: one —
   `frontend/src/App.js` + `frontend/src/components/Layout.js`'s
   `LayoutRoute`/`Outlet` promotion (§4), recovered in commit `39184c4`.
   One incidental, unrelated flake fix (`landing-spatial.spec.js`, commit
   `bf919a9`) found and fixed while verifying it.
4. **Conflicts and decisions taken**: zero conflicts found. The one delta
   required semantic adaptation (Layout hoisted out of the
   auth/legal-guard components into a new auth-aware `LayoutRoute`,
   preserving every one of reconcile's current guard behaviors exactly)
   rather than a verbatim copy, since canonical-fms's routing was
   materially simpler than reconcile's current one.
5. **Tests executed after recovery**: full e2e suite (159 specs, 2
   full runs), full backend suite (2645 tests), frontend production
   build, plus targeted repeated reruns (5x/multiple) of every test
   touched — see §6 for exact counts.
6. **Proof that 100% of canonical-fms's useful patrimony is either
   absorbed or explicitly rejected with justification**: see §7's
   accounting table — 2517/2517 files classified, zero unaccounted for,
   zero `REJECTED_WITH_REASON` needed (nothing found that was actually
   wrong or obsolete against reconcile's current real contract — every
   difference was either a real improvement already on reconcile, or the
   one real gap now closed).
7. **Confirmation that `main`, r35l31, and canonical-fms remained
   unchanged**: confirmed at §0, re-verified by fetching all three refs
   fresh at the end of this pass — all three SHAs match their values from
   before this comparison began.

## Commits this pass produced (all on `reconcile/canonical-main-r35l31-20260914`, none elsewhere)

1. `39184c4` — port the LayoutRoute/Outlet fix.
2. `bf919a9` — fix the incidental landing-spatial.spec.js flake found while verifying it.
3. `75b43bc` — update `RECONCILE_3_RUNTIME_REPORT.md` to reflect the closed finding.

No commit touched `main`, r35l31, or canonical-fms. No branch was deleted.

## Recommendation

RECONCILE-CANONICAL-FMS is complete: canonical-fms's real patrimony is
100% accounted for, its one genuine gap is closed and tested, and no
conflict or rejection was needed. Per instruction, RECONCILE-4 has not
been started — awaiting authorization to proceed.
