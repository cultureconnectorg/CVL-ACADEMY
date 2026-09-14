# CVLN Wallet (WAL-01→28) & CVE (CVE-01→15) — Reconciliation

```
RULE APPLIED: same corrected method — curriculum coverage ×
occupational distinctness, CONTENT_OVERLAP != PROFESSIONAL_DUPLICATE.
```

## Repo truth — the entire real Wallet footprint

`backend/wallet/{models,service,passes}.py` + `backend/api/wallet.py`
(this repo — no separate Wallet repo was named). Real, verified:

- `WalletAccount` (`jcc_balance`, `token_balance`, `badges`),
  `WalletTransaction` (**append-only**, 5 types: `badge_earned`/
  `jcc_earned`/`token_earned`/`reward_redeemed`/`payment`).
- `credit()` — **additive only**. No debit/hold/reservation function;
  a "spend" is a convention (caller passes a negative amount), not a
  distinct mechanism.
- `get_summary()`, `list_transactions()` — reads.
- **Real, unsigned** Apple/Google Wallet pass payload builders
  (`passes.py`) — correct documented shape for both platforms, and
  honestly never fakes a signed, installable pass. **Correction
  (re-verified directly, `docs/wal/wal24/`):** the file's own comment
  claims signing is "left as a 501," but no route raises
  `HTTPException(status_code=501)` anywhere in `backend/wallet/` or
  `backend/api/wallet.py` — both pass routes return a normal HTTP 200
  with `{"status": "unsigned", ...}` in the JSON body. The intent is
  honored; the "501" wording is the code's own comment, not its actual
  HTTP behavior — cite the real 200-plus-status-field pattern.
- Real, minimal REST API (`api/wallet.py`): `GET /wallet/me`,
  `GET /wallet/transactions`, `GET /wallet/pass/apple`,
  `GET /wallet/pass/google` — read-only; no public credit/transfer
  endpoint (crediting happens server-side from other services).
- **Explicit code-level boundary already documented** (models.py
  docstring): Wallet's `jcc_balance` is deliberately separate from
  `models.User.cc_credits` (Academy's own pedagogical progression
  currency) — "CC credits are Academy's own pedagogical currency; the
  Wallet is the cross-CVLN-ecosystem ledger." Any WAL-20 content must
  preserve this distinction verbatim, never conflate the two.

**No holds, no double-entry pairs, no reversals/refunds as a formal
mechanism, no idempotency keys, no transfer-between-users, no
marketplace/escrow, no treasury, no fee engine, no kill-switch, no
settlement/reconciliation.** This is a simple, honest rewards ledger —
richer than nothing, far short of the fintech-grade system WAL-01→28
as a whole implies.

## Repo truth delta — real CVLN Wallet product found (2026-09-06)

```
Founder correction: djsayd/CVLN-Wallet exists and was verified
directly this session. "No separate Wallet repo was named" above is
now superseded for the product side of WAL-19→28/WAL-X; it remains
accurate for describing THIS Academy's own additive ledger, which is
unchanged and still what WAL-19→28 must be built to teach honestly
(the operator role is "operate this Academy's ledger," not "operate
the external product").
```

`djsayd/CVLN-Wallet` (commit `359aaee1`, audited directly — see
`95_GAPS/REPO_REGISTRY.md`) is a real, financial-grade FastAPI product
with everything the paragraph above says this repo's own ledger
lacks: holds/authorization/capture, maker-checker, idempotency keys +
kill-switch, monetary precision, outbox/inbox delivery, refunds/
reversals/fees, settlement/reconciliation, virtual card audit/
security. It also has a real `docs/AGENTSKILL-WALLET-MAPPING.md`
showing `Payments.Request`/`Payments.Send`/`Wallet.Balance`/
`Assets.Portfolio` already integrated (P0), `FREK.Identity` and
`KORA.StreamIncome` as prepared-but-inactive interfaces, and an
explicit `REJECT` verdict on "Treasury bots illimités" for violating
least-privilege — a real, citable security-governance precedent.

