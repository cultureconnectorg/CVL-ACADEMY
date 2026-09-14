# Master Assessment Architecture

```
Consolidation des systèmes N1/N2/A01/Rubrics des 5 formations —
vérification de cohérence transversale, pas de nouveau contenu.
```

## Vue `KNOWLEDGE → APPLICATION → DECISION → PROFESSIONAL_EVIDENCE → CERTIFICATION`

| Niveau | Instrument | Ce qu'il teste | Volume total (KLT-01→05) |
|---|---|---|---|
| `KNOWLEDGE` | Banque N1 | Notions, responsabilités, limites, publics, éthique, méthode, reconnaissance de situation, lecture de contexte | 66 questions |
| `APPLICATION` / `DECISION` | Évaluations N2 | Situations dégradées à arbitrer, pas de récitation | 30 évaluations |
| `PROFESSIONAL_EVIDENCE` | Registre de preuves (module terminal) | Livrables réels de tous les modules, source/provenance/consentement documentés | 5 registres (un par formation) |
| `CERTIFICATION` | `KLTxx-A01` + `RUBRIC.md` | Articulation complète des compétences sous contrainte réelle | 5 assessments certificatifs |

## Progressivité de la difficulté — vérifiée, pas supposée

Chaque formation suit la même monotonie `N1 → N2 → N3` sans exception —
vérifié dans les 5 `00_*BLUEPRINTS.md` ("vérification de cohérence
transversale") :

| KLT | N1 (modules) | N2 (modules) | N2/N3 (modules) | N3 terminal |
|---|---|---|---|---|
| `KLT-01` | M01, M02 | M04-M09 | M10 | M11 |
| `KLT-02` | M01-M02 | M03-M08 | M09-M10 | M11 |
| `KLT-03` | M01-M05 | M06-M09 | M10 | M12 |
| `KLT-04` | M01-M02, M05-M07 | M03-M04, M08-M12 | M13 | M14 |
| `KLT-05` | M01-M02 | M03-M08 | M10 | M11 |

## Absence de duplication excessive — vérifiée par échantillon

Comparaison des N2 des 5 formations : aucune situation d'évaluation
n'est répétée à l'identique d'une formation à l'autre — chaque N2 est
ancrée dans l'objet propre de sa formation (ex. `KLT-01`/`E-N2-02`
arbitre une tension en atelier de médiation ; `KLT-05`/`E-N2-03` arbitre
la présentation d'une preuve simulée comme réelle — même famille de
rigueur, objets disjoints).

## Frontières entre métiers — testées explicitement dans les N2

Plusieurs N2 testent *spécifiquement* le respect des limites de rôle
(`ROLE_BOUNDARIES`), pas seulement la compétence métier :

| KLT | Évaluation | Ce qu'elle teste |
|---|---|---|
| `KLT-01` | `E-N2-05` | Refus de signer un accord institutionnel (renvoi vers `KLT-03`) |
| `KLT-02` | `E-N2-05` | Refus de négocier seul avec la DAC (renvoi vers `KLT-03`) |
| `KLT-03` | `E-N2-03` | Refus d'engager au-delà du mandat de négociation (renvoi CA/`KLT-04`) |
| `KLT-05` | `E-N2-02` | Refus de modifier les droits d'un autre compte (dépassement de rôle) |

**Verdict** : la frontière entre métiers n'est pas seulement déclarée
dans les référentiels — elle est **testée** dans au moins 4 des 5
formations. `KLT-04` n'a pas d'équivalent direct dans ses N2 actuelles
— ses critères éliminatoires de `RUBRIC.md` (positionnement dans les
limites du rôle) couvrent cette exigence au niveau terminal plutôt qu'en
N2.

## Conditions de réussite et critères éliminatoires — cohérence vérifiée

Les 5 `RUBRIC.md` partagent la même échelle (0-4, seuils observables,
convention FMS Rubric Master reprise) et le même principe : 3 à 4
critères éliminatoires par formation, jamais plus, jamais moins d'un
critère dédié au respect des limites du rôle.

| KLT | Nb critères | Nb éliminatoires | Critère éliminatoire propre à la formation |
|---|---|---|---|
| `KLT-01` | 10 | 3 (3, 6, 8) | — |
| `KLT-02` | 10 | 3 (3, 6, 9) | — |
| `KLT-03` | 10 | 3 (3, 7, 9) | — |
| `KLT-04` | 10 | 4 (3, 6, 8, 9) | — |
| `KLT-05` | 10 | 4 (2, 4, 8, 10) | Critère 10 : rappel explicite `OPERATOR_AUTHORIZATION` — le seul critère de tout le corpus qui porte sur la formulation du dossier plutôt que sur son contenu métier |

## Preuves nécessaires — cohérence du principe, pas du contenu

Les 5 formations exigent, sans exception, qu'aucune donnée non
observée ne soit présentée comme un fait (`NO_FAKE_OBSERVATORY` et ses
déclinaisons `KLT-02`/`03`/`05`), et qu'un consentement soit documenté
avant toute collecte de données personnelles sensibles (`KLT-01`/M09,
seule formation du corpus à traiter une interview de mémoire orale).
