# FRK-71 — Banque N1 (formatif)

Réserve `FRK71.SKILL.*`.

1. Cite verbatim les trois niveaux de l'échelle de maturité de FREK v3
   telle que définie par son propre corpus (`FREK_V3_Architecture_
   Review_Final.md` et alliés).
2. Pourquoi FREK v3 est-il classé `ARCHITECTURE_LEVEL_2` et non
   `Level 3 (Engineering)` — qu'est-ce qui manque précisément ?
3. Le FPGA est nommé par le corpus lui-même comme le pont non franchi
   vers le niveau 3 — pourquoi cette précision matérielle est-elle
   déterminante pour classer correctement la maturité ?
4. Pourquoi FRK-71 (frekcoreAout2026, `frek_v3/`) et `frek_core.py`
   (FRK-01/58, Academy) ne doivent-ils jamais être confondus, même s'il
   s'agit potentiellement du même produit à terme ?

## Corrigé indicatif

1. `1. Concept (dépassé) → 2. Architecture (✅ verrouillé) → 3.
   Engineering (⏳ prochaine phase, RTL/bits exacts/résultats
   expérimentaux)`.
2. Il manque le RTL, les timings exacts et des résultats expérimentaux
   — l'architecture est verrouillée conceptuellement, pas encore
   prouvée en ingénierie ni en matériel.
3. Sans franchissement FPGA, aucune preuve matérielle n'existe — la
   classification reste Level 2 tant que ce pont n'est pas traversé.
4. `frek_core.py` est une couche Academy simple (mint/emit/stub) ;
   `frek_v3` est une couche architecturale plus mature du même produit
   éventuel — les confondre fausserait la maturité réelle de chacune.
