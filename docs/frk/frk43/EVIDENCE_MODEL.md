# FRK-43 — Evidence Model

`READY_FOR_FREK_PROOF = FALSE`.

## Chaîne de preuve

Mécanisme store-and-forward annoté (persistance, backoff, dead-letter)
+ trace de comportement face à une panne longue durée → correcteur →
(jury si 2.0–2.5) → `FRK43.SKILL.STORE_AND_FORWARD.L1` (réservé).

## Ce qui compte comme preuve

Un mécanisme avec persistance locale réelle, backoff progressif
(ancré dans le calendrier `[30s, 2m, 10m, 1h, 6h]` de Good Mood) et
dead-letter ; une citation correcte de Good Mood comme illustration
seulement.

## Ce qui NE compte PAS comme preuve

Un mécanisme sans persistance ou à backoff fixe ; l'absence de
dead-letter ; toute présentation de l'outbox de Good Mood comme
infrastructure FREK.

- Réservation d'ID : `FRK43.SKILL.STORE_AND_FORWARD.L1` — réservé,
  non émis.
- Exemple travaillé réel : `frek_id_outbox`/`frek_outbox` (Good Mood,
  `docs/gmd/gmd31`/`gmd32`), calendrier `[30s, 2m, 10m, 1h, 6h]` —
  cité comme illustration, jamais comme infrastructure FREK.
- Base pour FRK-44 (récupération/synchronisation) — réutilisé par
  référence.
- Mapping `VALID_SIGNALS` : aucun aujourd'hui.
