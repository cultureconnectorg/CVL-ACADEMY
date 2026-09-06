# FRK-20 — Evidence Model

`READY_FOR_FREK_PROOF = FALSE`.

## Chaîne de preuve

- Réservation d'ID : `FRK20.SKILL.OFFLINE_VERIFICATION.L1` — réservé,
  non émis.
- Grounding réel : `is_remote_enabled()` (`frek_core.py`) est un
  simple booléen de disponibilité réseau (`bool(FREK_CORE_BASE_URL)`),
  jamais une vérification cryptographique offline — cité comme
  contre-exemple, pas comme implémentation du sujet.
- Mapping `VALID_SIGNALS` : aucun aujourd'hui.
