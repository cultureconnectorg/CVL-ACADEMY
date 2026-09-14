# FRK-60 — Evidence Model

`READY_FOR_FREK_PROOF = FALSE`.

## Chaîne de preuve

Note d'architecture annotée (exigences d'intégration + analyse
double-stub) → vérification correcteur (absence de toute affirmation
fonctionnelle) → (jury si 2.0–2.5) →
`FRK60.SKILL.FREK_INTELLIGENCE_OS_BRIDGE.L1` (réservé).

## Ce qui compte comme preuve

Une note documentant précisément les exigences d'une future
intégration (schéma d'échange, authentification mutuelle, contrat
d'erreur partagé) sans jamais les présenter comme construites, avec
une analyse correcte et séparée de la nature de chacun des deux
stubs cités.

## Ce qui NE compte PAS comme preuve

Toute affirmation qu'une intégration fonctionnelle existe déjà, côté
FREK ou côté Intelligence OS/Agent Infrastructure ; toute affirmation
qu'un seul des deux stubs suffit ; toute confusion entre la
coexistence des deux artefacts dans le dépôt et un câblage en cours.

- Réservation d'ID : `FRK60.SKILL.FREK_INTELLIGENCE_OS_BRIDGE.L1` —
  réservé, non émis.
- Grounding réel : `frek_core.py` (client Python interne, appelé
  en-process, sans route HTTP ni surface externe) et
  `services/integrations/registry.py` (configuration d'intégration
  écosystème générique, sans câblage FREK-spécifique réel) — les deux
  cités comme stubs, jamais comme implémentation du sujet.
  `CAPABILITY_NOT_IMPLEMENTED` des deux côtés.
- Mapping `VALID_SIGNALS` : aucun aujourd'hui.
