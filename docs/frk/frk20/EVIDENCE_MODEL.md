# FRK-20 — Evidence Model

`READY_FOR_FREK_PROOF = FALSE`.

## Chaîne de preuve

Flux offline-first annoté (vérification locale, synchronisation
différée) → note de gap CVLN sur `is_remote_enabled()` → correcteur →
(jury si 2.0–2.5) → `FRK20.SKILL.OFFLINE_VERIFICATION.L1` (réservé).

## Ce qui compte comme preuve

Un flux où la garantie cryptographique est établie entièrement en
local avant toute synchronisation ; la note de gap confirmant
précisément la nature de `is_remote_enabled()`.

## Ce qui NE compte PAS comme preuve

Un flux où la garantie de preuve dépend d'un appel réseau synchrone ;
toute confusion entre `is_remote_enabled()` et une vérification
cryptographique offline.

- Réservation d'ID : `FRK20.SKILL.OFFLINE_VERIFICATION.L1` — réservé,
  non émis.
- Grounding réel : `is_remote_enabled()` (`frek_core.py`) est un
  simple booléen de disponibilité réseau (`bool(FREK_CORE_BASE_URL)`),
  jamais une vérification cryptographique offline — cité comme
  contre-exemple, pas comme implémentation du sujet.
- Mapping `VALID_SIGNALS` : aucun aujourd'hui.
