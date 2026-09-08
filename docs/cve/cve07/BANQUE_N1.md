# CVE-07 — Banque N1 (formative, M1→M3)

```
Sourced directly against KORA_CVE_Specification_Mathematique_v1.0.md
§3.2, re-read in full this session.
```

## M1 — entropy formula literacy

1. Write the entropy formula `H_k(i,c)` exactly. (`H_k(i,c) = − Σ_j
   p_{i,j,k} · log(p_{i,j,k})`)
2. What does `p_{i,j,k}` represent? (The proportion of validated
   listens for work `i` within category `j` of axis `k`, over cycle
   `c`)
3. What does high entropy mean for cultural circulation on an axis,
   vs. low entropy? (High entropy = listens spread broadly across many
   categories on that axis; low entropy = concentrated in few
   categories)

## M2 — 6-axis + novelty coefficient literacy

4. Name all 6 real axes exactly. (`language, territory, diaspora,
   generation, style, collaboration`)
5. What does `ν_k(i,c) = 1` mean? (First-time penetration of category
   `j` on axis `k` for work `i`)
6. What does `ν_k(i,c) = 0.3` mean? (The category was already reached
   in previous cycles)
7. Is any novelty value between 0.3 and 1 named in the spec? (No —
   only the bounds `[0.3, 1]` and the two named calibration points are
   given; no intermediate value is defined)

## M3 — velocity factor literacy

8. Write the full Nebula Score formula. (`N_i,c = Σ_k H_k(i,c) ·
   ν_k(i,c) · φ(i,c)`)
9. What does `φ(i,c)` measure, and what is its bound? (A velocity
   factor, `φ(i,c) = 1 + (Δ_axis_coverage/Δt)`, normalized to
   `[1, φ_max]`)
