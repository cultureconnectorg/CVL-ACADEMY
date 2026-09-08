# CVE-03 — Banque N1 (formative, M1→M3)

```
Sourced directly against KORA_CVE_Specification_Mathematique_v1.0.md
§1.1-§1.2, re-read in full this session.
```

## M1 — `C_i,c` formula literacy

1. Write the `C_i,c` formula exactly. (`C_i,c = Σ (value_€ of
   attributed conversions, 14d window) / total_€ value of cycle
   conversions`)
2. What does the numerator sum? (The € value of conversions
   attributed to work `i` within the 14-day window)
3. What does the denominator represent? (The total € value of every
   conversion in the whole cycle)
4. What is the attribution window, exactly? (14 days)

## M2 — Validation-Filter upstream dependency

5. What gates whether an event is eligible to be counted at all,
   upstream of attribution? (The Validation Filter, §1.1:
   `TS_i(t_e) ≥ τ_fraude`)
6. Does the `C` formula itself define any fraud-resistance mechanism?
   (No — that is inherited entirely from §1.1's Validation Filter,
   never re-derived inside `C_i,c` itself)

## M3 — scope discipline

7. Does the frozen spec name any specific multi-touch attribution
   model (first-click, linear, time-decay)? (No — only the single
   14-day-window, value-proportional formula)
8. What is the honest answer if asked to "explain the CVE's
   multi-touch attribution model"? (State plainly that only the
   14-day-window formula exists in the frozen document; no named
   multi-touch model — first-click, linear, time-decay, or otherwise
   — is defined)
