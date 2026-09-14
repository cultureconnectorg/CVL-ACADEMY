# AF-17 — Integration Academy Package Note

## Réel vs. supposé

**Réel :** architecture réelle étroite (un client, une persona),
`backend/services/agent_factory.py`.

**Supposé :** `AF17.SKILL.*` réel dans le runtime de cette Academy —
inexistant (`NO_RUNTIME_BINDING`) ; aucune taxonomie de types d'agents,
aucune intégration à `CVLNAgentfactory` — jamais accordée
(`CAPABILITY_NOT_IMPLEMENTED`).

## Dépendances

`AGENT_FACTORY_IOS_BRAIN_CMD_LAURENTIA_RECONCILIATION.md`,
`docs/agf/internal/af16/REFERENTIAL.md` (prérequis, réutilisé par
référence).

## Ce qu'une future intégration exigerait

1. Une entrée `AF17` dans le registre de certification de cette
   Academy.
2. Une surface candidat réelle (ce corpus est markdown seul).
3. Un correcteur humain évaluant une vraie description construite —
   inexistant aujourd'hui.

## Status

`STATUS = PACKAGE_COMPLETE` — package complet construit cette passe.
`FULLY_COMPLETE` requiert un passage réel vérifié par un humain.
