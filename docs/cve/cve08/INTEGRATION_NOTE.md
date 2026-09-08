# CVE-08 — Integration Academy Package Note

## Réel vs. supposé

**Réel (re-vérifié directement cette session) :**
`KORA_CVE_Specification_Mathematique_v1.0.md` §3.3
(`v_i(t) = dVCF_i/dt`) et §6 (`Maximize: Σ_i VCF_i^{corrected}(t)`) —
les deux seules apparitions réelles de VCF, toutes deux comme entrée
assumée.

**Supposé :** toute équation définissant VCF — inexistante
(`FORMALIZATION_PENDING`). `CVI_i,c` comme proxy de VCF — une
hypothèse de travail, jamais une affirmation du document. Un lien
`CVE08.SKILL.*` réel dans le runtime de cette Academy — inexistant
(`NO_RUNTIME_BINDING`).

## Dépendances

- CVE-01, CVE-04 (prérequis, CVI comme analogue le plus proche),
  CVE-06 (même discipline `FORMALIZATION_PENDING`), `docs/
  cvln_academy_master/20_EXTERNAL/WALLET_CVE_RECONCILIATION.md`
  (`FD-CVE-001`), `70_EVIDENCE/EVIDENCE_ARCHITECTURE.md`.

## Ce qu'une future intégration exigerait

1. Une entrée `CVE08` dans le registre de certification de cette
   Academy.
2. Une surface candidat réelle (ce corpus est markdown seul).
3. Une nouvelle révision de la spécification définissant formellement
   VCF en fonction de primitives réelles — inexistante aujourd'hui.

## Status

`STATUS = PACKAGE_COMPLETE_FOR_CVE08` (`FORMALIZATION_PENDING`
toujours actif pour l'équation VCF elle-même) — référentiel, banques
N1/N2, assessment + rubric, evidence model, 3 guides, cette note
d'intégration existent tous. `FULLY_COMPLETE` non déclaré.
