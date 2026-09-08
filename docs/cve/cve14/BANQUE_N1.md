# CVE-14 — Banque N1 (formative, M1→M3)

```
Sourced directly against KORA_CVE_Specification_Mathematique_v1.0.md
H0 and §6 C6, re-read in full this session.
```

## M1 — H0 closure-principle literacy

1. State Global Hypothesis H0 exactly. ("All raw input signals are
   timestamped and identically reproducible by a third party from raw
   listening/transaction logs. Any quantity not satisfying H0 is
   excluded from the model")
2. What is the name of the principle that excludes non-reproducible
   quantities? (The "principle of closure," v1.1 §1.2)
3. Give a concrete example of a quantity that would be excluded under
   H0. (E.g. an internal, undocumented editorial score that cannot be
   independently recomputed by a third party from raw logs — excluded
   by construction)

## M2 — C6 as enforcement mechanism

4. State constraint C6 exactly. (§6: "∀ component, reproducible by a
   third party from raw logs — auditability")
5. How does C6 relate to H0? (C6 is H0's enforcement mechanism at the
   Fundamental Law level — it restates the same reproducibility
   requirement as a formal optimization constraint, not a separate
   idea)

## M3 — auditability gap-check across the corpus

6. Which two formations in this corpus teach content that is not yet
   fully specified enough to audit against H0/C6? (CVE-06 — Shapley,
   `FORMALIZATION_PENDING`; CVE-08 — VCF, `FORMALIZATION_PENDING`)
7. Why can't an unformalized quantity be verified reproducible? (A
   quantity that has no defining equation cannot be independently
   recomputed by a third party — auditability presupposes a formal
   definition to check against)
