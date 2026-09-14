# AF-04→15 — Evidence Model

`READY_FOR_FREK_PROOF = FALSE` (non applicable à ce domaine).

## Chaîne de preuve

- Réservation d'ID : `AF0415.SKILL.AGENT_ENGINEERING_DISCIPLINES.L1`
  — réservé, non émis, couvrant les 12 rangées AF-04→15.
- Grounding réel : `backend/services/agent_factory.py`
  (`chat_reply()`/`mentor_reply()` seuls) — cité comme contre-exemple
  systématique pour chacune des 12 disciplines, jamais comme
  implémentation.
- Mapping capacité : aucune des 12 disciplines n'est implémentée par
  un système CVLN observé.
- Contexte de marché cité, jamais substrat opérant : le vrai
  `CVLNAgentfactory` externe (`frekcore/`, 225 fichiers, ~143 routes,
  Agent Definition Language v1/v2, cycle de vie à 7 étapes) — preuve
  que certaines de ces disciplines existent à l'échelle ailleurs dans
  l'écosystème, jamais présenté comme opéré par cette Academy.

## Ce que cette chaîne ne prouve pas

Elle ne prouve pas qu'`agent_factory.py` ou tout autre système de
cette Academy implémente l'usage d'outils, la mémoire d'agent, la
coordination multi-agent, l'orchestration, le HITL, l'évaluation,
l'observabilité, la sécurité, la sûreté, la fiabilité, la gouvernance,
ou les opérations de production pour agents. Elle ne prouve pas non
plus qu'un câblage existe entre cette Academy et le vrai
`CVLNAgentfactory` externe.

## Pourquoi aucune preuve mission-éligible aujourd'hui

Ce cluster certifie une littératie de marché pure — aucune des 12
disciplines n'a de trace d'implémentation réelle dans cette Academy,
donc aucun chemin FREK n'existe pour ce patron.

## Conditions d'une future preuve

1. Un vrai passage vérifié par un correcteur humain sur les banques
   N1/N2, pour au moins une discipline choisie en profondeur.
2. Si un jour l'une de ces 12 disciplines était réellement implémentée
   dans cette Academy, une nouvelle formation ou une révision explicite
   documenterait ce nouvel état — jamais une extension silencieuse du
   périmètre actuel de AF-04→15.
