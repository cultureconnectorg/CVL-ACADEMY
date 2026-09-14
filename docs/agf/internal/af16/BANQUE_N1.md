# AF-16 — Banque N1 (formatif)

Réserve `AF16.SKILL.AGENT_FACTORY_OPERATOR.L1`.

1. Que fait réellement `chat_reply()` dans `backend/services/
   agent_factory.py`, et pourquoi est-il qualifié de "persona-
   agnostique" ?
2. Qu'est-ce que `mentor_reply()` et pourquoi est-ce la seule persona
   réellement enregistrée dans cette Academy ?
3. Le vrai `frekcore/CVLNAgentfactory` (225 fichiers, ~143 routes, ADL
   `AGT-\d{3}`, cycle de vie à 7 étapes, gates avec journal append-
   only) est cité comme contexte de marché — pourquoi ne doit-il
   jamais être présenté comme le substrat opérant de cette Academy ?
4. Pourquoi serait-il une erreur éliminatoire d'inventer un registre
   d'agents, un système de détachement/mission, ou un mécanisme de
   rollback pour cette Academy ?
5. Un candidat propose, à titre d'idée future, un "registre d'agents"
   pour cette Academy, en le qualifiant clairement d'hypothétique.
   Cette proposition est-elle acceptable ? Sous quelle condition ?
6. Pourquoi `chat_reply()` ne "sélectionne"-t-il aucune persona
   lui-même, alors que `mentor_reply()` en encapsule une ?

## Corrigé indicatif

1. `chat_reply()` est un transport de chat réel porté par Claude, sans
   logique de persona propre — il route simplement vers le modèle,
   quelle que soit la persona appelante.
2. `mentor_reply()` encapsule la seule persona réellement configurée
   ("Mentor CVLN") — aucune autre persona n'est enregistrée dans le
   code réel.
3. `CVLNAgentfactory` est un système réel et substantiellement plus
   sophistiqué, mais aucune intégration observée ne le relie à cette
   Academy — le citer comme substrat opérant inventerait une capacité
   inexistante.
4. Aucun de ces éléments n'existe dans `agent_factory.py` ni dans
   aucune intégration observée — les inventer romprait la discipline
   repo-truth-first.
5. C'est acceptable uniquement si la proposition est explicitement
   qualifiée d'hypothétique et de travail futur non entamé — jamais
   présentée comme une capacité actuelle, même partielle.
6. `chat_reply()` est une fonction de transport générique, réutilisable
   par n'importe quelle persona future ; `mentor_reply()` est une
   fonction spécifique qui appelle `chat_reply()` avec la
   configuration figée de la persona "Mentor CVLN" — la sélection de
   persona se fait par le choix de la fonction appelée, pas par une
   logique de routage interne à `chat_reply()`.
