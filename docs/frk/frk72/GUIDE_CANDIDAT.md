# FRK-72 — Guide Candidat

## Avant de commencer

Prérequis : FRK-71. Apprends la structure réelle du protocole
d'attestation FREK (283 octets, L0/L1/L2) et la preuve d'ingénierie
qui l'accompagne (vérificateur de référence, 16 tests passants,
ECDSA P-256).

## Ce que tu dois savoir faire

Décrire la structure du protocole sans jamais inventer de champ non
vérifié, distinguer conceptuellement L0/L1/L2, et articuler la
frontière de maturité héritée de FRK-71 (`ARCHITECTURE_LEVEL_2`,
jamais inflaté).

## Comment réviser

1. Relis `docs/frk/frk71/REFERENTIAL.md` (échelle de maturité,
   prérequis).
2. Lis `REFERENTIAL.md` §Objectives et §Modules de cette formation.
3. Fais les 7 questions de `BANQUE_N1.md`.
4. Traite les 3 cas de `BANQUE_N2.md`.

## Piège le plus fréquent

Inventer un champ, un offset, ou une valeur précise non présente dans
la spécification réelle — élimination automatique. Second piège :
affirmer que des tests logiciels passants constituent une preuve
matérielle.

## Règle absolue

`ARCHITECTURE_LEVEL_2` hérité de FRK-71, jamais inflaté vers un statut
matériel prouvé ou une intégration production.
