# CVE-02 — Banque N1 (formative, M1→M4)

```
Sourced directly against KORA_CVE_Specification_Mathematique_v1.0.md
§1 (Layer 1) and §2.1, re-read in full this session.
```

## M1 — Trust Score + Validation Filter

1. Write the Trust Score formula exactly, naming all 4 weighted
   signals. (`TS_i(t) = w_id·sig_id(t) + w_comp·sig_comp(t) +
   w_net·sig_net(t) + w_hist·sig_hist(t)`)
2. What must the 4 weights sum to, and what range does each `sig`
   occupy? (`w_id+w_comp+w_net+w_hist = 1`; each `sig ∈ [0,1]`)
3. What are the indicative initial calibration values for the 4
   weights? (`w_id=0.4, w_comp=0.3, w_net=0.2, w_hist=0.1`)
4. What condition must an event `e` satisfy to be retained for
   calculation, and where does that threshold come from? (`TS_i(t_e) ≥
   τ_fraude`, a threshold "fixed per cycle and published," per the
   Governance Protocol §6)
5. Is `τ_fraude` a fixed, universal constant? (No — it is set per
   cycle and published; a candidate who treats it as a single global
   constant is wrong)

## M2 — five raw components

6. Name all 5 components (`S,E,F,C,L`) and what each measures in one
   phrase. (`S` = validated streams, `E` = engagement,
   `F` = fidelity/active weeks, `C` = attributed conversions,
   `L` = legacy)
7. Which one of the 5 is explicitly NOT a raw signal but a *derived*
   quantity, and what derives it? (`L` — replaced by the CHL integral,
   §3.3; the other 4 are genuinely raw)
8. What does `F_i,c`'s formula weight Premium subscribers by, exactly?
   (A multiplier of 1.3 for active weeks where the listener is a
   Premium subscriber, vs. 1.0 otherwise, averaged over 12 weeks)
9. What is the time window for the `C` (attribution) component?
   (14 days)
10. What does `S_i,c` normalize by? (Percentile across the cycle's
    catalog — not a raw stream count)

## M3 — saturation transformation

11. Name both candidate forms of the concave transformation.
    (`x̂ = log(1+x)` or `x̂ = x^0.5`)
12. Has the choice between these two forms been made yet, per the
    spec's own words? (No — "to be empirically decided during
    chantier 2," which has not occurred)
13. What does Hypothesis H1 state about this choice? (The same
    transformation form is used for all components within the same
    cycle — no per-component differentiation, to preserve
    comparability)

## M4 — hand-off to Layer 2

14. What do the 5 (transformed) raw components feed into, and where
    is that formula fully taught? (The CES aggregation, `CVI_i,c`,
    §3.1 — taught in CVE-04, not re-derived here)
