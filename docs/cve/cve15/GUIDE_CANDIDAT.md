# CVE-15 — Guide Candidat

## Avant de commencer

Prérequis : `CVE-01`, `CVE-09`, `CVE-14`.

## Ce que tu dois savoir faire

Nommer et expliquer précisément les 8 contraintes C1→C8, expliquer le
pare-feu prévision/allocation (C8), et la discipline de publication de
gouvernance (C7).

## Comment réviser

1. Lis `KORA_CVE_Specification_Mathematique_v1.0.md` §6 toi-même,
   contrainte par contrainte.
2. Fais les 13 questions de `BANQUE_N1.md`.
3. Traite les 3 cas de `BANQUE_N2.md`.

## Piège le plus fréquent

Confondre C4 (plancher de diversité du catalogue) avec C5 (neutralité
culturelle individuelle) — deux garanties distinctes, à des échelles
différentes.

## Règle absolue

Ne valide jamais un ajustement silencieux de `θ` (viole C7), et ne
valide jamais l'usage de `Ŷ` dans l'allocation (viole C8) —
élimination automatique.
