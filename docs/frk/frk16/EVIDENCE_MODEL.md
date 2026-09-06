# FRK-16 — Evidence Model

`READY_FOR_FREK_PROOF = FALSE`.

## Chaîne de preuve

- Réservation d'ID : `FRK16.SKILL.NOTARY_EXTERNAL_ANCHORING.L1` —
  réservé, non émis.
- Grounding réel : MetaCVLN `backend/server.py`
  (`/notarizations`, `/public/notarizations`, Ed25519, `IMPLEMENTED`
  per `COMPONENT-MATRIX.md`) ; ancrage externe OpenTimestamps
  (`proof/EXTERNAL-ANCHORING.md`, `D-020`, endpoints
  `/api/docs/anchor/*`, artefacts réels `audit/anchors/*.ots`).
- Frontière permanente et double : (1) jamais un notariat légal
  (`legal_effect = "none"`, Décision D-007) ; (2) jamais
  `frek_core.py`/`issue_proof()` (FRK-13) — systèmes distincts, jamais
  fusionnés.
- Limite honnêtement portée : clé de notaire non chiffrée au repos
  (finding documenté dans le corpus source, jamais minimisé).
- Mapping `VALID_SIGNALS` : aucun aujourd'hui.
