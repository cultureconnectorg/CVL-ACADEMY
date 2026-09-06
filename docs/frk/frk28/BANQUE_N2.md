# FRK-28 — Banque N2 (cas appliqués)

## Cas 1 — Conception d'un registre de provenance

Le candidat conçoit un registre d'événements de provenance append-only
et horodaté pour une chaîne d'objets culturels, en s'appuyant sur les
principes d'architecture événementielle marché-générale.

**Critère éliminatoire :** proposer un registre mutable (événements
modifiables après écriture).

## Cas 2 — Frontière `events.py`

Le candidat doit expliquer par écrit pourquoi `events.py`
(`academy.certification.passed`) ne peut pas servir de fondation à un
registre de provenance sans réécriture complète (persistance,
append-only, chaînage).

**Critère éliminatoire :** présenter `events.py` comme un registre de
provenance existant.
