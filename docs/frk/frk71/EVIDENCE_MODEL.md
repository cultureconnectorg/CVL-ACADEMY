# FRK-71 — Evidence Model

`READY_FOR_FREK_PROOF = FALSE`.

## Chaîne de preuve

Classification de maturité annotée (échelle 3 niveaux, FPGA comme
pont non franchi) + note de frontière `frek_core.py` + distinction
maturité/intégration → correcteur → (jury si 2.0–2.5) →
`FRK71.SKILL.FREK_V3_ARCHITECTURE.L1` (réservé).

## Ce qui compte comme preuve

Une classification correcte contre l'échelle propre du corpus, sans
inflation ; une frontière explicite avec `frek_core.py` ; une
distinction correcte entre maturité architecturale et intégration
production.

## Ce qui NE compte PAS comme preuve

Toute validation d'une affirmation de niveau 3 pour FREK v3 ; toute
fusion des deux couches dans une seule évaluation ; toute
rétrogradation de la classification sur la base de la seule absence
d'intégration production.

- Réservation d'ID : `FRK71.SKILL.FREK_V3_ARCHITECTURE.L1` — réservé,
  non émis.
- Grounding réel : `frekcoreAout2026`, commit
  `fb272f1d491b09a6d068fb3f6c9c75d407bb0626`, `frek_v3/` (5 documents
  réels cités), classification `ARCHITECTURE_LEVEL_2` maintenue sans
  inflation.
- Frontière permanente vs. `frek_core.py` (FRK-01/58, Academy).
- Mapping `VALID_SIGNALS` : aucun aujourd'hui.
