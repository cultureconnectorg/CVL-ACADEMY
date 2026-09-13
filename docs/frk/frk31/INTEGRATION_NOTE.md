# FRK-31 — Integration Academy Package Note

## Réel vs. supposé

**Réel :** `VALID_SIGNALS` (`frek_core.py`) = 8 valeurs strictes
(`FREK-TIME/WORK/SCORE/LINK/CERT/CONTRIB/SHARE/MISSION`),
`emit_signal()` fait un no-op silencieux sur toute autre valeur.

**Supposé :** `FRK31.SKILL.*` réel dans le runtime de cette Academy —
inexistant ; le vocabulaire affinité/résonance/cadence n'est ni
implémenté ni prévu comme extension de `VALID_SIGNALS`
(`NO_RUNTIME_BINDING`, `CAPABILITY_NOT_IMPLEMENTED`).

## Dépendances

`FREK_01_75_RECONCILIATION.md`, `backend/services/frek_core.py`
(frontière obligatoire et permanente, jamais fusionnée).

## Ce qu'une future intégration exigerait

1. Une entrée `FRK31` dans le registre de certification de cette
   Academy.
2. Un vrai vocabulaire de signaux d'engagement construit et
   instrumenté — inexistant aujourd'hui.
3. Un correcteur humain évaluant un vrai schéma construit — ce corpus
   est markdown seul.

## Status

`STATUS = PACKAGE_COMPLETE` — package complet construit cette passe.
`FULLY_COMPLETE` requiert un passage réel vérifié par un humain.
