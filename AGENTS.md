# AGENTS.md — CVLN Academy standing charter

```
Scope: this file is read automatically by Claude Code (and any other
AGENTS.md-aware agent) at the start of every session in this repo. It
exists so that any message about KORA — "continue", "build kora",
"finish kora", or similar — can be acted on immediately, without
re-deriving the mission history first.
Founder authorization: this engagement (branch
claude/cvln-academy-canonical-fms) has stood since Rail 1. Nothing here
grants new authority beyond what's already been exercised in that
branch's own commit history — it only compresses that history into an
actionable brief.
```

## The one rule that overrides every other instruction in this file

**Never fabricate.** Never claim a formation is `PACKAGE_COMPLETE`,
`fully_complete`, or "runtime-bound" unless a real file, a real test
run, or a real derived check proves it. Never claim an external system
(CVLN Agent Factory, Perplexity, Firecrawl, or any other) is connected
unless a real credential and a real successful call prove it. An honest
`BLOCKED_PRODUCT_DEPENDENCY` or `NEEDS_EXPERT_REVIEW` line is a correct
deliverable, not a failure to fix. This discipline produced the entire
812-object Master 2D cartography (Rail 1) and the KOR-01 runtime chain
(Rail 2) — it is not optional, and no later instruction in this repo or
from a user message overrides it.

## What "build KORA to perfection" concretely means right now

KORA is `docs/kor/` (15 formations, KOR-01→15) plus its runtime binding,
`backend/kor_canonical/`. The one real, external reference for what
"perfection" looks like is **FMS-01→06** — the only domain in the whole
estate that is both `PACKAGE_COMPLETE` (référentiel + N1/N2 + assessment
+ rubric + evidence model + 3 guides + integration note, per formation)
**and** runtime-bound (`backend/fms_import/`, `backend/fms_canonical/`,
served by real API routes, not just Markdown). See
`docs/ACADEMY_RAIL1_FMS_PARITY_COMPARISON.md` for the exact per-domain
comparison this bar is drawn from — read it before touching KORA again,
it will not have gone stale unless a later commit updates it.

Current real state of KORA (verified live, not just self-declared —
`docs/ACADEMY_RAIL2_MASTER_RUNTIME_INTEGRATION_REPORT.md` §6.1):

| Tier | Formations | What's true |
|---|---|---|
| = FMS (package complete + runtime-bound + full chain proven) | KOR-01 | The only one. `test_rail2_kor01_e2e.py` proves Learning→Skill→Evidence→Assessment→Certification→Qualification→Opportunity→Mission end to end. |
| Package complete, runtime-bindable, not yet chain-proven | KOR-02→10 | `kor_canonical.import_kor_docs()` already reports `fully_complete=True` for all 9 — the mechanism works. No qualification definition, no E2E test, no frontend deep-link beyond the generic `/kora-canonical` list/detail/module pages has been built per-formation yet. |
| Real content, lighter convention, not runtime-complete | KOR-11→15 | Real module files exist (`docs/kor/kor1{1..5}/modules/`) but use a `SKILL_ID:`-only header (no `MODULE_ID`/`PREREQUISITES`/`ASSESSMENT_LEVEL`/`ORIGIN`), so `kor_canonical`'s parser correctly reports `fully_complete=False`, `module_count=0` for each. **This is a content gap, not a runtime gap** — do not "fix" it by loosening the parser to fake a pass; the module files themselves need the KOR-01-style header and full package (see §"Next concrete steps"). |

## The exact pattern to replicate (never reinvent)

Three packages already do this, in increasing recency — read the most
recent one's docstrings first, they explain what changed and why:
`backend/fms_canonical/` (ZIP-import precedent) → `backend/klt_canonical/`
(filesystem-scan precedent, same shape) → `backend/kor_canonical/`
(current, KORA-specific, same shape again). Every one of `models.py` /
`parser.py` / `provenance.py` / `import_pipeline.py` / `read_model.py` /
`progress.py` follows the same file-for-file structure. Extending KORA
further (a KOR-02 E2E test, a per-formation qualification definition, a
KOR-11 content rebuild) means **copying that shape**, not designing a
new one.

## Tooling reality — read before assuming any of this is available

