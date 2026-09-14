# AF-01, AF-02, AF-03 — AI Agent Engineering Foundations (external/market)

## Grounding

Per `AGENT_FACTORY_IOS_BRAIN_CMD_LAURENTIA_RECONCILIATION.md` :
coverage `PARTIAL (real persona/prompt pattern)`, distinctness
`DISTINCT_PROFESSION each`, action `NEW_EXTERNAL`. Ingénierie d'agent
IA marché-générale, réellement ancrée dans du code réel (le patron
persona-comme-donnée de `ai_assistant.py` est un vrai bon exemple
travaillé).

## Objectives

Un candidat qui complète AF-01→03 sait concevoir les fondamentaux
d'ingénierie de prompt/persona marché-générale, en s'appuyant sur le
patron réel `ASSISTANT_PERSONAS` sans jamais en tirer de conclusion
excessive :

- Enseigner les fondamentaux réels et actuels d'ingénierie d'agent IA
  (conception de prompt/persona, architecture de system prompt,
  définition de rôle d'agent) comme discipline industrielle
  marché-générale.
- Utiliser le vrai patron `ASSISTANT_PERSONAS` de cette Academy
  (`backend/services/ai_assistant.py` — personas étudiant/formateur/
  jury/correcteur comme **données, pas branches de code**) comme
  exemple travaillé authentique et citable d'architecture
  persona-comme-donnée — un vrai bon patron, pas une invention.
- Expliquer précisément pourquoi encoder les personas comme données
  (un dictionnaire de configuration) plutôt que comme branches
  conditionnelles rend le système extensible sans modification de
  code — un vrai principe d'ingénierie, illustré ici sur un cas réel
  et simple, indépendamment de la simplicité globale du système.
- Concevoir des principes d'architecture de system prompt
  indépendants de tout système CVLN : séparation claire des
  instructions de rôle, du contexte dynamique injecté, et des
  contraintes de sortie — un principe général applicable à tout
  système d'agent.
- Ne jamais affirmer que le système de persona de cette Academy
  implique une orchestration multi-agent, un usage d'outils, ou une
  mémoire — ce sont des disciplines séparées (`external/af04_15`), non
  couvertes ici : le système réel n'a qu'une persona opérationnelle
  (`mentor_reply()`).
- Expliquer précisément pourquoi affirmer qu'une conception de persona
  implique nécessairement une orchestration multi-agent serait une
  erreur éliminatoire : cela confondrait deux disciplines à des
  altitudes différentes — la persona définit le rôle d'un agent
  unique, l'orchestration coordonne plusieurs agents entre eux.

## Modules

1. **Fondamentaux de conception de prompt/persona** (marché-général).
2. **Architecture persona-comme-donnée**, travaillée sur le vrai
   patron `ASSISTANT_PERSONAS`.
3. **Discipline de frontière vs. `af04_15`** — les disciplines
   d'ingénierie d'agent plus larges (orchestration, outils, mémoire),
   jamais couvertes ici.

## Assessment

Un exercice de conception de persona utilisant la forme réelle
d'`ASSISTANT_PERSONAS` comme cas travaillé, noté contre la pratique
réelle d'ingénierie d'agent, avec règle éliminatoire sur tout encodage
en branches de code ou toute confusion avec l'orchestration
multi-agent.

## Evidence / mission eligibility

Aucun chemin d'éligibilité mission aujourd'hui.
`AF0103.SKILL.AGENT_ENGINEERING_FOUNDATIONS.L1` réservé une fois
approfondi.

## Status

`STATUS = PACKAGE_COMPLETE` — référentiel, banques N1/N2, assessment +
rubric, evidence model, 3 guides, cette note d'intégration existent
tous, deepened this pass. `FULLY_COMPLETE` non déclaré — requiert un
passage réel vérifié par un humain.
