# FRK-31 — Integration Academy Package Note

**Réel :** `VALID_SIGNALS` (`frek_core.py`) = 8 valeurs strictes
(`FREK-TIME/WORK/SCORE/LINK/CERT/CONTRIB/SHARE/MISSION`),
`emit_signal()` fait un no-op silencieux sur toute autre valeur.
**Supposé :** `FRK31.SKILL.*` réel — inexistant ; le vocabulaire
affinité/résonance/cadence n'est ni implémenté ni prévu comme
extension de `VALID_SIGNALS`.

## Dépendances

`FREK_01_75_RECONCILIATION.md`, `backend/services/frek_core.py`
(frontière obligatoire et permanente, jamais fusionnée).

## Status

`STATUS = PACKAGE_COMPLETE` — package complet construit cette passe.
`FULLY_COMPLETE` requiert un passage réel vérifié par un humain.
