# FRK-71 — Integration Academy Package Note

## Réel vs. supposé

**Réel :** `frekcoreAout2026` (`frek_v3/`), commit
`fb272f1d491b09a6d068fb3f6c9c75d407bb0626`, `ARCHITECTURE_LEVEL_2`
(`SOURCE_OBSERVED`), FPGA nommé comme pont non franchi vers le
niveau 3.

**Supposé :** `FRK71.SKILL.*` réel dans le runtime de cette Academy —
inexistant au-delà de la littératie architecturale
(`NO_RUNTIME_BINDING`). Tout niveau 3 (ingénierie/matériel prouvé) —
jamais accordé (`CAPABILITY_NOT_IMPLEMENTED`).

## Dépendances

`FREK_01_75_RECONCILIATION.md`, `REPO_REGISTRY.md` (G5/FD closure),
`docs/frk/frk01/REFERENTIAL.md` (contexte, frontière jamais fusionnée),
`docs/frk/frk72/`,`frk73/`,`frk74/`,`frk75/REFERENTIAL.md`
(spécialisations avales).

## Ce qu'une future intégration exigerait

1. Un franchissement réel du pont FPGA (RTL, timings exacts, résultats
   expérimentaux) — inexistant aujourd'hui.
2. Une intégration production réelle avec un FREKCORE vivant — non
   observée, y compris `frek_core.py` de cette Academy.
3. Un correcteur humain évaluant une vraie classification construite —
   ce corpus est markdown seul.

## Status

`STATUS = PACKAGE_COMPLETE` — package complet construit cette passe.
`FULLY_COMPLETE` requiert un passage réel vérifié par un humain.
