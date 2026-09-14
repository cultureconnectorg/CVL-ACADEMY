# AF-16 — Integration Academy Package Note

## Réel vs. supposé

**Réel :** `backend/services/agent_factory.py` — `chat_reply()`,
`mentor_reply()` (seule persona réelle enregistrée).

**Réel, mais externe et non câblé :** `frekcore/CVLNAgentfactory` (225
fichiers, ~143 routes, ADL, gates, event bus) — système réel et
substantiellement plus sophistiqué, cité comme contexte de marché.

**Supposé :** `AF16.SKILL.*` réel — inexistant au-delà de la
littératie de ce shim ; aucune intégration au vrai
`frekcore/CVLNAgentfactory` ; aucun registre, mission, ou rollback,
quelle que soit la formulation (actuelle ou en cours).

## Dépendances

`AGENT_FACTORY_IOS_BRAIN_CMD_LAURENTIA_RECONCILIATION.md`,
`backend/services/agent_factory.py`, `frekcore/CVLNAgentfactory`
(contexte de marché cité, jamais substrat opérant).

## Ce qu'une future évolution exigerait

1. Une décision produit explicite avant toute construction d'un
   registre multi-persona ou d'une intégration réelle avec
   `CVLNAgentfactory` — hors périmètre de cette formation aujourd'hui.
2. Une nouvelle formation ou une révision explicite documentant le
   nouvel état, jamais une extension silencieuse du périmètre actuel.
3. Un correcteur humain réévaluant la formation à la lumière du
   nouveau périmètre, si celui-ci se matérialisait.

## Status

`STATUS = PACKAGE_COMPLETE` — package complet construit cette passe,
deepened. `FULLY_COMPLETE` requiert un passage réel vérifié par un
humain.
