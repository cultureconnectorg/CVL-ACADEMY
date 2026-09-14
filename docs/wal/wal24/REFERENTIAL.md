# WAL-24 — CVLN Card Operations

```
Prerequisite: WAL-19. Cross-reference WAL-10 (market angle, same real
code, docs/cvln_academy_master/20_EXTERNAL/WALLET_CVE_RECONCILIATION.md).
```

## Repo truth

`build_apple_pass_payload()`/`build_google_pass_payload()`
(`wallet/passes.py`); routes `GET /wallet/pass/apple`, `GET /wallet/
pass/google` (`api/wallet.py`).

**Repo-truth finding (verified this session, corrects the file's own
comment):** `passes.py`'s docstring says signing is "explicitly left
as a 501" — but no route in this codebase raises
`HTTPException(status_code=501)`. Both pass routes return a normal
**HTTP 200** with `{"status": "unsigned", "note": "...", "payload":
{...}}` in the JSON body. The underlying intent (never claim a signed,
installable pass exists) is honored — the specific HTTP-501 wording is
not. Operators must cite the real 200-plus-status-field behavior, not
the comment's "501" framing verbatim.

## Prerequisites

WAL-19.

## Objectives

1. Operate the two real pass-payload builders and correctly report
   their real HTTP behavior (200 + `"status": "unsigned"`, not 501).
2. Explain exactly what is missing for a real installable pass on each
   platform (Apple: WWDR certificate + Pass Type ID; Google: Wallet
   Issuer account to sign the JWT) — citing the file's own comment,
   which is accurate on this point even where its "501" framing isn't.
3. Never present these payloads as installable passes today.

## Modules

| # | Module | Real grounding | Deliverable |
|---|---|---|---|
| M1 | Payload structure literacy | `build_apple_pass_payload()`, `build_google_pass_payload()` | Annotated payload for each platform |
| M2 | Real HTTP behavior correction | Direct `grep` across `backend/wallet/`/`backend/api/wallet.py` finding no 501 | Written note correcting the file's own comment — 200 + JSON status field, not an HTTP 501 |
| M3 | Signing-gap literacy | The named missing certificate/account per platform | Table: platform → what's built → what's missing for a real pass |

## Assessment

Per `../CERTIFICATION_MODEL.md`. M2 is a good discriminator between a
candidate who reads the comment and one who verifies the actual route
behavior — reward the latter.

## Evidence / certification / mission eligibility

Same general pattern as WAL-19.

## Status

`STATUS = PACKAGE_COMPLETE_FOR_WAL24` — full canonical package built:
`BANQUE_N1.md`, `BANQUE_N2.md`, `ASSESSMENT_AND_RUBRIC.md`,
`EVIDENCE_MODEL.md`, `GUIDE_CANDIDAT.md`, `GUIDE_CORRECTEUR.md`,
`GUIDE_JURY.md`, `INTEGRATION_NOTE.md`. Not yet delivered to a real
candidate — `FULLY_COMPLETE` still requires that verification, per
`../QUALITY_GATES.md`.
