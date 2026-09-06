# WAL-19 — CVLN Wallet Operator (umbrella)

```
Prerequisite for WAL-20/21/24/28. Orientation formation — teaches the
whole real ledger's shape before any specialization goes deep on one
part.
```

## Repo truth this formation is built on

`backend/wallet/models.py` (`WalletTransaction`, `WalletAccount`,
`WalletSummary`), `backend/wallet/service.py` (`credit()`,
`_get_or_create_account()`, `get_summary()`, `list_transactions()`),
`backend/api/wallet.py` (`GET /wallet/me`, `GET /wallet/transactions`,
`GET /wallet/pass/apple`, `GET /wallet/pass/google`). Full detail
already catalogued in `docs/cvln_academy_master/20_EXTERNAL/
WALLET_CVE_RECONCILIATION.md` §"Repo truth" — reused here by
reference, not restated.

## Prerequisites

None (entry point of this corpus). Recommended: basic REST API
literacy and Pydantic model literacy (shared with GMD-21's own
prerequisite note).

## Objectives

By the end of WAL-19, a candidate can:
1. Draw the real Wallet system map from memory (account, transaction,
   summary, the 4 real API routes) — a derivation from having read the
   actual code, not a memorized diagram.
2. Explain, for any given capability, whether it exists in this
   ledger or is a genuine product gap (WAL-22/23/25/26/27) — by
   checking the repo, never by assuming a "typical wallet" would have
   it.
3. State precisely why `WalletAccount.jcc_balance` is deliberately
   separate from `models.User.cc_credits` — the code's own docstring
   distinction, never conflated.
4. State precisely why this Academy's own ledger is not the same
   system as the real external `djsayd/CVLN-Wallet` product.

## Modules

| # | Module | Real grounding | Deliverable |
|---|---|---|---|
| M1 | System map — reading the models and service functions end to end | `WalletTransaction`/`WalletAccount`/`WalletSummary`, `credit()`/`get_summary()`/`list_transactions()` | Annotated map: one line per model/function, purpose, owning specialization (WAL-20/21/24/28) |
| M2 | Data model literacy | `TransactionType` (`badge_earned`/`jcc_earned`/`token_earned`/`reward_redeemed`/`payment`), `Currency` (`jcc`/`token`/`eur`) | Written note per type: what real-world event it represents, what it does NOT track (no double-entry pair, no hold/reservation) |
| M3 | CC vs. JCC boundary | `models.py`'s own docstring: "CC credits are Academy's own pedagogical currency; the Wallet is the cross-CVLN-ecosystem ledger" | Written distinction, verbatim-grounded, never invented |
| M4 | Academy Wallet vs. real `djsayd/CVLN-Wallet` product boundary | `WALLET_CVE_RECONCILIATION.md`'s repo-truth delta (holds/maker-checker/idempotency exist only in the real external product) | Written note: what this ledger has, what the real product has, and that no integration exists between them |

## Assessment

Per `../CERTIFICATION_MODEL.md`. N1: route/model-ownership quiz. N2:
"a new team member joins — brief them on the real Wallet ledger in 10
minutes, including what it is NOT (not the external product, not a
double-entry system)." Assessment: full annotated system map (M1
deliverable), graded against the real code.

## Evidence / certification / mission eligibility

Evidence = M1 annotated map + M3 + M4 written distinctions, all
checkable against the real repo. Certification eligibility: pass
Assessment at N2+. Mission eligibility: none directly (WAL-19 is a
prerequisite) — a candidate becomes mission-eligible once qualified in
at least one of WAL-20/21/24/28.

## Status

`STATUS = PACKAGE_COMPLETE_FOR_WAL19` — full canonical package built:
`BANQUE_N1.md`, `BANQUE_N2.md`, `ASSESSMENT_AND_RUBRIC.md`,
`EVIDENCE_MODEL.md`, `GUIDE_CANDIDAT.md`, `GUIDE_CORRECTEUR.md`,
`GUIDE_JURY.md`, `INTEGRATION_NOTE.md`. Not yet delivered to a real
candidate — `FULLY_COMPLETE` still requires that verification, per
`../QUALITY_GATES.md`.
