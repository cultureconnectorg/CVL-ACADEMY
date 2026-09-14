# FRK-54 — Evidence Model

`READY_FOR_FREK_PROOF = FALSE`.

## Chaîne de preuve

Contrat d'intégration webhook annoté (versionné, compatibilité
ascendante) + note de frontière `events.py` → correcteur → (jury si
2.0–2.5) → `FRK54.SKILL.EVENT_BUS_WEBHOOK_CONTRACTS.L1` (réservé).

## Ce qui compte comme preuve

Un contrat d'intégration webhook versionné, avec une stratégie de
compatibilité ascendante réelle ; une note distinguant précisément
bus interne et webhook externe, citant `events.py` uniquement comme
illustration.

## Ce qui NE compte PAS comme preuve

Toute présentation d'`events.py` comme infrastructure webhook ou FREK ;
toute affirmation qu'il notifie déjà des systèmes externes ; un
contrat évoluant sans mécanisme de compatibilité ascendante.

- Réservation d'ID : `FRK54.SKILL.EVENT_BUS_WEBHOOK_CONTRACTS.L1` —
  réservé, non émis.
- Exemple travaillé réel : `backend/services/events.py` (pub/sub
  en-process, `academy.certification.passed`) — cité comme
  illustration, jamais comme infrastructure FREK ou surface webhook.
- Base pour FRK-55 (standards transversaux) — réutilisé par référence.
- Mapping `VALID_SIGNALS` : aucun aujourd'hui.
