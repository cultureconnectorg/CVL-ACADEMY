# WAL-20 — CC/JCC Monetary Operations

```
Prerequisite: WAL-19.
```

## Repo truth

`WalletTransaction.currency` (`Literal["jcc","token","eur"]`,
`wallet/models.py`); `models.User.cc_credits` (a separate model
entirely, this Academy's own pedagogical progression currency). The
code's own docstring in `wallet/models.py` states the split
explicitly: "CC credits are Academy's own pedagogical currency; the
Wallet is the cross-CVLN-ecosystem ledger."

## Prerequisites

WAL-19.

## Objectives

1. Correctly classify any given transaction as CC, JCC, token, or
   `eur`-denominated, using only the real `Currency`/`cc_credits`
   fields.
2. Explain why no conversion function exists between CC and JCC in
   this codebase, and never invent one.
3. Recognize that `credit()`'s `currency` parameter only updates
   `jcc_balance` or `token_balance` — never `cc_credits`, which lives
   on a separate model entirely and is updated by different code paths
   outside `wallet/`.

## Modules

| # | Module | Real grounding | Deliverable |
|---|---|---|---|
| M1 | Currency taxonomy literacy | `Currency` type, `cc_credits` field | Table: currency → where it lives → what updates it |
| M2 | Non-conversion discipline | Absence of any CC↔JCC conversion function | Written note: why treating CC and JCC as interchangeable is a real error, not a simplification |
| M3 | Cross-reference to WAL-21 | `credit()`'s currency-specific `$inc` logic | Note distinguishing WAL-20 (classification) from WAL-21 (ledger mechanics) |

## Assessment

Per `../CERTIFICATION_MODEL.md`.

## Evidence / certification / mission eligibility

Same general pattern as WAL-19.

## Status

`STATUS = PACKAGE_COMPLETE_FOR_WAL20` — full canonical package built:
`BANQUE_N1.md`, `BANQUE_N2.md`, `ASSESSMENT_AND_RUBRIC.md`,
`EVIDENCE_MODEL.md`, `GUIDE_CANDIDAT.md`, `GUIDE_CORRECTEUR.md`,
`GUIDE_JURY.md`, `INTEGRATION_NOTE.md`. Not yet delivered to a real
candidate — `FULLY_COMPLETE` still requires that verification, per
`../QUALITY_GATES.md`.
