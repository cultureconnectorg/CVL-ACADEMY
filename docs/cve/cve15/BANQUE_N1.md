# CVE-15 — Banque N1 (formative, M1→M3)

```
Sourced directly against KORA_CVE_Specification_Mathematique_v1.0.md
§6, re-read in full this session.
```

## M1 — the 8 constraints, precisely

1. State the objective the Fundamental Law maximizes. (`Maximize:
   Σ_i VCF_i^{corrected}(t)`)
2. State C1 and its meaning. (`Σ_i UVC_i,c = MD_c` — fixed budget)
3. State C2 and its meaning. (`TS_i(t) ≥ τ_fraude ∀ retained event` —
   fraud resistance)
4. State C3 and its meaning. (`|w_a,c − w_a,c-1| ≤ 0.10`,
   `|ρ_c − ρ_c-1| ≤ bound_ρ` — cycle-to-cycle stability)
5. State C4 and its meaning. (`H_diversity(catalog,c) ≥
   diversity_floor` — cultural diversity)
6. State C5 and its meaning. (`E[UVC_i|CVI_i=v,culture_i=A] =
   E[UVC_i|CVI_i=v,culture_i=B] ∀A,B` — cultural neutrality)
7. State C6 and its meaning. (`∀ component, reproducible by a third
   party from raw logs` — auditability, H0's enforcement)
8. State C7 and its meaning. (`∀ change in θ, published + justified +
   archived` — governance)
9. State C8 and its meaning. (`Ŷ_i(t+Δ) ∉ inputs(UVC)` —
   forecast/allocation separation)

## M2 — forecast/allocation firewall (C8)

10. Where else does the document state this same separation, besides
    §6 C8? (§4: `Ŷ_i(t+Δ) ∉ inputs(Allocation)`)
11. Why does this separation matter as a governance safeguard? (It
    structurally prevents speculative forecasting bias from entering
    actual value distribution — Layer 3's output can never feed Layer
    4's real allocation)

## M3 — governance publication discipline (C7)

12. What three things does C7 require for any change to `θ`?
    (Published, justified, and archived)
13. Is a silent, undocumented parameter adjustment compatible with
    C7? (No — any change to weights, `ρ`, thresholds, or bounds must
    go through this publication discipline)
