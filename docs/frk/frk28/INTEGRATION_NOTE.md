# FRK-28 — Integration Academy Package Note

## Réel vs. supposé

**Réel :** `backend/services/events.py` existe et alimente
`academy.certification.passed` — pub/sub interne en mémoire, jamais un
registre de provenance.

**Supposé :** `FRK28.SKILL.*` réel dans le runtime de cette Academy —
inexistant (`NO_RUNTIME_BINDING`). Tout registre de provenance CVLN
réel — jamais accordé (`CAPABILITY_NOT_IMPLEMENTED`).

## Dépendances

`FREK_01_75_RECONCILIATION.md`, `backend/services/events.py`
(contre-exemple cité, jamais présenté comme implémentation du sujet).

## Ce qu'une future intégration exigerait

1. Un stockage persistant réellement append-only (pas seulement une
   convention côté application).
2. Un mécanisme de chaînage vérifiable entre événements successifs.
3. Un correcteur humain évaluant un vrai registre construit —
   inexistant aujourd'hui, ce corpus est markdown seul.

## Status

`STATUS = PACKAGE_COMPLETE` — référentiel, banques N1/N2, assessment
+ rubric, evidence model, 3 guides, cette note d'intégration existent
tous, deepened this pass. `FULLY_COMPLETE` non déclaré — requiert un
passage réel vérifié par un humain.
