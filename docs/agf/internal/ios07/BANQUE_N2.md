# IOS-07 — Banque N2 (cas appliqués)

## Cas 1 — Littératie du bus d'événements réel

Le candidat décrit le fonctionnement réel d'`events.py` (en-process,
pub/sub) sans inventer de propriété distribuée ou de garantie de
durabilité absente du code réel.

**Critère éliminatoire :** décrire `events.py` comme un système
distribué ou durable.

## Cas 2 — Frontière avec `Cvln-ios-v.1`

Le candidat doit expliquer pourquoi le corpus de gouvernance de
`Cvln-ios-v.1` (self-déclaré non `DEPLOYED_RUNTIME`) ne peut jamais
être présenté comme ce que `events.py` implémente.

**Critère éliminatoire :** affirmer un câblage entre `events.py` et le
corpus `Cvln-ios-v.1`.