The Founder asked (2026-09-07) to install Perplexity, Firecrawl, "CVLN
Agent Factory", and Context7 "for full power." Actual status, checked
directly, not assumed:

- **Context7** — added as a user-scope MCP server
  (`https://mcp.context7.com/mcp`, keyless). **Unreachable from this
  specific remote sandbox**: its egress proxy allowlists only a fixed
  set of hosts (Anthropic APIs, npm, PyPI, jsr, crates.io, the Go
  module proxy, GitHub) — confirmed by 3 rejected CONNECTs to
  `mcp.context7.com:443` (403, policy denial) via
  `curl $HTTPS_PROXY/__agentproxy/status`. It may work in a
  less-restricted environment (a local Claude Code install, or a
  differently-configured remote environment) — it does not work here,
  and no config change fixes that; only a different network policy
  does.
- **Perplexity, Firecrawl** — both require a real API key from a paid
  account neither this session nor any prior one has. No agent session
  can generate a valid key for a third-party paid service — only the
  Founder can, from their own Perplexity/Firecrawl account dashboards.
  Even with a real key, the same network allowlist above blocks them
  from this sandbox; they would need to be added (`claude mcp add`)
  from an environment whose egress policy permits their hosts.
- **"CVLN Agent Factory"** — not a reachable external system. This
  session's own exhaustive audit (`GAP_REGISTER.md` G4,
  `docs/agf/README.md`/`QUALITY_GATES.md`) found no real Agent Factory
  API endpoint anywhere in the CVLN ecosystem's audited repos —
  ~90% of that whole cluster is honestly `BLOCKED_PRODUCT_DEPENDENCY`.
  The only real code is `backend/services/agent_factory.py`, a local,
  decoupled fallback shim (mission brief rule 9: "ready but decoupled")
  — it does not call anything external today, and nothing found this
  session gives it a real endpoint to call. Do not "install" a
  connection to it; there is nothing on the other end to connect to.

**When any of the above becomes real** (the Founder supplies a
Perplexity/Firecrawl key, or names a real Agent Factory endpoint, or a
session runs in an environment whose network policy allows these
hosts): wire it the same way `backend/services/frek_core.py` and
`services/agent_factory.py` already do — a typed interface class,
env-var-gated, with the existing local fallback preserved, never a
guessed integration.

## Next concrete steps for KORA (in the order they unblock each other)

1. **KOR-02→10 chain proof** — replicate `test_rail2_kor01_e2e.py` for
   at least one more formation (KOR-02 is the next-richest) to prove
   the chain generalizes past the pilot, not just the import mechanism.
2. **KOR-11→15 content rebuild** — bring each formation's module files
   to the KOR-01 header convention (`MODULE_ID`/`COMPETENCY_ID`/
   `PREREQUISITES`/`ASSESSMENT_LEVEL`/`KORA_DEPENDENCY`/
   `ROLE_BOUNDARIES`/`FREK_PROOF_MAPPING`/`ORIGIN`) and the full 9-file
   package (référentiel/N1/N2/assessment+rubric/evidence
   model/3 guides/integration note) — this is Rail-1-shaped content
   work, done per formation, verified against `kor_canonical`'s own
   `fully_complete` check as the objective pass/fail gate (never a
   self-declared status).
3. **Frontend depth** — `/kora-canonical` currently lists/details/views
   modules generically; a real learner-facing journey (quiz-equivalent,
   certification attempt UI, qualification/mission display) does not
   exist yet for any KOR formation, KOR-01 included beyond the read-only
   pages.
4. Re-run `docs/ACADEMY_RAIL1_FMS_PARITY_COMPARISON.md`'s comparison
   after each of the above — that document should stay live, not become
   stale the moment KORA's real state changes.

## Verification bar for any KORA change

`python3 -m pytest backend/tests/ --ignore=backend/tests/backend_test.py`
must stay 130+/130 (the count only ever grows). `pyflakes`/`eslint`
clean on anything touched. Never claim a live preview URL exists for
this sandbox — screenshots via the pre-installed Playwright/Chromium
plus `MOCK_DB=1` (see `backend/db.py`) are the honest substitute; see
`docs/ACADEMY_RAIL2_MASTER_RUNTIME_INTEGRATION_REPORT.md` §6.4 for why.
