# AF-X-03 — Integration Academy Package Note

## Réel vs. supposé

**Réel :** moteur de compétence/certification de l'Academy
(`docs/kor/`, `70_EVIDENCE/EVIDENCE_ARCHITECTURE.md`) + système de
personas (`ai_assistant.py`) — deux blocs réels, aucun câblage entre
eux vers un concept de qualification d'agent.

**Réel, mais externe et non câblé :** l'ADL de `frekcore/
CVLNAgentfactory` (`AGT-\d{3}`, semver, cycle de vie à 7 étapes) — cité
comme preuve que le concept de qualification d'agent est réel et
mature ailleurs.

**Supposé :** `AFX03.SKILL.*` réel — inexistant ; aucun pont
Skill/Certification × Agent Qualification aujourd'hui, sous quelque
forme que ce soit.

## Dépendances

`AGENT_FACTORY_IOS_BRAIN_CMD_LAURENTIA_RECONCILIATION.md`,
`docs/agf/internal/af16/REFERENTIAL.md`, `docs/agf/internal/af17/
REFERENTIAL.md` (prérequis), `frekcore/CVLNAgentfactory` (ADL réel,
contexte de marché cité).

## Ce qu'une future évolution exigerait

1. Un mapping explicite Skill ID ↔ étape de cycle de vie ADL.
2. Une API de qualification et un mécanisme de validation — aucun des
   deux n'existe aujourd'hui.
3. Une décision produit explicite avant toute construction, et une
   nouvelle formation ou révision documentant le nouvel état — jamais
   une extension silencieuse d'AF-X-03.

## Status

`STATUS = PACKAGE_COMPLETE` — package complet construit cette passe,
deepened. `FULLY_COMPLETE` requiert un passage réel vérifié par un
humain.
