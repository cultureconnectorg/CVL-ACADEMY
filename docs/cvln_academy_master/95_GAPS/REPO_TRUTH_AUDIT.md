# CVLN Academy Master — Repo Truth Audit

```
METHOD: §28 mission ("repo truth beats speculative curriculum").
Repos inspected: cultureconnectorg/CVL-ACADEMY (this repo, full),
fms-os/fms (cloned, shallow, HEAD 70b8e03), gmfest972/goodmooddjsayd
(cloned, shallow, HEAD 704ef93). No other repo named in the mission
(Kiltikonet repo, FREKCORE repo, CVLN Wallet repo as separate repos,
Laurentia repo) was reachable via a named URL/owner — see
GAP_REGISTER.md for what that blocks.
```

## 1. CVL-ACADEMY (this repo)

| Capability | File | Verdict |
|---|---|---|
| FREK core | `backend/services/frek_core.py` | Real, local, decoupled client. Signal types: `FREK-TIME/WORK/SCORE/LINK/CERT/CONTRIB/SHARE/MISSION`. `emit_signal`, `issue_proof`, stable `FREK-NNN` id reservation. |
| Agent Factory | `backend/services/agent_factory.py` | Real, single generic client (`AgentFactoryClient`) — no detachment/mission-scope/escalation logic observed. |
| Wallet | `backend/wallet/{models,service,passes}.py` | Real. `WalletAccount` (jcc_balance, token_balance, badges), `WalletTransaction` (append-only ledger, 5 types), `WalletSummary`. **Simple** — no holds, no double-entry pairs, no cards, no marketplace/escrow. |
| Ecosystem integrations (generic) | `backend/services/integrations/registry.py` | Real decoupled stubs for: Intelligence OS, Brain, Command Center, Laurentia, KORA, Factory Maker Studio, Good Mood, Culture Connect, Kiltikonet. **No logic beyond a generic request/fallback interface.** No LabelOS, no CVE, no Wallet entry here (Wallet is its own real module, not a generic stub). |
| CVLN Brain — real usage | `backend/certification/service.py:140`, `backend/services/events.py`, `backend/services/integrations/subscribers.py` | Real. `academy.certification.passed` event fires on certification pass → posted to Brain's `/academy/certification-passed` via the generic integration. **Only** confirmed real Brain touchpoint. |
| FMS canonical corpus (FMS-01→06) | `docs/ACADEMY_FMS_CANONICAL_*`, `backend/fms_canonical/`, `backend/fms_import/`, `backend/fms_lineage/`, `backend/api/fms*.py` | Real, built, bound to runtime. **This is the Academy's own FMS training corpus — distinct from `fms-os/fms` (see below), which is a separate real business platform, not the training corpus.** |
| Kiltikonet corpus (KLT-01→08) | `docs/klt/`, `backend/klt_canonical/` (per prior session work) | Real, built (KLT-01→05 complete, KLT-06→08 partial). |
| KORA corpus (KOR-01→15) | `docs/kor/`, `docs/kora_master_package/` | Real, built (this session, prior turn). |
| LabelOS | grep across `backend/` | **Referenced only as a pole name** in `seed_data.py`, `seed_modules.py`, `catalog_cartography.py`, `external_calibration.py`, `agent_factory.py` — no LabelOS service, model, or route exists. |
| CVE | grep across `backend/` | **Zero occurrence** beyond KOR-10's own documentation of its absence. |
| CyberSecure, Blockchain, Tokenomics, Command Center (CVLN's own), Fondation Cœurvolan, CVLN Group, Gala Cook & Food, CVLN Hospitality | grep across `backend/`, `docs/` | **Zero footprint** — no code, no seed data, no prior Academy documentation beyond this cartography. |

## 2. fms-os/fms (real, external, cloned)

```
CLONE: shallow, HEAD 70b8e031e69c658cbd52a0cd66ce693b4810bed4
```

FastAPI backend (`backend/server.py`, 1028 lines), single `APIRouter`.
Confirmed real routes/models: auth (register/login/logout/me), public
site (services/leads/newsletter/contact/bookings/projects/artists/news
/site-config), and an `/os/*` admin layer: projects, artists, clients,
leads, bookings (+status), services, news, site-config,
**command-center**, **integrations** (+test), **audit-log**.

**This is a studio/business management OS** — projects, clients,
bookings, artists, content, plus its own admin command-center and
integrations layer. It is **not** a recording/mixing/production tool —
no audio/video processing routes exist. Grounds FMS-07 (Studio Ops),
FMS-15 (Client/Commercial Ops), FMS-16 (Booking/Planning), FMS-18
(Ecosystem Ops = this `/os` layer). Does **not** ground FMS-08→14,17
(recording, mixing, audiovisual/creative production, A&R, project
creative coordination, portfolio ops) — those remain pure
craft/market-skill formations with no code counterpart, which is
expected (creative crafts aren't backend routes) and not a gap to
"fix."

## 3. gmfest972/goodmooddjsayd (real, external, cloned)

```
CLONE: shallow, HEAD 704ef93cb057c8941839e8a486d0aca752a3ec5e
```

FastAPI backend (`backend/server.py`, 874 lines) + 3 dedicated service
modules: `email_service.py`, `frek_service.py`, `wallet_service.py`,
`ticketing_service.py` (QR generation).

Confirmed real routes: `/catalogue`, `/events`, `/tour`, `/newsletter`,
`/merch`, `/auth/*`, `/admin/catalogue` (CRUD), `/admin/events` (+
ticket-types, tickets, report), `/admin/fans`, `/admin/merch`,
`/admin/newsletter` (+export), `/admin/orders`, `/admin/outbox/frek-id`,
`/admin/outbox/wallet`, `/payments/checkout`, `/payments/status/{id}`,
`/scan/check`, `/scan/counter/{eid}`, `/stripe/webhook`, `/tickets/{id}`
(+ qr.png).

**FREK-ID outbox** (`frek_service.py`): synchronous best-effort POST to
`{FREK_ID_URL}/frek-id/events` with a persistent retry queue
(`db.frek_id_outbox`, exponential backoff 30s→6h, 5 attempts then
`failed`). `FREK_ID_URL` empty by default → straight to outbox,
`status=pending`. **Confirms the "ready but decoupled" outbox pattern
independently, at a third real product**, matching CVL-ACADEMY's own
`frek_core.py`/`agent_factory.py` convention.

**Wallet outbox** (`wallet_service.py`): identical mechanic, POSTs to
`{WALLET_URL}/wallet/tickets`, `db.wallet_outbox`. Same
`NOT_CONNECTED`-by-default behavior.

**"DJ Sayd" is not a separate product** — it is referenced throughout
this same repo (`email_service.py`, `server.py`,
`tests/test_catalogue_real_data.py`, `tests/test_iter7.py`, `i18n.js`,
`Landing.jsx`). Good Mood (the festival/ticketing platform) and DJ Sayd
(the artist/brand) share one backend. See `GAP_REGISTER.md` for the
reconciliation this forces on the cartography's 94 rows.

## What this audit does NOT cover

No URL/owner was named in the mission for a separate Kiltikonet repo,
a separate FREKCORE repo, a separate CVLN Wallet repo, or Laurentia —
so none were cloned. If the Founder has these as distinct
repositories, name them explicitly and they will be audited the same
way before any KLT-09→20, FREK, or Wallet-advanced referential is
written.
