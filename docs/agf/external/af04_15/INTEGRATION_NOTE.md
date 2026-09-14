# AF-04→15 — Integration Academy Package Note

## Réel vs. supposé

**Réel :** `agent_factory.py` = simple transport de chat à une
persona (`chat_reply()`/`mentor_reply()`) — aucune des 12 disciplines
(outils, mémoire, multi-agent, orchestration, HITL, évaluation,
observabilité, sécurité, sûreté, fiabilité, gouvernance, opérations
production) n'y est implémentée.

**Réel, mais externe et non câblé :** le vrai `CVLNAgentfactory`
externe (`frekcore/`, 225 fichiers, ~143 routes, Agent Definition
Language v1/v2, cycle de vie à 7 étapes) — cité comme preuve d'ampleur
réelle pour certaines de ces disciplines dans l'écosystème, jamais
comme ce que cette Academy opère.

**Supposé :** `AF0415.SKILL.*` réel — inexistant pour chacune des 12
disciplines côté CVLN, quelle que soit la formulation (état actuel ou
intention future).

## Dépendances

`AGENT_FACTORY_IOS_BRAIN_CMD_LAURENTIA_RECONCILIATION.md`,
`backend/services/agent_factory.py` (contre-exemple cité
systématiquement), `docs/agf/internal/af17/REFERENTIAL.md` (le vrai
client/persona unique, pour contraste), `docs/agf/external/af01_03/
REFERENTIAL.md` (frontière voisine — persona-as-data, une discipline
réellement illustrée).

## Ce qu'une future évolution exigerait

1. Une décision produit explicite avant toute implémentation réelle de
   l'une des 12 disciplines — hors périmètre de cette formation
   aujourd'hui.
2. Une nouvelle formation ou une révision explicite documentant le
   nouvel état, jamais une extension silencieuse du périmètre actuel.
3. Un correcteur humain réévaluant la formation à la lumière du
   nouveau périmètre, si celui-ci se matérialisait.

## Status

`STATUS = PACKAGE_COMPLETE` — package complet construit cette passe,
couvrant les 12 lignes AF-04→15, deepened. `FULLY_COMPLETE` requiert un
passage réel vérifié par un humain.
