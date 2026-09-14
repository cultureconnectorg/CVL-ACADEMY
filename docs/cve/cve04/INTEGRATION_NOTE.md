# CVE-04 — Integration Academy Package Note

## Réel vs. supposé

**Réel (re-vérifié directement cette session) :**
`KORA_CVE_Specification_Mathematique_v1.0.md` §3.1 (formule CES,
contrainte de poids).

**Supposé :** un lien `CVE04.SKILL.*` réel dans le runtime de cette
Academy — inexistant (`NO_RUNTIME_BINDING`).

## Dépendances

- CVE-01, CVE-02 (prérequis), CVE-05 (ρ_c en profondeur), CVE-07 (N en
  profondeur) — jamais dupliqués ici, `docs/cvln_academy_master/
  20_EXTERNAL/WALLET_CVE_RECONCILIATION.md` (`FD-CVE-001`),
  `70_EVIDENCE/EVIDENCE_ARCHITECTURE.md`.

## Ce qu'une future intégration exigerait

1. Une entrée `CVE04` dans le registre de certification de cette
   Academy.
2. Une surface candidat réelle (ce corpus est markdown seul).
3. Que le chantier 2 (calibration réelle de `ρ_c`, des poids) soit
   réalisé avant tout calcul CES réel.

## Status

`STATUS = PACKAGE_COMPLETE_FOR_CVE04` — référentiel, banques N1/N2,
assessment + rubric, evidence model, 3 guides, cette note
d'intégration existent tous. `FULLY_COMPLETE` non déclaré.
