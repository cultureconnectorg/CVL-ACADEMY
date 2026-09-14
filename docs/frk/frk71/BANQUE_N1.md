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
5. Que signifie précisément `NOT_PRODUCTION_INTEGRATED` — pourquoi
   l'absence de lien à un FREKCORE en production (y compris
   `frek_core.py`) ne remet-elle pas en cause la classification
   `ARCHITECTURE_LEVEL_2` ?
6. En quoi la présence d'un corpus interne cohérent (5 documents réels)
   distingue-t-elle FREK v3 d'une simple idée non documentée ?
7. Pourquoi `NEEDS_FOUNDER_DECISION = 0` est-il déclaré clos pour cette
   formation spécifiquement, alors que d'autres formations FRK
   restent en attente d'arbitrage produit ?
8. Un candidat affirme que « l'architecture verrouillée équivaut à une
   preuve d'ingénierie ». Pourquoi cette équivalence est-elle fausse ?

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
5. `NOT_PRODUCTION_INTEGRATED` signifie qu'aucun lien de production
   n'existe encore — un statut d'intégration distinct de celui de
   maturité architecturale ; l'architecture peut rester verrouillée
   (Level 2) même sans intégration, ce sont deux axes différents.
6. Un corpus interne cohérent démontre un travail de conception réel,
   documenté et vérifié par dépôt — au-delà d'une simple idée non
   formalisée, ce qui justifie la classification Level 2 plutôt
   que Level 1 (Concept, dépassé).
7. Parce que la maturité de FREK v3 a été vérifiée par dépôt cette
   session (`SOURCE_OBSERVED`, commit précis cité) — contrairement à
   d'autres sujets où l'existence même du produit reste incertaine ou
   en attente d'une décision produit du Founder.
8. Une architecture verrouillée conceptuellement ne constitue pas une
   preuve d'ingénierie — il manque le RTL, les timings exacts et des
   résultats expérimentaux ; verrouiller un concept et le prouver en
   matériel sont deux étapes distinctes de l'échelle.
