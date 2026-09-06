# CVE-03 — Cultural Contribution & Attribution

```
Prerequisite: CVE-01, CVE-02.
```

## Repo truth

§1.2 (Normalized Raw Components), specifically the `C_i,c` component:
`C_i,c = Σ (value_€ of attributed conversions, 14d window) / total_€
value of cycle conversions`. Also §1.1's Validation Filter
(`TS_i(t_e) ≥ τ_fraude`) as the attribution-gating mechanism upstream
of `C`.

## Prerequisites

CVE-01, CVE-02.

## Objectives

1. Explain the exact attribution window (14 days) and formula for the
   `C` component, and what "attributed conversion" means in this
   spec's own terms (a conversion whose `value_€` is counted within
   that window).
2. Explain how the Trust Score validation filter (§1.1) upstream
   affects which events are eligible for attribution at all.
3. Recognize that this spec does not name or define any specific
   multi-touch attribution model (e.g. last-click, linear, time-decay)
   beyond the single 14-day window formula given — never invent one.

## Modules

| # | Module | Real grounding | Deliverable |
|---|---|---|---|
| M1 | `C_i,c` formula literacy | §1.2 | Annotated formula: numerator/denominator, units, window |
| M2 | Validation-filter upstream dependency | §1.1 Validation Filter | Written note: how `τ_fraude` gates which events reach attribution |
| M3 | Scope discipline | Absence of a named multi-touch model beyond the 14d window | Honest note: this is the only attribution mechanism the frozen spec defines |

## Assessment

Per `../CERTIFICATION_MODEL.md`.

## Evidence / certification / mission eligibility

Same general pattern as CVE-01.

## Status

`STATUS = MODULE_CONTENT_DRAFTED`.
