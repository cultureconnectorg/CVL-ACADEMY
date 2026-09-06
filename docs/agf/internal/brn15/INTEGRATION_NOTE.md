# BRN-15 — Integration Academy Package Note

**Réel :** `backend/certification/service.py:140` émet
`academy.certification.passed` via `backend/services/events.py`,
relayé par `subscribers.py` vers `/academy/certification-passed`.
**Supposé :** `BRN15.SKILL.*` réel — inexistant au-delà de la
littératie de ce touchpoint unique ; aucun câblage à `/brain/ask`
(`MetaCVLN`).

## Dépendances

`AGENT_FACTORY_IOS_BRAIN_CMD_LAURENTIA_RECONCILIATION.md`,
`docs/agf/internal/ios07/REFERENTIAL.md` (prérequis, même mécanisme),
`docs/kor/kor12/REFERENTIAL.md` (langage de frontière repris verbatim),
`docs/frk/frk58/`, `frk60/REFERENTIAL.md` (convergence).

## Status

`STATUS = PACKAGE_COMPLETE` — package complet construit cette passe.
`FULLY_COMPLETE` requiert un passage réel vérifié par un humain.
