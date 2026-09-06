# FRK-31 — Banque N2 (cas appliqués)

## Cas 1 — Conception d'un vocabulaire d'engagement

Le candidat conçoit un petit schéma de signaux d'affinité/résonance/
cadence pour une plateforme culturelle générique, sans référence à
CVLN.

**Critère éliminatoire :** utiliser les noms `FREK-*` de `VALID_SIGNALS`
pour ce vocabulaire distinct.

## Cas 2 — Frontière obligatoire avec `VALID_SIGNALS`

Le candidat doit expliquer pourquoi appeler
`frek_core.emit_signal(user_id, "AFFINITY")` ne produirait aucun effet
réel (no-op silencieux, car `"AFFINITY"` n'est pas dans
`VALID_SIGNALS`).

**Critère éliminatoire :** affirmer que ce vocabulaire est déjà
implémenté par `frek_core.py`.
