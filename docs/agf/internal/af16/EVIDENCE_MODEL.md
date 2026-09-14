# AF-16 — Evidence Model

`READY_FOR_FREK_PROOF = FALSE` (non applicable — ce domaine n'utilise
pas le mécanisme de preuve FREK).

## Chaîne de preuve

- Réservation d'ID : `AF16.SKILL.AGENT_FACTORY_OPERATOR.L1` — réservé,
  non émis.
- Grounding réel : `backend/services/agent_factory.py`
  (`chat_reply()`, `mentor_reply()`).
- Contexte de marché cité, jamais substrat opérant :
  `frekcore/CVLNAgentfactory` (225 fichiers, ADL, gates, event bus).
- Aucun chemin d'éligibilité mission — aucune intégration observée à
  opérer.

## Ce que cette chaîne ne prouve pas

Elle ne prouve pas que cette Academy dispose d'un registre d'agents,
d'un système de mission/détachement, d'un mécanisme de rollback, ou
d'une intégration au vrai `CVLNAgentfactory`. Le shim réel se limite
strictement à deux fonctions de transport de chat.

## Pourquoi aucune preuve mission-éligible aujourd'hui

Aucune intégration observée n'existe entre `agent_factory.py` et un
quelconque système d'agents opérationnel — la certification AF-16
porte sur la littératie de ce shim narrow, pas sur une preuve
d'exécution mission vérifiable.

## Conditions d'une future preuve

1. Un vrai passage vérifié par un correcteur humain sur les banques
   N1/N2.
2. Si un jour ce shim évoluait vers un registre multi-persona ou une
   intégration réelle avec `CVLNAgentfactory`, une nouvelle formation
   ou une révision explicite documenterait ce nouvel état — jamais une
   extension silencieuse du périmètre actuel d'AF-16.
