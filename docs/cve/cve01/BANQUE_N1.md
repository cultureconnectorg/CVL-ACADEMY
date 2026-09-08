# CVE-01 — Banque N1 (formative, M1→M3)

```
Sourced directly against KORA_CVE_Specification_Mathematique_v1.0.md
§0 and the full section structure (§1→§6), re-read in full this
session (locally available, kora2024/kora-app/memory/).
```

## M1 — notation and conventions

1. What does `i` index? (A work, `i ∈ {1, ..., n}`)
2. What does `t` denote? (Continuous or discrete time, in days)
3. What does `c` denote? (A calibration cycle index — month or
   quarter, fixed)
4. What does `a` range over? (An index of a measurement component,
   `a ∈ {S,E,F,C,L,N}`)
5. What does the hat notation `x̂` mean, and what is its range?
   (Normalized value of `x`, `x̂ ∈ [0,1]` unless otherwise stated)
6. What does `MD_c` denote? (Distributable mass of cycle `c`)
7. What does `θ` denote? (The set of system parameters for a given
   cycle — weights, `ρ`, thresholds, bounds)

## M2 — Global Hypothesis H0

8. State Global Hypothesis H0 exactly. ("All raw input signals are
   timestamped and identically reproducible by a third party from raw
   listening/transaction logs. Any quantity not satisfying H0 is
   excluded from the model")
9. What happens to a quantity that does not satisfy H0, and what
   principle does the spec name for this? (It is excluded from the
   model — the "principle of closure," v1.1 §1.2)

## M3 — 4-layer map + chantier status

10. Name the 4 layers in order, with their section numbers.
    (Measurement §1 → Comprehension §3 → Forecasting §4 → Allocation
    §5)
11. Where does §2 (Normalization and Saturation) and §6 (Fundamental
    Law) fit relative to those 4 layers? (§2 is a transformation step
    applied within/between Layer 1 and Layer 2, not itself a named
    layer; §6 is a governing optimization program spanning all 4
    layers, also not itself one of the 4)
12. What chantier is this document, per its own status line, and what
    are chantiers 2 and 3? (Chantier 1 — formal specification;
    chantier 2 = simulation; chantier 3 = prototyping)
13. Have chantiers 2 or 3 been performed, per the document itself? (No
    — both are explicitly future work; this document "introduces no
    new concepts," it only consolidates v1.0→v1.4 in unique notation)
