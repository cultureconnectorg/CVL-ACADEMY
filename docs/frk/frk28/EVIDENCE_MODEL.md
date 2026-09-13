# FRK-28 — Evidence Model

`READY_FOR_FREK_PROOF = FALSE`.

## Chaîne de preuve

Registre de provenance conçu (append-only, chaîné) + note de frontière
`events.py` → correcteur → (jury si 2.0–2.5) →
`FRK28.SKILL.EVENT_PROVENANCE_REGISTRY.L1` (réservé).

## Ce qui compte comme preuve

Un registre techniquement append-only et chaîné (pas seulement
documenté comme tel) ; une note distinguant précisément `events.py`
(bus pub/sub en mémoire) d'un registre de provenance persistant ; un
mécanisme de correction par événement compensatoire.

## Ce qui NE compte PAS comme preuve

Un registre mutable ou append-only par convention seule (sans
mécanisme technique) ; toute présentation de `events.py` comme un
registre de provenance existant ; une correction par réécriture ou
suppression d'un événement.

- Réservation d'ID : `FRK28.SKILL.EVENT_PROVENANCE_REGISTRY.L1` —
  réservé, non émis.
- Contre-exemple cité : `backend/services/events.py` (réel, pub/sub
  en mémoire, `academy.certification.passed`) — jamais présenté comme
  un registre de provenance.
- Mapping `VALID_SIGNALS` : aucun aujourd'hui.
