# BCI-03 — Smart-Contract Security Auditing (Blockchain Engineering)

```
Flagship of the BCI-01→30 external market-general pathway (task
#185). Prerequisite: BCI-02 (smart-contract development fundamentals,
market-general).
```

## Grounding

Real market-standard discipline: smart-contract security auditing
(vulnerability classes, audit methodology, testnet-before-mainnet
discipline). **Worked example** cited by reference, never re-derived:
legacy formation `BCH-01`, module `BCH-01-M03` ("Smart contracts pour
royalties automatiques," `backend/seed_modules.py:1521-1528`) — a
real delivered module whose deliverable is "Smart contract déployé
testnet" (a smart contract for automatic royalty payments, deployed
to a real testnet as part of `BCH-01`'s own certification path). This
formation never claims a CVLN-operated production smart-contract
deployment or a real audit engagement exists beyond this one
pedagogical testnet exercise — `BCH-01` itself stays exactly as
delivered, untouched, cited only.

## Prerequisites

BCI-02 (market-general smart-contract development fundamentals).

## Objectives

1. Explain what `BCH-01-M03`'s real deliverable actually is and is
   not: a pedagogical smart contract for automatic royalty
   distribution, deployed to a **testnet** (not mainnet, not
   production) — never overstate it as a live, audited, production
   financial system.
2. Apply standard smart-contract security-audit methodology
   (reentrancy, integer overflow/underflow, access-control checks,
   oracle manipulation) to a royalty-distribution contract like
   `BCH-01-M03`'s, as a market-general skill.
3. Distinguish testnet deployment from a real security audit: a
   successful testnet deployment demonstrates the contract runs, not
   that it has been audited for the vulnerability classes in
   Objective 2 — never conflate the two.

## Modules

| # | Module | Real grounding | Deliverable |
|---|---|---|---|
| M1 | `BCH-01-M03` literacy | Real module citation (`seed_modules.py:1521-1528`) | Written note: what the module delivers and its real scope (testnet, royalty automation) |
| M2 | Standard vulnerability classes | Market-general audit methodology | Checklist applied to a royalty-distribution contract pattern |
| M3 | Testnet-vs-audited discipline | The real gap between `BCH-01-M03`'s testnet deployment and a genuine security audit | Written note, explicitly distinguishing the two |

## Assessment

Per `../../CERTIFICATION_MODEL.md`. N2 includes a case testing the
testnet-vs-audited distinction, eliminatory for claiming `BCH-01-M03`'s
contract has been professionally audited (it has not, per its own
real scope).

## Evidence / certification / mission eligibility

Evidence = M1 written note + M2 applied checklist + M3 distinction
note, checkable against `BCH-01-M03`'s cited real scope and standard
audit methodology. Certification eligibility: pass Assessment at N2+.
Mission eligibility: none — no real smart-contract audit engagement
exists to operate through this Academy.

## Status

`STATUS = PACKAGE_COMPLETE_FOR_BCI03` — full canonical package built:
`BANQUE_N1.md`, `BANQUE_N2.md`, `ASSESSMENT_AND_RUBRIC.md`,
`EVIDENCE_MODEL.md`, `GUIDE_CANDIDAT.md`, `GUIDE_CORRECTEUR.md`,
`GUIDE_JURY.md`, `INTEGRATION_NOTE.md`. Chosen as the flagship for the
BCI-01→30 cluster (task #185) — the other rows stay at
`MODULE_CONTENT_DRAFTED` per `../REFERENTIAL.md`. Not yet delivered
to a real candidate — `FULLY_COMPLETE` still requires that
verification, per `../../QUALITY_GATES.md`.
