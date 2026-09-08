# CVE-14 — Evidence Model

## Chaîne de preuve

M1 note H0 + exemple concret → M2 note reliant C6 à H0 → M3 note
d'écarts d'auditabilité croisés → correcteur → (jury si 2.0–2.5) →
`CVE14.SKILL.*` (réservé, non lié au runtime).

## Ce qui compte comme preuve

La note M1 citant H0 exactement avec un exemple d'exclusion concret ;
la note M2 reliant explicitement C6 à H0 ; la note M3 identifiant
correctement CVE-06/CVE-08 comme écarts d'auditabilité non comblés.

## Ce qui NE compte PAS comme preuve

Une quantité non reproductible validée, C6 traité comme indépendant
de H0, ou une méthode d'audit inventée pour une quantité non
formalisée.

`READY_FOR_FREK_PROOF = FALSE`. Seule une certification interne
Academy (`CVE14.SKILL.*`) est en jeu.

## Réservation Skill ID

`CVE14.SKILL.H0_CLOSURE_LITERACY`, `CVE14.SKILL.C6_ENFORCEMENT_LINK`,
`CVE14.SKILL.AUDITABILITY_GAP_CHECK` — réservés dans
`70_EVIDENCE/EVIDENCE_ARCHITECTURE.md`.
