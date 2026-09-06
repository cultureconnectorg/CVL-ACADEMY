# CVLN Academy Master — Repo Registry (canonical, cross-session)

```
Mandatory precondition for every INTERNAL/OPERATOR/BRIDGE/
CROSS_ECOSYSTEM W6 wave (Founder directive, 2026-09-06): repo-discovery
is exhaustive BEFORE concluding NO_REPO/PRODUCT_DEPENDENCY/BLOCKED/
NOT_IMPLEMENTED or escalating a Founder decision. Absence in
CVL-ACADEMY != absence in the CVLN ecosystem. This registry is the
running record of what has actually been checked, where, and what was
found — updated every time a repo is audited, never rewritten from
scratch.
```

## Registry

| Domain | Product | Repository | Branch/Commit audited | Last audited commit | Capabilities found | Maturity | Academy dependencies |
|---|---|---|---|---|---|---|---|
| Academy (self) | CVLN Academy OS | `cultureconnectorg/CVL-ACADEMY` | `claude/cvln-academy-canonical-fms` | (working branch, continuous) | Full FastAPI+Motor backend, React frontend, JWT auth, 30 seeded formations, quiz/badge/mission engine, `frek_core.py` (stub proof), `wallet/` (real additive ledger), `services/integrations/registry.py` (generic stubs), `docs/kor/` (KOR-01→15 complete), `docs/klt/` (KLT-01→08), `docs/gmd/` (W6 Wave 1) | `PRODUCTION_MVP` (Academy itself) | — (source of truth for Academy's own runtime) |
| FREK | FREKCORE v3 | `cultureconnectorg/frekcoreAout2026` | default branch tip `30d6a3b` + commit `fb272f1d491b09a6d068fb3f6c9c75d407bb0626` (fetched directly, not on default branch) | `fb272f1d491b09a6d068fb3f6c9c75d407bb0626` | `frek_v3/`: full architecture corpus (Attestation Protocol v0.1, Cryptographic Architecture Review v0.1, DSP Fingerprint Spec v0.1 — explicitly unfinished per its own `CE_QUI_MANQUE.md`), real Python reference verifier (`reference_verifier/`, 16 passing tests, golden vectors, real ECDSA P-256 crypto) | `ARCHITECTURE_LEVEL_2` — explicitly `NOT_FULL_ENGINEERING`/`NOT_HARDWARE_PROVEN`/`NOT_PRODUCTION_INTEGRATED` per the corpus's own maturity ladder (FPGA named as the un-crossed bridge to Level 3) | FRK-71→75 (`FREK_01_75_RECONCILIATION.md`) |
| FMS | Factory Maker Studio | `fms-os/fms` | default branch (shallow clone) | (recorded in `FMS_07_18_RECONCILIATION.md`) | Its own real `/os/command-center` route (unrelated to CVLN's "Command Center" — `CROSS_DOMAIN_CONTAMINATION` guard already in place), grounds FMS-07/15/18 | Partial, product-specific — see `FMS_07_18_RECONCILIATION.md` | FMS-07→18 |
| KORA | Kora-app / CVE | `kora2024/Kora-app` | default branch (shallow clone) | (cloned this session, `memory/KORA_CVE_Specification_Mathematique_v1.0.md` verified present) | Real, rigorous CVE Mathematical Specification v1.0 (frozen on Theory v1.4) — Layer 1 measurement model, saturation/normalization transforms. **Only the `memory/` doc was inspected this pass** — the rest of this repo (backend/frontend/schemas/routes) is not yet audited for KORA product capabilities beyond CVE. | `FORMALIZED_METHODOLOGY` (CVE only, confirmed) — repo's broader product maturity `NOT_YET_AUDITED` | CVE-01→15 (`WALLET_CVE_RECONCILIATION.md`) |
| Good Mood / DJ Sayd | Good Mood OS | `gmfest972/goodmooddjsayd` | default branch (shallow clone) | (recorded in `GOOD_MOOD_DJ_SAYD_RECONCILIATION.md`) | Full real backend: catalogue/events/tickets/QR/door-scan/fans/newsletter/merch/orders, real Stripe checkout+webhook, real FREK+Wallet outbox clients (env-gated, `NOT_CONNECTED` by default), JWT admin auth. No incident/rollback mechanism. | `PRODUCTION_MVP` (best-grounded internal-operator cluster of the whole cartography) | GMD-21→34 (built, `docs/gmd/`), SAY-01→50 |
| Intelligence OS | (unconfirmed name) | `cultureconnectorg/Cvln-ios-v.1` | — | `NOT_YET_AUDITED` | — | — | IOS-01→25 (`AGENT_FACTORY_IOS_BRAIN_CMD_LAURENTIA_RECONCILIATION.md`) |
| Laurentia | Laurent.ia | `cultureconnectorg/Laurent.ia` | — | `NOT_YET_AUDITED` | — | — | LAU-01→10 |
| Kiltikonet | Kiltikonet (network product) | `cultureconnectorg/Kiltikonet`, `Kiltikonet-Aout2026`, `Kiltikonet-mai2026` (3 repos/iterations — private: `Kiltikonet-mai2026`) | — | `NOT_YET_AUDITED` | — | — | KLT-09→20 (`KLT_09_20_RECONCILIATION.md`) |
| CultureConnect (umbrella) | CultureConnect 2026 | `cultureconnectorg/culutureconnect2026` | default branch (shallow clone) | (cloned and searched this session) | Confirms KORA named as a real ecosystem entity (`cvl_brain.py`); `FREK_AUDIT.md`, `WALLET_AUDIT.md`, `BRAIN_AUDIT.md`, `KILTIKONET_DOCUMENTATION.md`, `NFC_APP_SPEC.md` exist — **not yet read in depth**, searched only for CVE/KORA mentions | `NOT_FULLY_AUDITED` — large repo (91M, own audit docs suggest real depth) | Potentially Agent Factory/Brain/Command Center/Wallet/Kiltikonet — audit before those domains' waves |
| Agent Factory | (unconfirmed name) | Not found under `cultureconnectorg` via `list_repos` query "agent" | — | `NO_REPO_FOUND_YET` | — | — | AF-01→25, AF-X-01→09 |
| CVLN Brain | (unconfirmed name) | Not found via `list_repos` query "brain" — but `culutureconnect2026/backend/services/cvl_brain.py` exists (see above) | — | Partial — see CultureConnect row | — | — | BRN-01→15 |
| Command Center | (unconfirmed name) | Not found via `list_repos` query "command" | — | `NO_REPO_FOUND_YET` — do not confuse with `fms-os/fms`'s own unrelated `/os/command-center` | — | — | CMD-01→15 |
| CVLN Wallet (product, distinct from this Academy's ledger) | (unconfirmed name) | Not found via `list_repos` query "wallet" | — | `NO_REPO_FOUND_YET` | — | — | WAL-19→28 (internal), WAL-X |
| LabelOS | (unconfirmed name) | Not found via `list_repos` query "label" | — | `NO_REPO_FOUND_YET` — legacy formation `LOS-01` in `CVL-ACADEMY` itself is the only grounding so far | — | — | LOS-OP-01→15 |
| Gala Cook & Food | (unconfirmed name) | Not found via `list_repos` query "gala" | — | `NO_REPO_FOUND_YET` | — | — | GCF-19→30 |
| CVLN Hospitality | (unconfirmed name) | Not found via `list_repos` query "hospitality" | — | `NO_REPO_FOUND_YET` — legacy formation `HOS-01` in `CVL-ACADEMY` itself is the only grounding so far | — | — | (HOS internal layer, if any) |
| CVLN CyberSecure | (unconfirmed name) | Not found via `list_repos` query "cyber" | — | `NO_REPO_FOUND_YET` | — | — | CYB-31→42 |
| Blockchain/Tokenomics | (unconfirmed name) | Not found via `list_repos` query "block" | — | `NO_REPO_FOUND_YET` — legacy formation `BCH-01` in `CVL-ACADEMY` itself is the only grounding so far | — | — | BCI-31→40 |
| Fondation Cœurvolan / CIP Foundation | (unconfirmed name) | Not found via `list_repos` query "fondation" | — | `NO_REPO_FOUND_YET` — legacy formation `CIP-01` in `CVL-ACADEMY` itself is the only grounding so far | — | — | FDC-36→48 |

## Method (repeated per domain, never skipped)

Before any `NO_REPO`/`PRODUCT_DEPENDENCY`/`BLOCKED`/`NOT_IMPLEMENTED`
verdict or a Founder-decision escalation on an INTERNAL/OPERATOR/
BRIDGE/CROSS_ECOSYSTEM candidate:

1. Search all repos accessible to this session (`list_repos`, keyword
   variations — product name, legacy name, working-title name).
2. Inspect relevant branches — not just the default branch; a fetch by
   specific commit SHA (as done for `frekcoreAout2026`) can reach work
   not on `main`.
3. Search recent commits/branches that may carry an implementation
   absent from `main`.
4. Inspect `/docs`, `/memory`, backend, frontend, schemas, routes,
   tests, and integration points once a repo is found.
5. Record the result here — found or not found — before writing the
   domain's reconciliation verdict.

**`NO_REPO_FOUND_YET` is not a permanent verdict** — it means the
repos accessible to *this* session did not surface a match; a repo
under an owner/name not yet known to this session may still exist
(as `kora2024/Kora-app` and `cultureconnectorg/frekcoreAout2026`
demonstrated — neither was known before being named directly). Update
this row the moment a real repo is named or found.

## Status

`STATUS = LIVE REGISTRY`, updated per domain immediately before that
domain's W6 wave, never in one single audit pass.
