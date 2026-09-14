# FRK-60 — Integration Academy Package Note

## Réel vs. supposé

**Réel :** `frek_core.py` (client Python interne, appelé en-process,
sans route HTTP ni surface externe) et
`services/integrations/registry.py` (configuration d'intégration
écosystème générique, sans câblage FREK-spécifique réel) —
`CAPABILITY_NOT_IMPLEMENTED` des deux côtés pour toute intégration
FREK↔Intelligence OS/Agent Infrastructure. Leur coexistence dans le
dépôt ne constitue pas une intégration en cours.

**Supposé :** `FRK60.SKILL.*` réel dans le runtime de cette Academy —
inexistant (`NO_RUNTIME_BINDING`). Tout câblage FREK↔Intelligence
OS/Agent Infrastructure réel — jamais accordé
(`CAPABILITY_NOT_IMPLEMENTED`).

## Dépendances

`FREK_01_75_RECONCILIATION.md`, `backend/services/frek_core.py`
(contre-exemple cité, jamais présenté comme implémentation du sujet),
`backend/services/integrations/registry.py` (grounding double-stub
cité, jamais présenté comme fonctionnel).

## Ce qu'une future intégration exigerait

1. Un schéma d'échange défini entre FREK et l'infrastructure d'agents
   (format de message, champs obligatoires, versionnage).
2. Une authentification mutuelle — chaque côté doit pouvoir vérifier
   l'identité de l'autre, pas une simple clé partagée statique.
3. Un contrat d'erreur partagé — codes et sémantique communs aux deux
   systèmes, pour qu'un échec d'un côté soit interprétable de l'autre.

## Status

`STATUS = PACKAGE_COMPLETE` — référentiel, banques N1/N2, assessment
+ rubric, evidence model, 3 guides, cette note d'intégration existent
tous, deepened this pass. `FULLY_COMPLETE` non déclaré — requiert un
passage réel vérifié par un humain.
