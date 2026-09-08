# CVE-08 — Evidence Model

## Chaîne de preuve

M1 citations annotées des 2 apparitions → M2 note de vérification
d'écart → M3 note d'hypothèse labellisée → correcteur → (jury si
2.0–2.5) → `CVE08.SKILL.*` (réservé, non lié au runtime).

## Ce qui compte comme preuve

Les citations M1 exactes (§3.3, §6) ; la note M2 confirmant l'absence
d'une équation VCF définissante ; la note M3 proposant `CVI_i,c` comme
proxy, explicitement labellisée `HYPOTHESIS, NOT SPEC`.

## Ce qui NE compte PAS comme preuve

Une équation VCF inventée présentée comme spec réelle, ou une
affirmation que VCF et CVI sont identiques comme un fait du document.

`READY_FOR_FREK_PROOF = FALSE`. Seule une certification interne
Academy (`CVE08.SKILL.*`) est en jeu.

## Réservation Skill ID

`CVE08.SKILL.VCF_CITATIONS`, `CVE08.SKILL.GAP_VERIFICATION`,
`CVE08.SKILL.HYPOTHESIS_LABELING_DISCIPLINE` — réservés dans
`70_EVIDENCE/EVIDENCE_ARCHITECTURE.md`.
