# FRK-16 — Evidence Model

`READY_FOR_FREK_PROOF = FALSE`.

## Chaîne de preuve

Lecture d'état d'ancrage annotée + note double-frontière (légale,
FREK) + évaluation honnête de la limite de clé → correcteur → (jury si
2.0–2.5) → `FRK16.SKILL.NOTARY_EXTERNAL_ANCHORING.L1` (réservé).

## Ce qui compte comme preuve

Une lecture correcte d'un état d'ancrage réel (`pending`/`confirmed`/
`offline`/`unavailable`) ; les deux frontières obligatoires explicites
et distinctes ; une évaluation honnête de la limite de clé non
chiffrée, sans la minimiser ni l'exagérer.

## Ce qui NE compte PAS comme preuve

Toute affirmation d'un effet légal réel ; toute présentation de ce
système comme une capacité FREK/`frek_core.py` ; toute minimisation ou
exagération de la limite documentée.

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
