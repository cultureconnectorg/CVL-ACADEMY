# CVE-07 — Evidence Model

## Chaîne de preuve

M1 exemple numérique de `H_k` → M2 tableau des 6 axes + coefficients
de nouveauté → M3 note sur le facteur de vélocité → correcteur →
(jury si 2.0–2.5) → `CVE07.SKILL.*` (réservé, non lié au runtime).

## Ce qui compte comme preuve

L'exemple M1 vérifiable contre §3.2 ; le tableau M2 listant
exactement les 6 axes avec les 2 points de calibration `ν_k` nommés ;
la note M3 citant `φ(i,c)` et sa borne `[1, φ_max]`.

## Ce qui NE compte PAS comme preuve

Un 7e axe inventé, une valeur intermédiaire de `ν_k` inventée, ou une
interprétation d'entropie inversée.

`READY_FOR_FREK_PROOF = FALSE`. Seule une certification interne
Academy (`CVE07.SKILL.*`) est en jeu.

## Réservation Skill ID

`CVE07.SKILL.ENTROPY_LITERACY`, `CVE07.SKILL.SIX_AXIS_LITERACY`,
`CVE07.SKILL.VELOCITY_FACTOR` — réservés dans
`70_EVIDENCE/EVIDENCE_ARCHITECTURE.md`.
