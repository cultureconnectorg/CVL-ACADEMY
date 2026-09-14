# BRN-15 — Banque N2 (cas appliqués)

## Cas 1 — Trace complète de l'événement

Le candidat retrace le chemin complet de `academy.certification.passed`
(émission, bus, relais) en citant les fichiers réels précis, sans
inventer d'étape supplémentaire.

**Attendu :** `backend/certification/service.py:140` → émission via
`backend/services/events.py` (pub/sub en-process) → relais par
`subscribers.py` → route `/academy/certification-passed`. Aucune étape
d'analyse, d'enrichissement, ou de scoring intermédiaire.

**Critère éliminatoire :** inventer une étape de traitement (analyse,
enrichissement contextuel) absente du code réel.

## Cas 2 — Frontière `/brain/ask`

Le candidat doit expliquer pourquoi `/brain/ask` de `MetaCVLN` ne peut
jamais être présenté comme la destination de cet événement.

**Attendu :** `/brain/ask` est une vraie route d'interface Brain dans
un produit externe (`metacvln-spec/MetaCVLN`), citée uniquement comme
preuve que le concept de "Brain CVLN" existe dans l'écosystème — jamais
comme le point d'arrivée réel de `academy.certification.passed`, qui
s'arrête à `/academy/certification-passed` dans cette Academy.

**Critère éliminatoire :** affirmer un câblage entre l'événement et
`/brain/ask`.

## Cas 3 — Un candidat propose une architecture d'intégration

Un candidat, invité à documenter une future intégration entre cette
Academy et un vrai "Brain CVLN", produit un schéma où
`academy.certification.passed` est directement consommé par
`/brain/ask` pour produire une recommandation pédagogique en retour.

Le candidat doit d'abord classer honnêtement ce schéma : est-ce un état
actuel du système, ou une proposition hypothétique de travail futur ?
Il doit ensuite documenter, séparément, ce que cette intégration
exigerait réellement (un vrai câblage `registry.py`-style, un contrat
d'API entre les deux systèmes, une décision produit) sans jamais
présenter le schéma comme une capacité déjà existante.

**Attendu :** le candidat qualifie explicitement le schéma de
proposition hypothétique (`NO_RUNTIME_BINDING` aujourd'hui), et sépare
clairement la description du réel (le touchpoint unique existant) de
la description de l'hypothétique (l'intégration proposée).

**Critère éliminatoire :** présenter le schéma proposé comme une
description de l'état actuel du système, ou affirmer que le travail de
câblage est déjà fait ou en cours.
