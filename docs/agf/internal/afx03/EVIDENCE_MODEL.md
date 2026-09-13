# AF-X-03 — Evidence Model

`READY_FOR_FREK_PROOF = FALSE` (non applicable à ce domaine).

## Chaîne de preuve

- Réservation d'ID : `AFX03.SKILL.SKILL_AGENT_QUALIFICATION_BRIDGE.L1`
  — réservé, non émis.
- Grounding réel double : moteur de compétence/certification de
  l'Academy (`docs/kor/`, `70_EVIDENCE/EVIDENCE_ARCHITECTURE.md`) +
  système de personas (`ai_assistant.py`).
- Contexte de marché cité, jamais substrat opérant : ADL réel de
  `frekcore/CVLNAgentfactory`.
- Prérequis : AF-16, AF-17.

## Ce que cette chaîne ne prouve pas

Elle ne prouve pas qu'un pont Skill/Certification × Agent Qualification
existe, même partiellement, dans cette Academy. Les deux blocs de
construction cités sont réels et vérifiables séparément, mais aucun
câblage observé ne les relie l'un à l'autre.

## Pourquoi aucune preuve mission-éligible aujourd'hui

Aucun chemin FREK n'existe pour ce patron — la certification AF-X-03
porte sur la conceptualisation documentée du pont, pas sur une preuve
d'exécution vérifiable par le runtime.

## Conditions d'une future preuve

1. Un vrai passage vérifié par un correcteur humain sur les banques
   N1/N2, avec vérification de la maîtrise des prérequis AF-16/AF-17.
2. Une décision produit explicite avant toute construction réelle du
   pont — hors périmètre de cette formation aujourd'hui.
3. Si ce pont était un jour construit, une nouvelle formation ou une
   révision explicite documenterait ce nouvel état — jamais une
   extension silencieuse du périmètre actuel.
