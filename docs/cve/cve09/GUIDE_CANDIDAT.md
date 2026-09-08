# CVE-09 — Guide Candidat

## Avant de commencer

Prérequis : `CVE-04`, `CVE-05`, `CVE-07`.

## Ce que tu dois savoir faire

Dériver `UVC_i,c` à partir de `CVI_i,c` et `MD_c`, relier
algébriquement `value_UVC,c` à `UVC_i,c`, et expliquer pourquoi C1
rend toute allocation relative, jamais absolue.

## Comment réviser

1. Lis `KORA_CVE_Specification_Mathematique_v1.0.md` §5 et §6 C1
   toi-même.
2. Fais les 6 questions de `BANQUE_N1.md`.
3. Traite les 3 cas de `BANQUE_N2.md`.

## Piège le plus fréquent

Présenter `UVC_i,c` comme une "valeur culturelle intrinsèque" absolue
— c'est toujours une part proportionnelle du total du cycle.

## Règle absolue

Ne présente jamais UVC comme une valeur absolue, et ne valide jamais
une proposition qui violerait la contrainte de budget fixe C1 —
élimination automatique.
