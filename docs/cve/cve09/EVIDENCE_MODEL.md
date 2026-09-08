# CVE-09 — Evidence Model

## Chaîne de preuve

M1 exemple numérique UVC → M2 dérivation écrite reliant les deux
formules → M3 note sur la contrainte de budget fixe → correcteur →
(jury si 2.0–2.5) → `CVE09.SKILL.*` (réservé, non lié au runtime).

## Ce qui compte comme preuve

L'exemple M1 vérifiable contre §5 ; la dérivation M2 montrant
algébriquement l'équivalence des deux formules ; la note M3 citant
`Σ_i UVC_i,c = MD_c` (C1) et son implication (allocation toujours
relative).

## Ce qui NE compte PAS comme preuve

UVC présenté comme valeur absolue, ou une violation de C1 validée
sans être signalée.

`READY_FOR_FREK_PROOF = FALSE`. Seule une certification interne
Academy (`CVE09.SKILL.*`) est en jeu.

## Réservation Skill ID

`CVE09.SKILL.UVC_FORMULA`, `CVE09.SKILL.UNIT_VALUE_DERIVATION`,
`CVE09.SKILL.FIXED_BUDGET_DISCIPLINE` — réservés dans
`70_EVIDENCE/EVIDENCE_ARCHITECTURE.md`.
