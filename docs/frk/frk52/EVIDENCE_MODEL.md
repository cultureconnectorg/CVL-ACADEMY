# FRK-52 — Evidence Model

`READY_FOR_FREK_PROOF = FALSE`.

## Chaîne de preuve

Design d'API annoté (versionnage, gestion d'erreur) → note de gap
CVLN sur `frek_core.py` → correcteur → (jury si 2.0–2.5) →
`FRK52.SKILL.API_ENGINEERING.L1` (réservé).

## Ce qui compte comme preuve

Un design d'API avec versionnage explicite et gestion d'erreur
cohérente (codes sémantiques + corps structuré) ; la note de gap
confirmant précisément la nature interne de `frek_core.py`.

## Ce qui NE compte PAS comme preuve

Une API sans stratégie de versionnage ; toute affirmation que
`frek_core.py` expose une API publique.

- Réservation d'ID : `FRK52.SKILL.API_ENGINEERING.L1` — réservé, non
  émis.
- Grounding réel : `frek_core.py` = `FrekCoreClient`, client Python
  interne appelé en-process, aucune route HTTP propre — cité comme
  contre-exemple, jamais comme implémentation du sujet.
- Base pour FRK-53 (SDK engineering) — réutilisé par référence.
- Mapping `VALID_SIGNALS` : aucun aujourd'hui.
