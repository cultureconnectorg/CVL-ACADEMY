# CVE-06 — Integration Academy Package Note

## Réel vs. supposé

**Réel (re-vérifié directement cette session, texte intégral relu) :**
le terme "Shapley" n'apparaît nulle part dans
`KORA_CVE_Specification_Mathematique_v1.0.md`. Le mécanisme
d'attribution réel est `C_i,c` (§1.2, CVE-03). Le concept général de
valeur de Shapley (hors KORA) est un savoir de marché standard,
correctement labellisé comme tel.

**Supposé :** toute implémentation KORA d'une valeur de Shapley —
inexistante (`FORMALIZATION_PENDING`). Un lien `CVE06.SKILL.*` réel
dans le runtime de cette Academy — inexistant (`NO_RUNTIME_BINDING`).

## Dépendances

- CVE-03 (prérequis, le mécanisme d'attribution réel), `docs/
  cvln_academy_master/20_EXTERNAL/WALLET_CVE_RECONCILIATION.md`
  (`FD-CVE-001`), `70_EVIDENCE/EVIDENCE_ARCHITECTURE.md`.

## Ce qu'une future intégration exigerait

1. Une entrée `CVE06` dans le registre de certification de cette
   Academy.
2. Une surface candidat réelle (ce corpus est markdown seul).
3. Une nouvelle révision de la spécification KORA CVE définissant
   formellement une structure de coalition, une fonction de valeur, et
   un calcul de contribution marginale — aucune de ces trois choses
   n'existe aujourd'hui.

## Status

`STATUS = PACKAGE_COMPLETE_FOR_CVE06` (`FORMALIZATION_PENDING`
toujours actif pour le contenu KORA-spécifique) — référentiel, banques
N1/N2, assessment + rubric, evidence model, 3 guides, cette note
d'intégration existent tous. `FULLY_COMPLETE` non déclaré.