**What this changes:** WAL-19→28 (internal operator roles) and WAL-X
(cross-ecosystem bridges) were reconciled below against *this repo's*
thin ledger, correctly per the "upgrade in place, don't invent" rule.
That reconciliation was not wrong for WAL-19/20/21/24/28 — it stands.
**It undersold WAL-22/23/25/26/27 specifically**, which this repo's
own thin ledger has no equivalent of at all: those 5 rows have now
been re-checked directly against `djsayd/CVLN-Wallet` and reclassified
from `CAPABILITY_NOT_IMPLEMENTED` to buildable (see the dedicated
repo-truth delta further below, "WAL-22/23/25/26/27 found in
`djsayd/CVLN-Wallet`") — cited as real grounding for
coffres/transfer/marketplace/settlement/kill-switch concepts, exactly
as CVE cites the KORA spec, **without** claiming an Academy candidate
can operate the real product (no integration
observed between the two repos). CVE-01→15 verdicts below are
unaffected — CVE-01→15 already cites the correct KORA source
directly; nothing in `djsayd/CVLN-Wallet` changes that.

## WAL-01→18 (external/market) — reconciliation

All 18 are `DISTINCT_PROFESSION` (standard, real fintech-engineering
career specializations — ledger engineer, payments ops, card ops,
compliance, treasury, etc.) with `NONE` curriculum coverage in Academy
today (KOR-10 taught Wallet/JCC only from the *application/usage*
angle for a KORA creator — not the *systems-engineering* angle these
candidates require; the two never overlap, no duplication risk).
**Zero rejected.** Two are grounded better than the rest:

| Candidate | Coverage | Note |
|---|---|---|
| WAL-03 Digital Ledger & Double-Entry Accounting | `PARTIAL` | Real ledger exists but is **single-entry additive**, not double-entry — teach the real double-entry standard, then explicitly mark CVL-ACADEMY's own ledger as a simplified `CAPABILITY_PARTIAL` case study, never implied as double-entry. |
| WAL-08 Payment Infrastructure & Provider Integration | `PARTIAL` (via cross-ecosystem) | CVL-ACADEMY's own Wallet has no PSP integration, but `gmfest972/goodmooddjsayd` has a **real, working Stripe integration** (`/payments/checkout`, `/stripe/webhook`) — the one genuinely real payment-provider precedent anywhere in the ecosystem audited this session. Use it as the worked case. |
| WAL-10 Apple/Google Wallet & Tokenized Card Operations | `SUBSTANTIAL` | **Best-grounded WAL candidate** — real, correctly-shaped pass payloads exist for both platforms; the formation can teach the real code and its honest unsigned-pass boundary directly (HTTP 200 + `"status": "unsigned"`, not a literal 501 — see repo-truth correction above). |
| WAL-13 Financial API & Embedded Finance | `PARTIAL` | A real, minimal, read-only Wallet API exists (`api/wallet.py`) — small but genuine worked example. |

All others (WAL-01/02/04/05/06/07/09/11/12/14/15/16/17/18):
`NEW_EXTERNAL`, `CAPABILITY_NOT_IMPLEMENTED` beyond the ledger/API
above. WAL-14 (Payment Security, Fraud & Risk) and WAL-15 (Financial
Compliance & Audit) additionally flagged: WAL-14 joins the same
CyberSecure boundary question as FRK-48→51/KLT-17 (`G8`); WAL-15 is
`NEEDS_EXPERT_REVIEW` (financial regulation, never a universal recipe).

## WAL-19→28 (internal operator roles) — reconciliation

| Candidate | Coverage | Action |
|---|---|---|
| WAL-19 CVLN Wallet Operator | `PARTIAL` (real `credit`/read functions) | `NEW_INTERNAL`, buildable now. |
| WAL-20 CC/JCC Monetary Operations | `PARTIAL` | `NEW_INTERNAL` — must reuse the real code-level CC≠JCC distinction verbatim (see above), never invent a merged currency model. |
| WAL-21 CVLN Ledger Operator | `PARTIAL` (real `credit()`) | `NEW_INTERNAL`, buildable now. |
| WAL-22 Coffres & Allocation Operations | **UPGRADED, see delta below** | `NEW_INTERNAL`, buildable now — real `djsayd/CVLN-Wallet` grounding. |
| WAL-23 CVLN Payment & Transfer Operations | **UPGRADED, see delta below** | `NEW_INTERNAL`, buildable now — real `djsayd/CVLN-Wallet` grounding. |
| WAL-24 CVLN Card Operations | `PARTIAL` (real pass payload builders, operator angle vs WAL-10's market angle) | `NEW_INTERNAL`, buildable now — cross-reference WAL-10, don't duplicate its market content. |
| WAL-25 CVLN Marketplace Operations | **UPGRADED, see delta below** | `NEW_INTERNAL`, buildable now — real `djsayd/CVLN-Wallet` grounding. |
| WAL-26 Settlement & Reconciliation Operator | **UPGRADED, see delta below** | `NEW_INTERNAL`, buildable now — real `djsayd/CVLN-Wallet` grounding. |
| WAL-27 Financial Incident & Kill-Switch Operations | **UPGRADED, see delta below** | `NEW_INTERNAL`, buildable now — real `djsayd/CVLN-Wallet` grounding. |
| WAL-28 Wallet Audit & Evidence Operations | `PARTIAL` (real, genuinely append-only `db.wallet_transactions`) | `NEW_INTERNAL`, buildable now — same pattern as FRK-68 (Auditor): a real, inspectable audit surface even without cryptographic depth. |

**Zero rejected. Corrected count (was 5/10, see delta below): 10/10
buildable now on real code** — WAL-19/20/21/24/28 on this Academy's
own `backend/wallet/`, WAL-22/23/25/26/27 on the real external
`djsayd/CVLN-Wallet` product (no capability of theirs exists in
`backend/wallet/`, but all five exist, precisely named, in the real
product).

### Repo-truth delta — WAL-22/23/25/26/27 found in `djsayd/CVLN-Wallet` (checkpoint, 2026-09-06)

```
Founder checkpoint: before finalizing WAL-22/23/25/26/27 as
BLOCKED_PRODUCT_DEPENDENCY, cross-check against djsayd/CVLN-Wallet
(already cloned/audited this session) rather than treating this
Academy's own thin backend/wallet/ as the only source of truth for a
formation literally titled "CVLN Wallet Operator." Verification only
— the WAL-19/20/21/24/28 reconciliation above is not redone.
```

Direct verification this session, `djsayd/CVLN-Wallet/backend/
server.py` (re-read, not merely cited from the earlier session pass):

| Formation | Real capability found | Route(s) |
|---|---|---|
| **WAL-22** Coffres & Allocation Operations | Real vault system: create/list/delete a `coffre` (`goal_cc`, `amount_cc`), atomic move in/out backed by the ledger (`ledger_post`, `atomic_spend`/`apply_user_balance`) | `GET/POST /coffres`, `POST /coffres/{coffre_id}/move`, `DELETE /coffres/{coffre_id}` |
| **WAL-23** CVLN Payment & Transfer Operations | Real entity-to-user and entity-to-entity transfer, atomic entity debit, dual ledger posting, recipient resolved by FREK-ID or `entity_id` | `POST /v1/entity/transfer` |
| **WAL-25** CVLN Marketplace Operations | Real seeded catalog (8 items spanning the actual CVLN ecosystem: FREKCORE, Factory Maker Studio, Culture Connect, Laurentia, Kiltikonet, KORA, Factory Maker Academy, CVLN OS) + real idempotent buy flow (`atomic_spend`, `idem_begin`/`idem_finish`) | `GET /marketplace`, `POST /marketplace/buy` |
| **WAL-26** Settlement & Reconciliation Operator | Real settlement state machine (`PENDING→SUBMITTED→SETTLED`/etc., `_settlement_predecessors`, retry-safe re-submit), provider abstraction (`get_provider().submit()`), correlation IDs, event emission (`emit_event`), full state history; real reconciliation case lifecycle (`OPEN`/`INVESTIGATING`→`RESOLVED`/`ACCEPTED_DIFFERENCE`/`ESCALATED`) | `POST/GET /admin/settlements`, `POST /admin/settlements/{id}/submit`, `GET /admin/settlements/{id}`, `POST /admin/reconciliation/run`, `GET /admin/reconciliation/cases`, `POST /admin/reconciliation/cases/{case_id}/resolve`; doc: `docs/CVLN-SETTLEMENT-RECONCILIATION.md` |
| **WAL-27** Financial Incident & Kill-Switch Operations | Real global kill-switch, exactly 3 named switches (`"withdrawals"`, `"card"`, `"agents"`), admin-only, audited (`KillSwitch.Toggled`); separately, real per-user card freeze/unfreeze | `PUT /admin/kill-switch`, `POST /card/freeze`, `POST /card/unfreeze` |

**What this changes:** these 5 rows move from `CAPABILITY_NOT_
IMPLEMENTED`/`BLOCKED_PRODUCT_DEPENDENCY` to `NEW_INTERNAL`, buildable
now, grounded in `djsayd/CVLN-Wallet` directly (`docs/wal/wal2{2,3,5,
6,7}/REFERENTIAL.md`) — **matching the discipline already applied to
WAL-08** above (a real external precedent used as the worked case).
**What this does NOT change:** none of these five capabilities exists
in this Academy's own `backend/wallet/`, and no integration between
the two repos is observed — a candidate is taught to read and reason
about the real product's operator surface, never granted real
operational access to `djsayd/CVLN-Wallet` (a separate, human-governed
authorization decision, unchanged). Status discipline: this is a
`RECONCILED_NOT_BUILT`→`MODULE_CONTENT_DRAFTED` correction via real
work, not an artificial status promotion — none of these five reaches
`PACKAGE_COMPLETE` in this pass.

## CVE-01→15 — reconciliation

**CLOSED — `FD-CVE-001` (Founder decision, final).** A real
methodological source is named: `memory/KORA_CVE_Specification_
Mathematique_v1.0.md` (KORA), formalizing the Cultural Value Engine as
a Mathematical Specification v1.0, frozen on Theory v1.4. Canonical
status: **`FORMALIZED_METHODOLOGY` / `SOURCE_OBSERVED`** — this
replaces `PROPOSED_METHODOLOGY` wherever that label described the
*existence* of the CVE methodology itself. The Founder's decision
draws a strict line that this reconciliation preserves exactly:
**existence of the methodology ≠ empirical validation.** Any
parameter, weight, or calibration input the specification leaves open
(not yet simulated/tuned against real cultural-contribution data)
stays `CALIBRATION_PENDING` — this never degrades the formalized
methodology itself back to `PROPOSED`. Concretely: "Shapley Value for
Cultural Contribution," "Nebula Cultural Value Modeling," "VCF," "UVC
Allocation" are now `FORMALIZED_METHODOLOGY` as *named, specified*
constructs (source-observed, per Founder decision); their specific
numeric parameters/weights, where not yet calibrated against real
data, remain `CALIBRATION_PENDING`.

**Audit note (verification complete):** `kora2024/Kora-app` cloned and
inspected directly — `memory/KORA_CVE_Specification_Mathematique_v1.0.md`
confirmed present and real: "KORA Cultural Value Engine — Mathematical
Specification v1.0, Formal Reference Document, Frozen on Theory v1.4,
CVLN Group / Tech & Data Pole," a rigorous, self-consistent measurement
model (Layer 1 raw signals — Trust Score, normalized components —
through saturation/normalization transforms, explicitly noting it
"introduces no new concepts," consolidating CVE v1.0→v1.4). This is
this session's own direct verification, not merely Founder attestation
— the earlier reservation (source not directly located) is fully
resolved.

**Action for all 15**: `NEW_INTERNAL`/`NEW_EXTERNAL` per row (as for
any other formalized-but-uncalibrated methodology domain), never
`BLOCKED_PRODUCT_DEPENDENCY` for lack of a methodology — that blocker
is lifted. Any row whose specific numeric parameters are not yet
calibrated stays flagged `CALIBRATION_PENDING` at the module level once
W6 content is written; this is a normal build note, not a Founder
escalation.

**Naming-collision guard (verified again, monitored ahead of the
Wallet wave) — do not merge with `Cvln-ios-v.1/economics/CVE-v1.2.md`.**
The `cultureconnectorg/Cvln-ios-v.1` repo (`95_GAPS/REPO_REGISTRY.md`)
carries its own, unrelated document under the same acronym: **"CVE
v1.2 — CVLN Value Engine"** — a contribution/JCC value-recognition
model, self-labeled `status: TARGET`/`attribution: SPECIFICATION`,
explicitly stating "no economic engine implementation was observed."
Re-read directly again for this note: it models *value recognition
from verified contribution* (JCC accounting), which is a **different
system** from KORA's Cultural Value Engine (Trust Score, `w_id/w_comp/
w_net/w_hist`, S/E/F/C/L components) formalized under `FD-CVE-001`
above. Same three letters, two distinct specifications, two distinct
owners (KORA Tech & Data Pole vs. the Office of the Principal Systems
Architect's IOS audit). **CVE-01→15 module content must cite only the
KORA spec** (`kora2024/Kora-app/memory/
KORA_CVE_Specification_Mathematique_v1.0.md`) as its source of truth;
`CVE-v1.2.md`'s JCC/contribution-recognition model is out of scope for
this domain and must never be blended into a CVE-01→15 module,
however similar the acronym looks. If a future formation is ever built
to teach the *other* CVE (CVLN Value Engine / JCC), it must use a
different code — never `CVE-*` — precisely to keep this collision from
recurring at the Skill-ID or module-code level.

## Wallet/CVE cross (WAL-X-01→09)

Updated verdict: no longer `BLOCKED` on the CVE methodology question
(`FD-CVE-001` closed) — still depends on a richer Wallet (WAL-05/06/07
above) for some rows, so `PARTIAL`/`EXTEND_EXISTING` per row rather than
a blanket block. `CALIBRATION_PENDING` inherited from CVE where a row
touches an uncalibrated parameter.

## Summary

| Domain | New/Extend | Blocked | Founder decision |
|---|---|---|---|
| WAL-01→18 | 18 `NEW_EXTERNAL` (4 with real partial grounding) | 14 `CAPABILITY_NOT_IMPLEMENTED` | WAL-14 (CyberSecure boundary, `G8` — resolved) |
| WAL-19→28 | 10 `NEW_INTERNAL` (**10/10 buildable now**, corrected 2026-09-06 — see repo-truth delta above) | 0 `CAPABILITY_NOT_IMPLEMENTED` | — |
| CVE-01→15 | 15 `NEW_INTERNAL`/`NEW_EXTERNAL` (`FORMALIZED_METHODOLOGY`, `CALIBRATION_PENDING` per uncalibrated parameter) | 0 | **CLOSED** — `FD-CVE-001` |
| WAL-X-01→09 | Partial, per row | Depends on Wallet richness only | — |

**Zero rejections across all 52 rows.** Build priority: WAL-10 (best
grounded) → WAL-19/20/21/24/28 (internal, this Academy's own real code)
→ WAL-22/23/25/26/27 (internal, real `djsayd/CVLN-Wallet` grounding,
corrected 2026-09-06) → WAL-03/08/13 (partial, real worked examples) →
remaining WAL-01→18 (market-general fintech knowledge) → CVE-01→15
(formalized methodology, per `FD-CVE-001`) → WAL-X (per-row, no longer
CVE-blocked). **Build status (docs/wal/) as of 2026-09-06: WAL-19
`PACKAGE_COMPLETE`; WAL-20/21/24/28 and WAL-22/23/25/26/27
`MODULE_CONTENT_DRAFTED` — referential depth only, deepening to full
package is a future wave, never assumed complete from this
reconciliation alone.**

## Status

`STATUS = RECONCILED_NOT_BUILT`. No mutation of `backend/wallet/` or
`backend/api/wallet.py`.
