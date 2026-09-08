# CVE-13 — Banque N1 (formative, M1→M3)

```
Sourced directly against KORA_CVE_Specification_Mathematique_v1.0.md
(status line + every named hypothesis), re-read in full this session.
```

## M1 — chantier status literacy

1. What is chantier 1, per the document's own status line? (The
   formal specification itself — "consolidates in unique notation
   everything established between CVE versions v1.0 and v1.4")
2. What are chantiers 2 and 3, and have they been performed? (Chantier
   2 = simulation, chantier 3 = prototyping — neither has been
   performed; this document is explicitly "a prerequisite for" both)

## M2 — named-hypothesis inventory

3. Name Hypothesis H1, its section, and what it states. (§2.1: the
   chosen saturation-transformation form — `log(1+x)` or `x^0.5` — is
   identical for all components within the same cycle)
4. Name Hypothesis H2, its section, and what it states. (§3.1: `ρ_c`
   is constant within a cycle, re-estimated between cycles within the
   same bounds as the weights, §5.3)
5. Name Hypothesis H3, its section, and what it states. (§3.3: CHL
   peak detection requires a minimum of `N_min` post-peak observations
   to be validated, avoiding premature detection on noise)
6. Besides H1/H2/H3, what other parameters does the Governance
   Protocol (§6, C7) require to be empirically calibrated and
   published per cycle? (The weights `w_a,c`, `τ_fraude`, and every
   other element of `θ`)

## M3 — simulation-methodology literacy (never a claimed result)

7. What does H0 require of any simulation input, per its own
   reproducibility standard? (Timestamped, identically reproducible by
   a third party from raw listening/transaction logs)
8. If asked to describe how chantier 2 would validate H2, what must
   the answer avoid? (Presenting any simulated or empirical outcome as
   if it had already happened — the answer must describe methodology
   only, explicitly labeled as not-yet-performed)
