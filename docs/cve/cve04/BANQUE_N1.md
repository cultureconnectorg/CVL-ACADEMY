# CVE-04 — Banque N1 (formative, M1→M3)

```
Sourced directly against KORA_CVE_Specification_Mathematique_v1.0.md
§3.1, re-read in full this session.
```

## M1 — CES formula literacy

1. Write the CES aggregation formula exactly. (`CVI_i,c = ( Σ_a
   w_a,c · x̂_i,c,a^ρ_c )^(1/ρ_c)`)
2. What does `a` range over in this formula? (`a ∈ {S, E, F, C,
   CHL_integrated, N}` — 6 components)
3. Which two of those 6 components are themselves derived elsewhere,
   not raw Layer 1 signals? (`CHL_integrated`, §3.3; `N`, §3.2)

## M2 — weight-constraint discipline

4. What constraint must the weights `w_a,c` satisfy? (`Σ_a w_a,c = 1`,
   `w_a,c ≥ 0`)
5. Why does this constraint matter for interpretability? (It keeps
   `CVI_i,c` a genuine weighted combination of the 6 components,
   never an arbitrary unbounded sum)

## M3 — cross-reference discipline

6. Where is `CHL_integrated` fully derived, and is it re-derived
   inside CVE-04? (§3.3 — cross-referenced only, never re-derived
   here)
7. Where is `N` fully derived, and is it re-derived inside CVE-04?
   (§3.2 — cross-referenced only, never re-derived here)
8. Where is `ρ_c` itself taught in depth? (CVE-05 — CVE-04 only
   states its role inside this formula at a literacy level)
