# FRK-54 — Banque N2 (cas appliqués)

## Cas 1 — Conception d'un contrat d'intégration webhook

Le candidat conçoit un schéma d'événement webhook versionné pour un
système générique, en citant `events.py` comme illustration du patron
pub/sub sous-jacent.

**Critère éliminatoire :** présenter `events.py` comme une
infrastructure webhook FREK.

## Cas 2 — Frontière `events.py`

Le candidat doit expliquer pourquoi `academy.certification.passed`
(événement réel émis par `events.py`) ne peut aujourd'hui atteindre
aucun système externe sans construire une surface webhook
supplémentaire.

**Critère éliminatoire :** affirmer que `events.py` notifie déjà des
systèmes externes.
